# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_choppy-agitated-strong-close-fade | - | plan | inconclusive (+1.49) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1_high-close-fade-more-coins; 7.g: 061-01.g1_choppy-five-day-fall-continues, 061-01.g2_high-close-next-day-fade | 1.71 | 6.8 |
| 061-01.b1_high-close-fade-more-coins | 061-01_choppy-agitated-strong-close-fade | plan | inconclusive (+1.74) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1.b1_small-gain-high-close-fades; 7.g: 061-01.b1.g1_choppy-agitated-close-next-day-fade | 1.38 | 13.8 |
| 061-01.b1.b1_small-gain-high-close-fades | 061-01.b1_high-close-fade-more-coins | plan | inconclusive (+3.44) | not profitable enough (failed: Calmar, Trades per day) | - | 7.b: 061-01.b1.b1.b1_high-close-location-fades-weekly; 7.g: 061-01.b1.b1.g1_choppy-agitated-close-height-fade, 061-01.b1.b1.g2_high-close-without-gain-fades | 1.04 | 13.2 |

## Consumption
3 ideas, 4.13 USD, 33.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.12 | 1.9 |
| step4_backtest | 0.00 | 22.2 |
| step5_verdict | 0.59 | 2.1 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 0.89 | 2.9 |
| step7_7.g | 1.53 | 4.5 |
