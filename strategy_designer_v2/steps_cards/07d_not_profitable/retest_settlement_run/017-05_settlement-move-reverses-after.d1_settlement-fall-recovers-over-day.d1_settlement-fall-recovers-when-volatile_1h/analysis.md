---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4165 USD
---
## Findings
- **F1:** The effect is real only after an uptrend. On settlement bars with forecast ≥ 2, the 24-hour excess return is +0.24 % (t 2.69, 2758 cases) when the coin's 30-day return is positive, against −0.04 % (t −0.44, 2780 cases) when it is negative. Over 72 hours the same split is +0.92 % (t 3.42, 917 cases) against −0.14 % (t −0.52, 901 cases).
- **F2:** The book loses its gain in downtrends, which pulls it below holding (Sharpe minus holding −0.13). On bars in a position it earns 0.16 bp per bar when the 30-day return is negative and 0.86 bp when positive, with about the same allocation (0.52 vs 0.54). The uptrend bars carry 9.92 of its 11.77 summed bar gain, so 84 %.
- **F3:** The 30-day uptrend is not an effect of its own. On settlement bars without the signal (forecast < 2) it earns +0.04 % (t 0.60, 3859 cases) over 24 hours and −0.12 % (t −0.50, 1274 cases) over 72 hours. With the signal the same bars earn +0.24 % and +0.92 % (F1). This fits the brief's theory: after a run up, longs are the crowded, paying side, so the pre-settlement fall is the flow that reverses.
- **F4:** The effect grows with the signal inside an uptrend, as the idea says. With a positive 30-day return, forecasts above 10 give an excess return of +0.48 % (t 3.65, 1368 cases) over 24 hours and +1.60 % (t 4.05, 456 cases) over 72 hours. Forecasts from 2 to 5 give −0.11 % and −0.63 %.
- **F5:** The day is too short for the move to cover the cost; three days are long enough. Over 24 hours the total move per case is 0.23 %, against a trade cost of 0.19 %. Over 72 hours, strong uptrend cases make a total of +1.35 % (about 7 times the cost) and 1.97 % when the 7-day volatility ratio is also above 1 (t 3.24, 411 cases).
- **F6:** The 7-day trend gives the same split as the 30-day trend. For strong cases with a positive 7-day return the excess is +0.30 % over 24 hours (t 3.31, 2677 cases) and +0.87 % over 72 hours (t 3.29, 938 cases). With a negative 7-day return it is −0.09 % and −0.11 %.
- **F7:** The book's falls are close to the coin's own falls, which is why Calmar fails (0.15 against 0.75). The book is in a position on 72 % of bars, although the forecast is positive on only 4 % of them, because trades last 38 to 61 hours. Its window falls nearly match the coin's: w20 −29 % vs −29 %, w24 −34 % vs −39 %, w2 −43 % vs −58 %.
- **F8:** The volatility part of the idea works only together with the uptrend. In strong cases, a 7-day volatility ratio above 1 adds +0.20 % over 24 hours in a downtrend (t 1.23) and +0.39 % in an uptrend (t 2.70).

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile.d1_settlement-fall-recovers-in-uptrend` (from F1, F2, F3, F4, F5, F7, F8): After a coin's 30-day return has been positive, the rise over the 3 days after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the higher the coin's hourly volatility over the last 7 days stands against its volatility over the last 30 days.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile.d2_settlement-fall-after-weekly-rise` (from F6, F2, F3, F7): After a coin's 7-day return has been positive, the rise over the next day after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the higher the coin's hourly volatility over the last 7 days stands against its volatility over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
