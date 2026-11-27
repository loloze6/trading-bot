---
line: 7.b inconclusive
backtest: 074-01.b1.b1.b1.b1.d1.g2_width-and-depth-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.d1.g2_width-and-depth-bounce-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4133 USD
---
## Findings
- **F1:** The tested effect sits on the predicted side but just short of the bar. Its next-day short unusual move is +0.26 % with a day-clustered t of 1.88 over 6519 cases on 1426 days. On the folds shown (B, C) it is +0.46 % with t 2.05 over 2148 cases on 601 days.
- **F2:** The effect is carried by the depth of the 5-day loss and is absent elsewhere. By quintile of the 5-day return including the up day, the move is:
- **F3:** The strongest forecasts carry the result. The top fifth of |forecast| gives +1.61 % with t 2.95 (430 cases on 186 days). The other four fifths range from −0.15 % to +0.48 %, none with t above 1.36, and the correlation between forecast and the unusual move is −0.11.
- **F4:** Width helps less clearly than depth.
- **F5:** The effect is spent in one day, as the brief says. The unusual move is +0.46 % (t 2.05) over 1 day, +0.30 % (t 0.95) over 2 days and +0.24 % (t 0.68) over 3 days. It is also specific to up days: on falling-market down days the same short loses −0.32 % (t −1.38).
- **F6:** Where the agitation can be read (about 730 cases), the fade lives in agitated markets. Agitated: +1.00 %, t 1.97, 361 cases on 110 days. Calm: −0.52 %, t −1.07, 369 cases.
- **F7:** The effect is broad but not uniform across coins and periods.
- **F8:** Over all cases the size is too small to trade. The total move per case is +0.17 %, below the 0.22 % cost of a trade. The deepest-loss fifth (+1.98 %) and the strongest-forecast fifth (+1.61 %) are each several times that cost.

## Ideas
- `074-01.b1.b1.b1.b1.d1.g2.b1_still-down-bounce-fades-next-day` (from F2, F3, F4, F5, F8): In a falling market, an up day is followed by a fall over the next day, larger the wider its high-to-low range against the coin's average daily range over the past 20 days and the more the coin is still down over its 5-day return including that day, only while the coin is still down over its 5-day return including that day.
- `074-01.b1.b1.b1.b1.d1.g2.b2_agitated-downtrend-bounce-fade` (from F6, F2, F5): In a falling, agitated market, an up day is followed by a fall over the next day, larger the wider its high-to-low range against the coin's average daily range over the past 20 days and the more the coin is still down over its 5-day return including that day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
