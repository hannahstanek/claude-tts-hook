#!/bin/bash
set -e

echo "Installing Claude Code TTS Hook..."

# Install Python dependency
pip3 install edge-tts

# Copy script to Claude scripts directory
mkdir -p ~/.claude/scripts
cp tts_hook.py ~/.claude/scripts/tts_hook.py
chmod +x ~/.claude/scripts/tts_hook.py

# Add Stop hook to Claude settings
SETTINGS=~/.claude/settings.json

if [ ! -f "$SETTINGS" ]; then
  echo '{"hooks": {}}' > "$SETTINGS"
fi

# Check if the hook is already present
if grep -q "tts_hook.py" "$SETTINGS"; then
  echo "Hook already present in $SETTINGS — skipping."
else
  echo ""
  echo "ACTION REQUIRED: Add the following to the \"hooks\" > \"Stop\" array in ~/.claude/settings.json:"
  echo ""
  cat hook_snippet.json
  echo ""
fi

# Add shell aliases
ZSHRC=~/.zshrc
BASHRC=~/.bashrc

add_aliases() {
  local file=$1
  if [ -f "$file" ] && ! grep -q "listen-on" "$file"; then
    echo "" >> "$file"
    echo "# Claude Code TTS toggle" >> "$file"
    echo "alias listen-on='touch ~/.claude/tts_enabled && echo \"Listen mode enabled\"'" >> "$file"
    echo "alias listen-off='rm -f ~/.claude/tts_enabled && echo \"Listen mode disabled\"'" >> "$file"
    echo "Added listen-on / listen-off aliases to $file"
  fi
}

add_aliases "$ZSHRC"
add_aliases "$BASHRC"

echo ""
echo "Done! Run 'source ~/.zshrc' (or open a new terminal), then:"
echo "  tts-on   — enable voice output"
echo "  tts-off  — disable voice output"
