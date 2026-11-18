---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3402 USD
---
## Findings
- **F1:** The book's gain is too thin to match holding the coins, which is why it fails on gain against holding and on mean daily return. It is in a position on only 27.6 % of bars, with a mean position of 0.40 when in. Its mean daily return is 0.000436 on BTC and 0.000322 on ETH, against 0.001183 and 0.001368 for holding. Of its mean bar gain of 0.000522, only 0.000141 comes from the market's own rise.
- **F2:** The rebound after a fall exists only in the most volatile stretches, and there it is graded by fall size. In the top third of the 20-day/100-day volatility ratio, falls of 1–1.5, 1.5–2.5 and over 2.5 usual moves are followed by next-day returns of 0.60 %, 0.99 % and 2.18 % (t 2.29, n 57). In the bottom and middle thirds the same falls give −0.15 %/0.69 %/−0.70 % and −0.17 %/0.10 %/0.12 %, with no grading.
- **F3:** The book's fresh signals pay only at the top of the volatility ratio. By ratio quartile, their next-day position gain is −0.0032 at 0.81–1.10, −0.0006 at 1.10–1.23, 0.0031 at 1.23–1.49 and 0.0129 above 1.49 (about 124 signals each). Across all active bars, the ratio's top quartile gains 0.0080 per bar while the second quartile loses 0.0026.
- **F4:** The regime gate at a ratio just above 1.0 lets in many weak cases. The first 1.0 to 1.37 of the ratio holds half of the active bars, and its mean next-day return is only 0.02 % to 0.14 %. Holding these bars costs fees: about 0.000141 per bar against a gain of 0.000522. The mean trade nets 0.079 % after fees against 0.179 % before.
- **F5:** The deepest falls of the book come in long stretches where it keeps buying falls that do not rebound. ETH's book fell 38.3 % over 578 days from w19 to w23, while the coin's summed daily return was +0.91 over the same stretch. BTC's book fell 36.2 % over 100 days in w23–w24. That loss in w23–w24 is the main reason the Calmar ratio is only 0.38.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound.d1_rebound-scales-with-volatility-stretch` (from F2, F3, F4, F5): In a coin whose 20-day volatility is high relative to its last 100 days, a sharp one-day fall is followed by a rebound over the next day. The larger the fall relative to the coin's 60-day mean absolute daily move, and the further the 20-day volatility stands above its 100-day level, the larger that next-day rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
