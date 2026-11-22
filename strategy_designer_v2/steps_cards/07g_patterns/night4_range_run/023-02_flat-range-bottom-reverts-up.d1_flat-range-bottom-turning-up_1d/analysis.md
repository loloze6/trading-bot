---
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3589 USD
---
## Findings
- **F1:** Saturday is the strongest pattern in the bars, and it does not come from the idea. Saturday's daily return averages +0.45 % (t 5.53, n 2484), or +0.092 of the coin's 20-day volatility (t 5.37, n 2093). That is well above every other weekday: Sunday is +0.060 (t 3.14), Friday +0.048 (t 2.17), and Thursday is the only clearly negative day at −0.079 (t −3.38).
- **F2:** The Saturday rise holds up across coins and years. Its mean is positive in all 6 coins, from +0.06 % in BTC (t 0.50) to +0.53 % in XRP (t 1.76), with XMR at +0.44 % (t 2.39). It is positive in 6 of 8 years, for example 2020 at +1.00 % (t 3.30) and 2025 at +0.71 % (t 3.20). The exceptions are 2018 at −0.35 % (t −1.33) and 2023 at −0.02 % (t −0.13).
- **F3:** The Saturday return grows with the coin's rise over the 5 days up to Friday's close. Split into quarters of that rise, scaled by volatility, Saturday averages:
- **F4:** Daily moves in general do not continue the next day. After a 1-day move of more than 2 volatilities, the next day averages +0.05 of a volatility (n 481); after a move below −2 volatilities, +0.03 (n 411). This says the Friday-to-Saturday continuation in F3 is specific to the weekend.
- **F5:** The brief's reversion is absent in flat coins (30-day net move at most 0.3 of the 30-day range). The slope of the drift-removed 5-day return on the close's place in the range is −0.085 (t −0.58, n 835). Flat coins in the lowest fifth of the range gain only +0.71 % over 5 days (t 1.03), and those in the highest fifth lose −1.50 % (t −1.17).
- **F6:** In coins with a moderate trend, the place in the 30-day range points the other way, toward continuation.
- **F7:** The book does not use the weekend pattern. Its mean allocation is the same on every weekday, 0.046 to 0.048. It is in a position on only 16–30 % of bars depending on the coin, and its Sharpe of 0.57 beats holding's by just 0.016.

## Ideas
- `023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.g1_weekend-continuation-after-strong-week` (from F1, F2, F3, F4): In a coin, the larger its rise over the 5 days up to Friday's close, the more it rises over the following day (Saturday), while after a fall over those 5 days Saturday tends to fall.
- `023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.g2_moderate-trend-range-position-continuation` (from F5, F6): In a coin whose 30-day net move is moderate against its 30-day high-low range, the higher its close sits in that range, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
