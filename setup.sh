#!/bin/bash
# setup.sh - Install pro-mpt commands system-wide

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOCAL_BIN="$HOME/.local/bin"

echo "🚀 Setting up pro-mpt..."

# Create .local/bin if needed
mkdir -p "$LOCAL_BIN"

# Get absolute path to pro-mpt home
echo "PRO_MPT_HOME=\"$SCRIPT_DIR\"" > "$SCRIPT_DIR/.env"
echo "✓ Configuration saved"

# Copy all pro-* scripts
for script in pro-mpt pro-go pro-grow pro-log pro-record pro-review pro-export pro-search pro-chat pro-dashboard pro-setup; do
    if [ -f "$SCRIPT_DIR/$script" ]; then
        cp "$SCRIPT_DIR/$script" "$LOCAL_BIN/"
        chmod +x "$LOCAL_BIN/$script"
        echo "✓ Installed $script"
    fi
done

# Add to PATH if not already there
if ! grep -q "\.local/bin" ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "✓ Added ~/.local/bin to ~/.bashrc"
fi

if ! grep -q "\.local/bin" ~/.zshrc 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    echo "✓ Added ~/.local/bin to ~/.zshrc"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Now run: source ~/.bashrc"
echo "Then try: pro-mpt"
echo ""
echo "Available commands (from anywhere):"
echo "  pro-mpt              - Main launcher (or just 'pro-mpt' to start)"
echo "  pro-mpt go           - Interactive mode"
echo "  pro-mpt log          - Quick log from command line"
echo "  pro-mpt search       - Find prompts"
echo "  pro-mpt stats        - View statistics"
echo "  pro-mpt export       - Export data (JSON/CSV/backup)"
echo "  pro-mpt dashboard    - Live dashboard"
echo "  pro-mpt chat         - Chat with Claude"
echo "  pro-mpt help         - Show help"
echo ""
echo "Or use individual commands:"
echo "  pro-go, pro-log, pro-search, pro-dashboard, etc."
