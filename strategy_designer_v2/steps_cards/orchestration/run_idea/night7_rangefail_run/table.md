# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_choppy-upside-break-fades | - | plan | inconclusive (-0.70) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: no ideas: In choppy markets, closes beyond the 20-day range do not fade in these data. They continue at every horizon from 3 days on, with no grading by overshoot and no difference from trending markets, and the few fading groups are scattered and small (F2–F5), so the theme's effect is not in the data.; 7.g: 032-01.g2_choppy-upside-breaks-continue | 0.86 | 4.7 |
| 033-01_range-position-drift-follows | - | plan | inconclusive (+3.17) | not profitable enough (failed: Calmar) | - | 7.b: 033-01.b1_range-position-more-coins, 033-01.b2_beyond-range-close-drift; 7.g: 033-01.g1_calm-range-position-drift | 1.02 | 5.2 |
| 032-02_choppy-downside-break-rebounds | - | plan | inconclusive (-1.27) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.b: 032-02.b1_choppy-downside-break-one-day-rebound; 7.g: 032-02.g1_flat-base-upside-breaks-continue, 032-02.g2_tight-range-breakouts-run-further | 1.24 | 5.4 |
| 033-02_upside-break-continues-rising | - | plan | confirmed (+2.05) | not profitable enough (failed: Calmar) | - | 7.d: 033-02.d1_upside-break-five-day-hold, 033-02.d2_fresh-upside-break-rises; 7.g: 033-02.g1_upside-break-ten-day-rise, 033-02.g2_calm-market-range-drift, 033-02.g3_agitated-downside-break-continues | 1.32 | 6.3 |
| 033-03_downside-break-continues-falling | - | plan | inconclusive (+0.67) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 033-03.b1_upper-range-drifts-higher, 033-03.b2_rising-market-range-top-continuation; 7.g: 033-03.g1_calm-range-position-drift, 033-03.g2_calm-upside-break-continues | 1.06 | 5.2 |
| 032-02.b1_choppy-downside-break-one-day-rebound | 032-02_choppy-downside-break-rebounds | plan | inconclusive (+1.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar, Trades per day) | - | 7.b: 032-02.b1.b1_choppy-downside-break-rebound; 7.g: 032-02.b1.g1_downside-range-break-rebounds, 032-02.b1.g2_agitated-downside-break-rebound | 0.87 | 4.6 |
| 033-01.b1_range-position-more-coins | 033-01_range-position-drift-follows | plan | inconclusive (+1.39) | not profitable enough (failed: Calmar) | - | 7.b: 033-01.b1.b1_range-position-calm-market, 033-01.b1.b2_range-position-three-days; 7.g: 033-01.b1.g1_upper-range-strength-keeps-rising, 033-01.b1.g2_range-position-in-rising-markets | 1.14 | 9.7 |
| 033-03.b1_upper-range-drifts-higher | 033-03_downside-break-continues-falling | plan | inconclusive (+1.53) | not profitable enough (failed: Calmar) | - | 7.b: 033-03.b1.b1_range-position-more-coins; 7.g: 033-03.b1.g1_calm-range-position-drift, 033-03.b1.g2_rising-market-range-drift | 1.10 | 5.3 |
| 033-03.b2_rising-market-range-top-continuation | 033-03_downside-break-continues-falling | plan | confirmed (+3.08) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 033-03.b2.g1_calm-market-range-position-drift, 033-03.b2.g2_rising-range-top-long-drift | 0.64 | 5.0 |
| 033-01.b2_beyond-range-close-drift | 033-01_range-position-drift-follows | missing-components | - | - | - | - | 1.07 | 2.2 |
| 033-02.d1_upside-break-five-day-hold | 033-02_upside-break-continues-rising | plan | confirmed (+2.05) | not profitable enough (failed: Calmar) | - | 7.d: 033-02.d1.d1_rising-market-upside-break-hold, 033-02.d1.d2_narrow-range-upside-break-hold, 033-02.d1.d3_agitated-upside-break-hold; 7.g: 033-02.d1.g1_calm-range-position-drift, 033-02.d1.g2_calm-market-upside-break | 1.15 | 6.1 |
| 033-02.d2_fresh-upside-break-rises | 033-02_upside-break-continues-rising | missing-components | - | - | - | - | 0.07 | 0.4 |
| 032-02.b1.b1_choppy-downside-break-rebound | 032-02.b1_choppy-downside-break-one-day-rebound | plan | inconclusive (+1.90) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 032-02.b1.b1.b1_agitated-choppy-break-rebound, 032-02.b1.b1.b2_sharp-fall-break-one-day-rebound; 7.g: 032-02.b1.b1.g1_rising-market-breakout-continuation | 1.08 | 9.0 |
| 034-01_rising-nearness-to-high-rises | - | plan | inconclusive (+1.64) | profitable enough | - | 7.b: 034-01.b1_nearness-to-high-10-days, 034-01.b2_close-above-high-drifts; 7.e: 034-01.e1_rising-market-breakout-distance-continuation; 7.g: 034-01.g1_rising-nearness-ten-day-drift | 1.75 | 10.4 |
| 035-01_nearness-to-high-rises | - | plan | inconclusive (+1.58) | not profitable enough (failed: Mean daily return, on days in a position) | - | 7.b: 035-01.b1_calm-market-nearness-to-high; 7.g: 035-01.g1_near-high-side-carries-drift, 035-01.g2_choppy-market-nearness-to-high | 1.09 | 9.6 |
| 034-02_rising-break-swings-continues | - | plan | confirmed (+3.69) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 034-02.g1_choppy-deep-below-high-keeps-falling, 034-02.g2_nearness-to-high-every-market, 034-02.g3_rising-approach-to-high | 0.72 | 10.8 |
| 035-02_break-swings-above-continues | - | plan | confirmed (+2.07) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: no ideas: I looked at about 60 groupings: distance from the high and from the low, the last day's move, the volatility ratio, trend crossed with breakout, year, weekday, prior 5-day return, and trade duration, entry forecast and coin. No pattern outside the tested breakout effect reaches a day-clustered |t| of 2 in a graded way, so none stands out from chance across that many looks. | 0.66 | 10.8 |
| 034-03_rising-far-below-high-falls | - | plan | inconclusive (+0.64) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 034-03.b1_choppy-far-below-high-falls; 7.g: 034-03.g1_rising-above-high-breakout-drift | 1.06 | 10.1 |
| 035-03_far-below-high-falls | - | plan | inconclusive (+1.99) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 035-03.b1_choppy-far-below-high-falls, 035-03.b2_choppy-far-below-high-ten-day-falls; 7.g: 035-03.g1_deep-drawdown-bounce-fades, 035-03.g2_far-below-high-falls-when-falling | 1.75 | 10.1 |
| 034-01.e1_rising-market-breakout-distance-continuation | 034-01_rising-nearness-to-high-rises | plan | confirmed (+2.70) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 034-01.e1.g1_rising-breakout-ten-day-drift, 034-01.e1.g2_choppy-far-below-high-decline, 034-01.e1.g3_falling-far-below-high-decline | 1.49 | 11.7 |
| 034-01.b1_nearness-to-high-10-days | 034-01_rising-nearness-to-high-rises | plan | confirmed (+3.19) | profitable enough | unseen_2016_2017: holds; unseen_2026: holds | 7.g: 034-01.b1.g1_calm-rising-nearness-drift, 034-01.b1.g2_calm-market-nearness-short-drift | 0.75 | 11.9 |
| 034-03.b1_choppy-far-below-high-falls | 034-03_rising-far-below-high-falls | plan | inconclusive (+0.11) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 034-03.b1.b1_choppy-slip-falling-coin; 7.g: 034-03.b1.g1_rising-nearness-to-high-drift | 1.13 | 10.2 |
| 036-01_swing-scaled-fall-next-day-rebound | - | plan | confirmed (+2.15) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.d: 036-01.d1_beyond-one-swing-fall-rebound, 036-01.d2_widening-swings-fall-rebound; 7.g: 036-01.g1_agitated-sharp-fall-rebound | 1.14 | 10.6 |
| 037-01_choppy-swing-scaled-fall-continues | - | plan | inconclusive (+0.94) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 037-01.b1_choppy-extended-fall-continues; 7.g: 037-01.g2_choppy-month-fall-continues-longer | 1.07 | 9.9 |
| 038-01_calm-swing-scaled-rise-continues | - | plan | inconclusive (+1.12) | not profitable enough (failed: Calmar) | - | 7.b: 038-01.b1_calm-swing-scaled-move-continues, 038-01.b2_calm-scaled-rise-ten-days; 7.g: 038-01.g1_calm-two-sided-swing-continuation, 038-01.g2_calm-swing-scaled-fall-continues, 038-01.g3_calm-ten-day-swing-continuation, 038-01.g4_choppy-calm-break-continuation | 1.01 | 10.8 |

## Consumption
25 ideas, 26.24 USD, 195.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 4.79 | 15.0 |
| step4_backtest | 0.00 | 101.0 |
| step5_verdict | 4.16 | 14.8 |
| step6_check | 0.00 | 1.1 |
| chart_files | 0.00 | 0.4 |
| step7_7.d | 1.48 | 5.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.68 | 1.7 |
| step7_7.b | 5.28 | 15.7 |
| step7_7.g | 9.85 | 29.6 |
| similarity_check | 0.00 | 0.6 |
| unseen_test | 0.00 | 10.8 |
