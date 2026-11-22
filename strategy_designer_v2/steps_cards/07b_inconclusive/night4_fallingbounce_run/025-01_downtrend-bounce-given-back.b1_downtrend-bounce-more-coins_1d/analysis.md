---
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d
idea tested: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4643 USD
---
## Findings
- **F1:** The test came out inconclusive only because the plan's forecast is not graded the way the idea is. Its main measure is on the predicted side (+0.62 % unusual short move per case over 5 days, t 2.81, 2312 cases), but its correlation is −0.028. In my recount of the cases, the largest forecasts (8.7 to 20, 1172 cases) give only +0.17 % (t 0.51), while the middle quartile gives +1.30 % (t 3.11).
- **F2:** The grading the idea describes does show when the rise is measured raw in usual daily moves, as the idea states, instead of standardised against its own last 60 days. On the 5-day grid of falling coins, rises of 0 to 0.5 usual moves are followed by −0.11 % (n 621). Rises of 1.5 to 2 give +1.48 % (n 84), 2.5 to 3 give +5.08 % (t 2.85, n 23), and above 3 give +9.93 % (t 3.04, n 12). The Spearman correlation between the rise and the short move is +0.07 (Pearson +0.09).
- **F3:** The forecast fires mostly on ordinary rises. 690 of the cases follow a rise of under one usual daily move and 966 a rise of 1 to 2, against only 34 above 3. So the strongest bounces, where the move is largest, are a small share of the bets.
- **F4:** Large rises are followed by opposite moves in falling and in rising coins, as the brief's own test of the theory asks. After rises above one usual daily move, the 5-day short move in falling coins minus that in rising coins is +4.70 % (Welch t 4.06; 368 vs 534 cases). Above two usual moves it is +12.59 % (t 3.50; 78 vs 131).
- **F5:** In rising coins, a large rise is followed by further rises, graded. The short-direction unusual move is −1.48 % for rises of 1 to 1.5 usual moves (t −1.83), −2.38 % for 1.5 to 2 (t −2.33) and −5.69 % for 2 to 2.5 (t −2.94). Its Pearson correlation with the rise is −0.145 (Spearman −0.117).
- **F6:** Part of the main measure's gain is the falling regime itself, not the bounce. All 5-day grid bars in falling coins, whatever the day did, give +0.33 % (t 1.85, n 3579). That gain comes from shallow falls (top 90-day-return quartile +2.48 %, t 4.48) and reverses in the deepest falls (−1.63 %, t −1.79).
- **F7:** The effect varies strongly by year, so it is mixed over periods. By year the cases give +2.88 % in 2025 (t 5.74) and +1.21 % in 2022 (t 2.47), but −3.49 % in 2020 (t −3.86) and −1.21 % in 2023 (t −2.43). After rises above two usual moves, 2025 alone gives +17.3 % (n 14).
- **F8:** No more daily data is available: the test already used all 19 coins over folds A to D. As a book, the 5-day total move per case is −0.14 % against a 0.22 % trade cost.

## Ideas
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back` (from F1, F2, F3, F4): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days. The fall grows steeply with the size of the rise in usual daily moves: the largest bounces, of several usual daily moves, are given back the most, and ordinary rises are followed by almost nothing.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b2_uptrend-surges-keep-rising` (from F4, F5): In a coin whose 90-day return is positive, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days. The larger the rise in usual daily moves, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
