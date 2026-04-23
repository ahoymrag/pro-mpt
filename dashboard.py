#!/usr/bin/env python3
"""
Pro-MPT Dashboard - Terminal UI overlay showing progress and metrics
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
# Progress imports (not used directly but available)
from rich.table import Table
from rich import box
from rich.live import Live
from rich.align import Align
import time

console = Console()
DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"


class PromptMetrics:
    """Calculate metrics from database"""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def get_expertise_by_domain(self):
        """Get expertise level (0-100) for each domain"""
        self.c.execute("""
            SELECT domain, COUNT(*) as count, AVG(rating) as avg_rating
            FROM prompts
            GROUP BY domain
            ORDER BY avg_rating DESC
        """)
        results = self.c.fetchall()

        expertise = []
        for row in results:
            if row["avg_rating"]:
                level = min(100, int((row["avg_rating"] / 5.0) * 100))
                expertise.append({
                    "domain": row["domain"],
                    "level": level,
                    "count": row["count"],
                    "rating": row["avg_rating"]
                })
        return expertise

    def get_model_breakdown(self):
        """Get model usage breakdown"""
        self.c.execute("""
            SELECT model, COUNT(*) as count
            FROM prompts
            GROUP BY model
            ORDER BY count DESC
        """)
        results = self.c.fetchall()

        total = sum(r["count"] for r in results)
        breakdown = []
        for row in results:
            pct = int((row["count"] / total) * 100) if total > 0 else 0
            breakdown.append({
                "model": row["model"],
                "count": row["count"],
                "percentage": pct
            })
        return breakdown, total

    def get_rating_distribution(self):
        """Get distribution of ratings"""
        self.c.execute("""
            SELECT rating, COUNT(*) as count
            FROM prompts
            WHERE rating IS NOT NULL
            GROUP BY rating
            ORDER BY rating DESC
        """)
        results = self.c.fetchall()

        total = sum(r["count"] for r in results)
        distribution = {}
        for r in range(5, 0, -1):
            count = next((row["count"] for row in results if row["rating"] == r), 0)
            pct = int((count / total) * 100) if total > 0 else 0
            distribution[f"★{r}"] = {"count": count, "percentage": pct}

        return distribution, total

    def get_daily_progress(self, days=7):
        """Get prompts added per day for last N days"""
        dates = []
        for i in range(days, -1, -1):
            date = (datetime.now() - timedelta(days=i)).date()
            self.c.execute(
                "SELECT COUNT(*) as count FROM prompts WHERE DATE(timestamp) = ?",
                (date.isoformat(),)
            )
            count = self.c.fetchone()["count"]
            dates.append({"date": date.strftime("%m-%d"), "count": count})

        return dates

    def get_overall_stats(self):
        """Get overall statistics"""
        self.c.execute("SELECT COUNT(*) as total FROM prompts")
        total = self.c.fetchone()["total"]

        self.c.execute("SELECT AVG(rating) as avg FROM prompts WHERE rating IS NOT NULL")
        avg_rating = self.c.fetchone()["avg"] or 0

        self.c.execute("SELECT COUNT(DISTINCT domain) as count FROM prompts")
        domains = self.c.fetchone()["count"]

        self.c.execute("SELECT COUNT(DISTINCT model) as count FROM prompts")
        models = self.c.fetchone()["count"]

        return {
            "total": total,
            "avg_rating": avg_rating,
            "domains": domains,
            "models": models,
        }

    def close(self):
        self.conn.close()


def render_expertise_bars(metrics):
    """Render expertise progress bars"""
    table = Table(title="📈 Expertise by Domain", box=box.ROUNDED, border_style="cyan")
    table.add_column("Domain", style="cyan", width=15)
    table.add_column("Progress", width=25)
    table.add_column("Level", justify="right", style="green")
    table.add_column("Count", justify="right", style="dim")

    expertise = metrics.get_expertise_by_domain()

    for item in expertise:
        level = item["level"]
        bar_length = 20
        filled = int((level / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)

        color = "green" if level >= 80 else "yellow" if level >= 60 else "red"
        progress = f"[{color}]{bar}[/{color}] {level}%"

        table.add_row(
            item["domain"],
            progress,
            f"{item['rating']:.1f}⭐",
            str(item["count"])
        )

    return table


def render_model_breakdown(metrics):
    """Render model usage breakdown"""
    table = Table(title="🤖 Model Usage", box=box.ROUNDED, border_style="magenta")
    table.add_column("Model", style="magenta", width=15)
    table.add_column("Usage", width=25)
    table.add_column("Count", justify="right", style="dim")

    breakdown, total = metrics.get_model_breakdown()

    for item in breakdown:
        pct = item["percentage"]
        bar_length = 20
        filled = int((pct / 100) * bar_length)
        bar = "▰" * filled + "▱" * (bar_length - filled)

        progress = f"[magenta]{bar}[/magenta] {pct}%"

        table.add_row(
            item["model"],
            progress,
            str(item["count"])
        )

    return table


def render_rating_distribution(metrics):
    """Render rating distribution"""
    table = Table(title="⭐ Rating Distribution", box=box.ROUNDED, border_style="yellow")
    table.add_column("Rating", style="yellow", width=8)
    table.add_column("Distribution", width=25)
    table.add_column("Count", justify="right", style="dim")

    distribution, total = metrics.get_rating_distribution()

    for rating, data in distribution.items():
        pct = data["percentage"]
        bar_length = 20
        filled = int((pct / 100) * bar_length)
        bar = "★" * filled + "☆" * (bar_length - filled)

        progress = f"[yellow]{bar}[/yellow] {pct}%"

        table.add_row(
            rating,
            progress,
            str(data["count"])
        )

    return table


def render_daily_progress(metrics):
    """Render last 7 days of activity"""
    table = Table(title="📅 Last 7 Days", box=box.ROUNDED, border_style="green")
    table.add_column("Date", style="green", width=10)
    table.add_column("Activity", width=25)
    table.add_column("Count", justify="right", style="dim")

    daily = metrics.get_daily_progress(7)
    max_count = max((d["count"] for d in daily), default=1)

    for day in daily:
        count = day["count"]
        bar_length = 20
        filled = int((count / max_count) * bar_length) if max_count > 0 else 0
        bar = "▪" * filled + "▫" * (bar_length - filled)

        color = "green" if count > 0 else "dim"
        progress = f"[{color}]{bar}[/{color}]"

        table.add_row(
            day["date"],
            progress,
            str(count)
        )

    return table


def render_header(metrics):
    """Render top stats header"""
    stats = metrics.get_overall_stats()

    text = f"""
[bold cyan]Total Archive:[/bold cyan] {stats['total']} prompts
[bold magenta]Avg Rating:[/bold magenta] {stats['avg_rating']:.1f}⭐
[bold green]Domains:[/bold green] {stats['domains']} | [bold yellow]Models:[/bold yellow] {stats['models']}
"""
    return Panel(text.strip(), border_style="cyan", padding=(1, 2))


def create_layout(metrics):
    """Create the dashboard layout"""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="body"),
    )

    layout["header"].update(render_header(metrics))

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    layout["left"].split_column(
        Layout(render_expertise_bars(metrics)),
        Layout(render_rating_distribution(metrics)),
    )

    layout["right"].split_column(
        Layout(render_model_breakdown(metrics)),
        Layout(render_daily_progress(metrics)),
    )

    return layout


def main():
    """Run the dashboard"""
    console.clear()

    try:
        metrics = PromptMetrics()

        with Live(create_layout(metrics), refresh_per_second=1, screen=True) as live:
            try:
                while True:
                    time.sleep(2)
                    live.update(create_layout(metrics))
            except KeyboardInterrupt:
                console.print("\n[cyan]Dashboard closed[/cyan]\n")

        metrics.close()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[dim]Make sure you have at least one prompt logged[/dim]")


if __name__ == "__main__":
    main()
