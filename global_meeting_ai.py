"""Multilingual meeting assistant with optional Azure services.

This module implements a simple meeting tool capable of translating speech in
real time and generating meeting summaries.  When Azure Speech or OpenAI
services are not configured the assistant falls back to local packages
(`googletrans` and `gtts`).  Meeting logs are saved to the ``output``
directory so users can inspect the raw data.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import gradio as gr
import pandas as pd
import requests
from googletrans import Translator
from gtts import gTTS


class GlobalMeetingAI:
    """Meeting assistant supporting real-time translation and summaries."""

    def __init__(self) -> None:
        self.stt_endpoint = (
            "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        )
        self.tts_endpoint = "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1"
        self.gpt_endpoint = (
            "https://fimtrus-ai-project-resource.cognitiveservices.azure.com/openai/deployments/fimtrus-gpt-41/chat/completions?api-version=2025-01-01-preview"
        )

        # Keys are loaded from environment variables. Missing keys simply disable
        # the Azure features so the prototype can still run locally.
        self.speech_key = os.getenv("SPEECH_KEY", "")
        self.gpt_key = os.getenv("GPT_KEY", "")

        self.translator = Translator()
        self.meeting_history: list[dict[str, str]] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

        self.language_codes = {
            "한국어": {"stt": "ko-KR", "tts": "ko-KR-SunHiNeural", "translate": "ko"},
            "English": {"stt": "en-US", "tts": "en-US-JennyNeural", "translate": "en"},
            "中文": {"stt": "zh-CN", "tts": "zh-CN-XiaoxiaoNeural", "translate": "zh"},
        }

    # ------------------------------------------------------------------
    # Speech helpers
    # ------------------------------------------------------------------
    def stt_with_language(self, audio_path: str, language: str) -> str:
        """Return a transcript using Azure STT or fall back to whisper."""
        if not audio_path:
            return ""
        lang_code = self.language_codes[language]["stt"]

        if self.speech_key:
            endpoint = f"{self.stt_endpoint}?language={lang_code}"
            headers = {
                "Ocp-Apim-Subscription-Key": self.speech_key,
                "Content-Type": "audio/wav",
            }
            try:
                with open(audio_path, "rb") as f:
                    audio_data = f.read()
                resp = requests.post(endpoint, headers=headers, data=audio_data)
                if resp.status_code == 200:
                    return resp.json().get("DisplayText", "")
            except Exception as exc:  # pragma: no cover
                print("Azure STT error", exc)

        # Local whisper fallback if installed
        try:
            import whisper  # type: ignore

            model = whisper.load_model("base")
            out = model.transcribe(audio_path, language=lang_code.split("-")[0])
            return out.get("text", "")
        except Exception as exc:  # pragma: no cover
            print("Whisper fallback failed", exc)
            return ""

    def tts_with_language(self, text: str, language: str) -> str | None:
        """Generate an audio file for ``text`` in ``language``."""
        if not text:
            return None
        voice = self.language_codes[language]["tts"]

        if self.speech_key:
            headers = {
                "Ocp-Apim-Subscription-Key": self.speech_key,
                "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
                "Content-Type": "application/ssml+xml",
            }
            body = f"""
        <speak version='1.0' xml:lang='{self.language_codes[language]['stt'][:5]}'>
            <voice xml:lang='{self.language_codes[language]['stt'][:5]}' name='{voice}'>
                {text}
            </voice>
        </speak>
            """
            try:
                resp = requests.post(self.tts_endpoint, headers=headers, data=body)
                if resp.status_code == 200:
                    filename = self.output_dir / f"tts_{datetime.now().strftime('%H%M%S')}.wav"
                    with open(filename, "wb") as out:
                        out.write(resp.content)
                    return str(filename)
            except Exception as exc:  # pragma: no cover
                print("Azure TTS error", exc)

        try:
            lang_code = self.language_codes[language]["translate"]
            tts = gTTS(text=text, lang=lang_code)
            filename = self.output_dir / f"tts_{datetime.now().strftime('%H%M%S')}.mp3"
            tts.save(filename)
            return str(filename)
        except Exception as exc:  # pragma: no cover
            print("gTTS fallback failed", exc)
            return None

    # ------------------------------------------------------------------
    # Translation and logging
    # ------------------------------------------------------------------
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        if source_lang == target_lang:
            return text
        src = self.language_codes[source_lang]["translate"]
        tgt = self.language_codes[target_lang]["translate"]
        try:
            return self.translator.translate(text, src=src, dest=tgt).text
        except Exception as exc:  # pragma: no cover
            print("Translation error", exc)
            return text

    def add_to_meeting_log(
        self,
        speaker: str,
        original: str,
        translated: str,
        source_lang: str,
        target_lang: str,
    ) -> None:
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "speaker": speaker or "참석자",
            "original_text": original,
            "translated_text": translated,
            "original_language": source_lang,
            "target_language": target_lang,
        }
        self.meeting_history.append(entry)
        self.save_meeting_log()

    def save_meeting_log(self) -> None:
        if not self.meeting_history:
            return
        json_path = self.output_dir / f"meeting_log_{self.session_id}.json"
        csv_path = self.output_dir / f"meeting_log_{self.session_id}.csv"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.meeting_history, f, ensure_ascii=False, indent=2)
        pd.DataFrame(self.meeting_history).to_csv(csv_path, index=False, encoding="utf-8")

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------
    def _generate_local_summary(self, transcript: str) -> str:
        lines = transcript.splitlines()
        speakers = {l.split(":")[0] for l in lines if ":" in l}
        topics = [l.split(":", 1)[1].strip() for l in lines if ":" in l]
        excerpt = "\n".join(f"- {t[:100]}" for t in topics[:5])
        return (
            f"**참석자**: {', '.join(speakers)}\n"
            f"**주요 논의사항**:\n{excerpt}\n"
            f"**총 발언 수**: {len(lines)}개"
        )

    def _meeting_stats(self) -> str:
        if not self.meeting_history:
            return "통계 데이터 없음"
        lang_count: dict[str, int] = {}
        speaker_count: dict[str, int] = {}
        for e in self.meeting_history:
            lang_count[e["original_language"]] = lang_count.get(e["original_language"], 0) + 1
            speaker_count[e["speaker"]] = speaker_count.get(e["speaker"], 0) + 1
        parts = [
            f"- **총 발언 수**: {len(self.meeting_history)}개",
            f"- **참석자 수**: {len(speaker_count)}명",
            f"- **사용된 언어**: {', '.join(lang_count.keys())}",
            f"- **발언자별 통계**: {', '.join(f'{k}({v}회)' for k, v in speaker_count.items())}",
        ]
        return "\n".join(parts)

    def generate_meeting_summary(self) -> tuple[str, str | None]:
        if not self.meeting_history:
            return "회의 내용이 없습니다.", None
        transcript = "\n".join(f"{e['speaker']}: {e['original_text']}" for e in self.meeting_history)
        if self.gpt_key:
            headers = {
                "Authorization": f"Bearer {self.gpt_key}",
                "Content-Type": "application/json",
            }
            body = {
                "messages": [
                    {"role": "system", "content": "회의 내용을 요약하세요."},
                    {"role": "user", "content": transcript},
                ],
                "max_tokens": 800,
                "temperature": 0.6,
            }
            try:
                resp = requests.post(self.gpt_endpoint, headers=headers, json=body)
                if resp.status_code == 200:
                    summary_text = resp.json()["choices"][0]["message"]["content"]
                else:
                    summary_text = self._generate_local_summary(transcript)
            except Exception as exc:  # pragma: no cover
                print("GPT request failed", exc)
                summary_text = self._generate_local_summary(transcript)
        else:
            summary_text = self._generate_local_summary(transcript)

        stats = self._meeting_stats()
        full_summary = (
            f"# 회의 요약 보고서\n\n## 통계\n{stats}\n\n## 요약\n{summary_text}"
        )
        summary_file = self.output_dir / f"meeting_summary_{self.session_id}.md"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(full_summary)
        summary_audio = self.tts_with_language("회의 요약이 생성되었습니다.", "한국어")
        return full_summary, summary_audio

    def export_meeting_data(self) -> str:
        self.save_meeting_log()
        files = [
            f"meeting_log_{self.session_id}.json",
            f"meeting_log_{self.session_id}.csv",
            f"meeting_summary_{self.session_id}.md",
        ]
        return "\n".join(f"- {f}" for f in files)

    def clear_meeting_history(self) -> tuple[str, str]:
        self.meeting_history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        return "회의 히스토리가 초기화되었습니다.", ""

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def process_realtime_translation(self, audio, source_lang, target_lang, name):
        original = self.stt_with_language(audio, source_lang)
        translated = self.translate_text(original, source_lang, target_lang)
        tts_file = self.tts_with_language(translated, target_lang)
        self.add_to_meeting_log(name, original, translated, source_lang, target_lang)
        log = self.format_meeting_log()
        text = f"원본({source_lang}): {original}\n번역({target_lang}): {translated}"
        return tts_file, text, log

    def format_meeting_log(self) -> str:
        if not self.meeting_history:
            return "회의 내용이 없습니다."
        lines = ["## 회의 로그"]
        for e in self.meeting_history[-10:]:
            lines.append(
                f"[{e['time']}] {e['speaker']} ({e['original_language']}→{e['target_language']})"
            )
            lines.append(f"  - {e['original_text']} -> {e['translated_text']}")
        return "\n".join(lines)

    def create_meeting_interface(self):
        with gr.Blocks(title="글로벌 회의 AI", theme=gr.themes.Soft()) as demo:
            with gr.Tab("🎤 실시간 번역"):
                with gr.Row():
                    name = gr.Textbox(label="발언자", value="참석자")
                    src = gr.Dropdown(list(self.language_codes.keys()), label="원본 언어", value="한국어")
                    tgt = gr.Dropdown(list(self.language_codes.keys()), label="번역 언어", value="English")
                audio_input = gr.Audio(sources="microphone", type="filepath", label="음성 입력")
                translate_btn = gr.Button("실시간 번역")
                out_audio = gr.Audio(label="번역 음성")
                out_text = gr.Textbox(label="번역 결과")
                log_box = gr.Textbox(label="회의 로그", lines=10, interactive=False)

                def _trans(a, s, t, n):
                    f, text, log = self.process_realtime_translation(a, s, t, n)
                    return f or None, text, log

                translate_btn.click(_trans, [audio_input, src, tgt, name], [out_audio, out_text, log_box])

            with gr.Tab("📊 회의 요약"):
                summary_btn = gr.Button("회의 요약 생성")
                export_btn = gr.Button("데이터 내보내기")
                clear_btn = gr.Button("초기화")
                summary_text = gr.Textbox(label="AI 요약", lines=10, interactive=False)
                summary_audio = gr.Audio(label="요약 음성")
                export_status = gr.Textbox(label="내보내기 상태", interactive=False)

                summary_btn.click(self.generate_meeting_summary, None, [summary_text, summary_audio])
                export_btn.click(lambda: self.export_meeting_data(), None, export_status)
                clear_btn.click(self.clear_meeting_history, None, [summary_text, log_box])

            with gr.Tab("ℹ️ 시스템 정보"):
                info = gr.Markdown(
                    f"""
                    **세션 ID**: `{self.session_id}`  
                    **지원 언어**: {', '.join(self.language_codes.keys())}  
                    데이터는 `{self.output_dir}` 폴더에 저장됩니다.
                    """
                )
        return demo


def main() -> None:
    ai = GlobalMeetingAI()
    demo = ai.create_meeting_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
