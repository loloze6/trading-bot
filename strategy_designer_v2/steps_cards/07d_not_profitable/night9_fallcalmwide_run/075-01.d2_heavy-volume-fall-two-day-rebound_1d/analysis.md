---
line: 7.d confirmed, not profitable
backtest: 075-01.d2_heavy-volume-fall-two-day-rebound_1d
idea tested: 075-01.d2_heavy-volume-fall-two-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4161 USD
---
## Findings
- **F1:** The Calmar fails because the book is long on almost every down day whatever its volume: it is in a position on 83 % of coin-days and its daily returns correlate 0.77 with the coins'. On its 40 worst days it lost 5.0 % on average while the coins fell 11.4 %, and its chained deepest fall is -23.9 %. The four windows where the coins collapsed (w7, w9, w14, w16: coin falls of -43 % to -61 %) gave book falls of -20 % to -24 %.
- **F2:** The effect lives almost entirely in the strongest case. Down days with a forecast of 15 or more have a mean excess 2-day return of +1.95 % (t 4.36, 488 cases) and a total move of +2.40 %, about 11 times the 0.22 % round-trip cost. Down days with a forecast under 7 give -0.20 % (t -0.45, 1316 cases), and forecasts of 7 to 15 give +0.18 % to +0.56 % with t under 1 (1168 cases).
- **F3:** An unsized 2-day hold, after the 0.22 % cost, shows the same split:
- **F4:** Inside a rising 60-day trend (above +10 %), heavy-volume down days (forecast 12 or more) are followed by an excess 2-day return of +3.43 % (145 cases). Down days without heavy volume in the same rising trend give only +0.23 % (468 cases), so the rising condition alone is not the effect. In a falling trend the two groups give +0.18 % against -0.44 %, and in a choppy trend -1.83 % against -0.74 %. This fits the brief's theory: in a rising market a heavy-volume down day is mostly forced liquidation of crowded longs, which is absorbed and repaid.
- **F5:** Heavy-volume down days have a positive mean excess 2-day return in 8 of the 12 explored windows. Ordinary-volume down days are positive in only 5 of 12, and they make up most of the book's losing exposure in w7, w9 and w14 (-1.97 %, -1.44 %, -2.42 %).
- **F6:** The edge holds over a longer hold. After down days in each coin's top volume third, the coin rose +1.97 % over 2 days and +2.83 % over 5 days. After down days in the bottom third it rose +0.56 % and +1.64 %.

## Ideas
- `075-01.d2.d1_extreme-volume-down-day-rebound` (from F1, F2, F3, F5): The heavier a coin's volume on a day that closed lower, relative to its own average daily volume over the past 20 days, the larger its rise over the next two days. The rise comes from the days whose volume stands far above that average, while down days of ordinary volume are followed by no rise.
- `075-01.d2.d2_rising-market-heavy-volume-dip-rebound` (from F4, F1, F2): In a rising market, the heavier a coin's volume on a day that closed lower, relative to its own average daily volume over the past 20 days, the larger its rise over the next two days.
- `075-01.d2.d3_heavy-volume-fall-five-day-rebound` (from F6, F2): The heavier a coin's volume on a day that closed lower, relative to its own average daily volume over the past 20 days, the larger its rise over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
