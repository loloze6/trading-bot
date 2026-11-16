# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs | 002-03_price-cross-above-long-sma | plan | not observable (+1.22) | profitable enough | 7.a: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.a1_near-high-drift-wider-universe; 7.e: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs; 7.g: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal | 1.05 | 15.2 |

## Consumption
1 ideas, 1.05 USD, 15.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.00 | 0.0 |
| step4_backtest | 0.00 | 11.6 |
| step5_verdict | 0.14 | 0.6 |
| step6_check | 0.00 | 0.1 |
| step7_7.b | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.19 | 0.6 |
| step7_7.e | 0.36 | 1.1 |
| step7_7.g | 0.36 | 1.1 |
