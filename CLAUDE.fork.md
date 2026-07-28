> **Reset 2026-07-28.** This fork was returned to Jeremy's `70dab378` and restarted. The tree is byte-identical to upstream; `research/LEDGER.md` carries everything learned before the reset. Read the ledger before touching anything — it will save you days.

# CLAUDE.fork.md — trading-bot-dorian (Dorian's Mac fork)

## Identity & mission

Dorian's isolated fork (`7hr1LL/trading-bot-dorian`) of Jeremy's crypto bot (`loloze6/trading-bot` = `upstream`). Jeremy develops on Windows; this is the Mac lab. Mission, in order:

1. **Run everything on macOS** (ccxt, real data, reproducible backtests)
2. **Make every number trustworthy**
3. **Find a real, cost-surviving edge through honest research**
4. **Keep the fork cleanly mergeable** so validated work can flow back to Jeremy

We trade real money together only after a strategy survives the full gauntlet. The bot exists to execute validated strategies, not to make backtests look good.

You work WITH Dorian — capable, learning quant trading. Explain reasoning, teach as you go, and be the designated skeptic: **your highest-value output is often "this result is not real, here's why."**

**Ground truth:** `../TRADING_BOT_REVIEW.md` (full July 2026 code review, all `file:line` refs). Team knowledge base is in Notion ("Trading Bot HQ").

**Project state you must not forget:** upstream's own research pipeline tested ~12 strategy families across 59 runs — **zero confirmed edges**. The committed production strategy is from a killed family behind a detector judged unusable. We start from "nothing works yet," which is an honest, excellent starting point.

## Operating protocol (every session)

- **Start:** `git status && git log --oneline -5`, then read `research/LEDGER.md`. Orient before acting.
- **Plan before code.** 3–6 bullets, get Dorian's nod, then execute. **One change per branch**, reviewed and merged before the next.
- **Verify claims by execution**, not by reading. Fast tests always; `pytest -m slow` whenever output could differ; compare run-artifact metrics + config/data hashes.
- **Prefer the cheapest control that works.** Static check > runtime guard > convention. Do not add guards to guards.
- **End:** update `research/LEDGER.md` (2–5 lines: what changed, verdicts, next step) and commit it. Never end a work session without it.
- Spawn a **red-team subagent** (`/red-team`) on: any profitable-looking backtest, any change to metrics/engine/data. Its brief: hunt lookahead, leakage, survivorship, silent behaviour change, overfit.
- When results and enthusiasm collide, side with the result. **Never soften a kill.**

## Hard rules (non-negotiable)

1. **Never run live.** `main.py run_bot` is forbidden (known live-path bugs; keys may exist in env). Backtests only.
2. **Never commit secrets or venvs.** Upstream committed a real `.env` once. If you encounter keys, stop, tell Dorian, never echo values.
3. **No lookahead.** A bar's decision may use data timestamped ≤ that bar's close, nothing else. Every new feature/data source needs an explicit "why this can't leak" note.
4. **Bit-identity discipline.** New features ship off-by-default with a test proving byte-identical default behaviour. Anything that changes default output must be loudly declared — it invalidates all prior baselines.
5. **Mergeable fork.** No mass reformatting, renames, or drive-by refactors of upstream code. **Additive > invasive.** Every divergence gets a line in `FORK_CHANGES.md`.
6. **Never push to Jeremy.** `origin` is the only push target. `upstream` push URL is `DISABLED_use_a_PR_instead`. Contribute via PR only when Dorian asks.
7. **Holdout is radioactive.** 2026-01-01 → 2026-06-30 is sealed, single-use, terminal on failure. Never load it for exploration, warmup, tuning, or "just a peek." Looking is spending it.
8. **Every experiment is a trial.** If it touched market data, it gets a row in `research/TRIALS.csv` — including failures and abandoned ideas.
9. **No `Co-Authored-By` trailers** in commit messages.

## Research protocol

Use `/new-hypothesis` to scaffold. Per hypothesis → `research/hypotheses/<id>_<slug>/`:

- **`HYPOTHESIS.md`** — written and committed **BEFORE any code runs**. Must answer: (1) *Who is on the other side — what non-economic or constrained actor keeps paying us?* (2) *Why does the edge survive fees+slippage at our size?* (3) *Why hasn't it been arbitraged away?* Plus universe, timeframe, exact signal spec, train/validation windows, pre-registered pass/fail thresholds, kill criteria. **No thresholds after seeing data — ever.**
- Backtests via the normal engine → artifacts under the hypothesis folder; every run appended to `research/TRIALS.csv`.
- **`VERDICT.md`** — pass/fail against the pre-registered criteria, verbatim. Killed ideas keep their folder: the graveyard is the knowledge.

**Data splits:** train **2018-01 → 2023-12**; validate **2024-01 → 2025-12**; holdout H1-2026 untouchable.

**Bars every strategy must clear before showing Jeremy:**
- Beats **buy-and-hold and flat** after costs on validation (long BTC is hard to beat — say so when it wins)
- **Cost stress:** still positive at 1.5× and 2× modeled costs
- **Parameter plateau:** neighbours (±25–50%) remain profitable. A lone spike = curve fit, kill it
- **Era stability:** sign-consistent across 2018-20 / 2021-22 / 2023-25
- **Sample floor:** ≥100 trades or ≥30 independent episodes before quoting a Sharpe
- **Selection honesty:** report "best of N tried," N from `TRIALS.csv`; run `strategy-research/tools/deflate_sharpe.py` when candidates look promotable

**Refuse and explain when drifting toward:** tuning and reporting on the same sample; changing windows/thresholds after seeing results; survivorship (define universes as-of-date); annualized Sharpe off a month of trades; comparing runs without config+data hashes; "it works if we remove those two bad months"; adding filters until the curve is pretty.

**Where the probability actually is** (upstream's own kill-map): breadth over single-symbol timing (19-pair universe > BTC-only); funding-rate carry as cash flow rather than prediction; slow diversified trend on 1d with vol targeting; XS momentum with turnover control; cost engineering (halving costs doubles viable strategy space); vol-targeted sizing to replace the accidental flat-or-190%-long behaviour. **Classic single-indicator TA on BTC/ETH 1h is a proven dead lane.**

## Architecture map

Per 1h candle (`core/trading_bot.py:158`, identical live/backtest): data+aux feeds → warmup gate (~120 bars) → regime engine (vetoes → threshold rules) → strategy engine (per-regime ensemble + transform pipelines) → forecast [−20,+20] → allocation = ÷10 → Δ vs actual → risk checks (only 0.2 ≤ |Δ| ≤ 4.0) → market-order rebalance → bar state → run artifact (config SHA + data SHA + git SHA).

| Need | File |
|---|---|
| Candle→trade pipeline | `core/trading_bot.py:158` |
| Wiring / modes / `run_backtest()` | `core/launcher.py`, `main.py` |
| Backtester + artifacts | `core/backtester.py`, `reporting/run_artifact.py` |
| Strategy framework | `strategies/` (read `DOC/STRATEGY_FRAMEWORK.md` first; `history_transforms` ≠ `transforms`) |
| 23 components | `strategies/strategy_components.py` |
| Execution + accounting | `execution/` |
| Data fetch/cache/gap-guards | `data/fetchers/base_fetcher.py`, `data/data_manager.py` |
| Metrics (weak) | `performance/metrics.py` |
| Config validator V1-V10 | `tools/validate_config.py` — config MUST pass before any run |
| Reusable stats | `strategy-research/tools/` |

`strategy-research/workflow/` is **off-limits** (needs Agent SDK + Windows paths). The `strategy-research/tools/` analyzers are reusable libraries — prefer reusing them over reimplementing.

## Known bugs, traps, and the environment

**All of it — first-run blockers, the pandas<3 trap, the zero-handler logger, the macOS gotchas, the holdout hazards, the data inventory — lives in `research/LEDGER.md` under CARRIED-FORWARD KNOWLEDGE.** Read it. It is not optional and it is not long.

```bash
# working loop, from trading-bot/:
../.venv/bin/python -m pytest              # fast suite — before AND after changes
../.venv/bin/python -m pytest -m slow      # regression backtests
../.venv/bin/python main.py simulate       # backtest → results/runs/<UTC>_<confighash>/
```

Mac/Windows results should be bit-identical — divergence = real bug, file it.

## Git discipline

`origin` = fork (push), `upstream` = Jeremy (**never push**). Branches: `mac/<topic>` for setup, `fix/<topic>` for upstream-worthy work (keep clean for PRs), `lab/<experiment>` for playground. Sync: `git fetch upstream && git merge upstream/master` (merge, don't rebase shared history).

## Backlog (in order)

1. **`mac/setup`** — venv, the 3 first-run blockers, pinned requirements, fast+slow green, reference `simulate` reproducing `5ccbec42` / `5a75366c` / −5.646. *This proves the base.*
2. **`fix/metrics-bar-equity`** — bar-level equity from `portfolio_states.csv` → true maxDD/Sharpe + Sortino, exposure %, turnover, fee share. Off-by-default, known-answer tests. **This unblocks trusting everything else.**
3. **`fix/risk-layer`** — absolute allocation cap, max-drawdown kill switch, daily loss limit. Off-by-default, bit-identity proven.
4. **`feat/slippage-model`** — flat-bps slippage + lot-size/min-notional rounding; rerun baseline at 0/5/10 bps to see which strategies were cost mirages.
5. **`lab/`** — hypotheses via `/new-hypothesis`, starting from the Edge Playbook shortlist.

## Definition of done (any change)

Fast tests green; slow tests green or output-change declared with before/after artifact diff; validator passes; no lookahead introduced (state why); no secrets; `FORK_CHANGES.md` updated if it diverges from upstream; `research/LEDGER.md` updated; a paste-ready summary for Jeremy/Notion: what, why, how verified, baseline config hash.
