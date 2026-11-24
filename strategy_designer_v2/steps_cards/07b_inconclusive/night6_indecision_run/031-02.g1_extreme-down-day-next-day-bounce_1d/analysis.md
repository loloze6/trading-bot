---
line: 7.b inconclusive
backtest: 031-02.g1_extreme-down-day-next-day-bounce_1d
idea tested: 031-02.g1_extreme-down-day-next-day-bounce
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3316 USD
---
## Findings
- **F1:** The test's result is on the predicted side but short of the bar: the mean excess next-day return is +0.69 % with t 1.30 over 492 cases on 200 independent days, with a 57 % hit rate and a +0.56 % median. The supporting check passed (forecast-weighted +0.78 %), so the shortfall is in how sure the result is, not in its sign or its grading.
- **F2:** The result is weak because the cases are noisy and lean on a few of them: the per-case standard deviation is 6.2 % against a +0.69 % mean, the five largest cases carry 43 % of the summed excess, and the 5 %-trimmed mean is only +0.50 %.
- **F3:** Close location sorts the result as the idea predicts. Closes at the low (top 15 % of the range) are followed by +1.42 % (t 2.18, 208 cases, 107 days), closes near the low by +0.35 % (t 0.47, 230 cases), and closes mid-range or higher by −0.70 % (t −0.98, 54 cases). The correlation of close location with the next-day excess is 0.13.
- **F4:** The effect grows with the coin's recent volatility: in the calmest third of the 20-day volatility the excess is −0.63 % (t −1.48, 137 cases), in the middle third +0.25 % (t 0.41), and in the wildest third +2.10 % (t 1.69, 138 cases, 67 days).
- **F5:** The effect differs by coin and by year: XMR carries the strongest result (+2.04 %, t 2.72, 87 days), while LTC (−0.13 %) and ZEC (+0.17 %) show almost nothing. 2020 (+4.15 %) and 2021 (+2.83 %) are strong, while 2022–2025 are near 0 (−0.40 % to +0.28 %).
- **F6:** The test measured the idea at the right horizon, which is 1 day: the excess fades to +0.34 % at 2 days (t 0.75), −0.24 % at 3 days and −0.75 % at 5 days (t −0.96). A longer horizon would not sharpen it.
- **F7:** Only 6 coins were used, with 81–91 cases each, while daily data exists in folds A and D (and part of B and C) for 13 more coins. A test on all 19 coins would roughly double the independent cases behind a t that is now 1.30.

## Ideas
- `031-02.g1.b1_deep-down-day-bounce-more-coins` (from F1, F2, F6, F7): After a day on which a coin falls far more than it usually does in a day, it rises over the next 1 day. The deeper that day's fall ranks among the coin's own past daily returns, and the nearer its close sits to the day's low, the larger the rise.
- `031-02.g1.b2_volatile-coins-bounce-after-capitulation` (from F3, F4): After a day on which a coin falls far more than it usually does in a day and closes near its low, it rises over the next 1 day, and the more the coin's daily returns have swung over its past 20 days, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
