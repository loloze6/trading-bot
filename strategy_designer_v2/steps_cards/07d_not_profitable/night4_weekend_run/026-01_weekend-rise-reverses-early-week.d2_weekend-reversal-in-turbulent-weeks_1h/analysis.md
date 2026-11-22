---
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
idea tested: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3989 USD
---
## Findings
- **F1:** The book loses because fees take more than the trades gain: summed over all coins and windows, the gain before costs is +0.295 while fees are 0.396, so the book ends at −0.101. The fees fall almost entirely at entry and exit, 0.199 on Sunday's entry bar and 0.179 on Tuesday's exit bars, against less than 0.02 on all other days.
- **F2:** The Monday–Tuesday hold itself pays: its gain before costs sums to +0.822 (Monday +0.081, Tuesday +0.741). Per case it is +0.122 % of the book over the 48 bars, with t 0.84 over 563 cases. Each case's entry and exit fees are about 0.072 % of the book. So the hold nets roughly +0.05 % per case before what happens after it.
- **F3:** 18.8 % of cases still hold a short after the 48 bars, and the book is short on about 12 % of all Wednesday-to-Sunday bars. Those bars lose −0.526 in summed gain, which is about two thirds of the Monday–Tuesday gain. The 86 trades held over 200 hours average −4.24 % each before fees.
- **F4:** The reversal is almost all on Tuesday. The book was short on a similar share of bars both days (27.7 % Monday, 26.9 % Tuesday), but Tuesday's summed gain is +0.741 against Monday's +0.081.
- **F5:** The size of the forecast does not grade the fall. Across the quartiles of the forecast's size, the 48-bar coin return after the signal runs −0.30 %, −0.97 %, +0.69 %, −1.78 %, not a steady rise in the fall. The step-5 check of the larger half minus the smaller half is −0.08 %. The forecast standardises the weekend's 48-bar gain over only 60 hourly bars, so it compares the weekend mostly with itself.
- **F6:** The effect exists and is large per case: an unusual fall of +0.84 % over 48 bars (strength 0.118, t 2.80, 557 cases), against a 0.19 % cost per trade. But it is earned against the coin's normal drift (−0.27 % in the short's direction), and the book is short only, with a mean position of −0.39 of the book at entry.

## Ideas
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.d1_weekend-rise-against-usual-moves` (from F5, F6, F1): When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days, only while the coin's 30-day hourly volatility is high against its own last 6 months, and the larger the weekend gain against the coin's usual two-day move over the last 30 days, the larger the fall.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.d2_weekend-reversal-lands-tuesday` (from F4, F2): When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days, only while the coin's 30-day hourly volatility is high against its own last 6 months, with the larger part of the fall coming on Tuesday, the second day, and the larger the weekend gain, the larger Tuesday's fall.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.d3_reversal-ends-after-tuesday` (from F3, F2, F6): When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days, only while the coin's 30-day hourly volatility is high against its own last 6 months, and from Wednesday over the next five days it returns to rising with its normal drift, the more so the larger the weekend gain was.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
