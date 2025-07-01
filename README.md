# VoiceFashion Prototype

This repository contains prototypes for a multilingual meeting assistant and an integrated demo implementing the features from the MVP one-page report.

## Meeting Assistant

The meeting assistant translates speech in real time and stores the transcript so that a summary can be generated later. API keys are read from the environment variables `SPEECH_KEY` and `GPT_KEY`. If the keys are not set the code falls back to local packages such as `googletrans` and `gtts`.

Run the meeting assistant with:

```bash
python global_meeting_ai.py
```

All meeting data is written to the `output/` directory.

## VoiceFashion Pro

`voice_fashion_pro.py` combines a voice-based demand forecasting mock-up with the global meeting assistant. Run it with:

```bash
python voice_fashion_pro.py
```

