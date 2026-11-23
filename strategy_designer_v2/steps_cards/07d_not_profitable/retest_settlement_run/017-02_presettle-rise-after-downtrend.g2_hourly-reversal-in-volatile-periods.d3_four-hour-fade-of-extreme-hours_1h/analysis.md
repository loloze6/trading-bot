---
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4119 USD
---
## Findings
- **F1:** The edge per case is far smaller than a trade's cost. The book keeps a position on 100 % of coin-days, with a mean |allocation| of 0.49 and a mean |allocation change| of 0.136 per bar. That gives 11.87 trades a day across 208,476 trades lasting 7.5 h on average. Those trades lose -0.097 % before fees and -0.197 % after, against a cost of 0.19 % a trade. Over 4 hours the idea's own cases move only +0.03 % (strength 0.016), so the book loses -0.21 % a day while holding the coins earns +0.12 % a day.
- **F2:** The effect is graded, but its useful size sits in the extreme cases. On non-overlapping 4-hour samples the signed excess move rises with the forecast's size: +0.008 % in the lowest half (t 1.0, n 51,544), +0.07 % at the 80–90th percentile (t 3.3), +0.16 % at the 90–95th (t 4.2) and +0.21 % in the top 5 % (t 4.2, n 4,158). Only that top 5 %, where the forecast sits at its ±20 cap, beats the 0.19 % cost. The book instead trades every bar's forecast, and its entries in the 80–95th percentile still lose -0.31 % net.
- **F3:** The reversal grows with the horizon, and at 24 hours it clears the cost. Over 24 hours the signed excess move is +0.48 % at the 80–90th percentile (t 4.0, n 1,956), +0.59 % at the 90–95th (t 3.2, n 1,013) and +0.67 % at the 95–99th (t 2.8, n 767). The same groups give +0.07 %, +0.16 % and +0.21 % over 4 hours, and +0.14 % to +0.39 % over 12 hours. Every 24-hour figure is several times the 0.19 % cost of one trade.
- **F4:** The fade works only when recent volatility is above its 30-day level; when it is quiet, large hours continue. Among hours in the top 1 % of |move| per coin, the 4-hour fade earns +0.72 % when the 24-hour/720-hour volatility ratio is in its high tercile and -0.30 % when it is in its low tercile. For the 95–99th percentile of |move| the figures are +0.30 % against -0.24 %. A high ratio alone, without the signal's sign, earns only +0.04 % over 4 hours, so the condition is not an effect of its own. It is the idea's own comparison: its 24-hour volatility over its 30-day average.
- **F5:** The long side carries the effect. In the top 5 % of |forecast|, the bounce after a down hour earns +0.36 % over 4 hours and +0.57 % over 12 hours. The fade of an up hour earns +0.09 % over 4 hours and -0.09 % over 12 hours. The coin's normal drift in the case direction is about 0.00 % per 4 hours, so the long side's gain is not just holding the market.
- **F6:** The top-5 % fade does not rest on one period, and it has nothing to do with funding settlement. Across the 24 windows its mean 4-hour excess move is +0.23 %, with a 25th percentile of +0.02 % and a minimum of -0.26 %. Cases closing at the settlement hours 00, 08 and 16 UTC earn +0.12 % (n 393), against +0.23 % at other hours (n 4,804).

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours.d1_day-long-fade-of-extreme-hours` (from F1, F2, F3, F6): Over the next 24 hours, a coin moves against its last hour's move, and the larger that move times the coin's 24-hour volatility over its 30-day average, the larger the reversal.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours.d2_hourly-fade-in-volatile-periods` (from F1, F2, F4): Over the next 4 hours, a coin moves against its last hour's move, and the larger that move times the coin's 24-hour volatility over its 30-day average, the larger the reversal, only while the coin's 24-hour volatility is above its 30-day average.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours.d3_half-day-rebound-after-volatile-drops` (from F1, F2, F5): Over the next 12 hours, a coin rises after a falling hour, and the larger that fall times the coin's 24-hour volatility over its 30-day average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
