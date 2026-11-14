---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4366 USD
---
## Findings
- **F1:** Calmar fails because of one long fall: the pooled book's deepest drop is -43.0% (Calmar 0.3855 against a required 0.75). It runs 208 days from its peak in w15 to its trough in w17, and every coin lost in it (summed book returns from -0.42 for XRP to -0.70 for ETH). BTC and XMR lost even though their own coins rose over the same days (+0.025 and +0.169), so the book was positioned badly, not merely carried down by the market.
- **F2:** The losing long bars are those where the forecast has been shrinking. The 20-bar change in the forecast was 0 or negative on 3,003 long bars, and these earned -0.00003 per bar (Sharpe -0.02, worst 1% -0.0825). Long bars where it had risen earned 0.00255 to 0.00398 per bar (Sharpe 1.96 and 1.55).
- **F3:** Inside the fall windows w16–w18 the same split holds. Long bars after a falling forecast (n=488) lost -0.0003 per bar, while those after a rising forecast (n=558) gained +0.0047 per bar, summing to +2.61.
- **F4:** Keeping the position only while the forecast is rising nearly halves the fall and reaches the required Calmar before fees (all of this is a what-if on the same bars). Over 20 bars, the deepest fall drops from -42.7% to -19.7%, Calmar rises from 0.42 to 0.80 and Sharpe from 0.71 to 0.89, with 36% of long bars kept. Over 5 bars, the fall is -13.1%, Calmar 1.00 and Sharpe 0.89.
- **F5:** The coin's own fading move gives the same picture. Long bars with the 20-bar price change below -9.7% earned -0.00022 per bar (Sharpe -0.36), and with the 60-bar change below -9.8%, -0.00023 per bar (Sharpe -1.27). Bars whose distance above the SMA had shrunk by more than 17 points over 20 bars earned 0.00003 per bar (Sharpe 0.04), against 0.00350 per bar where it had grown by more than 21 points.
- **F6:** Size makes the falls worse: the worst 5% of long-bar losses came at a mean allocation of 1.00 against 0.51 on all long bars. Part of this is late in a trend: when the 60-bar price change was above +49.5%, Sharpe fell to 0.56, from 1.48–1.63 for changes between +11% and +49.5%.

## Ideas
- `002-03_price-cross-above-long-sma.d1_rising-distance-above-average` (from F1, F2, F3, F4, F5): While a coin's close sits above its long simple moving average, it keeps drifting upward with the size of its distance above the average, only while that distance is widening; when the distance has been narrowing over the recent bars, the coin above its average no longer outperforms holding it.
- `002-03_price-cross-above-long-sma.d2_above-average-with-recent-momentum` (from F2, F5, F6): While a coin's close sits above its long simple moving average, it keeps drifting upward with the size of its distance above the average, only while its own price over the recent weeks has been rising; the stronger that recent rise, the larger the drift that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
