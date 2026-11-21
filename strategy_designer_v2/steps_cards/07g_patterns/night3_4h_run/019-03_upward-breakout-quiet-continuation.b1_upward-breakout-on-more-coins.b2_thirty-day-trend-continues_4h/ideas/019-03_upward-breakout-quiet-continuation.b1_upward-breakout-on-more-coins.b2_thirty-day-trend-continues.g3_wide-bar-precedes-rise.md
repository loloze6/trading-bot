---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The wider a coin's last four-hour high-low range compared with its average four-hour range over the past 5 days, the more the coin rises over the next 3 days.
Consequence: A trader adds to longs after an unusually wide four-hour bar and trims them after an unusually narrow one.
Why:
- F1: The brief's premise does not hold on these 4h bars. After the narrowest ranges (5-day mean high-low range over its 30-day mean, lowest quintile) the 3-day move is below the coin's drift (strength -0.053, t -2.5, 1822 non-overlapping cases), while after the widest ranges it is above it (+0.094, t 3.5, excess +0.97 %). After narrow ranges, the direction of the last day does not predict the next 3 days (+0.016, t 0.8).
- F5: The width of the last 4-hour bar's range against its 5-day average adds to the 30-day forecast in a joint regression of the 3-day excess return: log range ratio t 5.0, forecast t 4.9, 5-day range compression t 1.3. The widest last-bar quintile ends +0.83 % above drift (t 3.1) and the narrowest -0.67 % (t -3.6).
