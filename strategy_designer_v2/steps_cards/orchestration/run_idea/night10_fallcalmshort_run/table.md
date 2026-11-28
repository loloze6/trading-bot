# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_falling-calm-scaled-rise-fade | - | plan | no effect (-0.28) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.c: 061-01.c1_falling-calm-decline-continues, 061-01.c2_low-close-keeps-sliding | 0.84 | 7.2 |
| 064-01_falling-calm-up-day-fades | - | plan | no effect (-0.69) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 064-01.c1_feeble-bounces-fail-in-calm-declines | 0.62 | 6.5 |
| 070-01_falling-calm-run-break-fade | - | plan | no effect (-0.18) | not profitable enough (failed: Sharpe minus holding's Sharpe, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 070-01.c1_deep-run-bounce-fades, 070-01.c2_weak-bounce-gives-back | 0.66 | 6.8 |
| 060-02_falling-calm-low-to-close-fade | - | missing-components | - | - | - | - | 0.09 | 0.5 |
| 086-02_down-up-volume-ratio-drift | - | missing-components | - | - | - | - | 0.12 | 0.5 |
| 050-03_falling-calm-range-scaled-week-fall | - | plan | no effect (-0.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 050-03.c1_calm-downtrend-3-day-fall-continues, 050-03.c2_calm-downtrend-near-low-continuation; 7.g: no ideas: In falling calm markets on these coins, no pattern on the short side stands out from chance after the many angles examined. The scaled weekly fall, 3-day falls, close location, range, volume, distance to recent extremes, volatility level and weekday all fail to grade the next days' fall consistently across windows and coins. The only gradient found (F2) is a long-side continuation of 3-day rises, which lies outside this research's short box. | 0.98 | 7.8 |
| 077-01_falling-calm-deep-close-drift | - | plan | no effect (+0.23) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 077-01.c1_short-window-peak-depth-continuation, 077-01.c2_calm-downtrend-fall-continuation; 7.g: no ideas: Across 11 bar measures, 4 horizons, weekdays, years, coins and the book's extreme days, nothing in falling calm markets on the short side stands out from chance (best t 2.26 among 44 tests); the only strong pattern, the one-day reversal in falling markets (t −2.99), lives outside the calm profile and is already held on the map. | 1.15 | 9.3 |
| 050-03.c1_calm-downtrend-3-day-fall-continues | 050-03_falling-calm-range-scaled-week-fall | plan | no effect (+0.58) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 050-03.c1.c1_calm-downtrend-fall-continues-5-days; 7.g: no ideas: Inside the falling calm profile on the short side, the only consistent pattern is that 3-day falls are followed by further weakness (+1.3 % to +2.5 %, t 1.6 to 1.7), and it neither grows with the fall's size nor clears chance across the many angles examined (F1, F2, F5). Its clearer two-sided form rests partly on rises, which fall outside the short-only box (F3, F4). | 1.05 | 8.4 |
| 032-01.b1_calm-fall-continuation-all-coins | 032-01_calm-fall-depth-continues | plan | no effect (+0.56) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 032-01.b1.c1_calm-decline-short-burst-continuation, 032-01.b1.c2_two-day-drop-keeps-falling; 7.g: 032-01.b1.g1_calm-decline-recent-fall-continuation | 1.01 | 7.1 |
| 086-01_down-day-volume-share-drift | - | plan | no effect (-0.27) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 086-01.c1_down-volume-share-next-day-drift | 1.55 | 7.1 |

## Consumption
10 ideas, 8.07 USD, 61.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.81 | 5.3 |
| step4_backtest | 0.00 | 35.0 |
| step5_verdict | 1.42 | 5.4 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 1.50 | 4.4 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 3.34 | 10.6 |
