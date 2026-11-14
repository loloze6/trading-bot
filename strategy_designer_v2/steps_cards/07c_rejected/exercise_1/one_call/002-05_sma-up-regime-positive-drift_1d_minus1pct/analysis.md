---
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
idea tested: 002-05_sma-up-regime-positive-drift
step 5: rejected
step 6: none
mode: one call
explorations: 2
cost: 0.2167 USD
---
## Findings
- **F1:** On BTCUSD daily bars, the 290 bars inside the 50-over-200 SMA stretch had a mean next-bar return of -0.85% against -0.03% on the 434 bars outside it (Welch t -4.14). Only 27% of in-stretch next bars closed up, against 48% outside, and the in-stretch median next bar was -1.06% against -0.06%.
- **F2:** The negative drift holds in every window that has in-stretch bars. The in-stretch mean was -1.76% in w1 (13 bars), -0.68% in w4 (82), -1.05% in w5 (122) and -0.70% in w6 (73). The out-of-stretch bars of the same windows averaged +0.94% (w4) and +0.62% (w6).
- **F3:** By year, the in-stretch mean was -1.76% in 2022 (13 bars) and -0.85% in 2023 (277 bars). The 2023 out-of-stretch bars averaged +0.76%, so the stretch underperformed even in a rising year.
- **F4:** The size of the forecast does not grade the effect. In-stretch forecast quartiles had means of -1.19%, -0.85%, -0.54% and -0.97%, and the correlation of forecast with next-bar return was 0.02.
- **F5:** The stretch's age does not change the effect either. Mean next-bar returns were -0.96% in its first 10 bars, -1.31% at bars 11–30, -0.32% at bars 31–60 and -1.14% after 60, so the drift is present from the cross onward.
- **F6:** The whole in-stretch loss sits in the gap from the close to the next open. That gap averaged -1.00% in-stretch against -0.001% outside, while the next bar's open-to-close averaged +0.11% in-stretch against -0.03% outside.
- **F7:** Price fell over the prior 20 bars on 220 of the 246 in-stretch bars, while the long average stayed above. Those 220 bars averaged -0.78% next bar, and the 26 bars after a rising 20 days averaged -1.01%.
- **F8:** The pattern is unusually even, which suggests a planted -1%-per-bar effect (the record's name ends in "minus1pct"); a reader should treat the result as a test case more than a market fact. Friday in-stretch bars had a next-bar sd of only 0.9% and 12% up bars. No trades were recorded.

## Ideas
- `002-05_sma-up-regime-positive-drift.c1_golden-cross-stretch-drifts-down` (from F1, F2, F3, F5): On a single coin's daily bars, while the 50-day SMA is above the 200-day SMA, the next day's close-to-close return is negative on average and down days outnumber up days, from the first bar after the up cross onward.
- `002-05_sma-up-regime-positive-drift.c2_in-stretch-loss-in-gap` (from F6, F8): On a single coin's daily bars, while the 50-day SMA is above the 200-day SMA, the drop comes in the gap from one day's close to the next day's open, and the next day's open-to-close return is flat to slightly positive.
- `002-05_sma-up-regime-positive-drift.c3_falling-price-above-crossed-averages` (from F7, F1): On a single coin's daily bars, when the 50-day SMA is above the 200-day SMA but the close is below its level of 20 bars earlier, the next day's return is negative on average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
