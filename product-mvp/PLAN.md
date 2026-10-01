# Prompt MVP — Delivery Plan

## 1. Define the canonical journal model
- A conversation is one journal page, with stable source and conversation identifiers.
- Store only user-authored turns, each with its original timestamp and ordering.
- Preserve source metadata (provider, app/project when available) separately from journal prose.
- Support safe updates as a conversation grows, deduplication, retries, and deletion.
- Migrate existing SQLite records without losing data; retain export and backup paths.

## 2. Make capture dependable
- Keep integrations modular behind a shared connector contract.
- Harden current Claude Code and Gemini CLI connectors: timestamp preservation, incremental updates, idempotency, clear errors, and restart-safe checkpoints.
- Add a capture status view: connected sources, last successful scan, captured pages, and actionable errors.
- Run capture in the background with a foreground/manual sync path and graceful shutdown.
- Ensure one malformed source file does not stop other sources from importing.

## 3. Build the journal experience
- Browse chronological conversation pages.
- Open a page to read the user's messages in order with friendly date/source metadata.
- Review, edit, exclude, or delete captured material.
- Keep manual capture available for anything an integration cannot reach.

## 4. Daily widget
- Show today's conversation count, message count, and connected-source capture status.
- Use warm, cheeky copy without ranking the user's productivity or implying meaning the data cannot support.
- Link directly to today's journal pages and the capture review queue.

## 5. Agnostic integrations
- Prioritize sources with dependable, user-authorized local or browser access.
- Treat each provider integration as an adapter into the canonical conversation format.
- Document requirements, captured fields, known gaps, and validation for each adapter.
- Do not promise access to a service solely because the user is signed in; use only supported, permissioned access paths.

## 6. Ship checklist
- Fresh install and upgrade preserve existing archives.
- Repeat scans do not create duplicate conversations or turns.
- Capture works after restart and reports failures clearly.
- Only user messages appear in journal pages.
- A full export/backup and deletion flow are available.
- README, setup guide, privacy statement, and integration matrix match verified behavior.
- Release tagged and pushed to GitHub after review.
