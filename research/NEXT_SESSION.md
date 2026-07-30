# Handoff → next Claude Code session (written 2026-07-28, after queue #1 merged)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a plain-text code block for clean copy-paste. If you change §1 here, change it there — that page is the one Dorian actually copies from.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: `CLAUDE.fork.md`, `research/LEDGER.md`, `research/NEXT_SESSION.md`. **`CLAUDE.fork.md` is NOT auto-loaded** — Jeremy's `CLAUDE.md` has no include for it, so you must read it explicitly. Then run `git status && git log --oneline -5`.
>
> **Where we are:** milestone 1 AND fork queue #1 are done. The bot runs on the Mac and reproduces the baseline byte-identically — `config_sha256 5ccbec42` / `data_sha256 5a75366c` / net −23.021% / sharpe −5.646 / 24 trades — and the **holdout data path is guarded**: fetches can no longer write past a requested end, `visualize_data` no longer names a sealed date, and `tests/test_no_sealed_date_literals.py` fails the suite on any executable production date at or beyond the seal's start. Branch `mac/setup`; check `git log` for the actual HEAD rather than trusting a hash written here. Fast suite **130 passed**, slow **9 passed / 1 skipped / 0 errors**. The baseline is a **reproducibility anchor, never a result** — the committed strategy is from a killed family, loses ~23%, and its Sharpe still comes off the trade-exit equity curve (that's queue #3).
>
> **Three PRs are open on Jeremy's repo — check all three at session start** (`gh pr view 1 --repo loloze6/trading-bot`, same for 2 and 3): PR #1 (first-run blockers + provenance-note fix `3e00f895`), PR #2 (fetch end-bound + UTF-8 seal-guard fix `7f0ad3a5`), PR #3 (regime fall-through, opened 2026-07-30 at Jeremy's request). Jeremy verified #1 and #2 on Windows 2026-07-28 and said **merge both**; his findings were fixed on the branches 2026-07-30. If he commented again, that may preempt the session plan — tell me before proceeding. Never push to his repo; PRs only. **His W8→W15 (7 commits, incl. a breaking `register_feed(window_seconds=...)` change) are still unpushed on his side — sync via `git fetch upstream && git merge upstream/master` once he pushes.**
>
> **The finish line ("good enough to start generating") is four things:** costs modelled, drawdown honest, **holdout guarded ✅**, trials counted. Three remain. Hold me to that line — "fix everything first" never ends.
>
> **Next task — `feat/slippage-model` (queue #2 of 5; board Fork order #4):** flat-bps slippage plus lot-size/min-notional rounding in `MockExecutionHandler` (`execution/execution_handler.py`). Today the backtest fills at the exact close with zero slippage, so every result is optimistic — and a generator optimising against zero-slippage fills systematically proposes high-turnover mirages. Cost error changes **which strategies survive selection**, not just their score, which is why this sits ahead of bar-equity. Requirements: **off-by-default with a bit-identity test** proving default output byte-unchanged (template: `tests/test_warmup_prefetch_bit_identical.py`; hard rule 4); slippage is a separate modelled cost, not folded into the 10 bps fee; then rerun the baseline at 0/5/10 bps — the 0 bps run must stay byte-identical, and the 5/10 bps deltas go in the ledger as the first measure of how much edge is a cost mirage. Propose the design in 3–6 bullets and get my nod before code.
>
> **After that:** 3 `fix/metrics-bar-equity` (drawdown honest), 4 `fix/workflow-macos-port` (cheap, reversible, inert until a campaign runs — pull forward whenever convenient), 5 verify trial accounting (`run_campaign.py:1119-1122` — a **killed** run must still land a row in `campaign_state.trial_sharpes`), then the first campaign. The ticket-level queue is Notion → 🐛 Bugs & Tasks → **🍎 Fork queue (in order)**; `CLAUDE.fork.md` is canonical if they disagree.
>
> **Lessons that must shape this session** (paid for on queue #1 — details in the ledger):
> 1. **A byte-identical baseline proves only the paths the baseline walks.** Queue #1's first cut had a real regression the baseline was blind to. Your bit-identity proof must cover the actual default path, and the reviews must probe the paths `simulate` does *not* walk.
> 2. **"The fix is correct" and "the fix is guarded" are separate claims.** Mutate your own new code (disable the flag, weaken a threshold, invert a condition) at the public entry point and watch a test fail — three such mutations survived the whole suite until a verifier lane caught them.
> 3. **Commit before mutation rounds** — `git checkout --` restores to HEAD and once ate uncommitted work mid-session.
> 4. **The OMC lane pattern worked; reuse it:** executor implements from a surgical spec → code-reviewer + red-team in parallel on the diff → separate verifier on the fixes — every stage independent of the author.
>
> **How I want you to work:**
> - Propose a plan in 3–6 bullets and get my nod **before writing any code**.
> - One change per branch. Reviewed and green before you start the next.
> - Prefer the cheapest control that works. Do not add guards to guards.
> - Verify by execution, never by reading. `main.py simulate` prints **nothing** — read the newest dir under `results/runs/` via `stat -f '%m %N' results/runs/* | sort -rn | head -1`.
> - Mutation-test new tests at the *public* entry point — and mutation-test the fix itself, not just the defect.
> - Never push to Jeremy. `origin` only. No `Co-Authored-By` trailers.
> - Keep Notion updated as findings land; update `research/LEDGER.md` before the session ends.
>
> Start by confirming the environment (git state, fast+slow suites) and telling me what you find.

---

## 2. State as of 2026-07-28 (evening)

| | |
|---|---|
| Branch | `mac/setup` @ `35b48736` (encoding-fix parity), pushed to `origin` |
| Upstream | Jeremy's GitHub still `70dab378` (local +7, W8→W15, unpushed); **PR #1, #2, #3 open** on `loloze6/trading-bot` |
| Fast suite | 130 passed (116 + 14 from queue #1) |
| Slow suite | 9 passed, 1 skipped *(the skip is the known dead `test_config_actually_loaded`)* |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades — byte-identical at `mac/setup` tip |
| Queue #1 | Merged `c641db9a`; PR branch `fix/data-holdout-safety-upstream` = the 7 code commits cherry-picked onto `upstream/master` |

## 3. The task: `feat/slippage-model` — design notes

- **Where fills happen:** `MockExecutionHandler` in `execution/execution_handler.py` fills at the exact bar close, zero slippage. All current results are optimistic by construction.
- **Shape:** flat-bps slippage applied against the trade direction, plus lot-size/min-notional rounding (Binance BTCUSDT filters; hardcode sensible constants — no network in backtests). Off by default; a config knob turns it on.
- **Bit-identity:** with the feature off, `simulate` must be byte-identical to the committed reference (`results/runs/20260728T132811Z_5ccbec42` — `cmp` all five files). With it on at 0 bps, decide and *pre-register* whether rounding alone may change output (it will, if lot-size rounding applies at 0 bps — separate the two knobs if so).
- **Why it ranks above bar-equity:** slippage fixes how you *rank* return; bar-level Sharpe fixes how you *score* risk. The Edge Playbook: halving costs doubles the viable strategy space — the generator's selection is only honest if costs are.
- **Interacts with the cost-stress bar:** strategies must survive 1.5×/2× modeled costs on validation. This model is what makes that bar meaningful.

## 4. Known-broken, deliberately not fixed (tracked in Notion)

- **Seven Binance caches carry sealed rows** — queue #1 blocks *new* leaks; it did not decontaminate. Never run a window past 2025-12-31.
- **Seal-test date regex misses T-form timestamps** (`'2026-…T00:00:00'` passes silently — `\b` can't match digit→`T`). Found by red-team 2026-07-30; fix validated (drop the trailing `\b`, zero new violations on the clean tree). Own small branch, Notion ticket — a good warm-up before or after slippage.
- **Seal scan aborts on the first undecodable file** (loud, fail-closed — but the sentinel never fires). Hardening ticket, unqueued.
- `test_config_actually_loaded` has never executed (dead fixture; the slow suite's `1 skipped`). Own branch, board order #8.
- `tools/ingest_kraken_archive.py` overwrites instead of merging AND calls `_merge_and_store` directly with a data-derived bound (no end-bound at all) — board order #9.
- `holdout_date_gate.sh` exists but is not wired into the installed pre-commit (unqueued ticket).
- `visualize_data` writes its 1m cache into tracked `trading-bot/data/` (wrong dir; gitignore guards the wrong path). Hygiene, deferred.
- `main.py simulate` rewrites tracked `results/trades.json` every run — restore with `git checkout --` after reproducibility checks.
- Whale's `_end_of_day_if_midnight` duplicates the midnight rule at microsecond precision (base uses millisecond) — correct output, wasted shard reads. Cosmetic.

## 5. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, backlog with queue #1 marked done. **Not auto-loaded.** |
| `research/LEDGER.md` | every trap and lesson; the 2026-07-28 queue #1 entry is the important one |
| `FORK_CHANGES.md` | rows 10–16: exactly what queue #1 changed and why |
| `execution/execution_handler.py` | the task's home — read `MockExecutionHandler` end to end first |
| `tests/test_warmup_prefetch_bit_identical.py` | the off-by-default bit-identity test template |

Notion — "Trading Bot HQ": 🐛 Bugs & Tasks → **🍎 Fork queue (in order)**. Tickets 1–3 read `Done + PR open`; Mac Fork — Home's top note is current as of this handoff.
