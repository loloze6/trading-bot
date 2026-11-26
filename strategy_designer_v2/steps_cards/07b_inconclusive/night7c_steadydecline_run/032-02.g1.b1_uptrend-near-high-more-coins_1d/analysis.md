---
line: 7.b inconclusive
backtest: 032-02.g1.b1_uptrend-near-high-more-coins_1d
idea tested: 032-02.g1.b1_uptrend-near-high-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3945 USD
---
## Findings
- **F1:** Step 5's top-minus-bottom-third difference is positive but short of the bar (+0.66 %, Welch t 0.94, 1179 cases per third). In folds B and C the test's forecast gives top-minus-bottom +2.41 % (t 1.51, 428 per third) at 5 days. The raw 28-day closing-high proximity, which is what the idea states, gives +4.50 % (t 2.73, 313 per third) at the same horizon. So standardising the proximity against its own past 60 values dilutes the effect the idea describes.
- **F2:** Dropping window w18, the test's forecast loses the effect (+0.96 %, t 0.56, 384 per third), while the raw proximity keeps it (+3.76 %, t 2.12, 285 per third). The standardised forecast's showing rests on one window (w18 t 5.84); the raw closeness does not.
- **F3:** Measured on raw proximity, the effect is graded and concentrated near the high. Mean excess 5-day returns by proximity quintile run −3.11 %, +1.83 %, −0.31 %, +0.99 %, +5.43 %. The 163 cases closing at the 28-day high average +6.40 %, against +0.05 % for the 1122 others. The day-clustered slope of the 5-day excess return on proximity has t 2.42 (941 cases on 160 days).
- **F4:** The effect is larger over 10 days than over 5. For raw proximity, top-minus-bottom is +7.44 % (t 2.92) over 10 days against +4.50 % (t 2.73) over 5. For the test's forecast it is +5.01 % (t 2.04) over 10 days against +2.41 % (t 1.51) over 5. Over 20 days it fades: +5.71 % (t 1.46) for raw proximity and −0.76 % (t −0.18) for the forecast.
- **F5:** Scaling the distance from the high by the coin's 30-day daily volatility sharpens the effect: top-minus-bottom +4.98 % (t 3.12) over 5 days and +8.54 % (t 3.43) over 10 days. Consistent with this, the test's forecast shows the effect in the calmer half of cases (+6.39 %, t 2.34) and hardly in the more volatile half (+1.07 %, t 0.66).
- **F6:** The effect is not equal across coins or years, though most point the same way. By coin, raw proximity's difference is positive in 9 of 11 measurable coins, strongest in XRP (t 2.80) and XMR (t 2.08), and negative in UNI (t −2.05) and LINK (t −0.64). By year it is positive in 2019, 2020 and 2021 (t 0.93, 2.77, 1.52) and flat in 2018 (t 0.08).

## Ideas
- `032-02.g1.b1.b1_uptrend-near-high-ten-days` (from F1, F3, F4): Among coins that have risen over the past 28 days, the closer the day's close is to the highest close of those 28 days, the larger the further rise over the next 10 days.
- `032-02.g1.b1.b2_uptrend-near-high-vol-scaled` (from F2, F4, F5): Among coins that have risen over the past 28 days, the smaller the day's distance below the highest close of those 28 days, measured in the coin's typical daily moves over the past 30 days, the larger the further rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
