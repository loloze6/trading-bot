---
line: 7.b inconclusive
backtest: 061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues_1d
idea tested: 061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2014 USD
---
## Findings
- **F1:** The test's own result points the way the idea predicts but falls short of the bar. The pooled slope of the drift-adjusted next 5-day return on the forecast is +0.00048, with a day-clustered t of 1.11 on 818 cases (374 days). The supporting check passes: the top third of |forecast| beats the bottom third by +1.08 %.
- **F2:** In folds B and C the effect is on the predicted side at every horizon up to 10 days but never clear. The mean signed drift-adjusted return is +0.11 % at 1 day (t 0.60, 1486 cases), +0.29 % at 3 days (t 0.66, 495 cases), +0.73 % at 5 days (t 0.91, 287 cases) and +0.91 % at 10 days (t 0.53, 143 cases). It turns to −1.40 % at 20 days (t −0.52, 71 cases), so the plan's 5-day horizon is already where the effect is largest and no other horizon makes it clearer.
- **F3:** The effect is mixed across coins. At 5 days, XRP (+3.17 %, t 2.09, 60 cases) and BTC (+0.95 %, t 0.81, 64 cases) follow through. ETH (−1.52 %, t −0.99, 31 cases), XMR (−0.76 %, t −0.54, 53 cases) and LTC (−0.31 %, t −0.18, 42 cases) reverse. Each coin has only 31 to 64 cases.
- **F4:** The effect is mixed across years. At 5 days, 2018 (−0.88 %, t −0.48, 62 cases) and 2019 (−0.30 %, t −0.40, 83 cases) reverse. 2020 (+1.86 %, t 0.94, 81 cases) and 2021 (+2.29 %, t 1.25, 61 cases) continue.
- **F5:** Most of the gain comes from the short side. Shorts after a 5-day fall earn +2.27 % (t 1.73, slope t 2.52, 138 cases), and more for larger falls: +0.41 % in the low third, +3.09 % in the middle third and +4.23 % in the high third. Longs after a 5-day rise earn −0.69 % (t −0.61, 149 cases). Each side alone is still under t 2.
- **F6:** The idea's measured size is far below what a trade costs. The unusual move is +0.13 % per case over 5 days (t 0.43 over 837 days), or 0.006 of the coin's usual 10.60 % move. The total move of +0.14 % is 0.7 times the 0.19 % cost of a trade. The book earns +2.8 % a year (Sharpe 0.24, 0.31 below holding), so only a clearer and larger effect could pay.

## Ideas
- `061-01.g1.d1.d2.g2.b1_choppy-scaled-move-more-coins` (from F1, F2, F3, F5): In a choppy market, the larger a coin's 5-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
