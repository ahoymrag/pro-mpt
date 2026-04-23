#!/bin/bash
# log-prompt.sh - Quick prompt logging
# Usage: ./log-prompt.sh "Your prompt here" [options]
#
# Examples:
#   ./log-prompt.sh "How do I handle state?"
#   ./log-prompt.sh "Fix this bug" --model gpt4 --rating 5
#   ./log-prompt.sh "Code review help" --app myapp --domain dev --rating 4

set -e

if [ -z "$1" ]; then
    echo "Usage: log-prompt.sh \"Your prompt\" [--model claude] [--app myapp] [--domain dev] [--rating 5]"
    echo ""
    echo "Examples:"
    echo "  ./log-prompt.sh \"How do I handle state?\""
    echo "  ./log-prompt.sh \"Fix the bug\" --model gpt4 --rating 5"
    echo "  ./log-prompt.sh \"Review this\" --app myapp --domain dev"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate venv if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Log the prompt with all arguments passed
python "$SCRIPT_DIR/pro_mpt.py" log "$@"

echo ""
echo "💾 Logged. View with: pro-mpt search \"$(echo "$1" | head -c 20)\""
