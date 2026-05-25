# Claude Code TTS Hook

Automatically reads Claude Code's responses aloud using Microsoft's neural text-to-speech engine. Designed for a fully hands-free workflow — speak your prompts via Wispr Flow or any dictation tool, and hear Claude's replies spoken back to you in a natural human voice.

## How It Works

Claude Code supports [hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) — shell commands that fire on events. This project wires a `Stop` hook to a Python script that:

1. Receives Claude's last response as JSON
2. Strips code blocks, markdown symbols, and URLs (hearing raw code is useless)
3. Sends the cleaned text to Microsoft Edge's free neural TTS engine
4. Plays the audio through your speakers via `afplay` (macOS)

The result: every time Claude finishes a response, it's read aloud to you automatically.

## Requirements

- macOS (uses `afplay` for audio playback)
- Python 3.8+
- Claude Code CLI
- Internet connection (Edge TTS streams from Microsoft's servers)

## Installation

**1. Install the Python dependency:**

```bash
pip3 install edge-tts
```

**2. Copy the script:**

```bash
mkdir -p ~/.claude/scripts
cp tts_hook.py ~/.claude/scripts/tts_hook.py
chmod +x ~/.claude/scripts/tts_hook.py
```

Or run the installer:

```bash
chmod +x install.sh && ./install.sh
```

**3. Add the hook to Claude Code settings:**

Open `~/.claude/settings.json` and add the Stop hook. If you already have a `hooks` section, merge it in:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/scripts/tts_hook.py",
            "async": true
          }
        ]
      }
    ]
  }
}
```

See `hook_snippet.json` in this repo for a copy-paste reference.

**4. Add toggle aliases to your shell:**

```bash
echo "alias tts-on='touch ~/.claude/tts_enabled && echo \"TTS enabled\"'" >> ~/.zshrc
echo "alias tts-off='rm -f ~/.claude/tts_enabled && echo \"TTS disabled\"'" >> ~/.zshrc
source ~/.zshrc
```

## Usage

```bash
tts-on    # Enable — Claude will read responses aloud
tts-off   # Disable — silent mode
```

TTS is **off by default**. Run `tts-on` once and it persists across sessions until you run `tts-off`.

## Changing the Voice

The default voice is **Aria** (`en-US-AriaNeural`). To use a different voice, edit `tts_hook.py` and change the `VOICE` constant.

List all available neural voices:

```bash
edge-tts --list-voices | grep en-US
```

Some good options:

| Voice | Style |
|---|---|
| `en-US-AriaNeural` | Female, natural and warm (default) |
| `en-US-JennyNeural` | Female, clear and conversational |
| `en-US-GuyNeural` | Male, calm and professional |
| `en-US-DavisNeural` | Male, expressive |

## What Gets Skipped

The script strips the following before speaking:

- Fenced code blocks (` ``` `)
- Inline code (`` ` ``)
- URLs
- Markdown headers, bold, italic
- Table rows
- Bullet/numbered list markers (content is still read)

## Hands-Free Workflow

This hook covers the **output** side. For the **input** side (speaking your prompts), use any system-wide dictation tool:

- **[Wispr Flow](https://wisprflow.ai)** — high-accuracy AI dictation that types into any app, including the Claude Code terminal
- macOS built-in dictation (System Settings → Keyboard → Dictation)

Combined workflow:
1. Activate dictation → speak your prompt → it types into Claude Code
2. Claude generates a response
3. Hook fires → Aria reads the response aloud
4. Speak your next prompt

Fully hands-free, no screen reading required.

## Troubleshooting

**TTS isn't speaking:**
- Confirm `~/.claude/tts_enabled` exists: `ls ~/.claude/tts_enabled`
- Check `edge-tts` is installed: `edge-tts --version`
- Confirm the hook is in `~/.claude/settings.json`

**Audio is delayed:**
- Edge TTS requires a network request. On slow connections there may be a 1-2 second delay before audio starts.

**Want offline TTS:**
- Replace the `speak()` function with a call to macOS `say`: `subprocess.run(["say", text])`
- Quality will be lower but works without internet.

## License

MIT
