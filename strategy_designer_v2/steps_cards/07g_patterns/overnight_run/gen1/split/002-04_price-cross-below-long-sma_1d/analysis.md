---
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.4022 USD
---
## Findings
- **F1:** The deepest short zone does not continue falling, it rebounds. Bars with forecast ≤ -15 are followed by a mean 10-bar coin return of +3.57% (t 7.73, 59.5% up) and a next-day return of +0.45% (t 3.24). That is more than the +1.58% after flat bars (forecast 0, t 7.72), and the short book is positioned against this rebound.
- **F2:** Below the SMA200, a 30-day crash leads to a rebound. Bars whose past-30-day return is ≤ -30% are followed by +2.87% over 10 bars (t 4.48, 58% up), against +0.22% to +1.20% for the milder below-SMA buckets.
- **F3:** Short-term momentum carries forward on both sides of the SMA. Bars in the top quintile of past-10-day return (> +10.4%) are followed by +3.86% over 10 bars (t 10.49), against +0.26% to +0.47% for the bottom three quintiles. Within the top quintile, the forward return is +4.35% (t 8.94) above the SMA and still +2.73% (t 5.81, 57.8% up) below it.
- **F4:** Above the SMA200, a pullback leads to further falls. Bars with a past-30-day return between -30% and -15% are followed by -3.94% over 10 bars (t -4.40, 38.7% up). This is the only clearly negative forward pocket found, and it lies where the book is flat.
- **F5:** The actual price crosses carry no edge. After the 257 crosses below the SMA200, the 10-bar return is +1.20% (t 1.39) and the 20-bar return +1.09% (t 0.83). After the 327 crosses above, the 10-bar return is +1.38% (t 1.57). The unconditional 10-bar mean is +1.35%.
- **F6:** Short trades split sharply by holding time. The 1,764 trades closed within 20 days lose about the same price amount whatever their length: -6.5%, -6.2%, -6.2% and -6.4% gross, with win rates of 1% to 22%. The 707 trades held beyond 20 days gain +2.05% gross (53% wins). Fees are small, about 0.1 to 0.3 points per trade.
- **F7:** Shallow-entry short trades are not better. Trades entered at forecast ≤ -15 average -5.24% net, against -2.89% to -4.66% for shallower entries, with a median of about -4.4% in every entry bucket.
- **F8:** The book's worst days follow sharp upside reversals while it is deeply short. On its 171 worst days (mean book return -19.3%), the coin rose +12.7% that day, with mean allocation -1.31 and SMA distance -32%. Its 171 best days came on -11.1% coin days after a -21.7% 10-day slide, at distance -46%.
- **F9:** Large down days are followed by up days. Daily moves below -1.5 sigma (20-day volatility) are followed by next-day returns of +0.43% (t 2.14, 61% up) and +0.89% (t 1.69, 61% up). Moves above +2.5 sigma are followed by a next day with only 41% up days, while their 10-bar return is still +5.39% (t 2.98).
- **F10:** Thursday and Friday are the strongest weekdays. Next-day mean returns on those two days are +0.34% (t 3.66) and +0.43% (t 5.24). Monday is -0.09% and Wednesday -0.18%. The Thursday-Friday premium holds in both 2018-2021 and 2022-2025 and in all six coins, for example LTC +0.61% vs -0.15% on other days.
- **F11:** The book's losses concentrate in high volatility. Mean daily book return is -0.22% (t -3.17) in each coin's top 20-day-volatility tercile, against +0.04% (t 1.41) in the low tercile. Next-day coin returns are highest in that same tercile, +0.26% (t 3.08).
- **F12:** The book loses in most years, and 2018 is the only one positive on average. Mean daily book return is +0.16% in 2018, -0.31% in 2020 (t -4.30) and -0.10% in 2021 (t -3.65). In 2020 and 2021 the coin's next-day return while the book was short was +0.72% (t 3.86) and +0.68% (t 3.39), higher than while flat.

## Ideas
- `002-04_price-cross-below-long-sma.g1_deep-below-average-rebound` (from F1, F7, F8): When a coin's close sits far below its 200-day average (forecast at or below -15), the coin tends to rise over the next 10 bars, more than after bars at or above the average.
- `002-04_price-cross-below-long-sma.g2_crash-below-average-rebounds` (from F2, F1): When a coin below its 200-day average has fallen 30% or more over the past 30 days, it tends to rise over the next 10 bars.
- `002-04_price-cross-below-long-sma.g3_strong-10-day-rise-continues` (from F3, F8, F12): When a coin's past-10-day return is in its top fifth (above about +10%), it tends to keep rising over the next 10 bars, both above and below its 200-day average.
- `002-04_price-cross-below-long-sma.g4_pullback-above-average-continues` (from F4): When a coin's close is above its 200-day average and its past-30-day return is between -30% and -15%, it tends to keep falling over the next 10 bars.
- `002-04_price-cross-below-long-sma.g5_large-down-day-bounces` (from F9, F8): After a daily drop larger than 1.5 times the coin's 20-day daily volatility, the next day tends to close up.
- `002-04_price-cross-below-long-sma.g6_thursday-friday-upward-drift` (from F10): A coin's return from Thursday's close and from Friday's close to the next close tends to be positive and larger than on other weekdays.
- `002-04_price-cross-below-long-sma.g7_high-volatility-upward-drift` (from F11, F12): When a coin's 20-day volatility is in the top third of its own range, its next-day return tends to be positive and higher than in calmer periods.
- `002-04_price-cross-below-long-sma.g8_short-held-shorts-reverse` (from F6, F5): A short opened when the close drops below the 200-day average and closed within 20 days tends to lose, because the coin rises back over the following days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
