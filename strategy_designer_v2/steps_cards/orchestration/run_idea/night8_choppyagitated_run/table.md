# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 058-01_choppy-agitated-weekly-rise-continues | - | plan | inconclusive (-0.12) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. In a choppy, agitated market the past week's rise is followed by an excess next-week return of zero over all folds (-0.12 %, t -0.12, F1). Where it can be seen, it leans to reversal, and more so the larger the rise (F2, F3). This holds at every horizon, on the mirror side, on every coin and in every year (F4 to F6). The only continuation found lives outside the theme's market (F7).; 7.g: no ideas: The theme's effect is not in the data. In-profile weekly continuation after a rise is null or negative (F1), the profile is too rare on daily bars to grade (F2), and the fall-side mirror stays under t 2 (F3). The only patterns that stand out are the down-day rebounds and the late-week gain (F5, F6), which the profile map already holds. This rests on the angles looked at: the forecast by quintile, in and out of profile, by sign, coin, window and trend; 1-, 3- and 7-day horizons; the day's range and close location; and the weekday. | 1.18 | 6.7 |
| 058-02_choppy-agitated-weekly-fall-continues | - | plan | inconclusive (-0.09) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. The fall continuation in a choppy, agitated market is zero (F1), its grading is reversed at every horizon (F2, F3), and its sign flips by window, year and coin (F4). Its only apparent strength is the market's own falls in two years (F5), so no narrower case of the theme's situation shows the effect.; 7.g: 0 ideas, 1 discoveries (2 explorations) | 0.94 | 6.3 |
| 059-01_choppy-calm-weekly-rise-continues | - | plan | inconclusive (+1.95) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 059-01.b1_choppy-calm-rise-more-coins; 7.g: no ideas: Over about 30 angles (profiles × horizons × years × weekdays × quintiles), the only patterns near a clustered t of 2 are noise around the tested idea (F1), single-year or single-tail effects (F3, F4), or effects the map already holds (F5, F6), so none stands out enough to be a finding worth testing. | 1.04 | 6.4 |
| 059-01.b1_choppy-calm-rise-more-coins | 059-01_choppy-calm-weekly-rise-continues | plan | inconclusive (+0.99) | not profitable enough (failed: Calmar) | - | 7.b: 059-01.b1.b1_choppy-calm-rise-two-weeks; 7.g: 059-01.b1.g1_calm-market-weekly-rise-continues | 1.02 | 12.2 |
| 059-01.b1.b1_choppy-calm-rise-two-weeks | 059-01.b1_choppy-calm-rise-more-coins | plan | confirmed (+2.76) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.d: 059-01.b1.b1.d1_choppy-calm-swing-scaled-rise, 059-01.b1.b1.d2_choppy-calm-rise-up-month; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.44 | 13.6 |
| 059-01.b1.b1.d1_choppy-calm-swing-scaled-rise | 059-01.b1.b1_choppy-calm-rise-two-weeks | plan | inconclusive (+0.82) | not profitable enough (failed: Calmar) | - | 7.b: 059-01.b1.b1.d1.b1_choppy-calm-rise-three-weeks; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.36 | 12.9 |

## Consumption
6 ideas, 6.98 USD, 58.1 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 0.46 | 2.8 |
| step4_backtest | 0.00 | 34.2 |
| step5_verdict | 1.08 | 3.9 |
| step6_check | 0.00 | 0.2 |
| chart_files | 0.00 | 0.1 |
| step7_7.d | 0.69 | 2.2 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 1.73 | 5.5 |
| step7_7.g | 3.02 | 9.2 |
| similarity_check | 0.00 | 0.1 |
