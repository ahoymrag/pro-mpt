# Prompt — MVP Product Brief

## Product promise
Prompt is a personal, human-readable journal of the things you ask AI, captured automatically with as little setup as possible and kept locally for years.

## Experience
- Each conversation is one journal page.
- Save the user's messages only; do not save AI replies.
- Sort pages chronologically by conversation activity.
- Add lightweight source and time metadata without making the journal feel like a database.
- Capture quietly in the background, with clear controls to review, edit, exclude, and delete.
- Provide a playful, cheeky daily stats widget showing useful activity and a direct path into today's pages.

## Product principles
- Be provider-agnostic. Integrations feed a shared conversation format rather than defining separate archives.
- Prefer connections to apps and services the user is already signed into.
- Be honest about what each integration can capture and how reliably it can do so.
- Keep the personal archive private and local-first by default.
- Make the archive pleasant to read years later; avoid turning it into a leaderboard or productivity score.

## MVP direction
Ship a focused, usable personal version with a dependable capture path, unified conversation pages, chronological browsing, privacy/review controls, and the daily stats widget. Add integrations incrementally based on supported local data or user-authorized browser connections. Do not claim universal coverage until each source is verified.

## Current repo notes
The existing code already has a SQLite archive, CLI, journal/morning commands, and local importers for Claude Code and Gemini CLI. Current import semantics differ: Claude Code stores only the first user message per session, while Gemini CLI stores individual user messages. The importer currently uses sidecar text files to track imported IDs and does not pass source timestamps through to the database insert path. These are key reliability and data-model gaps for the MVP.
