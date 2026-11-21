---
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3439 USD
---
## Findings
- **F1:** The test's main measure is on the side the idea predicts but short of the bar: bars with forecast ≥ 5 rose 0.25 % more than the coin's normal next day (t 1.51, 780 cases). The data held only BTC and ETH, because BNB has no data, so the test ran on 2 coins.
- **F2:** The effect is not convex, so the supporting check failed. The middle forecasts 5 to 20 earned +0.39 % (t 1.90, 436 cases), the forecasts at the cap of 20 only +0.06 % (t 0.24, 344). On raw size, falls of 2 to 3 of the 20-day volatility earned +0.96 % (t 2.08, 113), and falls beyond 3 earned −0.29 % (t −0.19, 28).
- **F3:** The rebound sits in high-volatility periods. Among forecast ≥ 5 bars, the highest third of 20-day volatility earned +1.15 % excess the next day (t 2.90, 219 cases), against −0.22 % (t −1.04) in the lowest third and −0.02 % (t −0.07) in the middle third.
- **F4:** The effect is too small for its cost overall. The unusual move is +0.06 % per case, 0.014 of the 4.01 % usual daily move, which is 0.5 times the 0.11 % round trip (about 10–11 bps on BTC and ETH by topic 38). The high-volatility third's +1.15 % is about 10 times that cost.
- **F5:** The rebound is a 1-day effect, uneven across years and the same with or without a 20-day trend.
- **F6:** Across all down days, the size of the fall barely ranks the next day's return (correlation 0.025, 2,389 days). The idea's grading by fall size alone is weak; the grading shows only through the volatility state.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls.b1_outsized-fall-rebound-more-coins` (from F1): The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, and this rise grows faster than the size of the fall itself, so the largest falls carry most of the rebound.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls.b2_rebound-after-falls-in-turbulence` (from F2, F3, F4, F6): The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, only while its 20-day daily volatility is high against its own past year, and the more so the higher that volatility stands.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
