#!/bin/bash
# start-with-recording.sh
# Start pro-mpt in background, then launch Claude Code

set -e

# Get the directory where this script is
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
echo "🚀 Activating pro-mpt environment..."
source "$SCRIPT_DIR/venv/bin/activate"

# Initialize database (creates if doesn't exist)
python "$SCRIPT_DIR/pro_mpt.py" stats > /dev/null 2>&1 || true

# Start a recording session (print session info)
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    PRO-MPT RECORDING SESSION                   ║"
echo "║                                                                ║"
echo "║  Your prompts will be automatically recorded.                  ║"
echo "║                                                                ║"
echo "║  When you ask Claude something important, log it:             ║"
echo "║  $ pro-mpt log \"your prompt\" --model claude --rating 5       ║"
echo "║                                                                ║"
echo "║  View what you've asked:                                       ║"
echo "║  $ pro-mpt search \"topic\"                                     ║"
echo "║                                                                ║"
echo "║  See your stats:                                               ║"
echo "║  $ pro-mpt stats                                               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Store the session start time
SESSION_START=$(date '+%Y-%m-%d %H:%M:%S')

# Trap to show session summary on exit
cleanup() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    SESSION ENDED                               ║"
    echo "║                                                                ║"
    echo "║  View your session:                                            ║"
    echo "║  $ pro-mpt morning                                             ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
}

trap cleanup EXIT

# Launch Claude Code
echo "🔧 Starting Claude Code (with pro-mpt recording)..."
echo ""

# Run Claude Code (or code command if available)
if command -v claude &> /dev/null; then
    claude code
elif command -v code &> /dev/null; then
    code
else
    echo "❌ Neither 'claude' nor 'code' command found"
    echo "   Install Claude Code CLI: https://claude.com/claude-code"
    exit 1
fi
