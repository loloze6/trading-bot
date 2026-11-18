---
line: 7.g patterns
backtest: 011-02_weekend-drop-rebounds-monday_1d
idea tested: 011-02_weekend-drop-rebounds-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5707 USD
---
## Findings
- **F1:** The day after a coin's largest falls it rebounds. Across all coins, bars in the lowest fifth of one-day return (in 20-day usual moves) are followed by a next-day excess return of +0.44 % (t 4.73, n 3188). The middle-upper fifth is followed by −0.25 % (t −3.01, n 3188), and the top fifth by −0.07 % (t −0.76).
- **F2:** The rebound after a fall is concentrated on high-volume days. Down days in the top third of relative volume (volume over its 20-day mean) are followed by +0.47 % excess the next day (t 4.31, n 2607). Down days in the low and middle thirds are followed by −0.04 % and +0.10 % (t −0.43 and 1.11). Up days on low and middle relative volume are followed by −0.21 % (t −2.52, n 2746) and −0.27 % (t −3.14, n 2661).
- **F3:** Weekend days show a two-sided, graded reversal that weekdays lack. On Saturdays and Sundays the next-day excess runs from +0.62 % (t 2.71, n 614) and +0.32 % (t 2.15) in the two lowest return fifths to −0.51 % (t −3.71, n 1044) and −0.50 % (t −2.56, n 732) in the two highest. On weekdays only the lowest fifth stands out (+0.40 %, t 3.92), and the top fifth is +0.06 % (t 0.57).
- **F4:** The tested idea's own situation shows no grading in any coin. Per-coin correlations of Sunday-drop size with the next 2-day excess return (scaled by volatility) range from −0.085 to +0.079, every t within ±1.15, with 150–201 Sundays per coin.
- **F5:** A coin's whole weekend (Saturday plus Sunday) move continues rather than reverses. Its correlation with the next 2-day excess return (scaled by volatility) is +0.069 (t 3.30, n 2261), while the Sunday move alone gives −0.030 (t −1.44). The two-day move ending Thursday continues even more strongly (corr +0.086, t 4.08, n 2261).
- **F6:** The book's gain comes from the Monday bar. Its mean return is +0.10 % on Mondays (t 2.96, n 2484) and −0.001 % on Tuesdays (t −0.04), while holding the coins returned −0.009 % on Mondays. Sunday-held positions in the top allocation third were followed by +0.56 % excess (t 2.16, n 338).
- **F7:** A day-range effect matches F1. Days in the top fifth of relative high-low range (over its 20-day mean) are followed by +0.32 % excess the next day (t 3.06, n 3216).

## Ideas
- `011-02_weekend-drop-rebounds-monday.g1_high-volume-drop-next-day-rebound` (from F1, F2, F7): A coin that falls on a day of high trading volume relative to its own last 20 days rises over the next 1 day. The larger the fall in usual daily moves and the higher that relative volume, the larger the rise.
- `011-02_weekend-drop-rebounds-monday.g2_weekend-rally-next-day-fade` (from F3): A coin that rises on a Saturday or a Sunday falls over the next 1 day, and the larger that day's rise in usual daily moves, the larger the fall.
- `011-02_weekend-drop-rebounds-monday.g3_thin-volume-rise-gives-back` (from F2, F1): A coin that rises on a day of low trading volume relative to its own last 20 days falls over the next 1 day. The lower that relative volume and the larger the rise, the larger the fall.
- `011-02_weekend-drop-rebounds-monday.g4_weekend-two-day-move-continues` (from F5, F4): A coin's Saturday-plus-Sunday return continues over the next 2 days (Monday and Tuesday) in the same direction, and the larger the weekend move in usual moves, the larger the follow-through.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
