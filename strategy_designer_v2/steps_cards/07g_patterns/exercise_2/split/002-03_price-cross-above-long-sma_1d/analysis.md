---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.4217 USD
---
## Findings
- **F1:** When the close was above the 200-day SMA, a daily up-move larger than 2 standard deviations was followed by a mean 5-bar return of +3.39% (t=3.81, n=323, overlapping windows). Below the SMA the same move was followed by only +0.78% (t=1.21, n=218), and ordinary days above the SMA by +0.98%. Across all bars, 20-bar returns rose from +2.8% after |z|<1 days to +8.3% after z of 2–3 (n=368) and +11.3% after z>3 (n=193).
- **F2:** Saturday-stamped daily returns averaged +0.44% (t=5.41, n=2433) and Friday +0.32% (t=3.41), while Tuesday (-0.09%) and Thursday (-0.18%) were negative. The Saturday mean was positive in all six coins (t from 1.40 to 2.92) and in 7 of 8 years, with t above 1.9 in 2019, 2020, 2021, 2024 and 2025. It was near zero only in 2018, 2022 and 2023.
- **F3:** The book's 2228 long trades won only 29.4% of the time (median net -3.7%) and made money only by holding long. Trades lasting 2 days or less lost 6.4% on average with a 1.7% win rate (n=415), and trades of 2–5 days lost 6.5% (n=365) and 5–15 days lost 4.6% (n=533). Trades of 40–100 days made +33.5% (n=300) and trades over 100 days +85.8% (n=71), and the ten best trades supplied 28% of all gross gains.
- **F4:** The upward cross itself carried no edge. Bars where the forecast went from 0 to positive were followed by +0.05% over 5 bars (t=0.09, n=272) and +2.47% over 20 bars, below the +2.82% non-overlapping 20-bar mean of all bars.
- **F5:** Forward 20-bar returns rose with the forecast level, but only at the top. On non-overlapping samples they were -0.36% for forecast 0–5 (t=-0.20, n=111), +1.6% for 5–10, +2.7% for 10–15 and +8.1% for 15–20 (t=1.69, n=113). Flat bars (forecast 0) earned +2.57% (t=2.42, n=412), so being just above the SMA did worse than being below it.
- **F6:** Bars more than 60% above the SMA had a 20-bar return of only +1.3% with a 36.6% hit rate and 6.4% daily volatility, against +5.6% for bars 30–60% above. The book's 1% largest daily losses (mean -22.5%) and gains (mean +27.7%) occurred at average distances of 82% and 141% above the SMA, with 20-day volatility of 0.080 against 0.044 for the average held bar. The large losses followed a -5.7% 5-day move, and the large gains followed a +28% 5-day move.
- **F7:** The filter failed in both bear years and in the bull years. In 2018 active bars had a 20-bar return of -17.0% against -7.0% for flat bars, and in 2022 -9.2% against -0.9%. In 2020 and 2021 flat (below-SMA) bars returned +16.0% and +12.4% over 20 bars, against +6.4% and +4.8% for active bars. Bars more than 15% below the SMA returned +2.8% on non-overlapping 20-bar samples (t=2.07, n=241).
- **F8:** Past 20-day return sorted the next returns more cleanly than the SMA distance did. From the lowest to the highest past-20-day quintile, the forward 20-bar return rose monotonically from +1.3% to +5.3%, and the next-day return from +0.11% to +0.32% (overlapping, pooled across coins).
- **F9:** Higher 20-day volatility came with higher next-day returns: they rose monotonically from +0.01% in the lowest volatility quintile to +0.29% in the highest. Forward 20-bar returns ran the other way, highest in the calmest quintile at +5.9%, against +1.6% to +3.6% in the others.

## Ideas
- `002-03_price-cross-above-long-sma.g1_big-up-day-above-trend` (from F1): When a coin's close sits above its 200-day SMA and the day's return is an up-move larger than 2 standard deviations of its recent daily returns, the coin keeps rising over the next 5 bars, further than after ordinary days above the SMA.
- `002-03_price-cross-above-long-sma.g2_weekend-daily-drift-up` (from F2): A coin's daily bar stamped Saturday rises more than its average day, and the Friday bar does too.
- `002-03_price-cross-above-long-sma.g3_twenty-day-momentum-persists` (from F8, F1): When a coin's past 20-day return is in the top part of its range, the coin's next 20 bars rise further than when its past 20-day return is low.
- `002-03_price-cross-above-long-sma.g4_overextension-above-trend-stalls` (from F6, F5): When a coin's close is very far above its 200-day SMA, more than 60%, and its 20-day volatility is high, the coin's next 20 bars rise less than when it sits moderately above the SMA, by 30 to 60%.
- `002-03_price-cross-above-long-sma.g5_calm-periods-drift-higher` (from F9): When a coin's 20-day volatility is in its lowest range, the coin rises further over the next 20 bars than when its volatility is higher.
- `002-03_price-cross-above-long-sma.g6_deep-discount-rebounds` (from F7, F5): When a coin's close is more than 15% below its 200-day SMA, the coin rises over the following 20 bars.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
