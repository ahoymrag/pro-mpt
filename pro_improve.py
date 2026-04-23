#!/usr/bin/env python3
"""
pro-improve - Automatic self-improvement console
Analyzes pro-mpt codebase and suggests/applies improvements
"""

import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from anthropic import Anthropic
import time

console = Console()
PRO_MPT_HOME = Path(__file__).parent


def get_codebase_stats():
    """Get statistics about the codebase"""
    stats = {
        "total_lines": 0,
        "files": [],
        "languages": {}
    }

    for file in PRO_MPT_HOME.glob("*.py"):
        if file.name.startswith("test_"):
            continue
        with open(file) as f:
            lines = len(f.readlines())
            stats["total_lines"] += lines
            stats["files"].append({
                "name": file.name,
                "lines": lines
            })
            stats["languages"]["python"] = stats["languages"].get("python", 0) + lines

    return stats


def render_improvement_dashboard(improvements):
    """Render dashboard showing improvements"""
    table = Table(title="🚀 Auto-Improvements", box=box.ROUNDED, border_style="cyan")
    table.add_column("Status", style="cyan", width=10)
    table.add_column("Improvement", style="white")
    table.add_column("Impact", justify="right", style="green")

    for i, imp in enumerate(improvements):
        status = "✅" if imp.get("applied") else "⏳"
        impact = imp.get("impact", "Medium")
        table.add_row(status, imp["title"], impact)

    return table


def analyze_codebase():
    """Analyze pro-mpt codebase for improvement opportunities"""
    client = Anthropic()

    stats = get_codebase_stats()

    # Build codebase context
    context = "# Pro-MPT Codebase Analysis\n\n"
    context += f"## Statistics\n- Total Lines: {stats['total_lines']}\n"
    context += f"- Files: {len(stats['files'])}\n\n"

    # Get key files
    key_files = [
        "pro_mpt.py",
        "dashboard.py",
        "analyze_growth.py",
        "pro_chat.py"
    ]

    context += "## Key Files\n"
    for file in key_files:
        path = PRO_MPT_HOME / file
        if path.exists():
            with open(path) as f:
                lines = f.readlines()[:30]
                context += f"\n### {file}\n```python\n"
                context += "".join(lines)
                context += "\n```\n"

    # Ask Claude for improvement suggestions
    console.print("[cyan]🤖 Claude is analyzing pro-mpt...[/cyan]")

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""Analyze this pro-mpt codebase and suggest 3-5 specific improvements.

{context}

For each improvement, provide:
1. What to improve
2. Why it matters
3. Impact level (High/Medium/Low)
4. Effort required (Quick/Medium/Complex)

Format as a numbered list."""
        }]
    )

    return response.content[0].text


def render_improvement_panel(analysis):
    """Render the improvement suggestions panel"""
    return Panel(
        analysis,
        title="💡 Auto-Improvement Suggestions",
        border_style="green",
        padding=(1, 2)
    )


def render_metrics():
    """Render live metrics dashboard"""
    stats = get_codebase_stats()

    metrics = f"""
[bold cyan]Codebase Health[/bold cyan]
  Total Lines: {stats['total_lines']}
  Python Files: {len(stats['files'])}

[bold green]File Breakdown[/bold green]
"""

    for file in sorted(stats["files"], key=lambda x: x["lines"], reverse=True)[:5]:
        pct = int((file["lines"] / stats["total_lines"]) * 100)
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        metrics += f"  {file['name']}: {file['lines']:>4} lines [{bar}] {pct}%\n"

    return Panel(metrics, border_style="cyan", padding=(1, 2))


def main():
    """Run the auto-improvement console"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(Panel(
            "[red]❌ ANTHROPIC_API_KEY not set[/red]\n\n"
            "Set your API key:\n"
            "[bold]export ANTHROPIC_API_KEY='sk-...'[/bold]",
            border_style="red",
            padding=(1, 2)
        ))
        return

    console.clear()
    console.print(Panel(
        "[bold cyan]🚀 PRO-MPT AUTO-IMPROVEMENT CONSOLE[/bold cyan]\n"
        "[dim]Analyzing codebase and generating improvements...[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()

    # Show current metrics
    console.print(render_metrics())
    console.print()

    # Analyze codebase
    try:
        with console.status("[cyan]🤖 Claude analyzing pro-mpt codebase...[/cyan]"):
            analysis = analyze_codebase()

        # Display suggestions
        console.print(render_improvement_panel(analysis))
        console.print()

        # Show next steps
        console.print(Panel(
            "[bold]Next Steps:[/bold]\n"
            "1. Review suggestions above\n"
            "2. Use [cyan]pro-chat[/cyan] to discuss improvements\n"
            "3. Apply changes incrementally\n"
            "4. Test with [cyan]pro-go[/cyan]\n"
            "5. Run [cyan]pro-improve[/cyan] again to find more opportunities",
            border_style="green",
            padding=(1, 2)
        ))

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[dim]Make sure ANTHROPIC_API_KEY is valid[/dim]")


if __name__ == "__main__":
    main()
