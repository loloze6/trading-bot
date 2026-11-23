---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a sharp falling hour, only while its volatility over the last 20 hours is high against its usual volatility over the past 30 days, and the higher that ratio, the larger the rise.
Consequence: A trader would buy a coin's sharp hourly falls and hold them for a day only when its recent hourly volatility is well above its month's norm, and would refuse the same falls in calm periods, where they keep falling.
Why:
- F1: The clean cases split by volatility regime, and the split is graded. The cases are the first hour in each 24-hour cell whose fall is at least 2.5 of the previous 20 hours' standard deviation. The regime is the 20-hour volatility over its 30-day median. The unusual 24-hour move rises steadily across the regime's quartiles: −0.47 % (t −4.11, 1571 cases), −0.30 % (t −2.71), −0.08 % (t −0.61), then +0.39 % (t 2.34, 1571 cases). In strength that is −0.093 up to +0.071. With falls of at least 1.5 standard deviations the same quartiles run from −0.31 % (t −4.15) to +0.55 % (t 4.65), with 3201 cases each.
- F2: Over all cases, a larger fall is followed by a smaller move, which is the reverse of what the idea predicts. The unusual 24-hour move is +0.02 % (t 0.38, 13774 cases) after falls of at least 1.5 standard deviations. It is −0.11 % (t −1.75, 6727 cases) after falls of at least 2.5, and −0.16 % (t −1.65, 3206 cases) after falls of at least 3.5, where the 48-hour move is −0.32 % (t −2.69). This matches step 5's failed supporting check: upper half minus lower half is −0.055 %.
- F3: The two regimes cancel each other in the pooled test, which leaves it near zero. Step 5 found +0.02 % per case (t 0.51, 17184 cases), a strength of 0.003. That is 0.1 times the 0.19 % cost of a trade. In the highest-volatility quartile alone, the unusual move of +0.39 % to +0.55 % would cover that cost about two to three times over (F1).
- F4: The effect is also carried by the market's own periods. Across all regimes, falls of at least 2.5 standard deviations were followed by −0.98 % in 2018 (t −4.05) and −0.42 % in 2022 (t −2.74), but by +0.24 % in 2023 (t 2.42) and +0.31 % in 2024 (t 2.04).
- F5: Inside the high-volatility half, the move is still unstable. By year it ranges from +0.58 % in 2023 (t 4.31) and +0.84 % in 2024 (t 3.23) down to −0.60 % in 2020 (t −1.54). It is also not graded by the size of the fall: +0.66 % (t 3.20) for falls of 2.5 to 3 standard deviations, against −0.04 % (t −0.25) for falls beyond 4.
