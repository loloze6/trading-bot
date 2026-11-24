---
line: 7.g patterns
backtest: 031-01.g1.g1.g2.g2_calm-volatility-short-term-trend_1d
idea tested: 031-01.g1.g1.g2.g2_calm-volatility-short-term-trend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4137 USD
---
## Findings
- **F1:** A coin's daily volume relative to its 20-day average grades its next 2 days: the excess 2-day return rises by +0.375 % per standard deviation of log relative volume (t 2.84 with same-day cases taken together, 7210 cases on 1265 days), from -0.44 % in the lowest fifth (t -2.6) to +0.73 % in the highest fifth (t 3.5).
- **F2:** The volume effect sits on falling days: after a down day the slope is +0.58 % per standard deviation (t 3.07, 3544 cases, 943 days), against +0.18 % after an up day (t 1.09, 3666 cases, 971 days).
- **F3:** The volume effect is positive on all 6 coins (per standard deviation from +0.07 % on BTC, t 0.5, to +0.72 % on ZEC, t 2.8) and in 6 of 8 years, so no single coin or year carries it.
- **F4:** Volume is separate from the tested forecast. Their correlation is 0.057, and in one regression of the 2-day excess return on both, volume keeps t 4.6 while the forecast keeps t 2.9.
- **F5:** The day's high-low range relative to its 20-day average carries nearly the same signal: +0.37 % per standard deviation, t 2.54 with same-day cases taken together, top fifth +0.77 % (t 3.7).
- **F6:** A close in the lower part of the day's range is followed by a higher next day (close-location slope -0.17 % per standard deviation, t -2.6, 17379 cases).
- **F7:** The tested idea's forecast rests on the 14-day return, but on its own that return grades the next 2 days only weakly (t 1.94, 7642 cases). Its 5-day grading is clearer (t 2.85, 2987 cases).
- **F8:** The book's gains come from its long side: longs average +2.48 % net per trade (2641 trades) and shorts -0.28 % (2868 trades); the book's daily returns are uncorrelated with the coins' (-0.01).

## Ideas
- `031-01.g1.g1.g2.g2.g1_heavy-volume-down-day-rebound` (from F1, F2, F3, F4): The heavier a coin's volume on a falling day compared with its 20-day average, the more the coin rises over the next 2 days, as a heavy-volume drop marks sellers running out.
- `031-01.g1.g1.g2.g2.g2_heavy-active-day-lifts-returns` (from F1, F3, F4, F5): The heavier a coin's volume and the wider its daily range compared with their 20-day averages, the higher its return over the next 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
