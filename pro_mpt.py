#!/usr/bin/env python3
"""
pro-mpt: Your personal prompt archive and expertise tracker
Track what you ask, which models, which apps, to see patterns and scale

A premium terminal UI for tracking your thinking journey.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import uuid
from typing import Optional, List, Dict, Any
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
from rich import box
from rich.columns import Columns
import time
import random
import shlex

app = typer.Typer(help="pro-mpt: Track your prompts, scale your systems")
console = Console()

# Color palette
COLORS = {
    "primary": "cyan",
    "accent": "magenta",
    "success": "green",
    "warning": "yellow",
    "info": "blue",
    "subtle": "dim white",
}


class Config:
    """Centralized configuration for pro-mpt"""

    # Paths
    DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"
    DATA_DIR = Path.home() / ".pro-mpt"

    # Display
    COLORS = COLORS
    DEFAULT_LIMIT = 10
    ANIMATION_DELAY = 0.05

    # Validation
    MIN_RATING = 1
    MAX_RATING = 5
    MAX_QUERY_LENGTH = 5000

    @classmethod
    def ensure_dirs(cls):
        """Ensure all required directories exist"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(cls):
        """Load config from environment variables (for Phase 2)"""
        # Future: Support .env files, cloud config, etc.
        pass


# Initialize config
Config.ensure_dirs()


from pro_mpt.db import Database

# Initialize config
Config.ensure_dirs()
data_store = Database(Config.DB_PATH)


class InputValidator:
    """Validate user input before processing with friendly messages"""

    @staticmethod
    def validate_query(query: str) -> str:
        """Validate and clean a prompt query"""
        if not query or not query.strip():
            raise ValueError("📝 Hmm, I need something to save. What's your prompt?")
        if len(query) > Config.MAX_QUERY_LENGTH:
            raise ValueError(f"📚 That's quite long! Keep it under {Config.MAX_QUERY_LENGTH} characters. (You can save shorter versions and add notes separately)")
        return query.strip()

    @staticmethod
    def validate_rating(rating: Optional[int]) -> Optional[int]:
        """Validate rating is in valid range"""
        if rating is None:
            return None
        if not isinstance(rating, int) or rating < Config.MIN_RATING or rating > Config.MAX_RATING:
            raise ValueError(f"⭐ Rating should be 1-5 stars. {Config.MIN_RATING} = 'meh', {Config.MAX_RATING} = 'chef's kiss'")
        return rating

    @staticmethod
    def validate_domain(domain: Optional[str]) -> Optional[str]:
        """Validate domain is reasonable"""
        if domain is None:
            return None
        if not domain.strip() or len(domain) > 100:
            raise ValueError("🏷️  Domains help organize your prompts. Try something like 'coding', 'creative', or 'analysis'")
        return domain.strip()


class CommandRegistry:
    """Registry of all interactive commands"""

    def __init__(self):
        self.commands = {}

    def register(self, name: str, fn: callable, help_text: str):
        """Register a command"""
        self.commands[name] = {
            "fn": fn,
            "help": help_text,
        }

    def get(self, name: str) -> Dict[str, Any]:
        """Get command by name"""
        return self.commands.get(name)

    def all(self) -> Dict[str, Dict[str, Any]]:
        """Get all commands"""
        return self.commands

    def help(self) -> str:
        """Generate help text for all commands"""
        help_text = "[bold cyan]PRO-MPT INTERACTIVE COMMANDS[/bold cyan]\n\n"
        for name, cmd in sorted(self.commands.items()):
            help_text += f"[bold]{name}[/bold]: {cmd['help']}\n"
        return help_text


def render_header():
    """Beautiful header with gradient effect"""
    header = Text()

    # Animated header with color gradient
    title = "◆ PRO-MPT ◆"
    subtitle = "Your Thinking Archive"

    header.append(title, style="bold cyan")

    return Panel(
        Align.center(
            f"[bold cyan]{title}[/bold cyan]\n[dim magenta]{subtitle}[/dim magenta]"
        ),
        border_style="cyan",
        padding=(1, 2),
    )


def render_success(message: str, details: Dict = None):
    """Beautiful success message with details"""
    content = f"[bold green]✓ {message}[/bold green]"

    if details:
        for key, value in details.items():
            content += f"\n  [dim cyan]{key}:[/dim cyan] [white]{value}[/white]"

    console.print(Panel(
        content,
        border_style="green",
        padding=(1, 1),
    ))


def render_rating_stars(rating: Optional[int]) -> str:
    """Convert rating to beautiful star display"""
    if not rating:
        return "○○○○○"
    stars = "★" * rating
    empty = "○" * (5 - rating)
    return f"[gold1]{stars}[/gold1]{empty}"


def render_prompt_card(row, show_response: bool = False):
    """Beautiful card for a single prompt"""

    # Header with query
    header = Text(row["query"], style="bold cyan")

    # Metadata row
    meta_parts = []
    if row["model"]:
        meta_parts.append(f"[magenta]{row['model']}[/magenta]")
    if row["app"]:
        meta_parts.append(f"[green]{row['app']}[/green]")
    if row["domain"]:
        meta_parts.append(f"[yellow]{row['domain']}[/yellow]")

    meta = " • ".join(meta_parts)

    # Rating
    stars = render_rating_stars(row["rating"])

    # Date
    date_str = row["timestamp"][:10]

    # Build content
    content = f"""[bold cyan]{row['query']}[/bold cyan]

[dim]ID:[/dim] {row['id']} [dim]|[/dim] {stars} [dim]|[/dim] {date_str}
{meta}"""

    if row["version"]:
        content += f"\n[dim]Version:[/dim] [cyan]{row['version']}[/cyan]"

    if row["notes"]:
        content += f"\n[dim italic]Note:[/dim italic] [white]{row['notes']}[/white]"

    if show_response and row["response"]:
        content += f"\n\n[dim]Response:[/dim]\n[white]{row['response'][:200]}[/white]"

    return Panel(
        content,
        border_style="cyan",
        expand=False,
        padding=(0, 1),
    )


@app.command()
def morning():
    """Morning greeting and quick stats"""
    do_morning()


def do_log(query: str, model: Optional[str] = None, agent: Optional[str] = None,
           app_name: Optional[str] = None, domain: Optional[str] = None,
           version: Optional[str] = None, response: Optional[str] = None,
           rating: Optional[int] = None, notes: Optional[str] = None):
    """Internal log function used by both CLI and interactive mode"""
    # Insert with animation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Archiving prompt...", total=None)
        time.sleep(0.3)

        prompt_id = data_store.add_prompt(
            query, model, agent, app_name, domain, version, response, rating, notes
        )

        progress.update(task, completed=True)

    # Success display
    details = {
        "ID": f"[cyan]{prompt_id}[/cyan]",
        "Query": query,
    }

    if model:
        details["Model"] = f"[magenta]{model}[/magenta]"
    if app_name:
        details["App"] = f"[green]{app_name}[/green]"
    if domain:
        details["Domain"] = f"[yellow]{domain}[/yellow]"
    if rating:
        details["Rating"] = render_rating_stars(rating)

    render_success("Prompt archived", details)


def do_search(query: str, app_filter: Optional[str] = None, 
              domain_filter: Optional[str] = None):
    """Internal search function"""
    results = data_store.search(query, app_filter, domain_filter)

    console.print(render_header())

    if not results:
        console.print(Panel(
            f"[yellow]⚠ No prompts found for '[bold]{query}[/bold]'[/yellow]\n[dim]Try a different search term[/dim]",
            border_style="yellow",
        ))
        return

    filter_text = ""
    if app_filter or domain_filter:
        filters = []
        if app_filter: filters.append(f"app: {app_filter}")
        if domain_filter: filters.append(f"domain: {domain_filter}")
        filter_text = f"\n[dim]Filters: {' • '.join(filters)}[/dim]"

    console.print(f"\n[bold cyan]Search: '{query}'[/bold cyan][dim] — {len(results)} result(s)[/dim]{filter_text}\n")

    for i, row in enumerate(results):
        console.print(render_prompt_card(row))
        if i < len(results) - 1:
            time.sleep(0.05)


def do_list(limit: int = 10, app_filter: Optional[str] = None):
    """Internal list function"""
    results = data_store.list_recent(limit, app_filter)

    console.print(render_header())

    if not results:
        console.print(Panel(
            "[yellow]No prompts yet[/yellow]\n[dim]Try: pro-mpt log \"your prompt here\"[/dim]",
            border_style="yellow",
        ))
        return

    table = Table(title=f"Recent {len(results)} Prompts", box=box.ROUNDED, border_style="cyan")
    table.add_column("Model", style="magenta")
    table.add_column("Query", style="white")
    table.add_column("Domain", style="yellow")
    table.add_column("Rating", justify="center")

    for row in results:
        rating_display = render_rating_stars(row["rating"]) if row["rating"] else "—"
        table.add_row(
            row["model"] or "—",
            row["query"][:40] + "..." if len(row["query"]) > 40 else row["query"],
            row["domain"] or "—",
            rating_display,
        )

    console.print(table)


def do_stats():
    """Internal stats function"""
    stats = data_store.get_stats()
    console.print(render_header())
    
    stats_text = f"""
[bold cyan]Your Statistics[/bold cyan]

[bold]Archive:[/bold] {stats['total']} prompts total
[bold]Models:[/bold] {stats['models']} active
[bold]Apps:[/bold] {stats['apps']} tracked
"""
    console.print(Panel(stats_text, border_style="cyan", padding=(1, 2)))


def do_journal(days: int = 7):
    """Display prompts grouped by day as milestones"""
    console.print(render_header())
    
    # Get prompts for the last N days
    conn = data_store._get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT DATE(timestamp) as day, COUNT(*) as count 
        FROM prompts 
        GROUP BY day 
        ORDER BY day DESC 
        LIMIT ?
    """, (days,))
    milestones = c.fetchall()

    if not milestones:
        console.print("[yellow]Your journal is empty. Start your journey by logging a thought![/yellow]")
        return

    for m in milestones:
        day_str = m["day"]
        count = m["count"]
        
        # Get intents for the day
        c.execute("""
            SELECT metadata FROM prompts 
            WHERE DATE(timestamp) = ? AND metadata IS NOT NULL
        """, (day_str,))
        meta_rows = c.fetchall()
        intents = {}
        for r in meta_rows:
            try:
                meta = json.loads(r["metadata"])
                intent = meta.get("intent", "unknown")
                intents[intent] = intents.get(intent, 0) + 1
            except: pass

        intent_summary = " • ".join([f"[cyan]{k}[/cyan]({v})" for k, v in intents.items()])
        
        console.print(Panel(
            f"[bold cyan]{day_str}[/bold cyan] — [white]{count} prompts[/white]\n"
            f"[dim]{intent_summary if intent_summary else 'No intent metadata'}[/dim]",
            border_style="blue",
            title=f"📅 Milestone",
            title_align="left"
        ))

        # Show prompts for this day
        day_prompts = data_store.search("", domain_filter=None) # Get all for now and filter manually
        day_prompts = [p for p in day_prompts if p["timestamp"].startswith(day_str)]
        
        for p in day_prompts[:5]: # Show top 5
            console.print(f"  [dim]•[/dim] {p['query'][:80]}{'...' if len(p['query']) > 80 else ''}")
        
        if count > 5:
            console.print(f"  [dim italic]... and {count-5} more[/dim italic]")
        console.print()

    conn.close()


def do_morning():
    """Internal morning greeting with milestones"""
    stats = data_store.get_stats()
    
    # Get yesterday vs today
    conn = data_store._get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM prompts WHERE DATE(timestamp) = DATE('now', '-1 day')")
    yesterday = c.fetchone()[0]
    conn.close()

    console.print(render_header())

    greeting = f"""[bold cyan]Good morning![/bold cyan]

[bold yellow]Milestone Status[/bold yellow]
  ✨ [bold white]{stats['today']}[/bold white] prompts today
  ⏮  [dim]{yesterday}[/dim] prompts yesterday
  📚 [bold cyan]{stats['total']}[/bold cyan] total moments in your archive

[dim italic]You are actively pushing for v1.1.0 and CITG production.[/dim]
"""
    console.print(Panel(greeting, border_style="cyan", padding=(1, 2)))


@app.command()
def journal(days: int = typer.Option(7, help="Number of days to show")):
    """View your thinking journey grouped by day"""
    do_journal(days)


def do_expertise(domain: Optional[str] = None):
    """Internal expertise function"""
    # Simple expertise view for now
    stats = data_store.get_stats()
    console.print(render_header())
    console.print(f"[bold cyan]Expertise Profile[/bold cyan]")
    console.print(f"You have tracked {stats['total']} prompts across {stats['apps']} applications.")


def do_export(fmt: str = "json"):
    """Internal export function"""
    results = data_store.list_recent(limit=1000)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Exporting...", total=len(results))

        filename = f"pro-mpt-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.{fmt}"
        if fmt == "json":
            with open(filename, "w") as f:
                json.dump(results, f, indent=2, default=str)
        else:
            import csv
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                if results:
                    writer.writerow(results[0].keys())
                    for row in results:
                        writer.writerow(row.values())
                        progress.advance(task)

    render_success(f"Exported {len(results)} prompts to {filename}")


@app.command()
def watch(interval: int = typer.Option(10, help="Interval in seconds")):
    """Ambiently watch for new prompts from all sources"""
    from ingest import main as run_ingest
    
    console.print(render_header())
    console.print(Panel(
        f"[bold green]Ambient Watch Active[/bold green]\n"
        f"[dim]Polling every {interval}s... Press Ctrl+C to stop.[/dim]",
        border_style="green"
    ))
    
    try:
        while True:
            run_ingest()
            time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[yellow]Watch stopped.[/yellow]")


@app.command()
def log(
    query: str = typer.Argument(..., help="The prompt you asked"),
    model: Optional[str] = typer.Option(None, help="Which model (claude, gpt4, etc)"),
    agent: Optional[str] = typer.Option(None, help="Which agent/service"),
    app_name: Optional[str] = typer.Option(None, "--app", help="Which app you were building"),
    domain: Optional[str] = typer.Option(None, help="Domain (dev, cooking, etc)"),
    version: Optional[str] = typer.Option(None, help="App version"),
    response: Optional[str] = typer.Option(None, help="The response you got"),
    rating: Optional[int] = typer.Option(None, help="Rate it 1-5"),
    notes: Optional[str] = typer.Option(None, help="Your notes"),
):
    """Log a prompt with beautiful confirmation"""
    do_log(query, model, agent, app_name, domain, version, response, rating, notes)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    app_filter: Optional[str] = typer.Option(None, "--app", help="Filter by app"),
    model_filter: Optional[str] = typer.Option(None, "--model", help="Filter by model"),
    domain_filter: Optional[str] = typer.Option(None, "--domain", help="Filter by domain"),
    min_rating: Optional[int] = typer.Option(None, "--min-rating", help="Minimum rating (1-5)"),
):
    """Search prompts with beautiful results"""
    do_search(query, app_filter, model_filter, domain_filter, min_rating)


@app.command()
def list(
    recent: int = typer.Option(10, help="Show N recent prompts"),
    app_filter: Optional[str] = typer.Option(None, "--app", help="Filter by app"),
):
    """List recent prompts in beautiful table"""
    do_list(recent, app_filter)


@app.command()
def expertise(
    domain: Optional[str] = typer.Option(None, help="Specific domain to analyze"),
    app_name: Optional[str] = typer.Option(None, "--app", help="Specific app to analyze"),
):
    """See your expertise journey with beautiful visualization"""
    do_expertise(domain or app_name)


@app.command()
def stats():
    """Dashboard-style stats"""
    do_stats()


@app.command()
def export(
    format: str = typer.Option("json", help="Format (json, csv)"),
    app_name: Optional[str] = typer.Option(None, "--app", help="Export specific app"),
):
    """Export prompts with progress animation"""
    do_export(format)


def parse_log_args(args: List[str]) -> Dict[str, Any]:
    """Parse arguments for log command"""
    query = None
    model = None
    rating = None
    app_name = None
    domain = None

    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            flag = args[i][2:]
            if i + 1 < len(args):
                if flag == "model":
                    model = args[i + 1]
                    i += 2
                elif flag == "rating":
                    try:
                        rating = InputValidator.validate_rating(int(args[i + 1]))
                    except (ValueError, TypeError):
                        raise ValueError(f"Invalid rating: {args[i + 1]}")
                    i += 2
                elif flag == "app":
                    app_name = args[i + 1]
                    i += 2
                elif flag == "domain":
                    domain = InputValidator.validate_domain(args[i + 1])
                    i += 2
                else:
                    i += 1
            else:
                i += 1
        else:
            # This is the query
            if query is None:
                query = args[i]
            else:
                query += " " + args[i]
            i += 1

    if not query:
        raise ValueError("Query cannot be empty")

    query = InputValidator.validate_query(query)
    return {"query": query, "model": model, "rating": rating, "app_name": app_name, "domain": domain}


def run_interactive_command(cmd_line: str):
    """Parse and execute a command from interactive mode"""
    if not cmd_line.strip():
        return True

    try:
        parts = shlex.split(cmd_line.strip())
    except ValueError as e:
        console.print(f"[red]Error parsing command: {e}[/red]")
        return True

    if not parts:
        return True

    command = parts[0]
    args = parts[1:]

    try:
        if command == "log":
            parsed = parse_log_args(args)
            do_log(**parsed)

        elif command == "search":
            if args:
                term = InputValidator.validate_query(args[0])
                do_search(term)
            else:
                raise ValueError("No search term provided")

        elif command == "list":
            do_list()

        elif command == "stats":
            do_stats()

        elif command == "morning":
            do_morning()

        elif command == "expertise":
            domain = None
            if "--domain" in args:
                idx = args.index("--domain")
                if idx + 1 < len(args):
                    domain = InputValidator.validate_domain(args[idx + 1])
            do_expertise(domain)

        elif command == "export":
            fmt = "json"
            if "--format" in args:
                idx = args.index("--format")
                if idx + 1 < len(args):
                    fmt = args[idx + 1]
            do_export(fmt)

        elif command == "help":
            show_interactive_help()

        elif command == "exit" or command == "quit":
            console.print("\n[cyan]Goodbye![/cyan]\n")
            return False

        elif command == "clear":
            import os
            os.system('clear' if os.name != 'nt' else 'cls')
            return True

        else:
            console.print(f"[yellow]Unknown command: {command}[/yellow]")
            console.print("[dim]Type 'help' for available commands[/dim]")

        return True

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        return True
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        return True


def show_interactive_help():
    """Show help for interactive mode"""
    help_text = """
[bold cyan]PRO-MPT INTERACTIVE COMMANDS[/bold cyan]

[bold]log[/bold] "query" [--model claude] [--rating 5] [--app myapp] [--domain dev]
  → Log a prompt you asked

[bold]search[/bold] "term" [--app myapp] [--domain dev]
  → Search your history

[bold]list[/bold]
  → Show recent prompts

[bold]stats[/bold]
  → View your statistics

[bold]morning[/bold]
  → Get your daily summary

[bold]expertise[/bold] [--domain dev]
  → Track your expertise growth

[bold]export[/bold] [--format json|csv]
  → Export your data

[bold]clear[/bold]
  → Clear the screen

[bold]help[/bold]
  → Show this help

[bold]exit[/bold] or [bold]quit[/bold]
  → Exit the interactive session

[dim]Tips:
• Always quote multi-word queries: log "How do I handle state?"
• Rate everything: --rating 5 for great, 3 for okay, 1 for not helpful
• Use --app and --domain to organize your work[/dim]
"""
    console.print(Panel(help_text, border_style="cyan", padding=(1, 2)))


@app.command()
def interactive():
    """Interactive mode - type commands like Claude Code"""
    import readline  # Enable history and arrow keys

    console.clear()
    console.print(render_header())
    console.print()
    console.print(
        Panel(
            "[bold cyan]Welcome to pro-mpt interactive mode![/bold cyan]\n"
            "[dim]Type 'help' for commands, 'exit' to quit[/dim]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()

    while True:
        try:
            user_input = console.input("[bold cyan]> [/bold cyan]")
            if not run_interactive_command(user_input):
                break
            console.print()
        except KeyboardInterrupt:
            console.print("\n[cyan]Goodbye![/cyan]\n")
            break
        except EOFError:
            console.print("\n[cyan]Goodbye![/cyan]\n")
            break


if __name__ == "__main__":
    app()
