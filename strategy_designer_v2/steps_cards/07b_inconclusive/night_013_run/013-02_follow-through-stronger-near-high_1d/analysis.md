---
line: 7.b inconclusive
backtest: 013-02_follow-through-stronger-near-high_1d
idea tested: 013-02_follow-through-stronger-near-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3029 USD
---
## Findings
- **F1:** The main measure is close to zero rather than just below the bar: the pooled slope of the excess forward 30-day return on forecast/10 is 0.0021 with t 0.13 over 526 grid cases, and its sign varies by coin (BTC t +2.30, XRP t −2.03) and by year (2019 t +2.70, 2025 t +2.48, 2018 t −1.60, 2024 t −1.96).
- **F2:** The carry-on shows only in the third of cases closest to the 52-week high: there the slope of the excess forward 30-day return on the plain past 30-day return is +0.151 (t 2.50, n 129), against −0.111 (t −1.21, n 129) in the farthest third and −0.104 (t −0.85, n 128) in the middle third.
- **F3:** The near-high effect does not depend on how the 52-week weight is defined: closeness to the in-window running high gives the same picture, with a near-third slope of +0.126 (t 2.30, mean close/high 0.97) against −0.112 (t −1.04) in the far third.
- **F4:** The forecast blurs this split: it ranks almost exactly like the past return (Spearman 0.87 between the component value and the past return), and the convex weight still leaves it non-zero far below the high, where past moves reverse; so its slope is only +0.031 (t 1.19) even in the near third and is negative in the far (−0.018) and middle (−0.039) thirds.
- **F5:** Near the high, the effect sits mostly on the up side: cases with a positive past 30-day return have a mean excess forward return of +0.043 (se 0.031, n 99), against −0.031 (se 0.041, n 30) after a fall; far below the high, both sides are negative (−0.033 and −0.041).
- **F6:** The near-high carry-on is not steady over time or horizon: it is +0.248 (t 3.75, n 91) in the later years and −0.260 (t −2.20, n 38) in the earlier years, and its slope is +0.038 (t 1.99) at 10 days, +0.021 (t 0.58) at 20 days and +0.156 (t 2.58) at 30 days.

## Ideas
- `013-02_follow-through-stronger-near-high.b1_momentum-only-near-52-week-high` (from F2, F3, F4, F5, F6): A coin's past 30-day return carries on into the next 30 days, only while the coin closes within its top range near its 52-week high, and more strongly the closer its close is to that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
