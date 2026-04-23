#!/usr/bin/env python3
"""
start.py - Simple entry point for pro-mpt
Run: python start.py [command] [args]
"""

import sys
import subprocess
from pathlib import Path

# Get the directory where this script is
BASE_DIR = Path(__file__).parent
VENV_PYTHON = BASE_DIR / "venv" / "bin" / "python"
VENV_ACTIVATE = BASE_DIR / "venv" / "bin" / "activate"
PRO_MPT = BASE_DIR / "pro_mpt.py"

def ensure_venv():
    """Check if venv exists and is activated"""
    if not VENV_PYTHON.exists():
        print("❌ Virtual environment not found!")
        print(f"   Run: python -m venv {BASE_DIR / 'venv'}")
        sys.exit(1)

def run_pro_mpt(args):
    """Run pro-mpt with the given arguments"""
    ensure_venv()
    cmd = [str(VENV_PYTHON), str(PRO_MPT)] + args
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def show_help():
    """Show available commands"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║              PRO-MPT - Commands                                ║
╚════════════════════════════════════════════════════════════════╝

DEFAULT (Interactive Mode):
  python start.py

  Once inside, type commands:
  > log "What you asked Claude" --model claude --rating 5
  > search "state management"
  > stats
  > exit

ONE-OFF COMMANDS:

  Log a prompt (no interactive session):
    python start.py log "Your question" --model claude --rating 5

  Search prompts:
    python start.py search "topic"

  See recent:
    python start.py list

  View stats:
    python start.py stats

  Morning summary:
    python start.py morning

  Your expertise:
    python start.py expertise --domain dev

  Export data:
    python start.py export --format json

  Show this help:
    python start.py help

EXAMPLES:

  1. Start interactive session:
     $ python start.py
     > log "How do I fix this bug?" --model claude --rating 5
     > search "state"
     > stats
     > exit

  2. Quick one-off log (no session):
     $ python start.py log "question" --model claude --rating 5

  3. Recording session:
     $ ./start-with-recording.sh

TIPS:

  • Interactive mode keeps history (use arrow keys)
  • Type 'help' in interactive mode to see all commands
  • Use 'exit' or 'quit' to leave interactive mode
  • Multi-word queries need quotes: log "how to handle state?"

═══════════════════════════════════════════════════════════════════

Full docs: README.md, MANIFESTO.md, NEXT_STEPS.md
""")

def main():
    """Main entry point"""

    # If no args, start interactive mode
    if len(sys.argv) == 1:
        run_pro_mpt(["interactive"])
        return

    # Check for help
    if sys.argv[1] in ["help", "-h", "--help"]:
        show_help()
        return

    # Check for version
    if sys.argv[1] in ["version", "-v", "--version"]:
        print("pro-mpt v0.1.0")
        return

    # Otherwise, pass all args to pro_mpt.py
    run_pro_mpt(sys.argv[1:])

if __name__ == "__main__":
    main()
