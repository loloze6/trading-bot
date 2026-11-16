# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|
| 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs | 002-03_price-cross-above-long-sma | plan | not observable (+1.22) | profitable enough | 7.a: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.a1_near-high-drift-wider-universe; 7.e: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs; 7.g: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal | 1.05 | 15.2 |
| 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days | 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs | plan | confirmed (+3.08) | not profitable enough (failed: Mean daily return, Calmar) | 7.d: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d2_near-high-drift-long-only, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d3_moderate-momentum-above-average; 7.g: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g2_sharp-drop-rebound-below-average | 1.34 | 13.7 |
| 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs | 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs | plan | confirmed (+3.32) | not profitable enough (failed: Mean daily return, Calmar) | 7.d: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.d1_push-to-the-high, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.d2_calm-breakouts-follow-through, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.d3_established-uptrend-near-highs; 7.g: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g2_monthly-losers-keep-falling | 0.86 | 13.1 |
| 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal | 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs | plan | inconclusive (+4.24) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, Lowest Sharpe, one window left out, Calmar) | 7.b: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days; 7.d: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.d1_buy-falls-not-fade-rises, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.d2_sharp-rises-keep-rising; 7.g: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g2_reversal-under-volatility-expansion, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g3_downtrend-one-day-reversal, 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g4_calm-market-one-day-continuation | 1.18 | 12.6 |

## Consumption
4 ideas, 4.42 USD, 54.6 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.43 | 1.3 |
| step4_backtest | 0.00 | 39.3 |
| step5_verdict | 0.55 | 2.6 |
| step6_check | 0.00 | 0.2 |
| step7_7.b | 0.32 | 1.1 |
| step7_7.d | 1.17 | 3.9 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.19 | 0.6 |
| step7_7.e | 0.36 | 1.1 |
| step7_7.g | 1.39 | 4.4 |
