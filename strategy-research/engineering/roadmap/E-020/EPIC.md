# E-020 — Cut per-dispatch codebase context cost (scoped CLAUDE.md, then re-evaluate tree-sitter)

**State:** new
**Owner:** Jérémy (coordinate with Dorian)
**Updated:** 2026-08-13

## Why

Raised directly by Dorian (Slack, 2026-08-10): working any single bug
routinely burns roughly half his context budget before he's even made a
change, which gets expensive fast with 3-5 subagents and multiple iteration
rounds on a ~1M-token codebase. Root cause candidate: `trading-bot/` (the
larger, older half of the repo) has no scoped `CLAUDE.md` and no doc-index
telling an agent where to look — `strategy-research/` already solved this
for itself (`CLAUDE.md` + `DOC_INDEX.md`, "the only mandatory read for an
agent starting cold"), but that pattern was never extended to
`trading-bot/`. Without it, every session — and every subagent dispatched
within it — re-derives the same known landmines from scratch (e.g. the CWD
dependency that breaks 3 `k3` tests from repo root, the exact-pin
requirement on `pandas<3`, the holdout-seal date-literal rules) instead of
reading one short paragraph.

Checked first (per Amendment 9): `engineering/DISPATCH_MODEL.md`'s existing
"Context economy" section already governs a *different* problem — research
director session length and chat-scroll hygiene for the campaign loop. It
does not address per-task codebase-read cost or `trading-bot/`'s missing
doc-index, so this epic is complementary, not a duplicate. No existing
`CLAUDE.md` coverage exists for `trading-bot/` beyond the repo root
(`find ... -iname CLAUDE.md` → only `/CLAUDE.md` and
`/strategy-research/CLAUDE.md`). No `tree-sitter` references exist anywhere
in the tree — genuinely unstarted.

Related but out of scope here: **E-006** (untrack the committed Windows
`venv/` — still 449 tracked files, still `new`) would also cut incidental
context bloat from broad file scans. Cite it as a parallel quick win; do
not fold its scope into this epic.

## Done when

- `trading-bot/` has a root `CLAUDE.md` plus scoped `CLAUDE.md` files in at
  least `core/`, `data/`, and `execution/`, each naming that folder's known
  landmines with a concrete file:line reference (verified by listing the
  files and checking each cites at least one).
- A measured before/after: 2-3 recent real bug dispatches replayed with vs
  without the new docs in place, reporting the token/tool-call cost of just
  the "figure out what to read" phase for each — not a narrative claim.
- A written go/no-go on tree-sitter that cites those measured numbers
  (per Amendment 10 — a mechanism's effect size must be measured before it
  drives a decision; do not build tree-sitter speculatively).

## Stories

- [ ] S1 — Inventory landmines: grep prior red-team findings, session
      reports, and the Notion ledger across both `trading-bot/` and
      `strategy-research/` for known gotchas, and list each with a
      file:line reference. This is raw material for S2, not invention.
- [ ] S2 — Write `trading-bot/CLAUDE.md` plus scoped `CLAUDE.md` files for
      its highest-traffic subfolders (`core/`, `data/`, `execution/`),
      each citing the S1 landmines relevant to that folder.
- [ ] S3 — Measure: replay 2-3 recent real bug fixes' file-discovery step
      with the new docs in place vs. without; record tokens/tool-calls
      spent on orientation only, and report the delta.
- [ ] S4 — Decision write-up: given S3's numbers, a go/no-go recommendation
      on a tree-sitter-based symbol index, plus a separate (zero build
      cost) recommendation on subagent-prompting discipline — handing
      subagents exact file:line references instead of open-ended
      exploration prompts, to cut duplicate exploration across parallel
      dispatches.

## Log

- 2026-08-13 — `new`. Raised by Dorian (Slack, 2026-08-10) re: per-dispatch
  token/context cost on a ~1M-token codebase; discussed with Jérémy + agent
  2026-08-13, who asked for this to be tracked as an epic and explicitly
  deferred execution ("not to do right now but to plan it"). Checked
  `DISPATCH_MODEL.md`'s "Context economy" section and the tree for prior
  art first (Amendment 9) — no overlap found; see Why.
