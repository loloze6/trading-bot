---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The wider a coin's high-low ranges over the past 5 days compared with its ranges over the past 30 days, the more a fall over its last day reverses into a rise over the next 3 days.
Consequence: A trader leans long after a one-day fall made in an unusually wide-ranging market, and does not read such a fall as a breakout to follow.
Why:
- F1: The brief's premise does not hold on these 4h bars. After the narrowest ranges (5-day mean high-low range over its 30-day mean, lowest quintile) the 3-day move is below the coin's drift (strength -0.053, t -2.5, 1822 non-overlapping cases), while after the widest ranges it is above it (+0.094, t 3.5, excess +0.97 %). After narrow ranges, the direction of the last day does not predict the next 3 days (+0.016, t 0.8).
- F4: After wide-range stretches (top quintile of the 5-day/30-day range ratio), a last-day fall is followed by a rise (strength 0.199, t 5.2, 855 cases) and a last-day rise by nothing (0.000, t 0.0). The larger the last-day move, the more it reverses (signed strength +0.034, -0.116, -0.199 by tercile, t up to -4.4). The reversal is negative in all 8 years.
