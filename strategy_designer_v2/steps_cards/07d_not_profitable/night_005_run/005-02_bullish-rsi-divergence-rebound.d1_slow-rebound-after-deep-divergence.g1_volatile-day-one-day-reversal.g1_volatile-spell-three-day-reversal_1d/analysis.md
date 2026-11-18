---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3735 USD
---
## Findings
- **F1:** The book did not fail on its forecast but on how far it falls. Its deepest fall was -34.0% over 277 days across w10–w13. Over that same stretch the coins themselves rose 0.39% a day. Of the fall's net loss, -0.304 came from shorts taken while the coin's 20-day return was negative, over 50 days with a volatility ratio near 1.14. All the other position types made money in that stretch (longs +0.058 and +0.263, shorts in rising 20-day trends +0.046).
- **F2:** The gain sits only where volatility is well above its average. Active bars were split into quarters by volatility ratio, with these mean ratios and daily results:
- **F3:** The positions were rescaled on the same daily returns and the same fee rate (0.082% per unit of turnover):
- **F4:** The fade pays most at the ends of the 20-day trend and loses in its middle. Active bars were split into fifths by 20-day return:
- **F5:** Fees take 0.033% a day from a mean gross of about 0.08% a day on the active bars. The book stays flat on 46% of bars, so it collects little of the market's own rise. Its gain is almost all timing (market part about -0.002% a day for each coin), and its Sharpe stays below holding's for both BTC (0.574 vs 0.652) and ETH (0.450 vs 0.574).

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal.d1_volatility-excess-graded-fade` (from F2, F3, F1): When a coin's 20-day volatility is high relative to its 60-day average, its return over the next 3 days runs against the day just closed. The larger that day's return relative to its 20-day volatility, the larger the move back. The move back grows with how far the 20-day volatility stands above its 60-day average: it is small when the two are close and largest when the 20-day volatility is far above it.
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal.d2_stretched-trend-fade-strength` (from F4, F1): When a coin's 20-day volatility is high relative to its 60-day average, its return over the next 3 days runs against the day just closed. The larger that day's return relative to its 20-day volatility, and the further the coin's 20-day return stands from zero in units of its 20-day volatility, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
