# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 061-01_choppy-agitated-strong-close-fade | - | plan | inconclusive (+1.49) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1_high-close-fade-more-coins; 7.g: 061-01.g1_choppy-five-day-fall-continues, 061-01.g2_high-close-next-day-fade | 1.71 | 6.8 |
| 061-01.b1_high-close-fade-more-coins | 061-01_choppy-agitated-strong-close-fade | plan | inconclusive (+1.74) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1.b1_small-gain-high-close-fades; 7.g: 061-01.b1.g1_choppy-agitated-close-next-day-fade | 1.38 | 13.8 |
| 061-01.b1.b1_small-gain-high-close-fades | 061-01.b1_high-close-fade-more-coins | plan | inconclusive (+3.44) | not profitable enough (failed: Calmar, Trades per day) | - | 7.b: 061-01.b1.b1.b1_high-close-location-fades-weekly; 7.g: 061-01.b1.b1.g1_choppy-agitated-close-height-fade, 061-01.b1.b1.g2_high-close-without-gain-fades | 1.04 | 13.2 |
| 061-01.b1.b1.b1_high-close-location-fades-weekly | 061-01.b1.b1_small-gain-high-close-fades | plan | confirmed (+3.13) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.d: 061-01.b1.b1.b1.d1_high-close-after-fall-fades, 061-01.b1.b1.b1.d2_quiet-high-close-fades, 061-01.b1.b1.b1.d3_high-close-fades-over-ten-days; 7.g: 061-01.b1.b1.b1.g1_falling-coin-high-close-fade | 1.20 | 13.9 |
| 061-01.b1.b1.b1.d1_high-close-after-fall-fades | 061-01.b1.b1.b1_high-close-location-fades-weekly | plan | confirmed (+3.80) | not profitable enough (failed: Calmar, Trades per day) | - | 7.d: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall, 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.33 | 13.9 |
| 061-01.b1.b1.b1.d2_quiet-high-close-fades | 061-01.b1.b1.b1_high-close-location-fades-weekly | plan | confirmed (+2.45) | not profitable enough (failed: Calmar, Trades per day) | - | 7.d: 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade, 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade, 061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade; 7.g: no ideas: The only patterns that stand out after many angles are the wide-range low-close rebound and its rising-market case (F1, F2), both already held by the profile map. The brief's own high-close fade does not show beyond the tested signal (F3). The rest cannot be told apart from chance (F5). | 1.21 | 13.9 |
| 061-01.b1.b1.b1.d3_high-close-fades-over-ten-days | 061-01.b1.b1.b1_high-close-location-fades-weekly | plan | inconclusive (+2.90) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1.b1.b1.d3.b1_persistent-high-closes-fade, 061-01.b1.b1.b1.d3.b2_quiet-high-close-fades; 7.g: no ideas: Across close location, prior-day return, range size, weekday, year and profile on 1-, 2-, 5- and 10-day horizons, nothing stands out from chance given that many angles. The strongest pattern, a one-day gradient with close location (F1), is at t 1.7 on its high-close side and is already the tested situation in a wider profile. The in-profile cells rest on about ten cases each (F2, F3, F6). | 1.10 | 12.8 |
| 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade | 061-01.b1.b1.b1.d2_quiet-high-close-fades | plan | inconclusive (+3.16) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1.b1.b1.d2.d1.b1_raw-range-location-ten-day-fade, 061-01.b1.b1.b1.d2.d1.b2_smallest-gain-high-close-fade; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.17 | 13.2 |
| 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade | 061-01.b1.b1.b1.d2_quiet-high-close-fades | plan | inconclusive (+1.68) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 061-01.b1.b1.b1.d2.d2.b1_near-high-quiet-day-fade; 7.g: 0 ideas, 1 discoveries (3 explorations) | 1.37 | 14.2 |
| 061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade | 061-01.b1.b1.b1.d2_quiet-high-close-fades | plan | confirmed (+2.45) | not profitable enough (failed: Calmar, Trades per day) | - | 7.d: 061-01.b1.b1.b1.d2.d3.d1_high-close-fade-held-longer, 061-01.b1.b1.b1.d2.d3.d2_pullback-high-close-fade, 061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade; 7.g: 061-01.b1.b1.b1.d2.d3.g1_choppy-agitated-close-height-fade | 4.45 | 27.5 |
| 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall | 061-01.b1.b1.b1.d1_high-close-after-fall-fades | plan | confirmed (+2.70) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.d: 061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall, 061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall, 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade; 7.g: 061-01.b1.b1.b1.d1.d1.g1_agitated-chop-high-close-five-day-fade | 1.49 | 14.3 |
| 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded | 061-01.b1.b1.b1.d1_high-close-after-fall-fades | plan | confirmed (+2.87) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.d: 061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded, 061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall; 7.g: 061-01.b1.b1.b1.d1.d2.g1_choppy-market-twenty-day-continuation, 061-01.b1.b1.b1.d1.d2.g2_choppy-market-five-day-continuation | 1.36 | 14.7 |
| 061-01.b1.b1.b1.d2.d3.d2_pullback-high-close-fade | 061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade | plan | inconclusive (+1.47) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar, Trades per day) | - | 7.b: 061-01.b1.b1.b1.d2.d3.d2.b1_quiet-high-close-fades; 7.g: 061-01.b1.b1.b1.d2.d3.d2.g1_choppy-agitated-high-close-fade, 061-01.b1.b1.b1.d2.d3.d2.g2_choppy-calm-big-day-continuation | 1.18 | 13.8 |
| 061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade | 061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade | plan | inconclusive (+0.91) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 061-01.b1.b1.b1.d2.d3.d3.b1_deep-pullback-high-close-fade, 061-01.b1.b1.b1.d2.d3.d3.b2_deep-pullback-two-day-fade; 7.g: no ideas: Across forecast, close location, past 5-day moves, day size, range width and its 5-day compression, weekday, profile, year and the book's extreme days, the only pattern that clears chance is the next-day rebound after a large down day (F2), which the profile map already holds many times; nothing new stands out. | 1.19 | 12.8 |

## Consumption
14 ideas, 21.17 USD, 198.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 2.27 | 8.9 |
| step4_backtest | 0.00 | 127.0 |
| step5_verdict | 2.85 | 10.3 |
| step6_check | 0.00 | 0.5 |
| chart_files | 0.00 | 0.3 |
| step7_7.d | 2.79 | 8.8 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.b | 2.95 | 8.9 |
| step7_7.g | 10.30 | 33.4 |
| similarity_check | 0.00 | 0.6 |
