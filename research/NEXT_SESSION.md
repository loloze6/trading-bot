# Handoff → next Claude Code session (written 2026-08-10 — issue #20 R4 SHIPPED as PR #21; PR #19 synced back; DIALING DOWN)

Paste §1 into a fresh session. Everything below is context §1 refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home* (keep the two in sync).

**LAUNCH:** `claude --model "claude-opus-4-8[1m]"` — quotes mandatory (zsh globs `[1m]`).
**1M context is the rule for every model/lane.** Model governance: **fable = brain** (plans + gates, use sparingly — constrained), **opus-4.8 = lead + adversarial** (`redteam-48`/`reviewer-48`), **sonnet-5 = implementation**.

**⚠️ DIALING DOWN (Dorian, 2026-08-09 evening): approaching usage limits — stepping back for a few days. No urgency on the queue below; keep lanes lean; fable is the constrained resource (use sparingly).**

---

## 1. The prompt — paste this

> Read `CLAUDE.fork.md` (say so if the fork guardrails are already in context; else read it), `research/LEDGER.md` (newest entry + CARRIED-FORWARD), and this file. Then `git status && git log --oneline -8`.
>
> WHERE WE ARE (2026-08-10): `mac/setup` tip is the 2026-08-10 bookkeeping commit (parents: candle-callback fix `37f73fa2` + PR-#19 sync-back merge `3590a81d`). **Two things shipped this session:** (1) **PR #19** (exchange-plumbing 12+13) was merged upstream and **synced back** as a byte-identical no-op merge `3590a81d`; (2) **issue #20 (candle-callback arity / A14-R4) implemented + gated + merged to mac/setup (`37f73fa2`) and OFFERED upstream as PR #21** (`loloze6/trading-bot#21`, `fix/candle-callback-arity-upstream`, single commit `c6107fb1` blob-identical to the verified tree, `Closes #20`). Awaiting Jeremy's merge. **DIALING DOWN — no rush on anything.**
>
> FIRST: check whether Jeremy merged PR #21 (`gh pr view 21 --repo loloze6/trading-bot`). If merged → sync back (`/sync-upstream`): merge-tree dry-run FIRST; the fork's fix is blob-identical to the offer, so expect a byte-identical no-op merge (like PR #19's `3590a81d` and E-012's `1b183758`). Close the FORK_CHANGES candle-callback row → Merged upstream.
>
> THEN the queue (NO urgency): (1) **kraken-funding ingest** (Notion order 14) — GATES the first kraken campaign: the C2 aux fail-loud (`AuxFeedVenueError`) blocks any kraken FEED_REGISTRY run until a `kraken_..._funding_8h.csv` exists (the qualified `cache_key` already defines the exact filename the engine looks for). Kraken *spot* funding raises ccxt `NotSupported` (no live client), so likely path = ingest a `kraken_*_funding_8h.csv` the way the price archive was ingested. (2) **first kraken breadth campaign** (19-pair `*USD` universe — where the edge probability is) via `/new-hypothesis`. (3) test-visibility follow-up (order 32 — run_protocol tests not in the default gate + need a dummy Gemini key to import). (4) R-LIT 3-literals (31), G1 read-only cache guard, risk layer (23), Venue epic (30, joint with Jeremy).
>
> HARD RULES: never run live; holdout sealed (never a window past 2025-12-31; never open `holdout_sealed/`); every market-data experiment → a `research/TRIALS.csv` row; no secrets; origin only, PRs to Jeremy (don't touch PR branches except on his feedback); no `Co-Authored-By`. zsh traps: unquoted `$var` doesn't word-split (use `${=var}`); `git commit -F <file>`; absolute paths. Commit gate: `basedpyright` (CLI at `~/.local/bin/basedpyright`, reads `pyrightconfig.json`) + `ruff` (`/opt/homebrew/bin/ruff`) on changed `.py`, DELTA only. **Kraken = strategic-primary (MiCA); technical default STAYS binance; kraken-primary stays OFF Slack.**

---

## 2. State (2026-08-10)

| | |
|---|---|
| Branch | `mac/setup` — candle-callback fix `37f73fa2` + sync-back merge `3590a81d` + this session's bookkeeping commit; pushed to origin |
| Upstream | `62a04569` (PR #19 merged); **PR #21 OPEN** (candle-callback R4, `fix/candle-callback-arity-upstream`) awaiting Jeremy |
| Baseline anchor | `5ccbec42`/`5a75366c`/24/−23.021%/−5.646; fast 318/slow 18 (fast +1 from the new default-wiring test) |
| Blocked on Jeremy | PR #21 merge; `loloze` SSH key (culi.to) |
| Open tickets | kraken-funding ingest (14, gating); test-visibility (32); R-LIT 3-literals (31); G1 guard; risk layer (23); Venue epic (30) |
| Next task | (no urgency) sync PR #21 when merged → kraken-funding ingest (14) → first kraken campaign |

## 3. The queue (fork-order top-first)

PR #21 merge + sync → **kraken-funding ingest (14, gating)** → first kraken breadth campaign (19-pair `*USD`) → test-visibility (32) → R-LIT (31) → G1 read-only guard → risk layer (23) → Venue-model epic (30, trigger-gated, joint with Jeremy).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | newest entry (this session) + CARRIED-FORWARD |
| `FORK_CHANGES.md` | 2026-08-10 candle-callback row + exchange-plumbing (Merged upstream) |
| Notion: Mac Fork — Home; Bugs & Tasks (tickets 14/30/31/32); Decisions log 2026-08-10 | statuses + locked decisions |
