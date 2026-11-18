---
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound_1d
idea tested: 005-02_bullish-rsi-divergence-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3008 USD
---
## Findings
- **F1:** The test's result points the wrong way rather than weakly the right way: across 78 independent divergence cases on BTC and ETH, the mean of x is −0.0088 (t −1.35), the mean raw 10-day return after a divergence is −1.29 % (t −0.89) against −0.25 % (t −0.17) for 98 new-low cases without one, and BNB, which the brief names, is not in the record at all.
- **F2:** The grading the idea relies on is absent: the Spearman correlation between forecast size and the 10-day return is −0.07 across divergence cases, and the top forecast tercile has the most negative mean 10-day return (−2.1 %, t −0.76; mean x −0.020) against −1.1 % for the bottom tercile.
- **F3:** The effect changes sign from year to year and follows the market rather than the divergence: the mean 10-day return after a divergence is +8.4 % in 2019 (t 2.88, n 9) and +6.1 % in 2021 (n 10), but −7.3 % in 2022 (t −2.18, n 15) and −4.0 % in 2025 (t −1.74, n 16), and new lows without a divergence move the same way in those years (2022 −6.1 %, 2021 +7.6 %).
- **F4:** No other horizon, coin or regime shows a clear rebound. At 3, 5 and 20 days every divergence-minus-no-divergence gap has |t| < 1 overall. Both coins have negative mean x (BTC −0.0036, t −0.54; ETH −0.0139, t −1.25). In falling 60-day trends the divergence-minus-no-divergence 10-day gap is +1.25 % (Welch t 0.28, n 26/33), in rising ones it is −3.7 % (t −0.57, n 7/11), and in low-volatility periods divergences fall 3.6 % more than the coin's average (t −1.55).

## Ideas
- No ideas: The divergence result is on the opposite side of the idea, its size does not grade the following return (F2), and no coin, year, trend, volatility regime or horizon shows a clear rebound that new lows without a divergence lack (F3, F4), so no amended idea has support.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
