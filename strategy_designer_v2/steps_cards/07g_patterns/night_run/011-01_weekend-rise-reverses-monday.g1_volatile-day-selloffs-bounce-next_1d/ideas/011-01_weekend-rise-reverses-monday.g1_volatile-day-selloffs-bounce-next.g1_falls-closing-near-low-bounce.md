---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin falls on a day by a large amount in units of its usual 60-day daily move, it rises over the next 1 day, and the closer that day's close sits to the day's low as a share of the day's high-low range, the larger the rise.
Consequence: A trader can lean long after a sharp fall that closed near the low, and refuse the bounce trade when the fall closed near the day's high.
Why:
- F1: Among large one-day falls (more than 1 usual 60-day move), the next-day bounce comes only from closes in the lower part of the day's range. Falls closing in the lowest close-location tercile earned +0.0066 next-day excess (t=3.60, n=863), while the four closing high in the range lost −0.067. In a regression on falls, close location (0 = at the low, 1 = at the high) has beta −0.030 (t=−2.59), alongside the fall's size (t=−3.66) and relative volatility (t=2.06).
- F2: The close-location split holds on the strategy's own active bars and in both halves of the windows. On bars with forecast ≥5, the bottom and middle close-location terciles earned +0.0091 (t=3.35) and +0.0098 (t=3.91), and the top tercile −0.0013 (t=−0.48), each with about 390 bars. Among falls, the top tercile was negative in both w1–12 (−0.0039) and w13–24 (−0.0011), while the bottom tercile was positive in both (+0.0121, t=3.13; +0.0080, t=1.85).
- F3: The near-low bounce shows in five of six coins. Next-day excess was +0.0062 for BTC, +0.0118 for ETH, +0.0077 for LTC, +0.0118 for XMR and +0.0180 for XRP (t between 1.6 and 2.8), and only +0.0029 for ZEC (t=0.57).
- F4: Across all days, closes in the coin's lowest close-location quintile were followed by +0.0045 next-day excess (t=3.86, n=1751), but the effect is not monotonic. The middle quintile gave −0.0035 (t=−2.89), and among days without a large move the low-close tercile gave only +0.0005 (t=0.56). So the pattern belongs to falls, not to closes near the low on their own.
