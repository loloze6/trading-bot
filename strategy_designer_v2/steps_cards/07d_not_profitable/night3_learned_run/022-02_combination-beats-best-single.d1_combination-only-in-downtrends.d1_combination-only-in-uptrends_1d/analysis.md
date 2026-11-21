---
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5503 USD
---
## Findings
- **F1:** The book's loss comes from its shorts. Short positions summed −10.46 of daily position gain, against +1.16 for longs. The 2189 short trades lost 5.95 % each on average after fees, while the 1638 long trades gained 1.96 %.
- **F2:** The combined score points the wrong way inside the 90-day rise. Its rank correlation with the next 5-day unusual move is −0.055 (p 0.023, 1704 cases). The 57 % of cases where it was short were followed by +0.85 % (t 2.14), and the cases where it was long by −0.73 % (t −1.80). That is why the idea's size is −0.43 % per case, 2.2 times the 0.19 % cost and of the wrong sign.
- **F3:** The relearned weights give two components the opposite sign to what they predict in a rise.
- **F4:** The weights do not carry forward from one period to the next. By year, the score's correlation with the 28-day return swings from −0.46 to +0.48, and its correlation with the move is negative in 7 of 8 years (−0.06 to −0.31).
- **F5:** The 28-day return alone does predict the move in a 90-day rise (rank correlation +0.081, p 0.004, 1272 cases).
- **F6:** In a 90-day rise, coins farthest from their 90-day high were followed by −1.22 % (t −1.74). Coins in the upper three fifths of closeness were followed by +1.02 % to +1.21 %.
- **F7:** When the combined score disagreed in sign with the 28-day return (696 cases, 77 % of them short), its bets earned −1.26 % per case. When they agreed (576 cases), they earned +0.55 %.
- **F8:** Outside a 90-day rise, the relation reverses. The 28-day return (−0.065, p 0.025) and closeness to the 90-day high (−0.074, p 0.007) both point to lower next 5-day returns.

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.d1_monthly-momentum-inside-uptrends` (from F1, F5, F7): While a coin's 90-day return is positive, the higher its 28-day return, the larger its rise over the next 5 days.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.d2_nearness-to-high-in-uptrends` (from F3, F6): While a coin's 90-day return is positive, the closer its close is to its 90-day closing high, the larger its rise over the next 5 days.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.d3_combination-agreeing-with-momentum` (from F1, F2, F4, F7): A coin's return over the next 5 days lines up more closely with its relearned combined score of its 28-day return, last 1-day return, closeness to its 90-day high and 30-day volatility than with the score of whichever single signal has predicted best, only while its 90-day return is positive and the combined score points the same way as its 28-day return, and the more positive that 90-day return the closer the fit.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.d4_momentum-reverses-in-downtrends` (from F8): While a coin's 90-day return is not positive, the higher its 28-day return, the lower its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
