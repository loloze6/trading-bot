# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 031-01_wide-flat-day-ends-uprun | - | plan | inconclusive (-0.93) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 031-01.b1_wide-day-extends-up-run, 031-01.b2_wide-doji-continues-strong-run; 7.g: 031-01.g1_wide-day-low-close-rebounds | 1.88 | 5.3 |
| 031-02_wide-flat-day-ends-downrun | - | plan | inconclusive (-0.52) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 031-02.b1_wide-flat-day-continues-uprun; 7.g: 031-02.g1_extreme-down-day-next-day-bounce | 1.20 | 5.4 |
| 031-03_uprun-size-scales-wide-flat-reversal | - | plan | inconclusive (-1.00) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 031-03.b1_wide-day-extends-up-run; 7.g: no ideas: Across the flat-day, wide-day, run-size, volatility, close-location, move-size, yearly and weekday angles (about 40 groups), no pattern stands out beyond |t| ≈ 2, which is what chance gives over that many looks. The loose hints of 5-day continuation (F2, F3, F4) are not strong or stable enough across years to support a new idea. | 1.04 | 4.9 |
| 031-04_downrun-size-scales-wide-flat-reversal | - | plan | inconclusive (-0.55) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: no ideas: The tested long-after-falls effect is zero or reversed at every horizon (F1, F2), on every coin and in every year (F3), and the wide range adds nothing to narrow flat days (F4), so no amended version of the tested idea has support. The only clear effect is continuation after rises (F6). Its grading by the size of the rise holds only on the looser definition (F7), so it is too uneven to state as a graded idea yet.; 7.g: 031-04.g1_close-at-low-fall-rebounds, 031-04.g2_sharp-daily-fall-reverses | 1.06 | 5.3 |
| 031-01.b1_wide-day-extends-up-run | 031-01_wide-flat-day-ends-uprun | plan | inconclusive (+1.43) | profitable enough | - | 7.b: 031-01.b1.b1_wide-day-extends-run-more-coins, 031-01.b1.b2_wide-day-extends-strong-run; 7.e: 031-01.b1.e1_strong-run-continues-three-days, 031-01.b1.e2_wide-day-in-strong-run; 7.g: no ideas: Of the angles examined (past 1-, 5- and 20-day returns, range ratio, close location, body, volatility, run direction with wide/flat days, weekday, year, positions, trades by forecast, and the book against holding), no pattern stands out beyond what about 75 cells would give by chance (largest |t| 2.76, none graded). The book's profit is explained by the market's rise (F1–F3), not by a separate effect that a new idea could take up. | 1.34 | 5.6 |
| 031-01.b1.e1_strong-run-continues-three-days | 031-01.b1_wide-day-extends-up-run | plan | confirmed (+4.38) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 031-01.b1.e1.g1_wide-down-day-rebounds, 031-01.b1.e1.g2_rejected-low-rebounds-higher | 0.75 | 4.6 |
| 031-01.b1.e2_wide-day-in-strong-run | 031-01.b1_wide-day-extends-up-run | plan | confirmed (+2.85) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: no ideas: About 40 cells were examined (range fifths by run direction, body and close location on wide days, size of the day's move, volatility-scaled run strength, volatility level, weekday, forecast fifths, coin). None of them shows a graded pattern outside the tested idea that survives this many looks and the correlation between coins. The strongest, the run-strength top-fifth step (F1), is a step rather than a slope and is already contained in the tested idea's rise-strength component. The weekday effect (F5) is unclustered and an on/off condition, not a graded situation. | 0.64 | 4.9 |
| 031-02.b1_wide-flat-day-continues-uprun | 031-02_wide-flat-day-ends-downrun | plan | inconclusive (+0.92) | not profitable enough (failed: Calmar, Trades per day) | - | 7.b: 031-02.b1.b1_wide-flat-uprun-more-coins, 031-02.b1.b2_flat-day-after-strong-rise; 7.g: 031-02.b1.g1_strong-up-day-carries-forward, 031-02.b1.g2_wide-strong-day-continues-run, 031-02.b1.g3_deep-down-day-partial-rebound | 1.23 | 5.6 |
| 031-03.b1_wide-day-extends-up-run | 031-03_uprun-size-scales-wide-flat-reversal | plan | confirmed (+2.54) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 031-03.b1.g1_wide-down-day-rebounds, 031-03.b1.g2_wide-day-capitulation-reverses | 0.61 | 4.4 |
| 031-01.b2_wide-doji-continues-strong-run | 031-01_wide-flat-day-ends-uprun | plan | mismatch | not profitable enough (failed: Calmar, Trades per day) | - | 7.g: 031-01.b2.g1_wide-down-day-rejected-rebound | 0.66 | 3.8 |

## Consumption
10 ideas, 10.41 USD, 49.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.67 | 5.9 |
| step4_backtest | 0.00 | 14.7 |
| step5_verdict | 1.74 | 6.2 |
| step6_check | 0.00 | 0.3 |
| chart_files | 0.00 | 0.1 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.e | 0.41 | 1.1 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 2.25 | 6.5 |
| step7_7.g | 4.34 | 12.3 |
| similarity_check | 0.00 | 0.1 |
| unseen_test | 0.00 | 2.5 |
