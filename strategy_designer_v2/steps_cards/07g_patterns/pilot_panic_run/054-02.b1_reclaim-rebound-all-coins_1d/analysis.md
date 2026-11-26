---
line: 7.g patterns
backtest: 054-02.b1_reclaim-rebound-all-coins_1d
idea tested: 054-02.b1_reclaim-rebound-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6593 USD
---
## Findings
- **F1:** In falling markets (60-day return below −10 %), the reclaim of a pierced 30-day low is graded against the tested idea: the higher the close sits above that low within the day's range, the worse the next 5 days. Over 71 non-overlapping cases on 41 days, Spearman between reclaim and the 5-day excess return is −0.28 (p 0.017). The day-clustered slope is −1.91 usual moves per unit of reclaim (t −1.97). By reclaim tercile, the mean excess 5-day return runs from +2.5 % (low) to +0.7 % to −5.3 % (high, median −4.8 %). This matches step 5's failed supporting check (Spearman −0.108).
- **F2:** The strongest reclaims (above the median) fall in every window they occur in: the mean is negative in 6 of 7 windows (w7, w12 to w16) and the seventh is +0.06 %. They also fall in every year: −5.9 % in 2018, −3.0 % in 2019, −7.9 % in 2020, −3.6 % in 2021. The effect is larger in calm falling bars (top tercile −7.0 %, 17 cases) than in agitated ones (−1.2 %, 7 cases).
- **F3:** The tested event itself is no edge, even inside a falling market. Pierce-and-reclaim days there have a +4.3 % excess over 5 days (t 1.46, 30 grid cases). The book's per-trade figures (84 trades, mean net +6.3 %, 81 % winners) rest on 0.0084 trades a day, and the idea's unusual move of +1.76 % has a t of 0.95. The cost is not what fails: the unusual move is 7.9 times the 0.22 % cost. The forecast sizes up the strong reclaims, which F1 shows do worst.
- **F4:** In calm markets (30-day swing at or below its 90-day level), a coin's 5-day return, scaled by its usual 5-day move, predicts the next 5 days in the same direction. The day-clustered slope is +0.375 usual moves per unit (t 3.23, 623 cases, 139 days). By quintile of the past 5-day move, the excess 5-day return rises steadily: −3.0 %, −1.9 %, +1.4 %, +1.5 %, +4.6 %.
- **F5:** In agitated markets the same past-5-day continuation is absent (slope +0.108, t 0.82, 100 days). It is strongest in choppy calm markets (slope +0.83, t 2.97, 50 days) and still present in falling calm ones (+0.32, t 2.22, 88 days). In calm bars, the 5-day excess taken in the direction of the past 5-day move is positive in 11 of 12 windows (w8 −0.1 %) and in all four years (+0.9 % to +3.4 %).
- **F6:** Other angles showed nothing beyond known or held effects, given how many angles were looked at:

## Ideas
- `054-02.b1.g1_strong-reclaim-fails-falling` (from F1, F2, F3): In a falling market, when a coin's day trades below its lowest price of the past 30 days and closes back above it, the coin falls over the next 5 days, and the fall is larger the higher the close sits above that low, measured against the day's range.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `054-02.b1.g2_calm-market-weekly-continuation` (from F4, F5): In a calm market, a coin keeps moving over the next 5 days in the direction of its last 5-day return, and the further that 5-day return is from zero, measured against the coin's usual 5-day move, the larger the move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
