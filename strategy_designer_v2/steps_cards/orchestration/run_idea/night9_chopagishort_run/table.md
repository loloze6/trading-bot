# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_choppy-agitated-strong-close-fade | - | plan | inconclusive (+1.49) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1_high-close-fade-more-coins; 7.g: 061-01.g1_choppy-five-day-fall-continues, 061-01.g2_high-close-next-day-fade | 1.71 | 6.8 |
| 061-01.b1_high-close-fade-more-coins | 061-01_choppy-agitated-strong-close-fade | plan | inconclusive (+1.74) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1.b1_small-gain-high-close-fades; 7.g: 061-01.b1.g1_choppy-agitated-close-next-day-fade | 1.38 | 13.8 |
| 061-01.b1.b1_small-gain-high-close-fades | 061-01.b1_high-close-fade-more-coins | plan | inconclusive (+3.44) | not profitable enough (failed: Calmar, Trades per day) | - | 7.b: 061-01.b1.b1.b1_high-close-location-fades-weekly; 7.g: 061-01.b1.b1.g1_choppy-agitated-close-height-fade, 061-01.b1.b1.g2_high-close-without-gain-fades | 1.04 | 13.2 |
| 061-01.b1.b1.b1_high-close-location-fades-weekly | 061-01.b1.b1_small-gain-high-close-fades | plan | confirmed (+3.13) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.d: 061-01.b1.b1.b1.d1_high-close-after-fall-fades, 061-01.b1.b1.b1.d2_quiet-high-close-fades, 061-01.b1.b1.b1.d3_high-close-fades-over-ten-days; 7.g: 061-01.b1.b1.b1.g1_falling-coin-high-close-fade | 1.20 | 13.9 |
| 061-01.b1.b1.b1.d1_high-close-after-fall-fades | 061-01.b1.b1.b1_high-close-location-fades-weekly | plan | confirmed (+3.80) | not profitable enough (failed: Calmar, Trades per day) | - | 7.d: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall, 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.33 | 13.9 |

## Consumption
5 ideas, 6.65 USD, 61.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.31 | 3.0 |
| step4_backtest | 0.00 | 41.2 |
| step5_verdict | 1.00 | 3.7 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.96 | 3.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.89 | 2.9 |
| step7_7.g | 2.49 | 7.4 |
| similarity_check | 0.00 | 0.2 |
