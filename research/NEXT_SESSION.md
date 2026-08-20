# Handoff → next Claude Code session (written 2026-08-13 — PRs #21+#22 synced back; Jeremy GREENLIT Ticket #32; code-graph tool chosen)

Paste §1 into a fresh session. Everything below is context §1 refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home* (keep the two in sync).

**TRIGGER:** start this session **once techlead has installed codebase-memory-mcp** (Dorian's gate).
**LAUNCH:** `claude --model "claude-opus-4-8[1m]"` — quotes mandatory (zsh globs `[1m]`).
**1M context for every model/lane.** Model governance: **fable = brain** (plans + gates), **opus-4.8 = lead + adversarial** (`redteam-48`/`reviewer-48`), **sonnet-5 = implementation**.

---

## 1. The prompt — paste this

> Read `CLAUDE.fork.md` (say so if the fork guardrails are already in context; else read it), `research/LEDGER.md` (newest entry + CARRIED-FORWARD), and this file. Then `git status && git log --oneline -8`.
>
> WHERE WE ARE (2026-08-13): `mac/setup` @ `f20ccd01`, pushed to origin, clean. **BOTH upstream PRs now fully reflected in the fork** — PR #21 (candle-callback) synced back (`0b50adae`/`f30f2458`), and **PR #22 (feed-dependency safety) MERGED upstream `34f90e78`** then synced back byte-identical no-op `2a30516d` (fork keeps 2 docstring lines) + bookkeeping `f20ccd01`; FORK_CHANGES feed-dependency row → **CONVERGED**. Baseline anchor `5ccbec42`/24/−23.021%/−5.646 unchanged; fast **339** / slow **20**. Separately (NOT a trading-repo change): **code-graph tool selection is done** — `codebase-memory-mcp` chosen, `codegraph` fallback; **techlead owns the estate install**. This session starts once techlead has installed it.
>
> FIRST — **check Slack, then EXECUTE Jeremy's GREENLIT #32 PR.** Jeremy reviewed the #32 plan (strategy-research keyless-green + 3 upstream fixes) and gave a **GO on 2026-08-13** (Slack DM `D0BLW7XBHPG`; full verdict on Notion "📬 Next session: act on Jeremy's verdict on Ticket #32"). Confirm no newer Slack message, then build it (`strategy-research/` ONLY, zero blast radius into `trading-bot/`):
> - Branch `fix/sr-tests-keyless-green`. Apply the **3 fixes**: (1) lazy `genai.Client()` accessor (`run_phase1_research.py:856`); (2) R2 traversal test — loosen the Windows-only assert cross-platform + add the hermetic containment companion (mutation-proven); (3) D3 census test (`test_c7ext_verdict_gates.py:753`) — replace `==9` with the independent-oracle agreement check (mutation-proven a/b/c). Jeremy **REVERTED his own earlier R2 patch** (it broke the verbatim-replay guarantee) — no collision.
> - Jeremy's decisions (all resolved): **(a)** drop `==9` for the agreement check → YES; **(b)** bundle the stale `_assert_promotion_ratified` docstring (`run_phase1_research.py:1860-1869`) + the two doc refs (`DISPATCH_MODEL.md:140`, `E-002/EPIC.md:160`) in the SAME PR → YES; **(c)** CI shape = `-m "not slow"` (self-contained, no network) → matches trading-bot's fast/slow split.
> - Reproduce green (from `strategy-research/`, venv at `<repo-root>/.venv`): **486 passed / 7 skipped / 0 failed**; networkless `-m "not slow"`: **482 passed / 7 skipped / 4 deselected**. CWD landmine: must run from `strategy-research/` (else 3 `k3` tests fail). The 7 skips = untracked BTC caches (fixture-not-present), expected.
> - Gate + ship: red-team the branch (`redteam-48`, blind); commit gate `basedpyright --venvpath <repo>` + `ruff` on changed `.py`, DELTA only; then open **ONE issue-first PR** to `loloze6/trading-bot` (PR only, never push upstream). Full detail + carry-forward facts: Notion "📬 Next session: act on Jeremy's verdict on Ticket #32".
>
> THEN the queue: (1) **Feature B** — real kraken funding via ccxt `krakenfutures` (Fork order 33): auto-fetching venue like binance, NOT a manual ingest; 4 gating problems — hourly cadence (pipeline hardcodes 8h in 5 places), symbol map (`BTCUSD` → `PF_XBTUSD`/`BTC/USD:USD`), ~2020+ coverage, and the spot+perp COHERENCE question (single-symbol engine can't express carry — must survive `HYPOTHESIS.md` first). Rides the shipped droppable-feed as its empty-coverage safety net. (2) **First kraken breadth campaign** — 19-pair `*USD`, runnable now with `drop_feeds=['funding_rate','fear_greed']` via `/new-hypothesis`. (3) `_close_all_positions_at_end` duplicate-final-bar-state bug (gates `fix/metrics-bar-equity`). (4) untrack `results/trades.json` (Low). (5) risk layer (23), Venue epic (30). **Optional:** exercise the newly-installed `codebase-memory-mcp` on `trading-bot/` as an **ISOLATED instance** — decoy+canary seal test FIRST (`strings`-scan the DB, exercise the watcher path) before the real repo is ever indexed; then the `register_feed` 5-refs (incl `core/backtester.py:114`) + `run_backtest` blast-radius accuracy checks.
>
> HARD RULES: never run live; holdout sealed (never a window past 2025-12-31; never open `holdout_sealed/`); every market-data experiment → a `research/TRIALS.csv` row; no secrets; origin only, PRs to Jeremy (don't touch PR branches except on his feedback); no `Co-Authored-By`. **ANY ccxt work → load the `ccxt-python` (or `ccxt-cli`) skill FIRST + confirm via `.has`/introspection — never from memory (standing rule).** zsh traps: unquoted `$var` doesn't word-split (use `${=var}`); `git commit -F <file>`; absolute paths; `cd` is zoxide-aliased (`cd <path> 2>/dev/null` or absolute paths); `main.py simulate` overwrites tracked `results/trades.json` (restore before commit). Commit gate: `basedpyright --venvpath <repo>` + `ruff` on changed `.py`, DELTA only. Kraken = strategic-primary (MiCA); technical default STAYS binance; kraken-primary stays OFF Slack.
>
> HOW DORIAN WANTS YOU TO WORK: OMC teams; fable = brain (plans + gates), opus-4.8 = lead + BLIND red-team/review, sonnet-5 = impl; all 1M, transcript-verify every lane; visual todo first; one change per commit, green before the next; verify by execution; keep Notion current; update `research/LEDGER.md` + commit before session end; rewrite `research/NEXT_SESSION.md` + its Notion mirror at session end; Slack wrap at session end.

---

## 2. State (2026-08-13)

| | |
|---|---|
| Branch | `mac/setup` @ `f20ccd01` — pushed to origin, clean tree (only untracked `results/runs/` artifacts) |
| Baseline anchor | `5ccbec42`/`5a75366c`/24/−23.021%/−5.646; fast **339** / slow **20** |
| Upstream | `34f90e78` — **PR #21 AND PR #22 both MERGED upstream**; both synced back into the fork. Nothing pending from Jeremy on the upstream-PR front |
| Jeremy's asks | **Ticket #32 GREENLIT** (2026-08-13, Slack DM `D0BLW7XBHPG`): GO on all 3 fixes, all 3 decision points resolved. Next session executes the PR |
| Code-graph tool | Selection DONE: **codebase-memory-mcp** (pick), **codegraph** (fallback). Techlead owns the estate install; this session is triggered by that install completing. Trading repo, if indexed, = its OWN isolated instance, decoy+canary seal test first |
| Open tickets | #32 (execute — GREENLIT); Feature B kraken funding (33); bar-state dup-row bug; untrack trades.json (Low); risk layer (23); Venue epic (30) |
| Next | (trigger: CBM installed) → check Slack → **execute Jeremy-approved #32 PR** → Feature B / first kraken breadth campaign |

## 3. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol |
| `research/LEDGER.md` | newest entry (2026-08-13 PR #22 sync-back) + CARRIED-FORWARD |
| `FORK_CHANGES.md` | 2026-08-11 feed-dependency section (now CONVERGED — both docstring-diff and upstream merge recorded) |
| Notion: 📬 Next session: act on Jeremy's verdict on Ticket #32 | the greenlit plan + 3 fixes + carry-forward facts + Jeremy's verdict |
| Notion: Ticket #32 Round-2 plan (`3ba1d1fb…9aa4ddc7908dc5cf`) | full evidence / prototype code for the 3 fixes |
| Notion: Mac Fork — Home; Bugs & Tasks | statuses + locked decisions |
