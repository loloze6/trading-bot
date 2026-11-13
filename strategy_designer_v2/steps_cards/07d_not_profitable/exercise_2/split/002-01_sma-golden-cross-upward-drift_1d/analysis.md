---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.3554 USD
---
## Findings
- **F1:** The forecast's size does not grade the coin's next-day return: the coin's mean next return rises only from 0.000942 (forecast 0–5, t 0.90) to 0.001549 (forecast 15–20, t 1.37), and across quintiles of the raw 50/200 spread it is highest in the lowest quintile (0.002726) and only 0.001443 in the highest. This matches the verdict's slope t of 0.37 and its share-positive gap of −0.021.
- **F2:** The book trails holding because it sits flat on 41% of bars (share invested 0.585) while the coin still earns 0.000894 per bar there. On flat bars after a 20-day rise the coin earns 0.001363 (2778 bars). The result is a mean book return of 0.000817 per bar against 0.001287 for the coin, and a mean window return of 18.5% against 23.1%. The book beats the coin in only 41% of coin-windows.
- **F3:** Fees are not the cause. Fee drag is 0.000022 per bar, and the mean trade gains 0.87% before fees against 0.30% commission. The gross gain is concentrated in a few long holds: only 31% of the 1091 trades (all LONG, median 34 days) win before fees.
- **F4:** The trade-length split decides the book. The 632 trades lasting at most 40 days lose −8.6% to −12.0% each before fees, summing to −6461% net. The 456 trades held over 40 days gain +16.1% each, summing to +7297% net.
- **F5:** Trades opened at a high forecast lose and those opened at a low one win. The 774 trades entered with forecast 10–20 average −1.42% gross with a 30.6% win rate. The 150 trades entered at forecast 2–5 average +9.15% gross and are held longer (56.7 against 38.6 days).
- **F6:** Within a long position, bars 10–30 of the run lose: coin mean −0.00075 and book −0.00102 over 2088 bars, a book sum of −2.13. Bars 30–60 earn coin 0.002326 (t 2.49) and bars 60–120 earn coin 0.002046 (t 2.66), book sums +5.42 and +9.15.
- **F7:** All of the invested profit comes when the coin has risen over the prior 20 days. Those 4342 invested bars earn a book mean of 0.003263, a sum of +14.17. The 5622 invested bars after a 20-day fall earn −0.000046, a sum of −0.26.
- **F8:** The losses cluster in falling-market years. The book summed −1.92 in 2018 and −1.08 in 2022 while invested 25% and 36% of bars, with the coin returning −0.0020 and −0.0022 per invested bar. In 2021 it earned +7.65 while invested 83% of bars.
- **F9:** Invested bars in the calmest third of volatility earn the coin only 0.000469, against 0.002037 in the most volatile third (book sums +2.91 against +6.03).
- **F10:** The poor Calmar of 0.00098 comes from deep per-window drawdowns. The mean book drawdown is −28.7% (coin −39.0%), but the worst book drawdown reaches −96.1% against the coin's worst of −77.0%. Windows w13 and w18 have mean book drawdowns of −75.6% and −71.1%.

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_trend-pays-after-it-ages` (from F4, F6, F5, F1): While the 50-day average is above the 200-day average, the coin's forward drift is concentrated in the late part of the run: returns over bars 30 to 120 after the up-cross are higher than returns over bars 10 to 30.
- `002-01_sma-golden-cross-upward-drift.d2_recent-rise-carries-forward` (from F7, F2): When the coin has risen over the prior 20 days, its forward return is higher than its average return, whether or not the 50-day average is above the 200-day average.
- `002-01_sma-golden-cross-upward-drift.d3_wide-spread-signals-exhaustion` (from F1, F5): When the 50-day average is wide above the 200-day average, the coin's forward return is lower than when the spread is narrow, so a stretched spread marks a mature, exhausting move.
- `002-01_sma-golden-cross-upward-drift.d4_trend-drift-needs-volatility` (from F9, F8): While the 50-day average is above the 200-day average and the coin's recent volatility is in its upper range, the coin's forward return is higher than when volatility is in its calm range.
- `002-01_sma-golden-cross-upward-drift.d5_pullback-inside-uptrend-loses` (from F7, F8, F10): While the 50-day average is above the 200-day average but the coin has fallen over the prior 20 days, the coin's forward return falls below its average return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
