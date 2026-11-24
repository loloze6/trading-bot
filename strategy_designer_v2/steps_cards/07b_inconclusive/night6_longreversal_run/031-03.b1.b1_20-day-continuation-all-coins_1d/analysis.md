---
line: 7.b inconclusive
backtest: 031-03.b1.b1_20-day-continuation-all-coins_1d
idea tested: 031-03.b1.b1_20-day-continuation-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3886 USD
---
## Findings
- **F1:** The effect shows at the plan's 10-day horizon and fades on either side of it: forecast/10 × excess return has a mean of 0.0106 with t 1.53 at 10 days (3598 cases, 304 days), against t 0.99 at 5 days, t 0.58 at 20 days and t −0.29 at 30 days.
- **F2:** The continuation is concentrated where the 20-day and 60-day returns point the same way: there the directional excess 10-day return is +2.32 % (t 2.26, 1211 cases, 144 days), against +0.64 % (t 0.49, 551 cases, 117 days) where they disagree. Under the same split, an up move with a 60-day fall gives −0.14 % (t −0.07), while an up move with a 60-day rise gives +2.60 % (t 1.68).
- **F3:** The effect is barely graded, inside or outside agreement.
- **F4:** The plan's standardisation of the forecast against its own last 60 values dilutes the signal. Measured instead as the 20-day return over the coin's 60-day daily volatility, the same product reaches t 1.99, and its sign alone reaches t 2.18 (2986 cases, 255 days). Its correlation with the excess return is 0.075, against 0.050 for the plan's forecast.
- **F5:** The effect is mixed across coins and years.
- **F6:** Both sides carry the effect equally: after falls +1.00 % (t 1.14, 1851 cases), after rises +1.06 % (t 1.03, 1747 cases). One side alone would not sharpen the test.
- **F7:** The test already used every coin and every fold available on daily bars, so more of the same data cannot be added. Inside that data, the result's side and size (+0.69 % unusual move per case, strength 0.041, total move 2.7 times the 0.22 % trade cost) leave a clear answer only where the effect concentrates.

## Ideas
- `031-03.b1.b1.b1_aligned-20-day-continuation` (from F2, F1, F4, F6): The larger a coin's 20-day return, the more its price moves further in the same direction over the next 10 days, only while its 60-day return is on the same side as its 20-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
