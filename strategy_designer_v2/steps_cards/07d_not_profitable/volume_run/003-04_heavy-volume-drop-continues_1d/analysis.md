---
line: 7.d not profitable
backtest: 003-04_heavy-volume-drop-continues_1d
idea tested: 003-04_heavy-volume-drop-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3193 USD
---
## Findings
- **F1:** The book is short only on the signal bar itself, and that short loses. Trades last a median of 1.0 day (mean 1.07), with 313 trades. The book holds a position on just 3.6% of days. The 329 held bars lose a mean of -0.65% each, of which only -0.12% is the coin's own rise; the rest is timing. Trades lose -1.43% each after fees, with a win rate of 39%.
- **F2:** The day the book holds is the day the coin bounces back. The excess return on day 1 after a signal is +0.57% (t 1.41, n 292), the day 2 return is flat (-0.00%, t -0.01), and the strong-forecast half bounces +1.01% on day 1.
- **F3:** The continuation the idea predicts is there, but only after that first day. From the close of day 1 to day 5 the excess return is -1.40% (t -2.68, n 286), and from day 2 to day 5 it is -1.33% (t -2.73). Day 3 alone gives -0.68% (t -2.56). The strong-forecast half falls -2.31% from day 1 to day 5 against -0.50% for the weak half.
- **F4:** Measured from the signal close, as the plan does, the 5-day excess is only -0.89% (t -1.51, n 292). The day-1 bounce hides the later fall, while the coins themselves rose 0.119% a day on average and the book returned -0.016% a day.
- **F5:** The continuation appears only where the coin's 60-day return is not already up. The 5-day excess is -2.08% (t -1.17, n 44) in the down third and -3.09% (t -1.83, n 44) in the middle third, but +1.05% (t 0.71, n 45) in the up third. Over 10 days these are -3.75% (t -1.80), -4.04% (t -1.94) and +2.09%.

## Ideas
- `003-04_heavy-volume-drop-continues.d1_heavy-volume-drop-continues-delayed` (from F1, F2, F3, F4): When a coin falls sharply over one day on volume well above its own 30-day average daily volume, it keeps falling over the 4 days that start one day after the fall, once the next day's rebound is over. The larger the fall and the heavier its volume against that average, the larger the further loss.
- `003-04_heavy-volume-drop-continues.d2_heavy-drop-continues-outside-uptrends` (from F5, F3): When a coin falls sharply over one day on volume well above its own 30-day average daily volume, it keeps falling over the next 5 days, only while its 60-day return is flat or negative. The larger the fall and the heavier its volume against that average, the larger the further loss.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
