---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
idea tested: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5160 USD
---
## Findings
- **F1:** Among large one-day falls (more than 1 usual 60-day move), the next-day bounce comes only from closes in the lower part of the day's range. Falls closing in the lowest close-location tercile earned +0.0066 next-day excess (t=3.60, n=863), while the four closing high in the range lost −0.067. In a regression on falls, close location (0 = at the low, 1 = at the high) has beta −0.030 (t=−2.59), alongside the fall's size (t=−3.66) and relative volatility (t=2.06).
- **F2:** The close-location split holds on the strategy's own active bars and in both halves of the windows. On bars with forecast ≥5, the bottom and middle close-location terciles earned +0.0091 (t=3.35) and +0.0098 (t=3.91), and the top tercile −0.0013 (t=−0.48), each with about 390 bars. Among falls, the top tercile was negative in both w1–12 (−0.0039) and w13–24 (−0.0011), while the bottom tercile was positive in both (+0.0121, t=3.13; +0.0080, t=1.85).
- **F3:** The near-low bounce shows in five of six coins. Next-day excess was +0.0062 for BTC, +0.0118 for ETH, +0.0077 for LTC, +0.0118 for XMR and +0.0180 for XRP (t between 1.6 and 2.8), and only +0.0029 for ZEC (t=0.57).
- **F4:** Across all days, closes in the coin's lowest close-location quintile were followed by +0.0045 next-day excess (t=3.86, n=1751), but the effect is not monotonic. The middle quintile gave −0.0035 (t=−2.89), and among days without a large move the low-close tercile gave only +0.0005 (t=0.56). So the pattern belongs to falls, not to closes near the low on their own.
- **F5:** The bounce after falls grows with the coin's volatility, from +0.0009 (t=0.35) in the lowest 60-day-volatility tercile to +0.0127 (t=3.06) in the highest. It is fading by year: +0.0227 (t=3.10) in 2020, −0.0004 in 2024 and −0.0023 in 2025.
- **F6:** Large rises are not reversed. Next-day excess after a rise of more than 1 usual move is near zero in every volatility tercile (|t| ≤ 1.7) and every volume tercile (|t| ≤ 0.7), so the effect runs one way.
- **F7:** The book's result rests on its extreme days, which ride the coins. The top 1% of book days (29 days, +0.060 mean, coins +0.089) sum to 132% of the book's total, and the bottom 1% (29 days, −0.068, coins −0.097) to −150%.
- **F8:** High volume on a fall day does not add to the bounce once the fall's size is known. Volume looked strong at first: the high-volume tercile of falls earned +0.0121 (t=3.27) against +0.0028 for the low tercile. But in a regression the log volume ratio has t=1.02 next to the fall's size (t=−2.78). Other angles stood out but rest on few cases among many cuts: Saturday falls gave +0.0175 (t=3.68, n=63), and falls beyond 2.5 usual moves gave +0.034 over the next 3 days (t=2.55, n=37).

## Ideas
- `011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.g1_falls-closing-near-low-bounce` (from F1, F2, F3, F4): When a coin falls on a day by a large amount in units of its usual 60-day daily move, it rises over the next 1 day, and the closer that day's close sits to the day's low as a share of the day's high-low range, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
