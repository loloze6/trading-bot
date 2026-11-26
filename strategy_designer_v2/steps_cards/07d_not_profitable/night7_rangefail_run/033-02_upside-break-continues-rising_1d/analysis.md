---
line: 7.d confirmed, not profitable
backtest: 033-02_upside-break-continues-rising_1d
idea tested: 033-02_upside-break-continues-rising
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5903 USD
---
## Findings
- **F1:** The book failed on Calmar alone (0.709 against 0.75; Sharpe 0.87 and every other measure passed), and its deepest fall in folds B, C (−8.5 %) is a slow bleed, not a crash. It took 253 days to reach its trough across w15 to w17, while holding the coins lost −27.7 % over the same stretch.
- **F2:** The idea's gain is earned in the first 5 days of a position and the book keeps positions far longer. Trades last 12.5 days on average (median 5, longest 121). Position-days aged 1 to 5 days earn +0.35 % a day (685 days), against about +0.00 % at 11 to 20 days (419 days) and +0.01 % beyond 40 days (928 days).
- **F3:** The aged part of positions carries the falls. In w15, the window of the deepest fall, position-days past day 5 lost −0.42 (summed daily gains) while the first 5 days gained +0.62. Aged days also lost in w7, w9, w13 and w14.
- **F4:** Cutting each position at 5 days, the idea's own horizon, repairs the failing measure on a rebuilt book (folds B, C, 0.095 % per change of position). Its Calmar rises from 1.39 to 1.53 and its deepest fall shrinks from −8.6 % to −6.3 %. Its Sharpe rises from 1.04 to 1.30, though its yearly return drops from +12.0 % to +9.7 %. Cutting at 10 days gives a Calmar of 1.53 and a deepest fall of −7.1 %.
- **F5:** Positions held while the coin's 60-day return is at or below +10 % earn nothing: −0.006 % a day over 716 days with the 60-day return below −10 %, and −0.06 % a day over 199 days between −10 % and +10 %. These are leftover aged positions, because fresh breaks in a choppy market still earn +10.7 % unusual over 5 days (6 cases, t 3.7).
- **F6:** The break works when it is fresh and fades when it repeats, in grades. With at most 2 closes above the 20-day high in the past 20 days, a break is followed by +8.7 % unusual over 5 days (22 cases, t 3.3). With 3 to 5 such closes it is +6.8 % (24 cases, t 1.6), and with 6 to 8 it is +0.1 % (9 cases).
- **F7:** The freshness condition is not an effect of its own. Without a break, the same few-prior-breaks bars earn −0.36 % over 5 days (898 cases, t −0.9). Among traded breaks, those with 5 or more breaks in the prior 10 days lost −5.3 % per trade (15 trades), against +6.2 % with none (208 trades). This fits the brief's theory: buying that has not yet finished is a property of a new break, while a coin that keeps re-breaking has already drawn its breakout buyers. Filtering on freshness alone did not lower the rebuilt book's deepest fall (−7.1 %, Calmar 1.29), so it belongs alongside the 5-day holding, not in place of it.
- **F8:** The size is not the obstacle. The total move of +2.34 % per case is 12.1 times the 0.19 % cost of a trade, and larger breaks earn more per trade: +1.1 %, +4.4 %, +9.0 % and +10.4 % mean net by quartile of the break's distance above the high.

## Ideas
- `033-02.d1_upside-break-five-day-hold` (from F1, F2, F3, F4, F8): When a coin closes above its 20-day high, it rises over the next 5 days, and it rises more the further the close sits above that high, with the rise completed within those 5 days of the break rather than continuing while the close stays above the range.
- `033-02.d2_fresh-upside-break-rises` (from F6, F7, F2, F5): When a coin closes above its 20-day high after few closes above that high over the past 20 days, it rises over the next 5 days, and it rises more the further the close sits above that high and the fewer such closes came before it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
