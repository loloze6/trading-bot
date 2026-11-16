---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days. Measured against the coin's own 20-day volatility, the rise is larger the calmer the coin's past 20 days have been.
Consequence: A trader would favour these longs when the coin is calm and size down in turbulent rises, which should shrink the falls that sink the Calmar.
Why:
- F5: Relative to the coin's own volatility, the follow-through is strongest in calm markets. In the lowest 20-day volatility quintile (2.05 % daily) the next-day return is 0.0019, about 0.093 of a day's volatility, and the gain is 0.00325. In the highest quintile (8.5 % daily) it is 0.0041, about 0.048 of a day's volatility, and the gain is only 0.0011.
- F3: The deepest fall is -25.4 %, running from w4 to w10 over 782 days. In those windows the active bars earned 0.00088 against 0.00217 elsewhere, and the next-day return was 0.00076 against 0.00303, while allocation was higher (0.73 against 0.54). Middle-tercile forecasts in those windows lost money: next-day return -0.00051, gain -0.00015, from 494 bars.
