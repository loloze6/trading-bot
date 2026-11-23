---
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4257 USD
---
## Findings
- **F1:** When 24-hour volatility is at or above its 30-day average, the next 24-hour excess return moves against the coin's past 24-hour return, scaled to the usual move, and it moves in steps: the lowest decile of that past return gives +1.45 % (t 5.0), then +0.61 % (t 2.6), +0.52 % (t 2.3) and +0.30 % (t 1.4), down to −0.43 % (t −1.8) and −0.61 % (t −3.5) in the 8th and 9th deciles, with 605–606 non-overlapping cases per decile.
- **F2:** For past 24-hour moves larger than 0.7 of the usual daily move, the reversal grows with how high volatility runs against its 30-day average: +0.31 % (t 2.5, 1628 cases) at a ratio of 1–1.3, +0.61 % (t 3.7, 1167) at 1.3–1.7, +0.99 % (t 4.0, 720) at 1.7–2.5 and +1.50 % (t 2.9, 299) above 2.5; smaller past moves give about 0 (t −0.04 to 0.42) below a ratio of 2.5.
- **F3:** This volatile-regime 24-hour reversal holds in each of the 6 coins (+0.47 % to +0.81 %, t 2.2 to 3.3) and is positive in 7 of 8 years (2024: −0.08 %, t −0.4). The falling side holds in both halves of the windows (w1–w12 +0.77 %, t 4.7, 919 cases; w13–w24 +0.94 %, t 4.2, 976 cases), but the rising side fades in the later half (+0.55 %, t 3.3, then +0.24 %, t 1.2).
- **F4:** Outside raised volatility the reversal is absent: with the ratio below 1, the most-fallen past-24-hour quintile gives +0.09 % (t 0.6, 1225 cases) and the most-risen quintile −0.04 % (t −0.3, 1273 cases).
- **F5:** The single sharp hour that was tested carries less than the day's move. In raised volatility, hours falling more than 3 usual hourly moves give +2.25 % (t 3.7) but only 185 grid cases, and falls of 1–2 moves give +0.61 % (t 2.9, 788). The tested measure's cases averaged +0.09 % (t 1.58, 9538), about half the 0.19 % cost of a trade, against +0.6 % to +1.5 % per case for the large 24-hour moves in F1–F2.
- **F6:** Apart from the idea, the 1-hour returns over 21:00–23:00 UTC average +0.055 % (t 6.7, 17403) and +0.044 % (t 5.7, 17417) against an all-hour mean near +0.005 %. This is positive in all 6 coins (t 3.0–4.4), in both halves (t 3.3 and 8.5) and in 7 of 8 years (2022 −0.02 %). At about 0.1 % over the two hours it is below the cost of a trade, and it falls at no funding clock time.
- **F7:** The weekday of the 24-hour grid cell matters: Friday's cells return +0.50 % above the coin's average (t 4.9, 2235), and Monday's (−0.33 %, t −2.9) and Thursday's (−0.39 %, t −3.2) return less. This is one of many angles looked at, and no grading was found for it.

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal.g1_volatile-day-move-reversal` (from F1, F3, F4, F5): While a coin's 24-hour volatility runs above its 30-day average, its return over the next 24 hours runs against its own 24-hour return. The larger that past 24-hour return in units of the coin's usual daily move, the larger the opposite move.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal.g2_rebound-grows-with-turbulence` (from F2, F3, F4): After a coin falls over its past 24 hours, it rises over the next 24 hours. The more its 24-hour volatility exceeds its 30-day average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
