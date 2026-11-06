# strategy_designer_v2

A research workflow that finds a profitable trading strategy by itself, runs on its own, and does not fool itself. The operator decides; the pipeline discovers. It uses `trading-bot/` as its backtester and never trades live.

## The rule of v2
v2 starts empty. A v1 piece enters only by hand, one at a time, with a one-line reason, when a v2 run asks for it. Nothing is copied by default. Every addition to this folder names the run that asked for it and the reason, in `CHANGES.md`.

## The two rules that come before everything else (operator, 2026-11-06)
- **The engine is the only reader of bars.** Branch 1 (was the idea right?) and branch 3 (is the book profitable?) are computed from the engine's own outputs. No step reads the price cache on its own. No quick check beside the engine, ever; if the engine is too slow, make the engine faster.
- **Forecasts are linear.** A claim carries a continuous strength, never a direction switch. The component emits that strength; the engine's standardise transform grades it. No on-off book.
These rules were not on this page before 2026-11-06, and the first version of v2 drifted from both. Everything built against them was deleted that morning (see `CHANGES.md`); their results are history, not evidence.

## The scars (rules learned in v1, kept as rules, not as code)
1. No lookahead: a bar's decision uses only data at or before that bar's close. Every claim says in one line why it cannot leak.
2. The holdout is sealed. Its dates are read only from `strategy-research/config/campaign_data_policy.yaml`, never written out. Its store is `local_data/holdout_sealed/`, never opened by research.
3. An idea is judged on months it has never seen: one fold, one verdict, fixed before the backtest.
4. One process at a time on the data and the records; every state write is atomic.
5. Every experiment that touches market data is a trial and gets a row in the trial ledger.
6. A budget per lineage and per day; the analyst is capped.
7. No secrets in the repo.

## The path, one idea at a time
1. **Brief** (operator): research goal, venue, product, strategy domain. The rest optional.
2. **Ideas** (AI): many distinct claims, each with its own pass condition. `steps/ideas/`.
3. **Config** (AI, then code checks): one strategy config per claim.
4. **Backtest** (engine): one fold.
5. **Three answers** (code, AI, code): the claim passed or failed; what the analyst saw and proposes; profitable enough or not.
6. **Record**: ideas, claims, configs, runs, results and the why, separate and referenced.
7. **Next idea**: picked from the record. The operator approves only new briefs and the holdout.

## Status (2026-11-06 morning, after the clean-up)
What remains and stands: the brief format and the briefs; the ideas step (`steps/ideas/`), to be changed so a claim carries a continuous strength; the analyst step (`steps/analyst/`); the engine step (`steps/engine/backtest.py`), which runs the bot's backtester over a fold at two sizes; the runner (`run.py`), which does not run until branch 1 is rebuilt; the records (`records/`), the query and the morning-file generator; `STEPBACK.md` and `CHANGES.md`; the tries and the runs as history.
What was deleted: the judge that read the price cache, the quick profit check and its sweep, the cache-based replication, the on-off engine component.
Built since, in order (2026-11-06): the linear claim format and component (try 09), branch 1 from the engine's per-window outputs (try 10), the analyst on the engine's outputs (try 11), the runner rewired (try 12). The loop runs engine-only. First real run under the rules: the operator's daily breadth brief on fold A, `runs/real_01_daily_breadth_fold_a/003`, ten claims, nothing validated, nothing profitable. Not built: the holdout path, a fold draw for child claims, a use for validated filters, replication as the engine on other coins, tests, a faster engine. The night's results before the clean-up are void.