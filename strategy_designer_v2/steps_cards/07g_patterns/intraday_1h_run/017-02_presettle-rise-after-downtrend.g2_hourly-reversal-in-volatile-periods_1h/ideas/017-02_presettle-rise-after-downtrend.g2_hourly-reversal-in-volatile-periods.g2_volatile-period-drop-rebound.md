---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high relative to its 30-day average, the coin rises over the next hour after a falling hour. The larger the fall relative to its usual hourly volatility, and the higher that volatility ratio, the larger the rise.
Consequence: A trader would buy sharp hourly drops in turbulent periods rather than fade both directions, and would refuse such buys if the rebound is not confirmed.
Why:
- F3: In high volatility, down hours reverse far more than up hours. In the top volatility fifth, down hours give 0.000572 (t 6.9, n 37,672) and up hours 0.000189 (t 2.4). In the lowest fifth, down hours continue slightly (-0.000074, t -2.0) while up hours still revert (0.000166, t 4.6).
- F2: The one-hour reversal is real and grows with the volatility level. The mean of -sign(last hour) × next hour rises from 0.000047 (t 1.8) in the lowest fifth of 24h-volatility-to-its-30-day-average to 0.000376 (t 6.6) in the highest fifth. The slope of next-hour excess return per unit of scaled move goes from +0.000006 to -0.000581 across the same fifths.
