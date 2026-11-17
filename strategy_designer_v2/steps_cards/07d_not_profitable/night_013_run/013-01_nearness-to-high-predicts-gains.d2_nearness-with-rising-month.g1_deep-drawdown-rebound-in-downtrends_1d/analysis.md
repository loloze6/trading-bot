---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3562 USD
---
## Findings
- **F1:** The deepest fall that fails Calmar is the book's whole first half. Chained in window order, the book fell 59.3% from a peak in w1 to a trough in w16, which took 1773 days. Over the same years the book's daily returns tracked the coins' with a correlation of 0.74, and it was long on 50% of bars.
- **F2:** The tested forecast carries no information, but the plain depth it is built from does.
- **F3:** Inside the regime, the raw depth sorts outcomes the way the idea says. The deepest third has a mean 7-day excess return of -0.15%, the middle third -1.12% and the shallowest third -1.47% (330 cases each). Sorted by the forecast instead, the top third returns -0.13% and the middle third -1.49% (about 409 cases each), with no ordering.
- **F4:** The depth effect is strongest when the coin's 90-day return is also negative.
- **F5:** The regime the book trades in loses money and pays fees on it, which is why it trails holding.
- **F6:** A rough reconstruction points the same way.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.d1_raw-depth-rebound-bear-quarter` (from F1, F2, F3, F4, F5, F6): While a coin's 30-day return is negative, the farther its daily close sits below its highest close of the past 60 days, the higher its return over the next 7 days. Here the distance is the plain percent gap below that high, not the gap compared with its own recent gaps, and the effect is strongest while the coin's 90-day return is also negative.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.d2_deep-gap-after-long-decline` (from F3, F4, F5): While a coin's 90-day return is negative, the more its 30-day return has fallen and the farther its close sits below its highest close of the past 60 days, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
