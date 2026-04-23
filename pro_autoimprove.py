#!/usr/bin/env python3
"""
pro-autoimprove - Automated continuous improvement
Runs improvements, applies them, tests, and reports
"""

import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box
from anthropic import Anthropic
import json
from datetime import datetime

console = Console()
PRO_MPT_HOME = Path(__file__).parent


def render_improvement_cycle():
    """Show the improvement cycle"""
    cycle = """
    [bold cyan]Auto-Improvement Cycle:[/bold cyan]

    1️⃣  [cyan]Analyze[/cyan] - Study codebase for issues
    2️⃣  [cyan]Suggest[/cyan] - Claude generates improvements
    3️⃣  [cyan]Review[/cyan] - Show suggestions to user
    4️⃣  [cyan]Apply[/cyan] - Make code changes
    5️⃣  [cyan]Test[/cyan] - Run tests & validate
    6️⃣  [cyan]Report[/cyan] - Show results & metrics
    7️⃣  [cyan]Repeat[/cyan] - Find more opportunities
    """
    return Panel(cycle, border_style="cyan", padding=(1, 2))


def get_improvement_log():
    """Get or create improvement log"""
    log_file = PRO_MPT_HOME / ".improvements.json"

    if log_file.exists():
        with open(log_file) as f:
            return json.load(f)

    return {
        "improvements": [],
        "total_changes": 0,
        "test_success_rate": 0,
    }


def save_improvement_log(log):
    """Save improvement log"""
    log_file = PRO_MPT_HOME / ".improvements.json"
    with open(log_file, "w") as f:
        json.dump(log, f, indent=2)


def render_improvement_history():
    """Show past improvements"""
    log = get_improvement_log()

    if not log["improvements"]:
        return Panel(
            "[dim]No improvements yet[/dim]",
            title="📋 Improvement History",
            border_style="dim"
        )

    table = Table(title="📋 Improvement History", box=box.ROUNDED, border_style="cyan")
    table.add_column("Date", style="dim")
    table.add_column("Improvement", style="white")
    table.add_column("Status", style="green")

    for imp in log["improvements"][-10:]:  # Last 10
        table.add_row(
            imp.get("date", "?"),
            imp.get("title", "Unknown")[:40],
            imp.get("status", "pending")
        )

    return table


def suggest_improvements():
    """Get improvement suggestions from Claude"""
    client = Anthropic()

    # Get codebase info
    py_files = list(PRO_MPT_HOME.glob("*.py"))
    total_lines = sum(len(open(f).readlines()) for f in py_files)

    prompt = f"""You are an expert code reviewer analyzing pro-mpt.

Current state:
- {len(py_files)} Python files
- {total_lines} total lines of code
- Key modules: pro_mpt.py, dashboard.py, pro_chat.py, etc.

Suggest ONE specific improvement that would:
1. Improve performance OR maintainability OR user experience
2. Be quick to implement (< 30 minutes)
3. Not break existing functionality

Format:
IMPROVEMENT: [title]
REASON: [why it matters]
FILE: [which file to change]
APPROACH: [how to implement]
IMPACT: [High/Medium/Low]
"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def main():
    """Main auto-improvement loop"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(Panel(
            "[red]❌ ANTHROPIC_API_KEY not set[/red]",
            border_style="red"
        ))
        return

    console.clear()
    console.print(render_improvement_cycle())
    console.print()

    # Show improvement history
    console.print(render_improvement_history())
    console.print()

    # Get suggestion
    try:
        with console.status("[cyan]🤖 Getting improvement suggestions...[/cyan]"):
            suggestion = suggest_improvements()

        console.print(Panel(
            suggestion,
            title="💡 Next Improvement",
            border_style="green",
            padding=(1, 2)
        ))

        # Log the suggestion
        log = get_improvement_log()
        log["improvements"].append({
            "date": datetime.now().isoformat(),
            "title": "New suggestion",
            "status": "reviewed",
            "suggestion": suggestion
        })
        save_improvement_log(log)

        console.print()
        console.print(Panel(
            "[bold]Ready to improve![/bold]\n\n"
            "Next steps:\n"
            "1. Review improvement above\n"
            "2. [cyan]pro-chat[/cyan] to discuss details\n"
            "3. Make code changes\n"
            "4. Test with [cyan]pro-go[/cyan]\n"
            "5. Run [cyan]pro-improve[/cyan] again",
            border_style="green",
            padding=(1, 2)
        ))

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
