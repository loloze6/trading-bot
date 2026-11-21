---
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3159 USD
---
## Findings
- **F1:** The test's result is near zero, not merely short of the bar. On 687 cases the mean 20-day excess return is +0.14 % (t 0.12; the step 5 verdict gives +0.35 %, t 0.30). At other horizons the same cases stay near zero too: 5 days −0.02 % (t −0.06), 10 days +0.33 % (t 0.55), 40 days +2.7 % (t 1.29). The main measure therefore cannot reach the bar by adding data.
- **F2:** The effect depends on the coin's prior trend. Breakouts taken while the 30-day return was positive gain an average of about +5.5 % over 20 days beyond drift (299 cases: lower half of the forecast +3.0 %, t 1.71; upper half +8.0 %, t 1.92). Breakouts taken while it was zero or negative lose −3.2 % (237 cases, t −2.68). The pooled test averages these two groups to zero.
- **F3:** The rise grows with the 30-day trend, and with the distance from the 50-day average up to a point. By prior 30-day return terciles, the 20-day excess is −2.9 % (t −2.06), +2.9 % (t 1.26) and +4.5 % (t 1.49); at 40 days it is −4.3 %, +6.4 % and +7.7 %. By distance from the 50-day average it is −5.0 % (t −2.73), +4.6 % and +1.2 %.
- **F4:** The idea's own grading (touches times margin) is not monotonic over all cases. By raw quartile the 20-day excess is +0.0 %, −1.6 %, +5.1 % and −2.8 %, with a Spearman correlation of −0.07. Inside positive-trend cases, though, the upper half of the raw value beats the lower half (+8.0 % against +3.0 %).
- **F5:** The supporting check could not run. The capped forecast sits at its maximum of 20 for more than half of the 827 signal bars (median 20), so a strict median split put 0 cases in the upper half. The grading in the forecast is mostly lost to the cap.
- **F6:** The result is drowned by the market's own years. Excess is −13.9 % in 2018 (76 cases, t −5.52) and −5.6 % in 2022 (83 cases, t −3.05), against +5.4 % in 2020 and +4.7 % in 2024 (t 1.79 and 1.81). Every coin's pooled mean is insignificant, between −1.7 % and +2.9 %. In positive-trend cases all 6 coins are positive, from +1.8 % to +13.9 %.
- **F7:** Cost is not the obstacle. The total move per case is +2.84 % against a round trip of 0.19 %, 14.7 times the cost, and the positive-trend subset's unusual move of about 5.5 % would be about 29 times it.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b1_breakout-continues-within-uptrend` (from F1, F2, F3, F4, F6, F7): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 20 days, only while its 30-day return is positive. The more times the level held, the further the close above it, and the larger that 30-day return, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails` (from F2, F3, F6): When a coin closes above a price where it turned down several times in the past 90 days after its 30-day return was negative, it tends to fall back over the next 20 days. The deeper that 30-day fall, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
