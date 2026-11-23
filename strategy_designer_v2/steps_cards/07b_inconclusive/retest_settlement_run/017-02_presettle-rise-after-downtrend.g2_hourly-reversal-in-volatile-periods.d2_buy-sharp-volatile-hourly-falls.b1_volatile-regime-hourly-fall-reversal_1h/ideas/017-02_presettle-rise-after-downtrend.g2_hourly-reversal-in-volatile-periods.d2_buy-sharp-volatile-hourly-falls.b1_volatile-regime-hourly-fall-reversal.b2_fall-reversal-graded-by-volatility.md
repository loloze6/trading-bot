---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a sharp falling hour, and the rise is larger the further the coin's 24-hour volatility is raised above its 30-day average at that hour.
Consequence: A trader would buy sharp hourly falls with more conviction the more turbulent the coin has become against its monthly norm, and would refuse falls that come in calm or merely average volatility.
Why:
- F3: The effect is graded by how far 24-hour volatility is raised against its 30-day average, and the plan's on/off line at a ratio of 1.0 admits mostly cases without it. Among the strategy's cases, the lower three ratio quartiles give −0.104 %, −0.079 % and +0.071 % (t −1.01 to 0.66), and the top quartile gives +0.506 % (t 3.49).
- F4: On all sharp falling hours (at least 1.5 usual moves, one per 24-hour cell), the 24-hour excess rises steadily with the volatility ratio. Below 1.0 it is −0.253 % (t −3.60, strength −0.081, n 4,523); from 1.0 to 1.3, +0.010 % (t 0.09); from 1.3 to 1.6, +0.351 % (t 2.13); from 1.6 to 2.0, +0.315 % (t 1.41); from 2.0 to 2.5, +1.179 % (t 2.73, strength 0.097); above 2.5, +1.539 % (t 2.84, n 337).
- F6: The average case is too small to pay for a trade, but the high-volatility cases are not. The average unusual move is +0.09 % per case (strength 0.015), half of the 0.19 % cost of a trade. Falls at volatility ratios above 2.0 carry +1.2 % to +1.5 % per case, about six to eight times that cost.
