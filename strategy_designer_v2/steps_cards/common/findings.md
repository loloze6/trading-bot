**Draft for the operator's review (improvement I2, `topics/30_review/WORKFLOW_REVIEW.md`). No step reads it yet.**

Findings: what the runs have measured about the market and about what pays, in short statements, each with its evidence.
They are what a researcher would know before writing the next brief or idea. A finding is not a rule: it refuses
nothing, it is open to new evidence, and a later run can change or withdraw it. Proposed readers: step 1 (briefs), step
2 (ideas), step 7 (the next ideas). An entry is added by a run's reading, on the operator's go, with its date and source.

| # | Finding | Evidence | Date |
|---|---|---|---|
| F1 | **A round trip costs about 21 to 23 bps** of the value traded on the venue as backtested (fees, spread, slippage), measured from the books' own records | hourly books of `std_time_pilot_run`, `hold2_rerun`, `more_coins_1h_run` (cost per unit traded 10.5 to 11.6 bps) | 2026-11-20 |
| F2 | **On hourly bars, an idea of 1 to 4 hours captures 4 to 13 bps per bet** once a trader can act (the close of the signal's bar), net of the coin's drift: below a round trip, whatever the holding | the book's diagnosis of settlement-move, late-evening rebound, post-settlement decline (`runs/HOLD2_AND_PILOT_RUN.md`, step back) | 2026-11-20 |
| F3 | **A daily idea held for its horizon pays about as well on hourly bars as on daily bars** (3 of 3: nearness to highs, golden-cross momentum, dual momentum); the hourly version adds no edge of its own | `runs/HOLD2_AND_PILOT_RUN.md`, step back, point 1 | 2026-11-20 |
| F4 | **A book that re-sizes every bar instead of holding each bet for its horizon pays its costs without earning the move**: hourly books without a holding period earned 0.3 to 4.6 bps per unit traded against about 10 of cost | `topics/30_why-hourly-ideas-rarely-pay.md`, reading A | 2026-11-19 |
| F5 | **On continuation ideas, much of the move happens on the signal's own bar**: 70 to 120 bps on hourly books (grinding-rises, dual momentum, golden-cross, nearness), which a trader acting at its close does not capture | the book's diagnosis, opening time | 2026-11-20 |
| F6 | **Confirmation is cheap on short horizons**: on hourly bars a 0.10 % move over 2 hours reaches t 9; a confirmed hourly idea is not a paying one (22 confirmed, 0 profitable) | topic 30, reading C | 2026-11-19 |
| F7 | **More coins do not shrink a fall the coins share**: volatile evening-fall's deepest fall is 35 % on 6 coins and on 19, over the same stretch, though all 19 coins earn | `runs/MORE_COINS_1H_RUN.md` | 2026-11-20 |
| F8 | **In a strong bull period a long book rarely beats holding the coin**: on the 2016-17 unseen dates holding's Sharpe is 3.2 to 4.1; 3 of 11 book records beat it (2 of them golden-cross more coins, one rule each), with Sharpes of 2.7 to 3.7 | unseen-dates tests of `hold_paying_run`, `hold2_rerun` | 2026-11-20 |
| F9 | **Several paying books' moves outlast their stated horizon**: still rising at twice it (golden-cross, nearness, dual momentum) | the book's diagnosis, closing time | 2026-11-20 |
| F10 | **Real ideas have about the same strength whatever their horizon: about 5 % of the coin's typical move over that horizon** (median 0.047 to 0.056 from 1 hour to 10 days, 120 confirmed ideas). The typical move grows with the horizon, the cost of a trade does not: on 1 to 4 hours an idea would need about 3 times the usual strength to cover a buy and a sell; over 2 to 10 days, less than half of it | `runs/RETRO_DIAGNOSIS_RUN.md`, fourth question | 2026-11-20 |
