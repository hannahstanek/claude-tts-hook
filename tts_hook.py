#!/usr/bin/env python3
"""
Claude Code TTS Hook
Reads Claude's responses aloud using Microsoft Edge neural TTS (Aria voice).
Triggered automatically via Claude Code's Stop hook.
Toggle with: tts-on / tts-off
"""
import asyncio
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts

TOGGLE_FILE = Path.home() / ".claude" / "tts_enabled"
VOICE = "en-US-AriaNeural"


def is_enabled():
    return TOGGLE_FILE.exists()


def clean_text(text):
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", text)
    text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[-*_]{3,}$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_last_assistant_text(event):
    text = event.get("last_assistant_message", "")
    if text:
        return clean_text(str(text))
    return None


async def speak(text):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp = f.name
    try:
        tts = edge_tts.Communicate(text, VOICE)
        await tts.save(tmp)
        subprocess.run(["afplay", tmp], check=False, timeout=300)
    finally:
        Path(tmp).unlink(missing_ok=True)


def main():
    if not is_enabled():
        return

    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
    except Exception:
        event = {}

    text = extract_last_assistant_text(event)
    if not text:
        return

    asyncio.run(speak(text))


if __name__ == "__main__":
    main()
