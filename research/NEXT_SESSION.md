# Handoff → next Claude Code session (written 2026-08-11 — FEED-DEPENDENCY SAFETY shipped + pushed + offered as PR #22)

Paste §1 into a fresh session. Everything below is context §1 refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home* (keep the two in sync).

**LAUNCH:** `claude --model "claude-opus-4-8[1m]"` — quotes mandatory (zsh globs `[1m]`).
**1M context for every model/lane.** Model governance: **fable = brain** (plans + gates), **opus-4.8 = lead + adversarial** (`redteam-48`/`reviewer-48`), **sonnet-5 = implementation**.

---

## 1. The prompt — paste this

> Read `CLAUDE.fork.md` (say so if the fork guardrails are already in context; else read it), `research/LEDGER.md` (newest entry + CARRIED-FORWARD), and this file. Then `git status && git log --oneline -8`.
>
> WHERE WE ARE (2026-08-11): **feed-dependency safety SHIPPED, pushed, and OFFERED upstream.** `fix/feed-dependency-safety` (Step 1 declarations + V1 → Step 2 `drop_feeds` + manifest → Step 3 V2 required-feed guard) merged to `mac/setup` `--no-ff` `d87b17bc`, pushed to origin (`e3639279`); three commits each opus-4.8-gated SHIP, Step 3 fable behaviour-checked. Byte-identical default (`5ccbec42`/24/−23.021%/−5.646, no `feeds` key); V2 (the one behaviour change, default-on) fires on NO shipped path. Fast 339 / slow 20. **Offered upstream as `loloze6/trading-bot#22`** (squashed `e46964a7`, red-teamed SHIP, mergeable-CLEAN). **PR #21 (candle-callback R4) was MERGED upstream (`9ae7507a`)** — a byte-identical sync-back is DUE.
>
> FIRST: (a) **Sync back PR #21** — it merged upstream (`9ae7507a`); `git fetch upstream && git merge upstream/master` into `mac/setup`; expect a **byte-identical no-op** (fork already carries the candle-callback fix; like `1b183758`/`3590a81d`). merge-tree dry-run first. (b) **Watch PR #22** (`gh pr view 22 --repo loloze6/trading-bot`) — if Jeremy merges it, sync back too (byte-identical no-op expected, fork == offer except 2 docstring lines the fork keeps). Don't touch the PR branch except on his feedback.
>
> THEN the queue: (1) **Feature B** — real kraken funding via ccxt `krakenfutures` (Notion Bugs & Tasks, Fork order 33): an auto-fetching venue like binance, NOT a manual ingest. 4 gating problems — cadence (hourly, not 8h; pipeline hardcodes 8h in 5 places), symbol map (`BTCUSD` → `PF_XBTUSD`/`BTC/USD:USD`), ~2020+ coverage, and the COHERENCE question (single-symbol engine can't express spot+perp carry — must survive `HYPOTHESIS.md` first). Rides on the shipped droppable-feed as its empty-coverage safety net. (2) **First kraken breadth campaign** — 19-pair `*USD`, now runnable with `drop_feeds=['funding_rate','fear_greed']` (no funding data needed) via `/new-hypothesis`. (3) **#32 double-gating (High, ticketed)** — get strategy-research tests into the gate (lazy `genai.Client()` OR a CI lane with a dummy key); a signature change silently broke 8 ungated tests this session. (4) `_close_all_positions_at_end` duplicate-final-bar-state bug (pre-existing, gates `fix/metrics-bar-equity`). (5) untrack `results/trades.json` (Low). (6) risk layer (23), Venue epic (30).
>
> HARD RULES: never run live; holdout sealed (never a window past 2025-12-31; never open `holdout_sealed/`); every market-data experiment → a `research/TRIALS.csv` row; no secrets; origin only, PRs to Jeremy (don't touch PR branches except on his feedback); no `Co-Authored-By`. **ANY ccxt work → load the `ccxt-python` (or `ccxt-cli`) skill FIRST + confirm via `.has`/introspection — never from memory (standing rule, in project memory).** zsh traps: unquoted `$var` doesn't word-split (use `${=var}`); `git commit -F <file>`; absolute paths; `cd` is zoxide-aliased (use `cd <path> 2>/dev/null` or absolute paths); `main.py simulate` overwrites tracked `results/trades.json` (restore before commit). Commit gate: `basedpyright --venvpath <repo>` + `ruff` on changed `.py`, DELTA only.

---

## 2. State (2026-08-11)

| | |
|---|---|
| Branch | `mac/setup` @ `e3639279` (feed-dependency-safety merged `d87b17bc` + bookkeeping) — pushed to origin |
| Feature branch | `fix/feed-dependency-safety` @ `5ee5ab16` (local); offer branch `fix/feed-dependency-safety-upstream` @ `e46964a7` (pushed to origin) |
| Baseline anchor | `5ccbec42`/`5a75366c`/24/−23.021%/−5.646; fast **339** / slow **20** |
| Upstream | `9ae7507a` (PR #21 candle-callback MERGED); **PR #22 (feed-dependency) OPEN, mergeable-CLEAN** |
| DUE | **sync back PR #21** (`9ae7507a` → `mac/setup`, byte-identical no-op) |
| Open tickets | Feature B (33); **#32 double-gating (High)**; bar-state dup-row bug; untrack trades.json (Low); test-visibility (32); risk layer (23); Venue epic (30) |
| Awareness | `mac/setup`'s FULL strategy-research suite has **2 pre-existing `c7ext` failures** (on `cd1701ae` too; unrelated) |
| Next | sync PR #21 → watch PR #22 → Feature B or first kraken breadth campaign (`drop_feeds`) |

## 3. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol |
| `research/LEDGER.md` | newest entry (feed-dependency-safety) + CARRIED-FORWARD |
| `FORK_CHANGES.md` | 2026-08-11 feed-dependency-safety section (PR #22 offered) |
| `.omc/plans/feed-dependency-safety-architecture.md` | the shipped design (status SHIPPED) |
| Notion: Mac Fork — Home; Bugs & Tasks (Feature B, #32, bar-state, trades.json) | statuses + locked decisions |
