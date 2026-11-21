---
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3829 USD
---
## Findings
- **F1:** The book's short trades lose and its long trades earn. The 1,699 short trades average −1.90 % net per trade (median −1.76 %, t −6.3). The 1,766 long trades average +0.86 % (median +0.66 %, t 2.3). The shorts carry the book's loss (Sharpe −0.35).
- **F2:** Short losses grow with the size of the entry forecast. By tercile of forecast size, shorts lose −1.18 %, −1.94 % and −2.28 % before fees (566 to 567 trades each). Longs show no such order (+0.82 %, +0.47 %, +1.59 %).
- **F3:** On decline bars (90-day return below zero), the coin rises after the combination says down. On the non-overlapping 5-day grid, after a negative forecast the coin's 5-day return is +0.63 % (764 cases, t 1.9). After a positive forecast it is +0.38 % (786 cases, t 1.1). The losing short trades last a median of 5 days, close to the idea's horizon.
- **F4:** The losses of F1 and F2 are far above the cost of a round trip (0.19 %). The losing move per short trade is about 6 to 12 times that cost, before fees.
- **F5:** Across all active bars, the forecast does not predict the next 5 days (Spearman ρ −0.012, p 0.63, 1,550 grid cases). This matches the idea's measured strength of −0.006.
- **F6:** After a Friday close, the next day's return beats the coin's drift by +0.30 % (2,363 days, t 3.6). It holds in both halves of the years (+0.43 %, t 3.0 to 2021; +0.19 %, t 2.1 after) and is positive on all 6 coins (t 0.3 to 2.4). Wednesday (−0.32 %, t −2.9) and Monday (−0.23 %, t −2.4) are negative, but Wednesday's sign weakens in the later half (t −1.2). This was one of about 15 angles looked at, and it is a calendar condition with no graded strength measured.
- **F7:** Inside the decline regime, the depth of the 90-day fall does not grade the next 5 days reliably (ρ −0.074, p 0.15, 379 grid cases). Only the shallowest fifth stands out (−2.4 %, t −2.9). Across all bars, the 90-day return's quintiles form a U shape (middle quintiles −1.9 % and −2.2 %, t −2.9 and −3.3; extremes +0.7 % and +1.5 %), not an order.
- **F8:** The other single-bar angles show no ordered effect on the 5-day return: the past 1-day, 5-day and 20-day returns, 20-day volatility, nearness to the 30-day high and the bar's range (Spearman p from 0.05 to 0.86). Their quintiles jump around with no monotone pattern.

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.g1_downtrend-combined-score-short-reversal` (from F1, F2, F3, F4): While a coin's 90-day return is negative, the more strongly its relearned combined score of its 28-day return, last 1-day return, closeness to its 90-day high and 30-day volatility points down, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
