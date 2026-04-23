#!/usr/bin/env python3
"""
Analyze growth patterns and generate insights
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"


def analyze():
    """Analyze patterns and generate insights"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get last 7 days of data
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()

    c.execute("""
        SELECT domain, COUNT(*) as count, AVG(rating) as avg_rating
        FROM prompts
        WHERE timestamp > ?
        GROUP BY domain
        ORDER BY count DESC
    """, (seven_days_ago,))
    recent_domains = c.fetchall()

    # Find your strongest domains
    c.execute("""
        SELECT domain, AVG(rating) as avg_rating
        FROM prompts
        GROUP BY domain
        HAVING COUNT(*) >= 3
        ORDER BY avg_rating DESC
        LIMIT 3
    """)
    strengths = c.fetchall()

    # Find areas needing attention (low ratings)
    c.execute("""
        SELECT domain, AVG(rating) as avg_rating, COUNT(*) as count
        FROM prompts
        WHERE rating IS NOT NULL AND rating <= 2
        GROUP BY domain
        ORDER BY count DESC
        LIMIT 3
    """)
    challenges = c.fetchall()

    # Get total stats
    c.execute("SELECT COUNT(*) as total FROM prompts")
    total = c.fetchone()["total"] or 0

    c.execute("SELECT COUNT(*) as count FROM prompts WHERE DATE(timestamp) = DATE('now')")
    today = c.fetchone()["count"]

    c.execute("SELECT AVG(rating) as avg FROM prompts WHERE rating IS NOT NULL")
    avg_rating = c.fetchone()["avg"] or 0

    conn.close()

    # Generate insights
    insights = []

    if today == 0:
        insights.append("💡 No prompts logged today. Start with: pro-log \"your question\" --rating 5")

    if recent_domains:
        top_domain = recent_domains[0][0]
        insights.append(f"📚 You're focused on [{top_domain}] this week ({recent_domains[0][1]} prompts)")

    if strengths:
        strong = [s[0] for s in strengths if s[1] >= 4.5]
        if strong:
            insights.append(f"⭐ You're strong in: {', '.join(strong)}")

    if challenges:
        insight_text = f"🔧 Areas to improve: {challenges[0][0]} (avg {challenges[0][1]:.1f}/5)"
        insights.append(insight_text)

    if total < 10:
        insights.append("📈 Log 10+ prompts to see meaningful patterns")

    if avg_rating >= 4.5:
        insights.append("🎯 Great selection of high-quality prompts!")

    # Display insights
    if insights:
        console.print("[bold cyan]💡 Insights & Suggestions[/bold cyan]")
        for insight in insights:
            console.print(f"  {insight}")
        console.print()


if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        console.print(f"[dim]Insights engine warming up... {e}[/dim]")
