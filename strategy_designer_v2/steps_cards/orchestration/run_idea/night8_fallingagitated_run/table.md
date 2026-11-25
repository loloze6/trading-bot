# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_agitated-decline-rally-giveback | - | plan | inconclusive (+0.49) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.b1_rally-giveback-all-coins; 7.g: 058-01.g2_agitated-decline-one-day-rise-fades | 1.14 | 6.9 |
| 058-01.b1_rally-giveback-all-coins | 058-01_agitated-decline-rally-giveback | plan | inconclusive (+1.74) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.b1.b1_rally-giveback-over-fifteen-days; 7.g: no ideas: Across the 10 angles examined (scaled rises over 3, 5 and 10 days, range, close location, weekday, trend and agitation profiles, years, coins, trades), no pattern stood out beyond what that many looks produce by chance. The best ones are a borderline momentum outside the profile (t about 2, F3, F4) and a weekday effect that is overstated and already held (F5). The brief's graded give-back is absent inside its profile (F1). | 1.03 | 11.6 |
| 058-01.b1.b1_rally-giveback-over-fifteen-days | 058-01.b1_rally-giveback-all-coins | plan | inconclusive (+1.21) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 058-01.b1.b1.b1_rally-giveback-over-twenty-days, 058-01.b1.b1.b2_large-rallies-fail-within-week; 7.g: 058-01.b1.b1.g1_rally-giveback-over-three-days | 1.00 | 11.7 |

## Consumption
3 ideas, 3.16 USD, 30.2 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.22 | 1.4 |
| step4_backtest | 0.00 | 18.9 |
| step5_verdict | 0.57 | 2.1 |
| step6_check | 0.00 | 0.1 |
| chart_files | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.b | 1.02 | 3.3 |
| step7_7.g | 1.35 | 4.5 |
