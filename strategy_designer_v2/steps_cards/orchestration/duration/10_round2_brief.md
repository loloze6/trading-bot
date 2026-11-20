# Engine speed, round 2: the brief for the session that does it (2026-11-20)

Written by the step and function designer session for the session that takes topic 33 (`topics/33_engine-speed-second-round.md`).
Read `CLAUDE.md` at the root first: its rules (business first; one rule, not patches; proof by rerunning fixed inputs;
shared code needs the operator's go; no merge into a working branch while a run goes on) apply in full.

## The goal (operator, 2026-11-20)
"It is really slowing us down to have one backtest per hour while we are continuously enhancing." Make an hourly
backtest faster **without changing any result**. Every idea, rule or setting tested since then must give the same files.

## Where the time goes today (measured)
- An hourly backtest is 6 coins x 24 windows (4 folds x 6) x about 2,900 hourly bars, about 420,000 bars, on 4 cores.
- 2026-11-19 (`runs/D_LINE_1H_RUN.md`): step 4 took 606 to 688 s per idea, about 80 % of an idea's time. Steps 3, 5 and
  6 together take about 1 min.
- 2026-11-20 (`runs/HOLDING_NIGHT_RUN.md`, `runs/HOLD2_AND_PILOT_RUN.md`): 15 to 65 minutes per hourly book with the
  holding period. A book that trades often is slowest: two-sided hourly books took 35 to 45 minutes. Volatile
  evening-fall in the pilot ran over 53 minutes (a component computed on few bars, with a regime detector).
- Round 1 (topic 21, `orchestration/duration/1_..9_`) made coins run in parallel (one process per coin, as many at
  once as cores) and sped up the data reading. Its method is the one to follow: measure, findings, plan, go, build,
  proof (`6_change1_proof.md`, `7_change2_proof.md`).

## How a backtest runs (the path to profile)
- Step 4's helper: `steps_cards/04_backtest/helper/run_backtest.py PLAN.md --python VENV --out-root DIR [--force]`. It
  calls `trading-bot/backtest/run_protocol.py` once per coin, on all that coin's windows. Each window warms up first,
  loading 2 x the strategy's required bars before it (`core/launcher.py`, `warmup_prefetch`).
- The bar loop: `trading-bot/core/trading_bot.py` (one call per bar per coin). Per bar it does:
  - the strategy update and its components (`strategies/`, `strategies/strategy_components.py`);
  - the forecast and sizing (`execution/forecast_manager.py`);
  - the holding period, a new module of 2026-11-20 (`core/holding_period.py`);
  - the risk layer (`risk/risk_manager.py`);
  - the execution, then the bar's record (`bars.csv`, with many debug columns).
- Data: local files only (`trading-bot/local_data/`, `coverage.yaml`); the holdout guard (`backtest/holdout_policy.py`).
  Never open `local_data/holdout_sealed/`, never write holdout dates.
- A good fixed input for measuring: `03_test_plan/hold_ideas_1h_run/plans/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h.md`
  (one component, always on), and one regime-gated plan, e.g. the volatile evening-fall d2 in the same folder. Profile
  one coin on one fold first (6 windows).

## What must not change: the research process
Every change is proven by identical result files on fixed inputs: `bars.csv`, `trades.json`, `metrics.json`,
`forecast_distribution.csv` per coin and window. The allowed differences are named in advance: run id, creation time,
commit id, temporary paths, the plan's path, log timestamps. A proof of this kind was done on 2026-11-20 for the holding
module (195 identical files, 53 differing only by those names).

**Options that would change the research itself are not speed changes.** They are proposed to the operator with their
impact on the research, never done as part of this work:
| Option | Why it is not a speed change | What it would touch |
|---|---|---|
| Fewer coins, folds or windows on hourly bars | step 5's verdict and step 6's checks are read over all of them; fewer cases change verdicts | topic 31 (choosing and judging an idea on different data), `common/data_available.md`, the folds (`trading-bot/config/folds.yaml`, `backtest/research_folds.py`) |
| Shorter windows, or joining windows | the folds' windows are the unit of every measure; returns are never computed across two windows (`common/measures.md`) | every step's measures |
| A shorter warm-up | the strategy must be ready on every recorded bar (`common/backtest_record.md`: no warm-up bar is recorded) | the forecasts of the first bars |
| Sampling bars, or skipping bars where nothing can happen | changes the record steps 5 and 7 read | `common/backtest_record.md` |
| Fewer recorded columns | steps 5 and 7 and the book diagnosis read them (`debug_info.components.*`, `sizing_target_allocation`, ...) | `common/backtest_record.md`, `common/book_diagnosis.md`, `topics/30_review`, `topics/36_review` |
| A different cost or fill model | step 6's results | `trading-bot/config/cost_model.yaml` |
| More cores, or a bigger machine | changes no result: the environment's choice | the operator's settings |

When a candidate change is in doubt, ask: "would any recorded file differ?" If yes, it is a research change: propose it.

## What is going on elsewhere (do not disturb)
- The step and function designer session runs backtests on the branch `ccr-6624e33e-aakrpv` (a queue: the
  `standardise` pilot, then reruns with the corrected holding rule; `runs/HOLD2_AND_PILOT_RUN.md`). Work on your own
  branch. Do not push to that branch. Nothing is merged into it while its queue runs, and nothing into master without
  the operator's go.
- The engine changed on 2026-11-20 (the holding period in `core/holding_period.py`; the merge `f1f66512`). Start from
  that branch's latest commit.

## The deliverable, in this order
1. **The measurement:** where an hourly backtest's time goes (per bar: the strategy, the components, sizing, the risk
   layer, execution, recording, and the per-window warm-up), on the fixed inputs above. With numbers.
2. **The findings**, and **the plan**: each change with its gain (measured or estimated), its effort and its risk, and
   whether it is a speed change (identical files) or a research change (to propose). Recommend one order.
3. Then **the operator's go**, then each change built on its own, with its proof of identical files.

Report plainly: a table or a few lines, counts not impressions; times for the operator in Paris time. Send a short
message to the designer session (`session_012maTgTczVA7J9MJ7Bk6egM`) when the measurement and the plan are ready.

## Cloud constraints (learned)
A background task stops after 2 hours and a container restart stops it too: make long scripts resume (skip what exists).
The venv is not in git: build it from `trading-bot/requirements.txt`. Chromium is not needed.
