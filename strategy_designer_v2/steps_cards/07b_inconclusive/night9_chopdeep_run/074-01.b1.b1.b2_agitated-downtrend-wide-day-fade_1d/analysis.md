---
line: 7.b inconclusive
backtest: 074-01.b1.b1.b2_agitated-downtrend-wide-day-fade_1d
idea tested: 074-01.b1.b1.b2_agitated-downtrend-wide-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4072 USD
---
## Findings
- **F1:** Within folds B and C, every up day in a falling, agitated market with a range above its 20-day mean is followed by a strong next-day fall: 103 cases on 51 days, mean excess fall +2.49 % with t 2.91, and 74 % of the next days are lower. The book's own cases, those whose forecast reached the −2 band, are only 87 cases on 59 days, with mean +1.47 % and t 1.21.
- **F2:** The test's forecast grades the width after standardising it over its past 60 values, and that grading does not follow the effect. Across the book's forecast terciles, the strongest third earns +0.01 % (t 0.00) against +2.42 % and +1.98 % for the mid and weakest thirds. The correlation of the cases' raw width multiple with their excess fall is 0.003.
- **F3:** Graded by the raw multiple of the 20-day mean range, the fade grows steadily in falling markets (318 cases, 146 days). From the narrowest to the widest fifth, with mean multiples of 1.05, 1.17, 1.35, 1.63 and 2.30, the mean excess next-day fall is −0.03 %, +0.27 %, +1.23 % (t 1.94), +1.93 % (t 2.50) and +2.15 % (t 2.24). The correlation is 0.177, and the ratio-weighted mean is 0.29 points above the unweighted mean.
- **F4:** The effect lives in the agitated part of the falling market. Falling wide up days outside the agitated regime fade by only +0.45 % (215 cases, 113 days, t 0.99), against +2.49 % (t 2.91) inside it. Rising markets show no fade, at −0.53 % (512 cases, t −1.30).
- **F5:** The fade is spent in one day, as the brief says. In falling markets the 2-day excess fall is only +0.24 % (t 0.47), against +1.11 % (t 2.47) over 1 day.
- **F6:** The weak part of the data is 2021 and window w18. Falling-market cases in 2021 fade by +0.10 % (t 0.17), and in w18 by −0.78 % (t −1.16). The earlier years 2018 to 2020 range from +0.8 % to +1.7 %.
- **F7:** The test's result is on the predicted side but short of the bar, at +1.47 % with t 1.97 on 160 days. It already used all 19 coins and all four folds of daily data, so no more data is available for the same idea. Its shortfall comes from how the forecast graded the cases (F2), not from too few cases.

## Ideas
- `074-01.b1.b1.b2.b1_agitated-downtrend-range-multiple-fade` (from F1, F2, F3, F4, F5): In a falling, agitated market, an up day whose high-to-low range is a large multiple of the coin's average daily range over the past 20 days is followed by a fall over the next day; the larger that multiple, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
