---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall, the larger its rise over the next 1 day.
Consequence: A trader would buy a coin after a sharp daily drop, sized with the depth of that drop, for a one-day rebound.
Why:
- F3: After a coin's largest 1-day falls (lowest quintile of the prior day's return), the next day's mean return is +0.0060 (t=6.09, n=3448). In the other four quintiles it stays between −0.0011 and +0.0007, all |t|<1.2.
