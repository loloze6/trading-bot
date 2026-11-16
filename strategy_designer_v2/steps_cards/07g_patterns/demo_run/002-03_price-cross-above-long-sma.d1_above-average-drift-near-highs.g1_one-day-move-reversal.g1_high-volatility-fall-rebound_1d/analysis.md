---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3667 USD
---
## Findings
- **F1:** The next-day reversal of a coin's one-day move, measured in its usual 20-day moves, grows steadily with its 20-day volatility rank against its past 100 days: the z × volatility-percentile interaction is -0.0083 (t -4.47, n 11188 bars), against a z slope alone of only +0.0009 (t 1.19). It holds in w1-12 (t -3.52, n 5590) and in w13-24 (t -3.15, n 5598), and in four of six coins (BTC t -3.37, ETH t -3.99, XMR t -2.51, LTC t -1.90); XRP (t 0.32) and ZEC (t -1.19) do not show it.
- **F2:** The reversal grows with each volatility level: the slope of next-day excess return on z is -0.0005 (t -0.93, n 4916) at low rank, -0.0021 (t -2.74, n 3726) at rank 0.3-0.6, -0.0050 (t -3.95, n 2251) at rank 0.6-0.8, and -0.0087 (t -2.56, n 295) at rank 0.8 and above.
- **F3:** The rebound is carried by falls, not by rises: at rank 0.6-0.8 the next-day excess return rises with the size of a fall (slope on |z| 0.0159, t 5.42, n 1089), while rises show no reversal (slope 0.0033, t 1.41, n 1162). Below a rank of 0.6 neither side shows anything (|t| ≤ 1.12).
- **F4:** Most of that graded rebound sits below the tested regime's 0.8 cut: at rank 0.6-0.8, falls of 1 to 2 usual moves are followed by +0.0080 excess (t 1.86, n 183), and falls of more than 2 usual moves by +0.0512 (t 2.58, n 29). Above rank 0.8 there are only 142 falls in my recomputed percentile, with a slope of t 0.78.
- **F5:** The book's gain rests on a few days: its daily return has a skew of 5.67, the top 1% of days carry 159% of its total gain and the top 5% carry 292%, and the book is active on only about 20% of coin-days. This fits a rule that is switched on only in rare high-volatility stretches.
- **F6:** Next-day excess return differs by weekday, but the pattern is not stable over time. After Thursdays and Fridays it is +0.0025 (t 2.63) and +0.0030 (t 3.76), and after Mondays and Wednesdays it is -0.0024 (t -2.53) and -0.0030 (t -2.70). The Thursday-plus-Friday premium comes mostly from 2018-2019 (t 3.37 and 5.82) and fades after 2020 (2021 -0.0002, 2022 +0.0000). It is not graded, so I propose no idea from it.
- **F7:** Twenty-day momentum does not rank the next five days' excess return in order (quintiles -0.0027, -0.0107, -0.0002, +0.0098, +0.0039, about 570 independent cases each), so I treat it as chance.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound.g1_volatility-graded-fall-rebound` (from F1, F2, F3, F4, F5): The larger a coin's one-day fall measured in its usual daily moves of the past 20 days, the larger its rise over the next day, and this rebound grows steadily with the coin's 20-day volatility rank against its past 100 days, already well below the most turbulent stretches.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
