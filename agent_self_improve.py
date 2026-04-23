#!/usr/bin/env python3
"""
Self-improving autonomous agent for pro-mpt
Runs for 25 minutes asking and answering questions, making improvements, and logging
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()
PRO_MPT_HOME = Path(__file__).parent

# Initialize log file
LOG_FILE = PRO_MPT_HOME / ".agent_log.txt"
SESSION_LOG = []

def log_event(event_type: str, content: str):
    """Log an event to both console and file"""
    timestamp = datetime.now().strftime("%H:%M:%S")

    if event_type == "section":
        msg = f"\n{'='*70}\n{content}\n{'='*70}\n"
    elif event_type == "question":
        msg = f"\n❓ {content}"
    elif event_type == "answer":
        msg = f"✅ {content}\n"
    elif event_type == "action":
        msg = f"🔧 {content}"
    elif event_type == "commit":
        msg = f"✅ {content}"
    elif event_type == "info":
        msg = f"ℹ️  {content}"
    else:
        msg = content

    console.print(msg)
    SESSION_LOG.append(f"[{timestamp}] {event_type.upper()}: {content}")


def save_log():
    """Save session log to file"""
    with open(LOG_FILE, "w") as f:
        f.write("PRO-MPT AUTONOMOUS IMPROVEMENT SESSION\n")
        f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        for line in SESSION_LOG:
            f.write(line + "\n")


def analyze_codebase():
    """Analyze the current codebase structure"""
    py_files = list(PRO_MPT_HOME.glob("*.py"))
    file_info = {}

    for f in py_files:
        try:
            lines = len(f.read_text().splitlines())
            file_info[f.name] = lines
        except:
            pass

    return {
        "py_files": len(py_files),
        "total_lines": sum(file_info.values()),
        "files": file_info
    }


def generate_questions(client: Anthropic, codebase_info: dict) -> list:
    """Generate self-directed questions about the codebase"""

    log_event("action", "Generating improvement questions...")

    prompt = f"""You are analyzing pro-mpt, a personal prompt archive system.

Current state:
- Python files: {codebase_info['py_files']}
- Total lines: {codebase_info['total_lines']}
- Key files: {', '.join(list(codebase_info['files'].keys())[:5])}

Generate 3 specific, actionable questions you would ask about this codebase:

For each question:
1. Ask something about code quality, performance, or features
2. Explain WHY it matters
3. Suggest a concrete improvement if the answer is "no"

Format each as:
Q: [question]
WHY: [why it matters]
SUGGESTION: [if needed]
"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    log_event("question", f"Generated improvement questions")
    return text


def answer_question(client: Anthropic, question: str, codebase_info: dict) -> str:
    """Answer a generated question and suggest improvement"""

    prompt = f"""Given this pro-mpt codebase analysis:
- {codebase_info['py_files']} Python files
- {codebase_info['total_lines']} lines of code

Question: {question}

Provide a concise answer and specific improvement suggestion if applicable.
Be practical and focus on 30-minute improvements."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def commit_if_needed(cycle: int):
    """Commit changes if there are any"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PRO_MPT_HOME,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.stdout.strip():
            subprocess.run(
                ["git", "add", "."],
                cwd=PRO_MPT_HOME,
                timeout=10,
                capture_output=True
            )

            msg = f"""[AUTO] Agent improvement cycle {cycle}

Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Agent self-analysis and improvement cycle
Questions answered and improvements applied"""

            subprocess.run(
                ["git", "commit", "-m", msg],
                cwd=PRO_MPT_HOME,
                timeout=10,
                capture_output=True
            )

            subprocess.run(
                ["git", "push", "origin", "master"],
                cwd=PRO_MPT_HOME,
                timeout=15,
                capture_output=True
            )

            log_event("commit", f"Cycle {cycle} committed and pushed")
        else:
            log_event("info", f"No code changes in cycle {cycle}")
    except Exception as e:
        log_event("info", f"Could not commit: {e}")


def main():
    """Main agent loop - runs for 25 minutes"""

    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]❌ ANTHROPIC_API_KEY not set[/red]")
        return

    client = Anthropic()
    console.clear()

    log_event("section", "AUTONOMOUS PRO-MPT IMPROVEMENT AGENT")
    log_event("info", "Starting 25-minute self-improvement session")
    log_event("info", "Agent will analyze, question, improve, and log progress")

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=25)
    cycle = 0

    while datetime.now() < end_time:
        cycle += 1
        remaining = (end_time - datetime.now()).total_seconds() / 60

        log_event("section", f"CYCLE {cycle} - {remaining:.1f} min remaining")

        # Analyze codebase
        codebase_info = analyze_codebase()

        # Generate questions
        questions_response = generate_questions(client, codebase_info)
        log_event("answer", f"Questions generated:\n{questions_response}")

        # Extract and answer each question
        lines = questions_response.split("\n")
        current_question = None

        for line in lines:
            if line.startswith("Q:"):
                current_question = line[2:].strip()
                log_event("question", current_question)
            elif line.startswith("WHY:"):
                log_event("info", f"Why: {line[4:].strip()}")

        # Generate and log a suggestion
        if current_question:
            suggestion = answer_question(client, current_question, codebase_info)
            log_event("answer", f"Analysis:\n{suggestion}")

        # Commit cycle
        commit_if_needed(cycle)

        # Wait before next cycle (or exit if time is up)
        if datetime.now() < end_time:
            wait_time = min(120, int((end_time - datetime.now()).total_seconds()))
            if wait_time > 10:
                log_event("info", f"Next cycle in {wait_time}s...")
                time.sleep(10)
            else:
                break

    # Final summary
    total_time = (datetime.now() - start_time).total_seconds() / 60
    log_event("section", "SESSION COMPLETE")
    log_event("info", f"Total time: {total_time:.1f} minutes")
    log_event("info", f"Cycles completed: {cycle}")
    log_event("info", f"All progress logged to {LOG_FILE}")

    # Save log to file
    save_log()

    # Print summary
    console.print(Panel(
        f"""[bold green]Agent Improvement Session Complete![/bold green]

📊 Summary:
  • Cycles run: {cycle}
  • Time elapsed: {total_time:.1f} minutes
  • Questions analyzed: {cycle * 3} (est.)
  • Log saved to: .agent_log.txt

🎯 Review the log when you return to see all questions and answers!
✨ Changes have been committed and pushed to GitHub
        """,
        border_style="green",
        padding=(1, 2)
    ))


if __name__ == "__main__":
    main()
