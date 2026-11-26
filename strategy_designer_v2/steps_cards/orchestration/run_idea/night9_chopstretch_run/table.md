# Run table (run_idea)

One row per idea run; every status is read from the step's own result file. Each step call: `journal.jsonl`; each helper's output: `logs/`.

| Idea | Parent | Step 3 | Step 5 | Step 6 | Unseen dates | Step 7: ideas proposed | USD | Minutes |
|---|---|---|---|---|---|---|---|---|
| 067-01_choppy-up-stretch-keeps-rising | - | plan | inconclusive (+0.73) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 067-01.b1_choppy-down-stretch-keeps-falling; 7.g: 0 ideas, 2 discoveries (2 explorations) | 1.18 | 6.5 |
| 067-01.b1_choppy-down-stretch-keeps-falling | 067-01_choppy-up-stretch-keeps-rising | plan | inconclusive (-0.56) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 067-01.b1.b1_choppy-stretch-carries-both-ways; 7.g: 0 ideas, 1 discoveries (2 explorations) | 1.05 | 6.5 |
| 067-01.b1.b1_choppy-stretch-carries-both-ways | 067-01.b1_choppy-down-stretch-keeps-falling | plan | inconclusive (+0.91) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar) | - | 7.b: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling, 067-01.b1.b1.b2_choppy-stretch-carry-all-coins; 7.g: 067-01.b1.b1.g1_choppy-downside-stretch-keeps-falling | 1.01 | 6.2 |
| 074-01_agitated-stretch-below-rebounds | - | plan | inconclusive (+1.03) | not profitable enough (failed: Calmar) | - | 7.b: 074-01.b1_agitated-stretch-all-coins; 7.g: 0 ideas, 2 discoveries (2 explorations) | 0.84 | 6.6 |
| 074-01.b1_agitated-stretch-all-coins | 074-01_agitated-stretch-below-rebounds | plan | inconclusive (+0.68) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: no ideas: The theme's effect is not in the data. In agitated markets a close below the 20-day average is followed by no rebound at 3, 5, 10 or 20 days (F1), the move does not grow with depth (F2), no trend, year or coin shows the rebound (F4), and the test already covered all the data available (F5).; 7.g: 074-01.b1.g1_choppy-agitated-stretch-keeps-falling | 1.08 | 13.7 |
| 067-02_choppy-down-stretch-keeps-falling | - | plan | inconclusive (+0.44) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 067-02.b1_raw-swing-stretch-keeps-falling; 7.g: 067-02.g1_choppy-down-stretch-five-days | 1.01 | 6.4 |
| 067-02.b1_raw-swing-stretch-keeps-falling | 067-02_choppy-down-stretch-keeps-falling | plan | inconclusive (+0.18) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 067-02.b1.b1_two-sided-swing-stretch-five-days; 7.g: 067-02.b1.g1_choppy-agitated-fall-carries | 0.98 | 5.9 |
| 074-02_calm-stretch-below-keeps-falling | - | plan | inconclusive (+0.29) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-02.b1_calm-stretch-falls-five-days; 7.g: 0 ideas, 2 discoveries (2 explorations) | 0.95 | 6.9 |
| 074-02.b1_calm-stretch-falls-five-days | 074-02_calm-stretch-below-keeps-falling | plan | inconclusive (-0.85) | not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 074-02.b1.b1_calm-stretch-falls-more-coins; 7.g: no ideas: The one strong pattern, calm stretch continuation (F1), is not graded on the side the idea tested (F2), is unsteady across windows (F3) and repeats the calm nearness-to-high and range-edge continuation books the map already holds. The brief's agitated rebound is not in the data at 5 or 10 days (F4). The agitated and falling-agitated reversals repeat held ideas or are not graded (F5, F6). The weekday pattern does not stand out once same-day cases and the many angles searched are allowed for (F7). | 1.07 | 7.6 |
| 076-01_agitated-wide-high-close-fades | - | plan | inconclusive (+1.29) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 076-01.b1_agitated-wide-close-fade-more-coins; 7.g: no ideas: Across the many angles examined (close location by width, the day's and the 5-day scaled return by trend and agitation, weekday, year, coin, forecast quarters), only the falling-agitated next-day reversal (F1, F2) stands out. It is already held by 058-02.b1.g1.b1.b1 and the falling-agitated rebound family. The candidate for the empty choppy-agitated short cell (F4, t −1.94) and the tested wide-high-close fade (F3, t −1.88) do not clear the bar that this many looks require. | 1.94 | 8.1 |
| 076-01.b1_agitated-wide-close-fade-more-coins | 076-01_agitated-wide-high-close-fades | plan | inconclusive (-1.85) | not profitable enough (failed: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar) | - | 7.b: 076-01.b1.b1_agitated-wide-upper-close-fade; 7.g: no ideas: The brief's fade of wide high-closing agitated days is absent in rising markets and too small to cover costs (F1, F5). Its one strong cell (falling agitated, F6) rests on two windows and repeats a close-height fade the map already holds. The clear pattern in the book, the rebound after wide low-closing days (F2–F4, F8), is a family the map already holds, and the choppy calm cell is ungraded and indistinguishable from chance across the many angles examined (F7). | 1.23 | 14.6 |
| 077-01_choppy-calm-swing-rise-carries | - | plan | inconclusive (+1.28) | not profitable enough (failed: Sharpe minus holding's Sharpe, Calmar) | - | 7.b: 077-01.b1_swing-rise-carry-more-coins; 7.g: 077-01.g1_choppy-calm-swing-fall-carries, 077-01.g2_choppy-calm-two-sided-swing-carry | 0.90 | 6.9 |

## Consumption
12 ideas, 13.25 USD, 95.8 minutes in all.

| Step | USD | Minutes |
|---|---|---|
| step3_plan | 1.92 | 6.4 |
| step4_backtest | 0.00 | 52.5 |
| step5_verdict | 2.01 | 7.1 |
| step6_check | 0.00 | 0.4 |
| chart_files | 0.00 | 0.2 |
| step7_7.e | 0.00 | 0.0 |
| step7_7.a | 0.00 | 0.0 |
| step7_7.d | 0.00 | 0.0 |
| step7_7.c | 0.00 | 0.0 |
| step7_7.b | 3.77 | 11.8 |
| step7_7.g | 5.56 | 17.3 |
