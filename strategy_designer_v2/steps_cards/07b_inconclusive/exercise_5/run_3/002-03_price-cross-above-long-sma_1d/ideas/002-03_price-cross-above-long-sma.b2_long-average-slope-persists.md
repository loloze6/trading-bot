---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The steeper a coin's 200-day simple moving average has risen over the past 20 days, the more the coin rises beyond its usual drift over the next 20 days.
Consequence: A trader can size trend longs by the long average's own slope instead of by the price's distance from it.
Why:
- F2: The rising or falling of the 200-day average splits the active bars into two opposite groups: with the average up over the past 20 days the next-20-day excess is +0.026 (t 1.17, n 266), with it down it is −0.037 (t −2.03, n 133); over all bars the excess climbs from −0.020 in the steepest-falling slope quintile to +0.034 and +0.019 in the two rising quintiles (n 134 each).
- F4: Being above the average does not carry the effect, and fresh crosses do not continue: raw-distance quintiles at 20 days are flat (+0.002, +0.004, −0.007, +0.008, +0.006, all |t| < 0.5), and active bars in the first 20 days after a cross average −0.008 (n 95) and 20–60 days −0.020 (n 62), so the plan's "after the cross" situation shows nothing.
- F6: Most of the book's gain is the market's own rise, not timing: the mean daily return is 0.000554, of which the market part is 0.000352 (mean allocation 0.272 × coin mean daily 0.001294), leaving 0.000202 for timing.
