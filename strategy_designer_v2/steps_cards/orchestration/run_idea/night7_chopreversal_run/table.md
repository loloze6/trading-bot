# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 032-01_choppy-agitated-weekly-rise-reverts | - | plan | inconclusive (-1.30) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. The tested result points the wrong way (F1), and inside the choppy agitated profile larger weekly rises are not followed by larger falls at any horizon (F2, F4). The only fall seen follows rises and falls alike (F3), and the reversal is no stronger in the profile than outside it (F5), so no amended idea on the theme has a finding to rest on.; 7.g: 032-01.g1_choppy-market-weekly-reversal | 0.96 | 5.5 |
| 033-01_scaled-daily-fall-next-day-rebound | - | plan | confirmed (+2.63) | not profitable enough (failed: Calmar) | - | 7.d: 033-01.d1_agitated-outsized-fall-rebound, 033-01.d2_falling-agitated-fall-rebound; 7.g: 033-01.g1_heavy-volume-outsized-fall-rebound, 033-01.g2_agitated-market-scaled-fall-rebound | 1.12 | 5.4 |
| 032-02_choppy-agitated-weekly-fall-reverts | - | plan | inconclusive (-0.54) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 032-02.b1_choppy-agitated-weekly-rise-fades; 7.g: 0 ideas, 3 discoveries (2 explorations) | 1.00 | 5.6 |
| 034-01_agitated-scaled-fall-next-day-rebound | - | plan | inconclusive (+1.89) | not profitable enough (failed: Calmar) | - | 7.b: 034-01.b1_agitated-fall-rebound-more-coins, 034-01.b2_falling-agitated-fall-rebound; 7.g: 034-01.g1_agitated-extreme-fall-convex-rebound, 034-01.g2_agitated-deep-fall-two-day-rebound, 034-01.g3_agitated-three-day-fall-rebound, 034-01.g4_scaled-fall-rebound-every-market | 1.05 | 6.1 |
| 035-01_falling-agitated-scaled-fall-rebound | - | plan | confirmed (+2.62) | profitable enough | unseen_2016_2017: holds; unseen_2026: does not hold | 7.g: 035-01.g1_second-down-day-rebound, 035-01.g2_scaled-fall-two-day-rebound | 0.65 | 5.7 |

## Consumption
5 ideas, 4.77 USD, 28.4 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.37 | 2.0 |
| step4_backtest | 0.00 | 11.2 |
| step5_verdict | 0.82 | 2.8 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.44 | 1.2 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.04 | 3.1 |
| step7_7.g | 2.10 | 6.6 |
| similarity_check | 0.00 | 0.1 |
| unseen_test | 0.00 | 1.1 |
