---
line: 7.g patterns
backtest: 035-02_rising-market-narrowing-ranges-rise_1d
idea tested: 035-02_rising-market-narrowing-ranges-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4104 USD
---
## Findings
- **F1:** In rising markets, the level of a coin's mean daily high-to-low range over the last 14 days predicts the next 3 days' excess return downward. Measured as a rank against the coin's own ranges, the calmest fifth of cases earned +2.00 % (t 3.32, 213 cases) and the widest fifth −2.37 % (t −2.67). Top minus bottom is −4.38 %, Welch t −4.07, and the t with each day's cases taken together is −2.32 over 290 days.
- **F2:** The tested ratio does not carry this effect:
- **F3:** The same pattern holds with the 14-day standard deviation of daily returns, ranked against the coin's own history, in rising markets. The lowest fifth earned +1.85 % (t 3.12) and the highest fifth −1.06 %. Top minus bottom is −2.91 %, Welch t −2.67, and the t with each day's cases together is −1.92 over 290 days.
- **F4:** Each of the six coins shows the same ordering in rising markets: its lowest third of 14-day swing earns more over 3 days than its highest third. The pairs are:
- **F5:** The effect is stronger in the later windows. Lowest third minus highest third is +3.49 % in w13–w18 against +0.97 % in w7–w12.
- **F6:** The effect needs the uptrend. Outside rising markets the 14-day swing has the opposite, weak slope: lowest fifth −0.62 %, highest fifth +0.70 %, Welch t +1.81, t with each day's cases together +1.10 over 357 days.
- **F7:** The other angles did not stand out with each day's cases taken together. These were:
- **F8:** The book's gain comes from the coins' drift, not from the idea. The book has a Sharpe of 0.92 and failed only on Calmar (0.70). Per case, the total move of +0.34 % is 1.8 times the 0.19 % cost of a trade. The unusual move is −0.02 % (t −0.05).

## Ideas
- `035-02.g1_calm-level-uptrend-continuation` (from F1, F2, F4, F5, F6): In a rising market, a coin rises more over the next 3 days the narrower its mean daily high-to-low range over the last 14 days is compared with its daily ranges over the past year.
- `035-02.g2_low-volatility-rising-coins-continue` (from F3, F4, F6): In a rising market, a coin rises more over the next 3 days the lower the standard deviation of its daily returns over the last 14 days is compared with that standard deviation over the past year.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
