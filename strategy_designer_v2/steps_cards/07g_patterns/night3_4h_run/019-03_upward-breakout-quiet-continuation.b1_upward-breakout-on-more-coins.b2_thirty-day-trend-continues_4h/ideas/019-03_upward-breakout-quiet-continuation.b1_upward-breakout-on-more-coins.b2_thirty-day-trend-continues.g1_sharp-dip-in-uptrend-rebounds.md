---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall compared with its typical 1-day move over the past 5 days, the more the coin rises over the next 3 days, most strongly while its 30-day return is positive.
Consequence: A trader buys sharp one-day dips in coins that have risen over the past month, more the deeper the dip, rather than treating the dip as the end of the trend.
Why:
- F2: The larger a coin's last-day fall measured against its own 5-day volatility, the more it rises over the next 3 days. The largest-fall decile ends +1.18 % above drift (strength 0.125, t 4.5, 1156 cases), the next decile +0.42 % (0.054, t 2.0), and the middle deciles end slightly below drift. The rebound is about 5 times a round trip's 0.22 %.
- F3: This rebound after a large fall is concentrated where the 30-day forecast is on: 0.161 (t 5.0, 932 cases) against 0.041 (t 1.7, 1379 cases) when it is off. It is positive in 6 of 8 years, but negative in 2018 (-0.203, t -2.1) and flat in 2022 (-0.035).
- F6: The tested forecast works only from mid values up. Cases at 0 to 5 end below drift (-0.056, t -2.3, 1578 cases), and cases from 5 to 20 end above it (+0.067 to +0.101, t 2.3 to 3.4). Coins whose 30-day return is in the second-lowest quintile do worst (-0.117, t -5.7).
