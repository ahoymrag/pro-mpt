#!/usr/bin/env python3
"""
pro-export - Export your prompt archive to various formats
Export as JSON, CSV, Markdown, or backup your entire database
"""

import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(help="Export your prompt archive")
console = Console()

# Database path
DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"


def get_all_prompts():
    """Get all prompts from database"""
    if not DB_PATH.exists():
        console.print("[red]❌ No prompts database found[/red]")
        console.print("   Run [cyan]pro-go[/cyan] to start logging prompts first")
        raise typer.Exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prompts ORDER BY timestamp DESC")
    prompts = cursor.fetchall()
    conn.close()

    return [dict(p) for p in prompts]


@app.command()
def json(
    min_rating: Optional[int] = typer.Option(None, "--min-rating", "-r", help="Only export prompts rated >= this"),
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Filter by domain"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Filter by model"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file (default: prompts.json)"),
):
    """Export prompts to JSON"""
    prompts = get_all_prompts()

    # Apply filters
    if min_rating:
        prompts = [p for p in prompts if p.get("rating") and p["rating"] >= min_rating]
    if domain:
        prompts = [p for p in prompts if p.get("domain") == domain]
    if model:
        prompts = [p for p in prompts if p.get("model") == model]

    # Output file
    output_file = output or Path("prompts.json")

    with open(output_file, "w") as f:
        json.dump(prompts, f, indent=2)

    console.print(Panel(
        f"[green]✅ Exported {len(prompts)} prompts[/green]\n"
        f"📁 Saved to: [cyan]{output_file.absolute()}[/cyan]",
        border_style="green",
        title="Export Complete"
    ))


@app.command()
def csv(
    min_rating: Optional[int] = typer.Option(None, "--min-rating", "-r", help="Only export prompts rated >= this"),
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Filter by domain"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file (default: prompts.csv)"),
):
    """Export prompts to CSV"""
    prompts = get_all_prompts()

    # Apply filters
    if min_rating:
        prompts = [p for p in prompts if p.get("rating") and p["rating"] >= min_rating]
    if domain:
        prompts = [p for p in prompts if p.get("domain") == domain]

    output_file = output or Path("prompts.csv")

    if prompts:
        keys = prompts[0].keys()
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(prompts)

        console.print(Panel(
            f"[green]✅ Exported {len(prompts)} prompts[/green]\n"
            f"📁 Saved to: [cyan]{output_file.absolute()}[/cyan]",
            border_style="green",
            title="Export Complete"
        ))
    else:
        console.print("[yellow]⚠️  No prompts match your filters[/yellow]")


@app.command()
def backup(output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output directory (default: ./backups)")):
    """Backup your entire prompt database"""
    if not DB_PATH.exists():
        console.print("[red]❌ No prompts database found[/red]")
        raise typer.Exit(1)

    output_dir = output or Path("backups")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = output_dir / f"prompts_backup_{timestamp}.db"

    with open(DB_PATH, "rb") as src:
        with open(backup_file, "wb") as dst:
            dst.write(src.read())

    console.print(Panel(
        f"[green]✅ Database backed up[/green]\n"
        f"📁 Saved to: [cyan]{backup_file.absolute()}[/cyan]",
        border_style="green",
        title="Backup Complete"
    ))


@app.command()
def stats(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file (default: stats.json)"),
):
    """Export statistics as JSON"""
    if not DB_PATH.exists():
        console.print("[red]❌ No prompts database found[/red]")
        raise typer.Exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Collect statistics
    stats = {}

    cursor.execute("SELECT COUNT(*) as total FROM prompts")
    stats["total_prompts"] = cursor.fetchone()["total"]

    cursor.execute("SELECT AVG(rating) as avg FROM prompts WHERE rating IS NOT NULL")
    stats["avg_rating"] = cursor.fetchone()["avg"]

    cursor.execute("SELECT COUNT(*) as today FROM prompts WHERE DATE(timestamp) = DATE('now')")
    stats["today"] = cursor.fetchone()["today"]

    cursor.execute("SELECT domain, COUNT(*) as count FROM prompts GROUP BY domain ORDER BY count DESC")
    stats["domains"] = {row["domain"]: row["count"] for row in cursor.fetchall()}

    cursor.execute("SELECT model, COUNT(*) as count FROM prompts GROUP BY model ORDER BY count DESC")
    stats["models"] = {row["model"]: row["count"] for row in cursor.fetchall()}

    conn.close()

    output_file = output or Path("stats.json")

    with open(output_file, "w") as f:
        json.dump(stats, f, indent=2)

    console.print(Panel(
        f"[green]✅ Statistics exported[/green]\n"
        f"📁 Saved to: [cyan]{output_file.absolute()}[/cyan]\n\n"
        f"📊 Summary:\n"
        f"   • Total prompts: {stats['total_prompts']}\n"
        f"   • Avg rating: {stats['avg_rating']:.1f}/5 ⭐\n"
        f"   • Today: {stats['today']} prompts",
        border_style="green",
        title="Stats Export Complete"
    ))


@app.command()
def markdown(
    min_rating: Optional[int] = typer.Option(None, "--min-rating", "-r", help="Only export prompts rated >= this"),
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Filter by domain"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Filter by model"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file (default: prompts-[domain].md)"),
):
    """Export prompts to Markdown journal format"""
    prompts = get_all_prompts()

    # Apply filters
    if min_rating:
        prompts = [p for p in prompts if p.get("rating") and p["rating"] >= min_rating]
    if domain:
        prompts = [p for p in prompts if p.get("domain") == domain]
    if model:
        prompts = [p for p in prompts if p.get("model") == model]

    if not prompts:
        console.print("[yellow]⚠️  No prompts match your filters[/yellow]")
        return

    # Generate markdown
    md_lines = []
    md_lines.append(f"# Pro-mpt Archive Export\n")
    md_lines.append(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if domain:
        md_lines.append(f"**Domain:** {domain}\n")
    if model:
        md_lines.append(f"**Model:** {model}\n")
    if min_rating:
        md_lines.append(f"**Min Rating:** {min_rating}⭐\n")

    md_lines.append(f"**Total:** {len(prompts)} prompts\n\n")
    md_lines.append("---\n\n")

    # Add each prompt
    for i, prompt in enumerate(prompts, 1):
        timestamp = prompt.get("timestamp", "").split("T")[0]
        rating = "⭐" * (prompt.get("rating") or 0) if prompt.get("rating") else "unrated"

        md_lines.append(f"## {i}. {prompt.get('query', 'Untitled')[:80]}\n\n")
        md_lines.append(f"**Date:** {timestamp}\n")
        md_lines.append(f"**Model:** {prompt.get('model', 'unknown')}\n")
        md_lines.append(f"**Domain:** {prompt.get('domain', 'general')}\n")
        md_lines.append(f"**App:** {prompt.get('app', 'general')}\n")
        md_lines.append(f"**Rating:** {rating}\n\n")

        if prompt.get("query"):
            md_lines.append(f"**Query:**\n```\n{prompt['query']}\n```\n\n")

        if prompt.get("response"):
            md_lines.append(f"**Response:**\n```\n{prompt['response'][:500]}\n```\n\n")

        if prompt.get("notes"):
            md_lines.append(f"**Notes:** {prompt['notes']}\n\n")

        md_lines.append("---\n\n")

    # Write file
    output_file = output or Path(f"prompts-{domain or 'archive'}.md")
    with open(output_file, "w") as f:
        f.writelines(md_lines)

    console.print(Panel(
        f"[green]✅ Exported {len(prompts)} prompts[/green]\n"
        f"📁 Saved to: [cyan]{output_file.absolute()}[/cyan]",
        border_style="green",
        title="Markdown Export Complete"
    ))


@app.callback()
def main():
    """Export your prompt archive in various formats"""
    pass


if __name__ == "__main__":
    app()
