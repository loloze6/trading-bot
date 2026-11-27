---
line: 7.g patterns
backtest: 076-01_run-break-three-day-fade_1d
idea tested: 076-01_run-break-three-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3926 USD
---
## Findings
- **F1:** How deep the broken run fell sorts the fade much better than how many days it lasted. On 3-day non-overlapping cases, run-breaking up days after the deepest fifth of run falls were followed by an unusual move of -3.23 % (t -2.62, 152 cases on 66 days). The other four fifths gave -0.65 %, +1.02 %, +0.11 % and -0.19 %, with t from -0.64 to +1.20.
- **F2:** The same deepest fifth fades already over the next day. Its unusual 1-day move is -2.10 % (t -3.63, 468 cases on 193 days), against -0.35 % to +0.16 % in the other fifths. Over 5 days it is -3.80 % (t -1.56, 83 cases), so the fade is mostly done within the first days.
- **F3:** The count of down days matters only through depth. Breaks after 3 or more down days with a deep run (the two deepest fifths) gave -3.47 % over 3 days (t -2.90, 119 cases). Breaks after 3 or more days with a shallow run gave -0.79 % (t -0.86, 46 cases). A day-clustered regression of the 3-day unusual move on both gives the run's fall a coefficient of 0.149 (t 1.79) and the count -0.005 (t -1.14).
- **F4:** Scaling the run's fall by the coin's 20-day volatility keeps the effect. The most extreme fifth of the scaled depth gives -3.30 % over 3 days (t -2.37, 139 cases); the other fifths range from -1.15 % to +0.74 %, all with |t| < 1.3.
- **F5:** By run count alone, 3-day unusual moves after breaks run as follows:
- **F6:** The deep-run fade sits in falling and choppy markets. With the 60-day return below -10 %, deep breaks gave -2.89 % over 3 days (t -1.66, 90 cases). In choppy markets they gave -1.99 % (t -1.41). Above +10 % they gave +1.36 % (t 0.61). None of these reaches t 2 alone, so no profile is named.
- **F7:** The deepest-fifth fade points the same way in each year shown (2018 to 2021), from -0.5 % to -6.2 % over 3 days. It sits well above the cost of a trade: the 3-day fade is about 17 times the cost and the 1-day fade about 11 times (cost 0.19 %).
- **F8:** Other angles showed nothing that stands out after this many looks; no |t| above 1.5 except one, and none graded:

## Ideas
- `076-01.g1_deep-run-break-fade` (from F1, F3, F4, F7): In any market, the first up day after a run of down days is followed by a fall over the next three days, and the fall is larger the deeper the run's total fall was, measured against the coin's recent daily swing.
- `076-01.g2_deep-run-break-next-day-fade` (from F2, F3, F7): In any market, the first up day after a run of down days is followed by a fall over the next day, and the fall is larger the deeper the run's total fall was.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
