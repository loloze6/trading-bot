# Generation 2: selection

**Pool.** 35 ideas from 11 analyses (one call) on generation 1's four backtests (lines 7.b, 7.d, 7.g; 7.b skipped N1-04, confirmed).

| Chosen | Idea | Why |
|---|---|---|
| N2-01 | the bar after Friday rises more than an average day | the night's most recurrent effect (6 times in generation 1, 4 more here), t 4.3 on 2,430 cases, every coin |
| N2-02 | capitulation: far below the long average after a sharp fall, high volatility, then a rebound | 4 times, three lines |
| N2-03 | a deep 20-day loss, then a rebound over 20 days | twice (a U-shape) |
| N2-04 | 60-day and 20-day returns both positive, then a rise | twice |
| N2-05 | after a very large up day, a rise over 5 days | new, distinct |
| N2-06 | N1-04's rebound, in high volatility only | 3 times |

Run with the overnight test catalogue and record description. N2-01 was refused once (rightly: `WeekdayReturnComponent` alone tests another claim) and rewritten with `WeekdayComponent` (`03_test_plan/overnight_run/plans_rerun/`).
