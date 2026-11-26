---
line: 7.b inconclusive
backtest: 058-02.b1.g1.b1_falling-rally-fades-more-coins_1d
idea tested: 058-02.b1.g1.b1_falling-rally-fades-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4025 USD
---
## Findings
- **F1:** Step 5's result points the way the idea predicts, a −0.25 % weighted excess next-day return, but it is too weak (t −1.47) and its slope is +2.5e-5; the cause is that the fade after a rise in a falling market does not grow with the rise: in folds B and C, up days in the falling profile are followed by −0.48 % excess (t −2.11, 2118 cases, 594 days), the smallest-forecast quintile by −0.82 % (t −2.22), the largest by only −0.37 % (t −0.90), and the Spearman correlation of the scaled rise with the next day is 0.002.
- **F2:** The effect lives on the plan's one-day horizon only: the excess return after a falling-market rise is −0.46 % at 1 day (t −2.05), −0.30 % at 2 days (t −0.95), −0.24 % at 3 days (t −0.68) and −0.11 % at 5 days (t −0.22).
- **F3:** The pull is graded once both sides of the day's move are measured, not rises only: across all falling-market days, the sextiles of the day's return over its 20-day swing go from a scaled move of −1.65 to +1.32, and the next day's excess falls from +0.73 % (t 1.43) through +0.29 %, −0.14 %, −0.69 % (t −2.13), −0.47 % to −0.41 %; the Spearman correlation is −0.10 over about 3,940 cases, and falling-market down days are followed by +0.32 % (t 1.35).
- **F4:** The reversal is concentrated in agitated falling markets: up days there are followed by −0.74 % (t −1.95, 999 cases) and down days by +0.68 % (t 1.84, 1061 cases), against −0.29 % (t −1.16) and −0.18 % (t −0.61) in calm falling markets.
- **F5:** The fade after a rise is broad but not uniform: it is negative on 10 of 12 coins (BTC −0.68 % t −2.43, LTC −0.62 % t −2.24, XMR −0.68 % t −2.14) and in 3 of 4 years (2018 −0.82 %, 2019 −0.62 % t −2.13, 2020 +0.04 %, 2021 −0.31 %).
- **F6:** Outside the falling profile the same reversal is weaker: up days are followed by −0.24 % (t −1.24, 4110 cases) and down days by +0.32 % (t 1.20).
- **F7:** The test's own size per case is small next to the cost of a trade: an unusual move of +0.27 % (t 1.62) is 1.2 times the 0.22 % cost, and the total move of +0.11 % is 0.5 times it; the one-day moves of 0.5 to 0.7 % in the agitated falling cells (F4) would cover the cost about 3 times.

## Ideas
- `058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal` (from F3, F4, F2, F7): In a falling, agitated market, the larger a coin's one-day rise is against its usual daily swing over the last 20 days, the larger its fall over the next day, and the larger its one-day fall against that swing, the larger its rise over the next day.
- `058-02.b1.g1.b1.b2_falling-market-next-day-reversal` (from F1, F3, F5, F6): In a falling market, the larger a coin's one-day rise is against its usual daily swing over the last 20 days, the larger its fall over the next day, and the larger its one-day fall against that swing, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
