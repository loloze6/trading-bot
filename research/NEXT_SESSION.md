# Handoff → next Claude Code session (written 2026-08-11 — FEED-DEPENDENCY SAFETY shipped to mac/setup, NOT pushed)

Paste §1 into a fresh session. Everything below is context §1 refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home* (keep the two in sync).

**LAUNCH:** `claude --model "claude-opus-4-8[1m]"` — quotes mandatory (zsh globs `[1m]`).
**1M context for every model/lane.** Model governance: **fable = brain** (plans + gates), **opus-4.8 = lead + adversarial** (`redteam-48`/`reviewer-48`), **sonnet-5 = implementation**.

---

## 1. The prompt — paste this

> Read `CLAUDE.fork.md` (say so if the fork guardrails are already in context; else read it), `research/LEDGER.md` (newest entry + CARRIED-FORWARD), and this file. Then `git status && git log --oneline -8`.
>
> WHERE WE ARE (2026-08-11): **feed-dependency safety SHIPPED** — `fix/feed-dependency-safety` (Step 1 declarations + V1 registration guard → Step 2 `drop_feeds` + manifest provenance → Step 3 V2 required-feed guard) merged to `mac/setup` `--no-ff` as `d87b17bc`; three commits (`e67edaf6`/`094cbacf`/`5ee5ab16`), each opus-4.8-gated SHIP, Step 3 additionally fable behaviour-checked. Byte-identical default (`5ccbec42`/`5a75366c`/24/−23.021%/−5.646, no `feeds` key); V2 (the one declared behaviour change, default-on: a required feed that is empty raises `AuxFeedRequiredError` on every venue) fires on NO shipped path. Fast 339 / slow 20. **NOT pushed to origin — Dorian's push decision is pending.**
>
> FIRST: (a) **push decision** — `origin/mac/setup` is behind local `mac/setup` by the 3 feature commits + the merge + bookkeeping; push only on Dorian's OK. (b) Check PR #21 (`gh pr view 21 --repo loloze6/trading-bot`) — if merged, sync back (merge-tree dry-run first; byte-identical no-op expected).
>
> THEN the queue: (1) **Feature B** — real kraken funding via ccxt `krakenfutures` (Notion Bugs & Tasks, Fork order 33): an auto-fetching venue like binance, NOT a manual ingest. 4 gating problems — cadence (krakenfutures funding is hourly, not 8h; pipeline hardcodes 8h in 5 places), symbol map (spot `BTCUSD` → perp `PF_XBTUSD`/`BTC/USD:USD`), ~2020+ coverage (won't reach 2018 train start), and the COHERENCE question (single-symbol engine can't express a spot+perp carry trade — must survive `HYPOTHESIS.md` first). Depends on the shipped droppable-feed as its empty-coverage safety net. (2) **First kraken breadth campaign** — 19-pair `*USD`, now runnable with `drop_feeds=['funding_rate','fear_greed']` (no funding data needed) via `/new-hypothesis`. (3) **#32 double-gating (High, ticketed)** — get strategy-research tests into the gate (make `run_phase1_research`'s `genai.Client()` lazy, OR a CI lane with a dummy key); a signature change silently broke 8 ungated tests this session. (4) `_close_all_positions_at_end` duplicate-final-bar-state bug (pre-existing, gates `fix/metrics-bar-equity`). (5) untrack `results/trades.json` (Low). (6) risk layer (23), Venue epic (30).
>
> HARD RULES: never run live; holdout sealed (never a window past 2025-12-31; never open `holdout_sealed/`); every market-data experiment → a `research/TRIALS.csv` row; no secrets; origin only, PRs to Jeremy (don't touch PR branches except on his feedback); no `Co-Authored-By`. **ANY ccxt work → load the `ccxt-python` (or `ccxt-cli`) skill FIRST + confirm via `.has`/introspection — never from memory (standing rule, in project memory).** zsh traps: unquoted `$var` doesn't word-split (use `${=var}`); `git commit -F <file>`; absolute paths; `cd` is zoxide-aliased (use `cd <path> 2>/dev/null` or absolute paths). Commit gate: `basedpyright --venvpath <repo>` + `ruff` on changed `.py`, DELTA only. Kraken = strategic-primary (MiCA); technical default STAYS binance.

---

## 2. State (2026-08-11)

| | |
|---|---|
| Branch | `mac/setup` @ `d87b17bc` (feed-dependency-safety merged `--no-ff`) — **4 commits ahead of `origin/mac/setup`, NOT pushed** |
| Feature branch | `fix/feed-dependency-safety` @ `5ee5ab16` (kept locally; merged) |
| Baseline anchor | `5ccbec42`/`5a75366c`/24/−23.021%/−5.646; fast **339** / slow **20** |
| Upstream | `62a04569`; **PR #21 OPEN** (candle-callback R4) awaiting Jeremy |
| Blocked on Dorian | push `mac/setup` → origin; upstream offer of feed-dependency-safety (issue-first) |
| Open tickets | Feature B (33); **#32 double-gating (High)**; bar-state dup-row bug; untrack trades.json (Low); test-visibility (32); risk layer (23); Venue epic (30) |
| Awareness | `mac/setup`'s FULL strategy-research suite has **2 pre-existing `c7ext` failures** (reproduce on `cd1701ae`; unrelated to this feature) |
| Next | push decision → Feature B (`/new-hypothesis`) OR first kraken breadth campaign (`drop_feeds`) |

## 3. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol |
| `research/LEDGER.md` | newest entry (feed-dependency-safety) + CARRIED-FORWARD |
| `FORK_CHANGES.md` | 2026-08-11 feed-dependency-safety section |
| `.omc/plans/feed-dependency-safety-architecture.md` | the shipped design (status SHIPPED) |
| Notion: Mac Fork — Home; Bugs & Tasks (Feature B, #32, bar-state, trades.json) | statuses + locked decisions |
