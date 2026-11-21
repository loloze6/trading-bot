---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more negative a coin's 7-day return, measured in units of its own 4h volatility, the more the coin falls over the next three days.
Consequence: A trader would sell, or refuse to buy, a coin after a week that was weak for its volatility, and expect the fall to carry over the next three days.
Why:
- F3: At the tested 3-day horizon the effect sits mostly in the weakest weeks. The lowest forecast quintile is followed by -0.74 % (t -3.1, 1145 cases). The highest is only +0.35 % (t 1.2), and the fourth +0.43 % (t 1.6).
- F2: At the 12-day horizon both ends of the forecast carry the effect. The lowest forecast quintile is followed by -3.05 % excess (t -3.6, 281 cases) and the highest by +3.11 % (t 2.5, 281 cases). On the raw vol-scaled 7-day return the extremes are -1.86 % (t -2.0) and +2.99 % (t 2.5, 252 cases each). The three middle quintiles show no order (-1.9 % to +1.0 %).
- F8: The book beats holding only in falling years. It earned +0.05 % a day in 2018 while the coins lost 0.35 %, and +0.08 % in 2022 against -0.18 %. In the rising years 2020, 2021 and 2023 to 2025 it lagged the coins by 0.2 to 0.35 % a day. It lost money on XMR (-0.04 % a day while XMR rose 0.11 %).
