#!/usr/bin/env python3
"""
pro-chat - Talk to Claude about pro-mpt
Chat conversationally to design, build, and improve pro-mpt
"""

import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from anthropic import Anthropic

console = Console()

PRO_MPT_HOME = Path(__file__).parent
SYSTEM_PROMPT = f"""You are Claude, an expert software engineer helping build and improve pro-mpt.

CONTEXT:
- pro-mpt is a personal prompt archive tool written in Python
- Location: {PRO_MPT_HOME}
- Current features: interactive mode, logging, searching, analysis, dashboard
- Architecture: DataStore (data layer), InputValidator (validation), CLI commands via Typer, beautiful UI via Rich

YOUR ROLE:
1. Answer questions about pro-mpt architecture and features
2. Suggest improvements and new features
3. Help the user design solutions by asking clarifying questions
4. When appropriate, provide specific code suggestions
5. Help refactor existing code
6. Explain technical decisions

IMPORTANT:
- Ask clarifying questions before suggesting major changes
- Suggest one thing at a time, not overwhelming lists
- Be conversational and helpful
- Reference specific files/functions when discussing code
- Explain trade-offs when there are multiple approaches

START: Greet the user and ask what they'd like to do with pro-mpt."""


def get_codebase_context():
    """Get relevant files from codebase for context"""
    context = "\n\nRELEVANT CODE STRUCTURE:\n"

    # Add key files
    key_files = [
        "pro_mpt.py",
        "dashboard.py",
        "analyze_growth.py",
        "setup.sh",
    ]

    for file in key_files:
        path = PRO_MPT_HOME / file
        if path.exists():
            with open(path) as f:
                lines = f.readlines()[:20]  # First 20 lines
                context += f"\n### {file} (first 20 lines)\n"
                context += "".join(lines)
                context += "...\n"

    return context


def chat():
    """Main chat loop"""
    client = Anthropic()
    conversation_history = []

    console.clear()
    console.print(Panel(
        "[bold cyan]🤖 pro-mpt AI Assistant[/bold cyan]\n"
        "[dim]Chat with Claude about building pro-mpt\n"
        "Type 'exit' to quit[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()

    # Initial greeting from Claude
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": "Hello, I'm ready to work on pro-mpt!"
            }]
        )

        greeting = response.content[0].text
        console.print(f"[cyan]Claude:[/cyan] {greeting}\n")
        conversation_history.append({
            "role": "assistant",
            "content": greeting
        })
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[dim]Make sure ANTHROPIC_API_KEY is set[/dim]")
        return

    # Chat loop
    while True:
        try:
            user_input = console.input("[bold green]You:[/bold green] ")

            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[cyan]Thanks for improving pro-mpt! Goodbye![/cyan]\n")
                break

            if not user_input.strip():
                continue

            # Add user message to history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })

            # Get Claude's response
            console.print("[dim]Claude is thinking...[/dim]")

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=conversation_history
            )

            assistant_message = response.content[0].text
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            console.print(f"\n[cyan]Claude:[/cyan] {assistant_message}\n")

        except KeyboardInterrupt:
            console.print("\n[cyan]Chat ended[/cyan]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]\n")


def main():
    """Entry point"""
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(Panel(
            "[red]❌ ANTHROPIC_API_KEY not set[/red]\n\n"
            "Set your API key:\n"
            "[bold]export ANTHROPIC_API_KEY='your-key-here'[/bold]\n\n"
            "Get one at: [link]https://console.anthropic.com/[/link]",
            border_style="red",
            padding=(1, 2)
        ))
        return

    chat()


if __name__ == "__main__":
    main()
