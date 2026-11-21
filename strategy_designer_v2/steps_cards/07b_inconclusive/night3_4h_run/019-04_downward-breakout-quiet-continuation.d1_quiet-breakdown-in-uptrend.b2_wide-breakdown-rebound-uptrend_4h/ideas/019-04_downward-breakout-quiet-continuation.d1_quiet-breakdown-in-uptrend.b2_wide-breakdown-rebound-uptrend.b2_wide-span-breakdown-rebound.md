---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
line: 7.b inconclusive
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The rise is larger the more of the coin's 30-day average four-hour ranges that two-day stretch spans.
Consequence: In a coin that has risen over the past month, buy a break below a two-day range that spans many average four-hour ranges, and refuse the short most firmly when that span is largest.
Why:
- F2: The rise is all in the widest broken stretches, measured as the prior two-day span counted in average 4h bar ranges, with no standardisation. The three narrowest fifths (spans of 1.0 to 3.0 bar ranges) each lose -0.32 % to -0.52 % over 3 days, with t from -0.58 to -0.94 on about 184 cases each. The two widest fifths (3.0 to 14 bar ranges) gain +1.44 % (t 2.60, 184 cases) and +2.23 % (t 2.99, 185 cases).
- F3: The test's forecast sees this ordering less sharply than the plain width does. Its Spearman with the excess return is 0.078, against 0.127 for the plain width count, and its standardisation against its own past 180 values mixes narrow and wide stretches across its quartiles.
- F4: The forecast's top quartile (forecast 8.8 to 20) gains +1.42 % over 3 days (t 2.66, 300 cases), a strength of 0.158. That is about 7 times the 0.19 % cost of a trade. The rise keeps growing to +1.84 % at 6 days (t 2.32, 287 cases).
- F7: As tested, the idea barely pays for itself. Its total move of +0.64 % per case is 3.3 times the cost of a buy and a sell, but its unusual move of +0.24 % is only 1.2 times that cost. Cases in the widest stretches carry an unusual move of +1.4 % to +2.2 %, many times the cost.
