# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_falling-calm-scaled-rise-fade | - | plan | no effect (-0.28) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar, Trades per day) | - | 7.c: 061-01.c1_falling-calm-decline-continues, 061-01.c2_low-close-keeps-sliding | 0.84 | 7.2 |
| 064-01_falling-calm-up-day-fades | - | plan | no effect (-0.69) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 064-01.c1_feeble-bounces-fail-in-calm-declines | 0.62 | 6.5 |
| 070-01_falling-calm-run-break-fade | - | plan | no effect (-0.18) | not profitable enough (failed: Sharpe minus holding's Sharpe, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 070-01.c1_deep-run-bounce-fades, 070-01.c2_weak-bounce-gives-back | 0.66 | 6.8 |
| 086-01_down-day-volume-share-drift | - | missing-components | - | - | - | - | 0.06 | 0.3 |
| 060-02_falling-calm-low-to-close-fade | - | missing-components | - | - | - | - | 0.09 | 0.5 |
| 086-02_down-up-volume-ratio-drift | - | missing-components | - | - | - | - | 0.12 | 0.5 |
| 050-03_falling-calm-range-scaled-week-fall | - | plan | no effect (-0.98) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 050-03.c1_calm-downtrend-3-day-fall-continues, 050-03.c2_calm-downtrend-near-low-continuation; 7.g: no ideas: In falling calm markets on these coins, no pattern on the short side stands out from chance after the many angles examined. The scaled weekly fall, 3-day falls, close location, range, volume, distance to recent extremes, volatility level and weekday all fail to grade the next days' fall consistently across windows and coins. The only gradient found (F2) is a long-side continuation of 3-day rises, which lies outside this research's short box. | 0.98 | 7.8 |
| 077-01_falling-calm-deep-close-drift | - | plan | no effect (+0.23) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.c: 077-01.c1_short-window-peak-depth-continuation, 077-01.c2_calm-downtrend-fall-continuation; 7.g: no ideas: Across 11 bar measures, 4 horizons, weekdays, years, coins and the book's extreme days, nothing in falling calm markets on the short side stands out from chance (best t 2.26 among 44 tests); the only strong pattern, the one-day reversal in falling markets (t −2.99), lives outside the calm profile and is already held on the map. | 1.15 | 9.3 |

## Consumption
8 ideas, 4.52 USD, 39.0 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.71 | 4.0 |
| step4_backtest | 0.00 | 22.2 |
| step5_verdict | 0.90 | 3.5 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.g | 0.71 | 2.1 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 2.19 | 6.9 |
