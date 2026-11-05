# strategy_designer_v2

A research workflow that finds a profitable trading strategy by itself, runs on its own, and does not fool itself. The operator decides; the pipeline discovers. It uses `trading-bot/` as its backtester and never trades live.

## The rule of v2
v2 starts empty. A v1 piece enters only by hand, one at a time, with a one-line reason, when a v2 run asks for it. Nothing is copied by default. Every addition to this folder names the run that asked for it and the reason, in `CHANGES.md`.

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

## How to run
`python3 run.py briefs/<brief>.md --fold A --rounds 2`. One brief, one fold, a round budget. Outputs under `runs/<brief>/<n>/`; records under `records/`. A run resumes from the last file written.

## Status
Tries 01 to 06 under `tries/`: the ideas step, the claim judge, brief to verdict, the profit answer, the analyst and the next idea, the runner. The pipeline runs on its own on three fake briefs. First candidate book on the shelf (`records/shelf.yaml`), one fold, awaiting the operator. Step-backs in `STEPBACK.md`; every addition in `CHANGES.md`.
