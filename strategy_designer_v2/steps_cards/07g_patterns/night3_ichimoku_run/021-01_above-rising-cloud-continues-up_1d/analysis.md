---
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up_1d
idea tested: 021-01_above-rising-cloud-continues-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3592 USD
---
## Findings
- **F1:** After a down day, the next day's return beats the coin's normal daily drift, and the gap grows with the size of the fall. With the day's return in units of its 20-day volatility (z), the excess is +0.50 % after z between -2 and -1 (t 3.57, 1414 days) and +0.80 % after z below -2 (t 2.89, 510 days). The slope of the next day's excess on z across down days is -0.0037 (t -5.59, 7443 days). Up days show no such slope (t 0.02, 7618 days).
- **F2:** This next-day rebound after falls of more than one volatility is large enough to trade. Per case the unusual move is +0.58 % and the total move +0.68 %, about 3.6 times the 0.19 % round trip, with a strength of 0.12 (1924 cases).
- **F3:** The rebound is stable across the two halves of the windows, at +0.53 % in w1–12 (t 3.28) and +0.64 % in w13–24 (t 3.25). It is positive on all 6 coins, ranging from +0.23 % on BTC (t 0.99) to +1.03 % on XMR (t 3.43). It is weak in some years: about 0 in 2019, 2024 and 2025, and +1.4 % to +1.8 % in 2020–2021 (t 3.4 to 4.0).
- **F4:** The rebound lasts one day only. Over 3 days the excess after falls of more than one volatility is +0.35 % to +0.43 % (t 0.61 to 0.87). Over 7 days it is about 0 or negative (t -1.18 to 0.01).
- **F5:** Strong up days are followed by continuation over the next days rather than the next day. Over 7 days the excess is +2.58 % after z between 1 and 2 (t 2.35, 213 cases) and +3.41 % after z above 2 (t 1.71, 89 cases). Over 3 days, the slope of the excess on z across up days is +0.0053 (t 3.10, 2544 cases). Given how many angles were examined, this is weaker evidence than F1.
- **F6:** The tested cloud regime adds little over 26 days. Its excess return is +4.8 % per case (t 1.30, 149 cases), against -1.7 % off the regime (t -1.39, 427 cases). The book earns less than holding the coin on every coin, for example 0.075 % vs 0.118 % per day on BTC and 0.005 % vs 0.155 % on ZEC. It beats holding only in the falling or flat years 2018, 2019 and 2022.
- **F7:** Several other angles showed no pattern that stands out from chance. These include the weekday effect, which flips between the halves of the windows (Monday +0.06 % vs -0.47 %), and 26-day returns by quintile of 26-day return, 7-day return, volatility, range position and range width (no monotone ordering, best t 2.3 among about 25 groups).

## Ideas
- `021-01_above-rising-cloud-continues-up.g1_one-day-rebound-after-falls` (from F1, F2, F3, F4): When a coin closes down on the day, its return over the next day is above its normal drift, and the larger the day's fall relative to its 20-day volatility, the larger the rebound.
- `021-01_above-rising-cloud-continues-up.g2_week-long-continuation-after-surges` (from F5, F4): When a coin closes up on the day, its return over the next 7 days is above its normal drift, and the larger the day's rise relative to its 20-day volatility, the larger the move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
