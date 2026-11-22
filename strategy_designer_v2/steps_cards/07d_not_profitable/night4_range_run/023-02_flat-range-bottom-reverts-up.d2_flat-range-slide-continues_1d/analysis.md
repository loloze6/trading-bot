---
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3622 USD
---
## Findings
- **F1:** The deepest 10-day falls are followed by rebounds rather than further falls, so the graded driver is backwards exactly where the book is largest. On mean-reversion grid bars, a forecast below -10 is followed by +0.64 % over 5 days (+0.07 % above drift, n=296). Forecasts between -10 and -5 are followed by -0.77 % (-1.36 % against drift, n=241). Forecasts between -5 and -2 are followed by -0.78 % (-1.36 %, n=161). That is why the slope's t is -0.02.
- **F2:** The book loses on the trades themselves, not mainly on fees. All 2907 trades are shorts, averaging -1.54 % gross and -1.64 % net. Trades entered at a forecast below -10 lose the most: -1.84 % gross, n=1570. Bars held at a forecast below -10 (mean position -0.81) lose 0.23 % a bar, while bars held at -10..-5 gain 0.11 %.
- **F3:** Among the active shorts with 60 days of history, the next 5 days fall more than drift only when the coin's 60-day return is down. Below -20 % the excess is -4.19 % (t -4.9, n=95); between -20 % and -5 % it is -2.19 % (t -2.2, n=78). Between -5 % and +5 % it is +0.06 % (t 0.06, n=51), and above +20 % it is -1.59 % (t -1.0, n=81). The r60 slope is +0.032 (p 0.064).
- **F4:** Once the 60-day return is known, the 10-day fall adds nothing. With a 60-day return below -20 %, forecasts below -10 give -4.36 % against -4.05 % for milder ones. With a 60-day return above +20 %, the stronger forecasts are followed by +1.34 % against drift, a rebound against the short, versus -2.43 % for milder ones.
- **F5:** Closes deep in the bottom of the 30-day range continue down more than closes nearer the middle. The lowest quartile of range position (0.02–0.20) is followed by -2.52 % against drift (n=143), against -0.80 % to -1.19 % for the other quartiles.
- **F6:** Being short coins that drift up costs the book about 0.023 % a day; the drift part runs from -0.013 % to -0.025 % a day across coins. The total move per case is -0.04 %, so the trade earns nothing before a 0.19 % cost. Mean daily return is -0.026 %, and timing is negative in 13 of 24 windows (for example -0.10 % a day in w10 and w11).

## Ideas
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.d1_flat-slide-inside-decline` (from F1, F3, F4, F6): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 10 days, the more it falls over the next 5 days, only while its 60-day return is negative, the more so the deeper that 60-day fall.
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.d2_flat-range-long-decline-continues` (from F3, F4, F6): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 60 days, the more it falls over the next 5 days.
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.d3_range-bottom-pin-continues-down` (from F5, F2): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the closer its close sits to the bottom of that 30-day range, the more it falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
