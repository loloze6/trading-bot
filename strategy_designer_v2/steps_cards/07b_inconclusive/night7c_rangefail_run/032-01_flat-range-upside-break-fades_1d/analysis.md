---
line: 7.b inconclusive
backtest: 032-01_flat-range-upside-break-fades_1d
idea tested: 032-01_flat-range-upside-break-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5459 USD
---
## Findings
- **F1:** Step 5's result is on the opposite side from the idea's prediction. The mean short-side unusual 10-day move is -4.35 % (t -1.97 over 118 days, 136 cases), so after the breakout the coin keeps rising rather than falling back. In folds B and C the short cases lose even more clearly at shorter horizons: -3.8 % at 3 days (t -2.33) and -6.0 % at 5 days (t -2.74), on 74 cases over 61 days.
- **F2:** Fresh closes above the prior 60-day high in trendless coins (efficiency ratio at or below 0.3, cases at least 10 days apart) are followed by a rise above the coin's drift. The rise is +7.4 % over 10 days (t 1.63, 52 cases, 40 days) and +8.6 % over 20 days (t 2.03, 39 cases, 29 days). Breakouts in trending coins (ratio above 0.3) number only 7, so the brief's comparison between trendless and trending coins cannot be made here.
- **F3:** The size of the overshoot does not grade the outcome in either direction, so the "larger break, larger give-back" part of the idea has no support. Step 5's slope on the raw overshoot is -0.0022. In folds B and C the short side's move by overshoot tercile is -6.2 %, -0.1 % and -4.9 %. The slope of the 20-day move on the overshoot is -0.32 (t -0.59, 35 cases).
- **F4:** The continuation is uneven and partly carried by a few large moves. XRP alone averages +46 % over 10 days on 6 cases; without XRP the 10-day rise is +2.7 % (t 0.80, 37 cases) and the 20-day rise +5.4 % (t 1.36). Window w12 goes against the rest (-16 % over 10 days). Only 51–54 % of cases rise over 10 days, but 70 % rise over 20 days.
- **F5:** The continuation tends to be larger the flatter or tighter the range the coin broke out of, but this grading is weak:
- **F6:** The fade cannot pay as tested. Its move per case is -5.53 % total and -4.35 % unusual, against a cost of 0.19 % per trade. The book's Sharpe is -0.56 and its yearly return -3.5 % over 7.94 years.

## Ideas
- `032-01.b1_flat-range-upside-breaks-continue` (from F1, F2, F4, F5): In a coin whose price has gone nowhere over the past 60 days, a daily close above the prior 60-day high is followed by a further rise over the next 20 days. The narrower and flatter the 60-day range it broke out of, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
