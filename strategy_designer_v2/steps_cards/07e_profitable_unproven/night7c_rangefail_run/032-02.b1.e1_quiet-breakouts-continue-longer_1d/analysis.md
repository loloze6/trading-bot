---
line: 7.e profitable but not proven
backtest: 032-02.b1.e1_quiet-breakouts-continue-longer_1d
idea tested: 032-02.b1.e1_quiet-breakouts-continue-longer
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4105 USD
---
## Findings
- **F1:** The book's gain is not mainly the market's rise: of its mean daily return of 0.0334 %, the market's own rise accounts for 0.0071 % (about 21 %), so about 79 % is timing.
- **F2:** The book earns on breakouts themselves and over a longer horizon than the plan's 10 days. On the first close above the prior 60-day closing high in each 10-day grid cell, the unusual move is +10.6 % over 10 days (t 2.91, 84 cases) and +15.4 % over 20 days (t 4.40, 66 cases). The book's trades last 18.5 days on average (219 trades, 70 % winners).
- **F3:** The plan's grading has no support. The breaking day's 1-day gain does not predict the 10-day unusual move (Spearman −0.009 on the forecast-rise cases, −0.014 on breakouts), and the supporting check of the larger-forecast half minus the smaller-forecast half was −0.0139.
- **F4:** The width of the prior 60-day range, scaled by the coin's daily volatility × √60, grades the 20-day rise (Spearman −0.25, 66 cases). The narrowest quartile gives +24.8 % (t 3.36) and the middle quartiles +13.1 % (t 2.78) and +14.4 % (t 2.62). The widest quartile gives −2.3 % (t −0.53), and −4.8 % over 10 days (t −1.49).
- **F5:** The smaller the coin's 20-day return before the break, the larger the 20-day rise after it (Spearman −0.31). The lowest quartile gives +25.9 % (t 3.24) and the second +14.5 % (t 3.31), against +5.0 % (t 1.30) and +11.2 % (t 1.63) in the top two. The 60-day return points the same way: lowest quartile +21.7 % (t 2.78), top quartile +4.1 % (t 0.60).
- **F6:** Breaks in trendless coins carry the move. With the 60-day efficiency ratio below 0.3, breakouts give +16.8 % over 20 days (t 4.28, 58 cases); the 8 breaks in trending coins give +5.1 % (t 0.80).
- **F7:** A smaller break above the high is followed by a larger 20-day rise (Spearman −0.18). Breaks under 0.75 % past the high give +19.1 % (t 2.60), and breaks over 5.5 % give +7.4 % (t 1.24).
- **F8:** The gain is concentrated in a few coins and windows.

## Ideas
- `032-02.b1.e1.e1_tight-range-breakouts-continue` (from F2, F4, F6): In a coin that closes above its prior 60-day closing high, the narrower that 60-day range of closes was relative to the coin's typical daily move, the larger the coin's rise over the next 20 days.
- `032-02.b1.e1.e2_unextended-breakouts-keep-rising` (from F2, F5, F7): In a coin that closes above its prior 60-day closing high, the smaller its return over the 20 days before the break, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
