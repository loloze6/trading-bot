# Try 12: the runner, rewired to the engine-only loop (2026-11-06)

**What ran.** `python3 run.py briefs/fake_01_btc_overreaction.md --fold A --rounds 1 --max-claims 3`. One brief, one fold, the first three ideas, one analyst round. Two model calls, 0.44 USD, 21 minutes wall, eight engine runs (four claims at two sizes). Every number below came from the engine's own outputs: branch 1 from the per-window bars, branch 3 from the per-window metrics, the analyst's observations from the book summaries. No step read the price cache.

| claim | branch 1 (rank correlation on event bars, t) | branch 3 (net, median window Sharpe) |
|---|---|---|
| signed flow pressure continues | fail, -0.042, t -5.6 | fail, -97.7%, -2.5 |
| wick pressure persistence | fail, -0.047, t -6.2 | fail, -99.8%, -4.9 |
| thin volume drift reverts | pass, +0.035, t 4.7, 6 of 6 windows | fail, -99.8%, -6.5 |
| analyst's next: slower anchor-based reversion | fail, t 1.9 | fail, -1.3 |

**What it shows.** The three branches now answer three different questions from one engine run. One idea held on its event bars and its book lost everything as traded on every bar; the analyst read the book summary, said why in twelve observations (holds of about four bars, allocation churn of 0.6 per bar), and proposed a slower claim whose horizon matches its holding time. That claim failed too. The shelf has one validated claim, nothing profitable.

**What the dense-strength rule costs.** A graded forecast on every bar trades every bar. Fees ate every book in this try. The claim's strength must be smooth enough to hold, which is now the ideas step's problem to solve, as the analyst's next claim already tried.

**Defects.** None in the run. Two things to know: the summary step reads the horizon from `claims.yaml` only, so an analyst-written claim's event-bar forward return uses 12 bars; and `--rounds 1` still means one analyst round plus its claim through the engine.
