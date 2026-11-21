---
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea tested: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3476 USD
---
## Findings
- **F1:** The book fails on its falls and not on its trading costs: its deepest fall is 54.5 % over 556 days in w14–w18, where the book summed −0.73 while holding the coins summed +0.83, and its fees are only 0.002 % to 0.006 % of the book per bar.
- **F2:** The idea is real but far too small to pay: per case over 5 days the unusual move is +0.12 % (strength 0.004, against about 0.05 for confirmed ideas so far), and the total move is +0.07 %. A round trip costs 0.19 %, so the moves are 0.6 and 0.4 times the cost.
- **F3:** The book's gain comes from its longs only. Long bars earn +0.118 % per bar (7497 bars); short bars earn −0.009 % (8190 bars), although the book is short about half the time in every stretch (46 % to 51 %).
- **F4:** In w14–w18 both sides lose, shorts −0.165 % per bar (1609 bars) and longs −0.051 % (1872 bars), while in w1–w13 both earn (+0.068 % and +0.172 %). The book's deepest fall is therefore a period in which the reversed volatility relation did not hold.
- **F5:** The book's gain sits in the bets that agree with the coin's 28-day return:
- **F6:** Nearness to the 90-day high separates the 5-day timing gain by more than the cost of a trade:
- **F7:** The forecast's size is graded. Bars in the top quintile of |forecast| gain +0.120 % per bar, against −0.003 % in the bottom quintile, and shorts in the highest-volatility quintile lose −0.090 % per bar.

## Ideas
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d1_volatility-reversal-with-trend` (from F1, F3, F4, F5): For a coin's 30-day volatility, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power for that coin's 5-day returns over the following 90 days. This reversal is larger the more the side it points to agrees with the coin's own 28-day return.
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high` (from F2, F6): The closer a coin's daily close sits to its highest close of the past 90 days, the higher its return over the next 5 days.
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues` (from F2, F5): The larger a coin's 28-day return, the larger its return over the next 5 days in the same direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
