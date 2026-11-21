---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's return over its last 24 hours, the more the coin moves the opposite way over the next day: the deeper its 24-hour fall, the more it rises over the next 24 hours, and the larger its 24-hour rise, the more it falls.
Consequence: A trader should lean against a coin's last day, buying after a sharp daily fall and refusing to chase a sharp daily rise, with a bet that grows with the size of that day's move.
Why:
- F1: The past day's return reverses over the next day, and this is the strongest pattern in the record. On the daily grid of non-overlapping 24-hour cells, one standard deviation of the coin's 24-hour return is followed by -45 bps of excess return over the next 24 hours (t -11.3, 15950 cases). It holds on every coin (t -3.5 to -6.6) and in both halves of the windows (t -6.1 and -9.3). It holds in 6 of 8 years with t below -2.
- F2: The reversal is large enough to cover a trade. After the 20 % largest 24-hour falls (mean size 620 bps), the next day's excess return is +48 bps (t 4.5, 3191 cases). After the 20 % largest 24-hour rises (mean 662 bps) it is -33 bps (t -3.3, 3191 cases). Both are larger than this backtest's round-trip cost of 19 bps, while the middle quintiles show -14 to +1 bps.
- F3: How the day's move was made adds nothing to its reversal, contrary to the brief's jump mechanism. Adding the largest hour's share of the day's absolute moves leaves the 24-hour reversal at -44 bps (t -10.6). That share scores t -1.5 and its interaction with the 24-hour return scores t -1.1.
