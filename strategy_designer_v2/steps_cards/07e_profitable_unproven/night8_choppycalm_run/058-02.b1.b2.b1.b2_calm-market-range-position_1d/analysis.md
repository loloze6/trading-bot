---
line: 7.e profitable but not proven
backtest: 058-02.b1.b2.b1.b2_calm-market-range-position_1d
idea tested: 058-02.b1.b2.b1.b2_calm-market-range-position
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3967 USD
---
## Findings
- **F1:** The book's gain is not the market's own rise: its mean daily return is 0.116 % (t 2.83 over 1,449 days), of which only 0.004 % comes from the market's rise, so timing is 0.112 % a day. Every one of the 10 coins has a positive mean daily return (0.037 % for DOGE to 0.231 % for ADA), and 10 of the 12 windows are positive (w9 −0.055 %, w12 −0.052 %).
- **F2:** Long days carry the book: they sum to +9.39 (mean 0.32 % a day over 2,914 coin-days), against +1.61 for short days (mean 0.057 % over 2,809).
- **F3:** In calm bars, on a non-overlapping grid without clustering by day, the raw 20-day range position predicts the coin's excess return at every horizon: slope t 4.9 at 1 day (4,727 cases), 5.6 at 3 days (1,519), 7.2 at 5 days (904), 4.6 at 10 days (442) and 2.8 at 20 days (209). In agitated bars it predicts nothing (t −0.4, 0.2, 0.9, 0.7, −0.8). The plan tested a 60-day-standardised version of this position, clustered by day, and got only t 1.70.
- **F4:** Within calm bars at 5 days, the slope is steepest when the 60-day trend is choppy (0.092, t 4.9, 126 cases). It is lower in rising markets (0.065, t 4.1, 206 cases) and falling ones (0.042, t 3.4, 265 cases), and absent where there is no 60-day history (0.014, t 1.5, 307 cases).
- **F5:** The effect is continuation, the opposite of the brief's reversion, and it sits at the top of the range. By 5-day quintile of calm range position, the excess return is −2.4 % in both lower quintiles (t −3.3 and −3.6), 0.1 % in the middle quintile, 0.4 % in the fourth and +4.4 % in the top quintile (t 4.5, mean position 0.79).
- **F6:** The 5-day slope in calm bars is positive in 10 of 12 windows but reaches t ≥ 2 in only one (w10, t 2.5). The effect resembles the held calm "nearness to high" book 035-01.b1; only its choppy-calm form is a thin cell of the profile map.

## Ideas
- `058-02.b1.b2.b1.b2.e1_choppy-calm-range-continuation` (from F3, F4, F5): In a choppy, calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.
- `058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon` (from F2, F3, F5, F6): In a calm market, the nearer a coin's close is to its 20-day high, the larger its rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
