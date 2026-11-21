---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's fall over the past 24 hours, made while its 24-hour volatility is high against its 30-day average, is followed by a rise over the next 24 hours. The larger the fall against the coin's usual 24-hour move, the larger the rise.
Consequence: A slower one-day capitulation signal gives fewer, larger rebounds per trade, well above a round trip's cost.
Why:
- F7: A 24-hour fall in high volatility carries the same graded rebound over the next 24 hours. It is +74 bps (t 4.0, n 994) for 1 to 2 usual 24-hour moves, +124 bps (t 4.0) for 2 to 3 and +308 bps (t 3.5) beyond.
- F4: The reversal is graded by the size of the 2-hour fall, and only the larger falls clear the 19 bps cost. On the 8-hour grid, in high volatility, the unusual move counted in both directions is 3.5 bps for |z| up to 1 (n 11,421) and 17 bps for 1 to 2 (n 4,477). It rises to 32, 50, 53 and 68 bps for 2–3, 3–4, 4–6 and above 6. After falls alone, over 24 hours, it is 7, 36, 87, 222 and 541 bps (t 3.5 in the top bin).
- F6: The book's trading is mostly in cases too small to pay. Its position earns 0.12 bps per bar before costs, against about 0.46 bps of estimated turnover cost. Bars with |forecast| between 0.5 and 10 lose -0.31 to -0.52 bps each.
