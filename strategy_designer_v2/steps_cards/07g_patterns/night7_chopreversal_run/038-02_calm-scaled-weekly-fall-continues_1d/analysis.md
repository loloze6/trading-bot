---
line: 7.g patterns
backtest: 038-02_calm-scaled-weekly-fall-continues_1d
idea tested: 038-02_calm-scaled-weekly-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3717 USD
---
## Findings
- **F1:** In calm markets (the book's calm gate), a coin's 3-day return scaled by its 30-day daily swing predicts the unusual 5-day move in the same direction: the slope is +0.0225 (t 5.97, 773 non-overlapping cases). In agitated markets it is +0.0009 (t 0.15, 591 cases). The continuation lives only in the calm profile.
- **F2:** In calm markets the unusual 5-day move rises steadily across the scaled 3-day move quintiles: -3.24 % (t -3.63, 149 cases), -1.21 %, +0.21 %, +1.19 %, +2.31 % (t 2.49, 152 cases). In agitated markets the quintiles show no order (+2.02 %, -1.99 %, +0.77 %, -0.72 %, +1.19 %). The extreme calm quintiles move 12 to 17 times the 0.19 % cost of a trade.
- **F3:** The calm continuation holds on both sides. The unusual 5-day move in the direction of the past 3 days is +1.56 % after falls (t 2.91, 370 cases) and +1.16 % after rises (t 2.41, 403 cases). The tested idea was short only, so it left out the rising half. That half also gets the coin's normal drift of about +0.65 % per 5 days in its favour, so its total move is about +1.8 % per case.
- **F4:** The calm 3-day slope is positive in 10 of the 12 windows shown (t above 2 in w9, w10 and w14) and in all 6 coins (t 1.65 to 3.75; above 2 for ETH, LTC, XMR and XRP). It is not one window's or one coin's effect.
- **F5:** The 3-day scaling beats the tested 7-day one in calm markets: slope t 5.97 for 3 days against 5.29 for 7 days and 4.76 for 20 days. The 7-day quintiles are not monotonic (+1.11 %, then -0.30 %, in the middle).
- **F6:** The book loses on its short trades: 858 trades of 5 days or less average -4.00 % net. Its edge is only in the few long-held trades (107 trades over 20 days average +13.3 %). The book was still short on 24 % of calm days in the top 7-day quintile, against a rise that continues (F3).
- **F7:** Two other patterns did not stand out against the number of angles looked at, so I propose no idea on them. The weekday of the next day gave t from -2.78 (Thursday) to +2.80 (Friday) over about 1190 days each. A 1-day scaled fall in agitated markets was followed by +1.73 % over 3 days (t 2.12, 185 cases).

## Ideas
- `038-02.g1_calm-scaled-three-day-continuation` (from F1, F2, F3, F4, F5): In a calm market, the larger a coin's 3-day move measured against its 30-day daily swing, the larger its further move in the same direction over the next 5 days, for rises and falls alike.
- `038-02.g2_calm-scaled-rise-continues` (from F1, F2, F3, F6): In a calm market, the larger a coin's 3-day rise measured against its 30-day daily swing, the larger its further rise over the next 5 days.
- `038-02.g3_calm-scaled-monthly-trend-continues` (from F1, F5): In a calm market, the larger a coin's 20-day move measured against its 30-day daily swing, the larger its further move in the same direction over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
