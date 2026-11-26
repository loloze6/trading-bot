---
line: 7.g patterns
backtest: 031-04_yearly-low-break-reverses_1d
idea tested: 031-04_yearly-low-break-reverses
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3472 USD
---
## Findings
- **F1:** The coin's 10-day return scaled by its volatility grades the next 10 days only weakly. Its top quintile has an unusual move of +2.6 % (strength 0.17, 274 cases) and its middle quintile −2.2 % (strength −0.14). The graded slope has a day-clustered t of only 1.43 over 255 days (Spearman 0.05). By year, Spearman flips sign: −0.14 in 2018, +0.21 in 2020, −0.12 in 2025. So it cannot be told from chance.
- **F2:** Where the close sits in its 60-day range shows the same shape. The top quintile is +2.5 % (strength 0.17, 164 cases) and the second quintile −2.2 % (strength −0.14, 158 cases). Yet its graded t is 1.18 over 151 days, and its yearly Spearman swings from −0.34 in 2018 to +0.40 in 2019. That is too unstable to count.
- **F3:** By weekday, cases starting Thursday gain +2.5 % unusual (t 2.28, 224 cases) and cases starting Saturday lose −2.1 % (t −2.41, 240 cases). These are the two extremes of 7 weekdays, among about 20 groupings examined, and are not clustered by day. That is the size expected by chance.
- **F4:** Volatility level grades nothing. The 20-day volatility quintiles have unusual moves of −0.3 % to +0.5 %, every |t| is under 0.5, and Spearman is −0.03 (p 0.30).
- **F5:** The past 3-day return grades nothing either. Spearman is −0.01 (p 0.69), and its quintiles lie between −1.6 % and +0.8 %.
- **F6:** The tested situation is rare. Only 227 of 17,044 bars are in the mean_reversion regime, and grid cases per coin number 3 to 8. Their means range from −5.0 % (ETH) to +12.3 % (XMR), and the book's 25 trades include a ZEC range from −16.5 % to +79.4 %. The pattern behind its +7.15 % size cannot be separated from a few large rebounds.

## Ideas
- No ideas: Across momentum over 5 to 30 days, range position, volatility, weekday, year and the regime's cases, no pattern stood out beyond chance: the best graded slope had a day-clustered t of 1.43 and flipped sign across years, and the two notable weekdays are the expected extremes of many comparisons.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
