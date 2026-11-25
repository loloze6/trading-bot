---
line: 7.g patterns
backtest: 035-03_far-below-high-falls_1d
idea tested: 035-03_far-below-high-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3866 USD
---
## Findings
- **F1:** Distance from the 20-day high, in daily swings, ranks the coin's next-5-day unusual move in order across almost the whole range. By sextile it goes -1.55 %, -0.76 %, -2.06 % (day-clustered t -2.38, 150 days), +0.18 %, +1.00 % and +3.19 % (t 1.82, 112 days). Its correlation with the unusual move is positive in all four years (0.004, 0.099, 0.176, 0.063), so the tested short side is half of a single graded relation.
- **F2:** The short side's edge depends on the year. Closes at least 2 swings below the high were followed by -2.98 % (262 cases) in 2018, -2.53 % (236) in 2019 and -0.99 % (216) in 2020, but +0.22 % (356) in 2021. Closes near or above the high were followed by -1.17 % in 2018, +2.34 % in 2020 and +4.90 % in 2021. Which side carries the effect follows the market's own trend.
- **F3:** Among closes at least 2 swings below the high, an up day predicts a fall. The highest last-day-return tercile was followed by -1.99 % over 5 days (t -3.21, 357 cases), against -0.22 % (t -0.33) for the lowest tercile. The top quartile of the last day's move in swings gave -2.48 % (day-clustered t -1.92, 79 days). Deep closes after an up day were negative in every year: -2.07 % (111 cases), -0.05 % (84), -2.55 % (74) and -2.47 % (129).
- **F4:** Among the same deep closes, the biggest 3-day falls were followed by no further fall: the lowest 3-day-return quartile gave -0.07 % (t -0.04, 70 days), against -1.72 % to -2.04 % for the other three quartiles. Further weakness keeps drifting only when it has not just been flushed out.
- **F5:** The book lost when its coins rose and earned when they fell. In w10 and w11 the coins rose 0.55 % and 1.93 % a day while the book fell 0.30 % and 0.22 % a day. In w7 and w14 the coins fell 0.47 % and 0.43 % a day while the book gained 0.22 % and 0.30 % a day. This fits a short exposure to the market more than timing, and the -0.81 % normal drift against the short side leaves a total move of -0.13 % per case.
- **F6:** I also grouped the bars by recent volatility, close location and weekday, and nothing there stands out given how many angles I looked at. The deep-below-high fall was about the same in all three volatility terciles (-1.86 %, -2.02 %, -1.80 %; t -2.5, -3.2, -2.2). Friday's next-day move of +0.39 % (t 2.94) and Monday's -0.36 % (t -2.59) are not day-clustered, so I do not count them.

## Ideas
- `035-03.g1_deep-drawdown-bounce-fades` (from F3, F4, F1): A daily close that rises on the day while the coin sits many daily swings below its 20-day high is followed by a fall over the next 5 days, larger the larger that day's rise measured in the coin's daily swings.
- `035-03.g2_far-below-high-falls-when-falling` (from F2, F5, F1): A daily close many daily swings below the coin's 20-day high is followed by a fall over the next 5 days, larger the more daily swings it sits below that high, in a falling market.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
