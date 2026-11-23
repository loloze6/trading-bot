---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 12 hours, a coin rises after a falling hour, and the larger that fall times the coin's 24-hour volatility over its 30-day average, the larger the rise.
Consequence: A trader would buy sharp volatile down hours and hold the rebound for half a day, leaving out the short fade of up hours that earns nothing.
Why:
- F1: The edge per case is far smaller than a trade's cost. The book keeps a position on 100 % of coin-days, with a mean |allocation| of 0.49 and a mean |allocation change| of 0.136 per bar. That gives 11.87 trades a day across 208,476 trades lasting 7.5 h on average. Those trades lose -0.097 % before fees and -0.197 % after, against a cost of 0.19 % a trade. Over 4 hours the idea's own cases move only +0.03 % (strength 0.016), so the book loses -0.21 % a day while holding the coins earns +0.12 % a day.
- F2: The effect is graded, but its useful size sits in the extreme cases. On non-overlapping 4-hour samples the signed excess move rises with the forecast's size: +0.008 % in the lowest half (t 1.0, n 51,544), +0.07 % at the 80–90th percentile (t 3.3), +0.16 % at the 90–95th (t 4.2) and +0.21 % in the top 5 % (t 4.2, n 4,158). Only that top 5 %, where the forecast sits at its ±20 cap, beats the 0.19 % cost. The book instead trades every bar's forecast, and its entries in the 80–95th percentile still lose -0.31 % net.
- F5: The long side carries the effect. In the top 5 % of |forecast|, the bounce after a down hour earns +0.36 % over 4 hours and +0.57 % over 12 hours. The fade of an up hour earns +0.09 % over 4 hours and -0.09 % over 12 hours. The coin's normal drift in the case direction is about 0.00 % per 4 hours, so the long side's gain is not just holding the market.
