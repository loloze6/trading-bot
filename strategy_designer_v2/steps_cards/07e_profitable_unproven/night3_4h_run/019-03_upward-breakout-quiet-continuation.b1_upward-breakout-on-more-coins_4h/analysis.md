---
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4929 USD
---
## Findings
- **F1:** Most of the book's gain is the market's own rise, not timing: the book's mean daily return is 0.1003 %, of which 0.0709 % is the position held times the coins' mean daily return and only 0.0293 % is timing, over 2898 days. Holding the coins earns more per day (0.1388 %); the book's higher Sharpe (0.92 against 0.61) comes from being invested only about 55 % of the bars.
- **F2:** The breakout itself does not predict a move large enough to pay at any horizon. Recomputed from prices, the first close above the prior 12-bar high in each grid cell is followed by an unusual move of +0.12 % over 18 bars (t 0.80, 5034 cases), +0.25 % over 36 bars (t 0.98, 3530 cases) and −0.67 % over 72 bars (t −1.53, 2114 cases). Its only t above 2 is +0.12 % over 3 bars (t 2.80, 8815 cases), about half the 0.22 % cost of a round trip.
- **F3:** Narrowness, the idea's grading, does not grade the 18-bar move. By quintile of the 30-day mean range over the 12-bar stretch range, the unusual moves from least to most narrow are +0.62 %, −0.40 %, +0.62 %, −0.01 % and −0.25 % (about 1007 cases each). The recorded forecast is also saturated at its cap of 20 on at least 75 % of breakout bars, so it carries no grading either.
- **F4:** The coin's past 7-day return grades the 18-bar move after breakouts. By quintile of the 7-day return over the 30-day volatility, the unusual move runs from −1.03 % (strength −0.10, t −4.38) to −0.46 %, +0.50 %, +0.51 % and +1.12 % (strength +0.098, t 2.19), about 1000 cases each. The plain 7-day return gives the same order, from −1.16 % (t −4.71) to +1.23 % (t 2.33).
- **F5:** The same past-week grading holds on ordinary bars, so it is momentum rather than a breakout effect. On all 18-bar grid bars (about 1821 cases per quintile), the unusual move by quintile of the 7-day return over volatility is −0.18 %, −0.71 % (t −3.87), −0.47 % (t −2.28), +0.22 % and +0.92 % (t 3.18, strength 0.094). The 30-day return grades breakout cases the same way, from −0.41 % and −0.60 % (t −2.40) in the two lowest quintiles to +0.78 % (t 2.59) and +0.93 % in the two highest.
- **F6:** The book earns in coins that rose the week before. Its mean daily return by quintile of the coin's prior 7-day return goes from −0.039 % to −0.011 %, +0.044 %, +0.134 % and +0.370 %, while its mean allocation goes from 0.16 to 0.71. Trades entered in the highest 7-day quintile net +3.82 % on average, against +0.46 % in the lowest (about 1984 trades each).
- **F7:** Breakouts after a falling week are worse than ordinary bars after a falling week. In the lowest 7-day quintile, breakout cases lose −1.03 % unusual (t −4.38), against −0.18 % on grid bars, a gap of about 4.7 times the 0.22 % cost of a trade.
- **F8:** The timing gain sits in a few windows, coins and trades.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation` (from F4, F5, F6, F1): The larger a coin's return over the past 7 days, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails` (from F7, F4, F2): When a four-hour bar closes above the highest high of the preceding two days after the coin has fallen over the past 7 days, the coin falls over the next three days, and the deeper the past week's fall, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
