#!/usr/bin/env python3
"""
pro-export - Export your prompt archive to various formats
Export as JSON, CSV, or backup your entire database
"""

import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional
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


@app.callback()
def main():
    """Export your prompt archive in various formats"""
    pass


if __name__ == "__main__":
    app()
