---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4622 USD
---
## Findings
- **F1:** The book's profit comes from one window. Window w16 summed +183 % in trade returns over 7 trades and +1.19 in daily book returns, across six coins (BTC +0.40, XMR +0.23, XRP +0.23, ADA +0.17). The other windows of folds B and C give it back: w11 −164 % over 7 trades, w17 −41 % over 18 trades and w18 −43 % over 25 trades.
- **F2:** The idea's effect looks like a 20-day continuation that lives in choppy markets. The 20-day return scaled by the coin's 30-day swing predicts the next 5 days' unusual move in choppy markets (slope 0.066, t 3.32, 152 cases, 68 days). It does not in falling markets (slope 0.005, t 0.50, 437 cases) and only weakly in rising markets (slope 0.021, t 1.62, 377 cases).
- **F3:** Over 10 days the choppy-market continuation is stronger. The slope is 0.091 with t 5.49 (77 cases, 33 days), against 0.012 with t 0.48 in falling markets and 0.046 with t 2.23 in rising markets. It is the largest t across all the angles explored.
- **F4:** The continuation is graded in choppy markets. The next 5 days' unusual move runs from −15.2 % after the steepest scaled 20-day falls (t −2.38, 20 cases, 12 days) through −1.8 % (t −1.22) and −2.2 % (t −1.53) to +1.7 % (t 1.00) and +8.1 % after the steepest scaled rises (t 1.36, 20 cases).
- **F5:** Agitation is not what carries the effect. The choppy-market slope holds in calm markets (0.055, t 3.45, 117 cases) as well as in agitated ones (0.105, t 2.26, 35 cases), which matches the brief's second refutation case.
- **F6:** The brief's own situation is not in these bars. In choppy, agitated markets, closes in the top fifth of the day's range are followed over 2 days by −0.6 % unusual (t −0.40, 25 cases), with no gradient across close location (t from −1.90 to +0.29). In choppy, calm markets the top fifth gives −0.1 % (t −0.10).
- **F7:** The other angles show nothing that stands out once the number of looks is counted:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.d1.d1.g1_choppy-month-scaled-continuation` (from F2, F3, F4, F5): In a choppy market, a coin keeps moving in the direction of its 20-day return over the next ten days, and the larger that 20-day return measured against the coin's own daily swing over the last 30 days, the larger the move that follows.
- `061-01.b1.b1.b1.d1.d1.d1.g2_choppy-scaled-month-fall-continues` (from F2, F4, F5, F6): In a choppy market, a coin whose 20-day return is a fall falls further over the next five days, and the larger that fall measured against the coin's own daily swing over the last 30 days, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
