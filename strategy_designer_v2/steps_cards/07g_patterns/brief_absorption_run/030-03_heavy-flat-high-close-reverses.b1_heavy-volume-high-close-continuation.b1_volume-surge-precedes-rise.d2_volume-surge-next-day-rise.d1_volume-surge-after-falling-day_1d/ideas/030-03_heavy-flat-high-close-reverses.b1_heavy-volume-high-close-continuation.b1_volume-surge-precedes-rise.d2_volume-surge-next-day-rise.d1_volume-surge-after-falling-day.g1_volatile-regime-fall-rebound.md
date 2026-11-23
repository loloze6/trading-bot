---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, measured in its usual daily moves, the more it rises over the next day. The rebound grows with how high its 20-day volatility stands against its own level over the past 120 days, and it is largest when recent volatility is most elevated.
Consequence: A trader buys a coin's sharp daily fall when its recent volatility is elevated against its own norm, sizing larger the higher that ratio, and refuses the same fall in calm periods.
Why:
- F1: The rebound after a down day depends on how volatile the coin has been, not on its volume. In a regression of the next day's return (in usual daily moves) the term "fall × log(20-day volatility over its 120-day median)" has beta -0.278 with t -7.75. On days falling more than one usual move (z < -1), the next-day excess return by volatility tercile is +0.01 % (t -0.05, n 542), +0.61 % (t 2.23, n 366) and +1.48 % (t 4.05, n 302).
- F2: The high-volatility rebound after large falls holds up in every subset. It is positive in every year 2018–2025 (for example 2018 +2.23 % t 2.78; 2023 +1.90 % t 4.77; 2024 +0.73 % t 1.18). It is also positive in every coin, from +1.27 % for LTC to +1.88 % for ZEC, with BTC at t 2.53 and ZEC at t 2.14.
- F3: Once the fall's size, its interaction with volatility and the 5-day return are in the same regression, volume adds nothing. The tested interaction "fall × log volume ratio" has t -1.12, and log volume ratio alone has t 0.74. The volume-ratio quintile effect (top quintile +0.33 %, t 3.08) therefore looks like a stand-in for the size of the fall and for volatility.
- F6: The book's worst 2 % of days (n 348) coincide with coin falls averaging -8.35 %, and its best 2 % with coin rises of +8.91 %. Its tails are the coin's own large moves while it is held long. This fits F1: long positions taken after falls in calm periods carry losses without the rebound.
