# linear-tool

One script, `linear_archive.py`, to archive Linear issues by a simple condition.

## Why this exists

Linear's Free plan caps **non-archived** issues at 250 (the in-app label is
"Issues (excluding archive)"). Closing/canceling an issue does **not** free
up room — it still counts until archived.

The product has **no manual archive action anywhere** — not web, not
desktop, not mobile. Linear's own docs: *"Archiving happens automatically
with no option to manually archive items."* The only in-product path is
auto-archive after an inactivity period (configurable in Team Settings →
Issue statuses & automations, range roughly 1–12 months, defaults 28
days/completed and 7 days/canceled).

The GraphQL API's `archiveIssue` mutation works immediately regardless of
plan tier, even though the UI doesn't expose it. This script calls that
mutation directly. Archiving is reversible — archived issues stay
searchable and can be restored from the team's Archives page.

## Getting a key

Linear → Settings → Security & access → API keys → create a personal API
key. Works on the Free plan. Auth header format is `Authorization: <key>`
(no `Bearer` prefix — that's OAuth2-only).

**Never** commit the key, pass it as a CLI argument (it'll land in shell
history), or paste it into a chat/log.

**Where to put it — pick one:**

1. **Local file (persists across sessions):** create
   `strategy-research/engineering/linear-tool/.env` containing one line:
   ```
   LINEAR_API_KEY=lin_api_...
   ```
   This exact path is already covered by the repo's root `.gitignore`
   (bare `.env` pattern matches at any depth) — it will never be committed.
   Sanity-check with `git check-ignore -v strategy-research/engineering/linear-tool/.env`
   if you want to be sure before trusting it. The script reads this file
   automatically if `LINEAR_API_KEY` isn't already set in the environment.

2. **Env var (one-off, doesn't persist):**
   ```
   export LINEAR_API_KEY=lin_api_...
   python linear_archive.py ...
   unset LINEAR_API_KEY
   ```

If a key is ever pasted somewhere it shouldn't be (chat, ticket, etc.),
treat it as compromised and rotate it (revoke + generate a new one) —
don't assume deleting the message removes it from logs.

## Usage

Always dry-run first — the script only prints matches unless you pass
`--execute`:

```
python linear_archive.py --state completed,canceled,duplicate --closed-before 2026-08-31
python linear_archive.py --state completed,canceled,duplicate --closed-before 2026-08-31 --execute
python linear_archive.py --ids CUL-34,CUL-142 --execute
```

- `--state` — comma-separated state *types* (not display names): `completed`,
  `canceled`, `duplicate`. Never pass an active type here.
- `--closed-before` / `--closed-after` — `YYYY-MM-DD`, inclusive, checked
  against whichever of `completedAt`/`canceledAt` is set.
- `--ids` — explicit identifier list (`CUL-34,CUL-142`); overrides
  `--state`/`--closed-*` when given.
- `--team` — defaults to `CUL` (the only team as of 2026-09).

Every real (`--execute`) run appends a dated entry to
`linear_archive_log.md` in this folder — condition used, count, identifiers.
Check that file before asking "what's already been archived."

## Known limits (kept deliberately out of the script to keep it simple)

- Fetches one page (250 non-archived issues) and hard-fails if there are
  more. At that point archive a batch, re-run, or raise the page size in
  the script.
- No `--label` / `--project` filter. If you need those, add a condition to
  `matches()` — it's a five-line function.
- Doesn't support un-archiving. Use the Linear UI's Archives page to
  restore (`G` then `X`, or the team's three-dot menu).

## Lesson learned building this (2026-09-05)

The first attempt built the GraphQL mutation by hand-escaping quotes in a
bash loop (`\\\"`) — it silently produced malformed JSON on every batch
("Bad control character in string literal") and archived nothing. Fixed by
building the request body with `json.dumps` in Python instead of shell
string concatenation, which is what this script does. If you're tempted to
do this ad hoc in a shell one-liner again: don't, use this script.
