---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its 20-day volatility, and the heavier that day's volume relative to its 20-day average, the more the coin rises over the next 1 day.
Consequence: A sharp fall on heavy volume is a reason to buy for a next-day rebound and to refuse a short into it.
Why:
- F3: A large down day on heavy volume reverses more the next day than a large down day on normal volume. Down moves are measured against 20-day volatility. In a regression of next-day excess return on the down move, log volume ratio and their product, the product's coefficient is -0.0022 at t -3.61 (n 14500). In the lowest down-move quintile, heavy days are followed by +0.98 % against +0.32 % on normal-volume days. All days in that quintile give +0.42 % at t 4.37 (n 3007).
- F5: The heavy-volume low-close effect is a one-day effect. On a non-overlapping 3-day grid its slope falls to 2.67 % at t 1.54 (n 447), and 2.71 % at t 1.21 once the day's return is controlled. For down moves in general, the 2-day reversal holds at t -2.85 (n 7498) and the 3-day at t -1.94 (n 4859).
