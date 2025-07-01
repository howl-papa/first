from __future__ import annotations

import random
import gradio as gr
from global_meeting_ai import GlobalMeetingAI


class VoiceFashionPro:
    """Combined demo implementing features from the MVP report."""

    def __init__(self):
        self.meeting_ai = GlobalMeetingAI()
        # Example inventory levels for a couple of products
        self.inventory = {
            "청바지": 200,
            "우산": 150,
        }

    def voice_forecast(self, audio: str, item: str, language: str):
        """Predict demand from a spoken question and return speech output."""
        if not audio or not item:
            return "", "상품과 음성을 입력해주세요.", None

        question = self.meeting_ai.stt_with_language(audio, language)
        stock = self.inventory.get(item, 100)
        forecast = random.randint(50, 120)
        response = f"현재 재고 {stock}개, 예상 판매량 {forecast}개. 충분합니다!"
        tts = self.meeting_ai.tts_with_language(response, language)
        return question, response, tts

    def create_interface(self):
        with gr.Blocks(title="VoiceFashion Pro") as demo:
            with gr.Tabs():
                with gr.TabItem("\ud83d\udcca \uc218\uc694\uc608\ucc28"):
                    gr.Markdown("### \uc74c\uc131 \uae30\ubcf8 \ud328\uc158 \uc218\uc694\uc608\ucc28")
                    item = gr.Dropdown(list(self.inventory.keys()), label="\uc0c1\ud488", value="\uccad\ubc14\uc9c0")
                    lang = gr.Dropdown(list(self.meeting_ai.language_codes.keys()), label="\uc5b8\uc5b4", value="\ud55c\uad6d\uc5b4")
                    audio = gr.Audio(sources="microphone", type="filepath", label="\uc9c8\ubb38 \ub178\ubd80\ub974\uae30")
                    btn = gr.Button("\uc608\ucc28")
                    question_box = gr.Textbox(label="\uc778\uc2dd\ub41c \uc9c8\ubb38", interactive=False)
                    answer_box = gr.Textbox(label="\uc608\ucc28 \uae30\ub2a5", interactive=False)
                    answer_audio = gr.Audio(label="\uc608\ucc28 \uc74c\uc131")
                    btn.click(self.voice_forecast, [audio, item, lang], [question_box, answer_box, answer_audio])

                with gr.TabItem("\ud83c\udf0d \ud68c\uc758 \uc5b4\uc2dc\uc2a4\ud2b8"):
                    name = gr.Textbox(label="\ubc1c\uc5b8\uc790", value="\ucc38\uc11d\uc790")
                    src = gr.Dropdown(list(self.meeting_ai.language_codes.keys()), label="\uc6d0\ubcf8 \uc5b8\uc5b4", value="\ud55c\uad6d\uc5b4")
                    tgt = gr.Dropdown(list(self.meeting_ai.language_codes.keys()), label="\ubc88\uc5ed \uc5b8\uc5b4", value="English")
                    m_audio = gr.Audio(sources="microphone", type="filepath", label="\uc74c\uc131 \uc785\ub825")
                    m_btn = gr.Button("\uc2e4\uc2dc\uac04 \ubc88\uc5ed")
                    out_audio = gr.Audio(label="\ubc88\uc5ed \uc74c\uc131")
                    out_text = gr.Textbox(label="\ubc88\uc5ed \uacb0\uacfc")
                    log = gr.Textbox(label="\ud68c\uc758 \ub85c\uae30", lines=10, interactive=False)
                    sum_btn = gr.Button("\ud68c\uc758 \uc694\uc57d")
                    clr_btn = gr.Button("\ucd08\uae30\ud654")
                    sum_text = gr.Textbox(label="AI \uc694\uc57d", lines=10, interactive=False)
                    sum_audio = gr.Audio(label="\uc694\uc57d \uc74c\uc131")

                    def _trans(a, s, t, n):
                        f, txt, lg = self.meeting_ai.process_realtime_translation(a, s, t, n)
                        return f or None, txt, lg

                    m_btn.click(_trans, [m_audio, src, tgt, name], [out_audio, out_text, log])
                    sum_btn.click(self.meeting_ai.generate_meeting_summary, None, [sum_text, sum_audio])
                    clr_btn.click(self.meeting_ai.clear_meeting_history, None, [sum_text, log])
        return demo


def main():
    app = VoiceFashionPro().create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
