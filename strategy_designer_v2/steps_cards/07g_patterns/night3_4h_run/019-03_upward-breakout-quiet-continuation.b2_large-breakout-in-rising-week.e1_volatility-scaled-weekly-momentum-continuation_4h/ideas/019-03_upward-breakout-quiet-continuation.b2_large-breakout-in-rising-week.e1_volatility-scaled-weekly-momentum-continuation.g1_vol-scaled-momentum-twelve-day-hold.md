---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days.
Consequence: A trader would hold volatility-scaled weekly momentum positions for about two weeks rather than three days, so the move each position captures is several times the cost of its trades.
Why:
- F1: The vol-scaled 7-day momentum grows larger at longer horizons, enough to cover the cost of a trade. Over 18 bars (3 days) the unusual move is +0.28 % per case (strength 0.030, t 3.3, 5724 cases), which is about 1.5 times the 0.19 % round trip. Over 72 bars (12 days) it is +0.88 to +0.93 % (strength 0.043 to 0.045, t 3.2 to 3.5, 1260 to 1404 cases), about 4.6 times the cost. Over 108 bars (18 days) it is +1.50 % (strength 0.050, t 2.4 to 2.8, 720 cases), about 8 times the cost.
- F2: At the 12-day horizon both ends of the forecast carry the effect. The lowest forecast quintile is followed by -3.05 % excess (t -3.6, 281 cases) and the highest by +3.11 % (t 2.5, 281 cases). On the raw vol-scaled 7-day return the extremes are -1.86 % (t -2.0) and +2.99 % (t 2.5, 252 cases each). The three middle quintiles show no order (-1.9 % to +1.0 %).
- F4: The 3-day momentum fades over time. Its directional strength is 0.083 in 2018 and 0.089 in 2019 (t 1.7 and 2.4, about 678 cases each), but 0.004 to 0.034 in every year from 2020 to 2025 (all t below 0.8). At 12 days it is negative in 2022 (-0.18, t -2.5, 156 cases).
