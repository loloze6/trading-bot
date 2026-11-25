---
line: 7.e profitable but not proven
backtest: 032-02.g1.b1_uptrend-near-high-more-coins_1d
idea tested: 032-02.g1.b1_uptrend-near-high-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4027 USD
---
## Findings
- **F1:** The book's mean daily return of 0.124 % (t 2.73 over 1449 days) splits into 0.0705 % from the market's own rise (the position held times each coin's mean daily return) and only 0.0536 % from timing. More than half of what the book earns is the coins' drift, and holding the coins averaged 0.202 % a day.
- **F2:** The gain rests on a few days and a few trades. Without its 10 best days the book's mean falls from 0.124 % to 0.053 % a day, and without its 30 best days to −0.017 %. Its 2537 trades have a median of −0.45 % after fees and win 48 % of the time, against a mean of +11.7 %. The 10 best trades carry 23 % of the summed trade gains, and DOGE alone carries 7541 of 29788 summed percentage points.
- **F3:** The plan's regime alone, the coin's 28-day return above 0, separates the next moves. On the non-overlapping grid, excess returns in the regime minus out of it are +1.81 % over 5 days (Welch t 2.70; 1285 vs 1139 cases) and +3.65 % over 10 days (t 2.80; 637 vs 563). The difference is positive in 12 of 13 coins but in only 7 of 12 windows.
- **F4:** Closeness to the 28-day highest close predicts the move across all bars, not only in uptrends, and more strongly over 10 days than over 5. The top proximity quintile minus the bottom gives +3.95 % excess over 5 days (t 2.67; 363 vs 363 cases) and +9.19 % over 10 days (t 3.65; 179 vs 179). The Spearman correlation of proximity with the excess return is 0.106 at 5 days and 0.194 at 10 days.
- **F5:** Inside the uptrend regime the proximity gradient is steepest over 10 days. Proximity quintiles run from −2.53 % to +10.13 % excess, against −3.11 % to +5.43 % over 5 days. It does not hold over 20 days (−3.39 % to +3.03 %, non-monotone).
- **F6:** The gradient is not stable over time. The top-minus-bottom proximity quintile over 5 days is positive in only 6 of 12 windows, ranging from −7.7 % to +9.6 %.
- **F7:** The size of the past rise is graded but fades at the extreme. Across all bars, the Spearman correlation with the next 10-day excess return is 0.125 for the 28-day return and 0.150 for the 14-day return. But inside uptrends the top 28-day-return quintile is followed by −0.29 % over 5 days and −0.12 % over 10 days, while the fourth quintile gets +4.52 % and +6.89 %.

## Ideas
- `032-02.g1.b1.e1_near-high-predicts-ten-day-rise` (from F4, F5, F3): The closer a coin's daily close is to its highest close of the past 28 days, the larger its rise over the next 10 days. This holds whatever the coin's 28-day trend.
- `032-02.g1.b1.e2_two-week-rise-continues-ten-days` (from F7, F3): The larger a coin's rise over the past 14 days, the larger its further rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
