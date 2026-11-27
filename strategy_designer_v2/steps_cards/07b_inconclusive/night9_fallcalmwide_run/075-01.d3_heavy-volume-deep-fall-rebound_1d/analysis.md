---
line: 7.b inconclusive
backtest: 075-01.d3_heavy-volume-deep-fall-rebound_1d
idea tested: 075-01.d3_heavy-volume-deep-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3867 USD
---
## Findings
- **F1:** Every fold, window and coin available on daily bars was already in the test, so the near miss (weighted mean +0.32 %, t 1.95 on 18,271 cases over 2,413 days) cannot be repeated on more data. The same measure on folds B and C alone gives +0.77 % with t 2.66 (5,995 cases, 1,125 days), so the shortfall comes from folds A and D.
- **F2:** The effect lives only in the strongest forecasts. Among bars with forecast > 0 in folds B and C, the two highest forecast quintiles give +0.72 % (t 2.34, 521 days) and +1.07 % (t 2.59, 337 days). The three lowest give −0.11 %, −0.15 % and −0.02 % (t −0.41 to −0.07). Most of the plan's cases carry no effect and dilute its t.
- **F3:** The depth of the fall carries the grading more than the volume does. On down days split by volume tercile and fall tercile, the deepest falls give +0.86 % (t 2.03, 253 days) on middle volume and +1.06 % (t 2.34, 288 days) on heavy volume. Shallow falls are near 0 at every volume level (−0.10 %, +0.09 %, −0.10 %). Light-volume deep falls give −0.29 % (t −0.54).
- **F4:** By fall quintile, the deepest fifth of active down days gives +1.09 % (t 2.34, 257 days), and the response fades steadily to +0.01 % and +0.15 % (t 0.02 and 0.51) in the two shallowest fifths. By volume quintile only the heaviest fifth stands out, at +1.37 % (t 2.89, 401 days).
- **F5:** The strong cases point the same way across coins and periods. The top two forecast quintiles have a positive mean in all 13 coins and in 11 of 12 windows (91.7 %). Their t is concentrated in w10 (+1.47 %, t 3.22) and w18 (+3.33 %, t 2.43), so the effect is real in direction but small against the market's daily noise (about 0.03 of a usual 5.3 % move).
- **F6:** The rebound belongs to the next day. The weighted excess return is +0.77 % (t 2.66) at 1 day, +0.71 % (t 1.98) at 2 days, +0.82 % (t 1.90) at 3 days and +0.50 % (t 0.95) at 5 days, so a longer horizon only adds noise.
- **F7:** The brief's light-volume side shows on up days in folds B and C, graded by volume. Up days in the lightest volume tercile are followed by −0.59 % next-day excess return (t −2.86, 660 days), the middle tercile by −0.35 % (t −1.74), and the heaviest by −0.13 % (t −0.49).

## Ideas
- `075-01.d3.b1_heavy-volume-outsized-fall-rebound` (from F2, F3, F4, F5, F6): The heavier a coin's volume on a day that closed lower, relative to its own average daily volume over the past 20 days, and the deeper that day's fall against its 30-day daily swing, the larger its rise over the next day, only after a fall larger than the coin's usual daily move over the past 30 days.
- `075-01.d3.b2_light-volume-up-day-fade` (from F7): The lighter a coin's volume on a day that closed higher, relative to its own average daily volume over the past 20 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
