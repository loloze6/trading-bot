---
line: 7.d not profitable
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
idea tested: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3081 USD
---
## Findings
- **F1:** Before fees the book earns less than it pays: mean hourly gross gain is 0.167e-4 against 0.239e-4 in fees, at 3.45 trades a day. Fees exceed gross on four of six coins, for example XMR at 0.134e-4 gross against 0.334e-4 in fees and ZEC at 0.088e-4 against 0.204e-4, so the mean daily return is -0.0002 and the Sharpe is -0.38.
- **F2:** The forward 3-day excess return is positive only for the most extreme moves. The top decile of signed 3-day return (mean +16.2%) gives +0.0154 (t 3.24, n 554) and the bottom decile (mean -14.3%) gives +0.0056 (t 1.25). The eight middle deciles sit between -0.0100 and +0.0016, with decile 4 (about -0.4% past move) at -0.0100 (t -3.45).
- **F3:** Only the top forecast quintile pays. It earns +0.0100 on the up side (forecast about 9.8, past +10.7%) and +0.0067 on the down side (forecast about 9.7, past -10.0%). The lower four quintiles average about -0.002, ranging from -0.0061 to +0.0013, yet they still get a long position.
- **F4:** The book is long almost all the time, with no non-zero forecast on only 234 of about 416,800 bars and an average allocation of about 0.25. Its gross gain comes mainly from up-move bars, 0.292e-4 against 0.037e-4 on down-move bars, while fees are the same on both sides (about 0.24e-4).
- **F5:** The book trails holding the coin in every year except the two falling ones. For example, 2020 gives book +0.00085 against coin +0.0042 a day and 2024 gives -0.00004 against +0.0024. In 2018 the book returned -0.0008 against the coin's -0.0035, and in 2022 -0.0013 against -0.0018.

## Ideas
- `016-01_up-grind-price-continuation.g1_big-moves-precede-rises.d1_extreme-moves-precede-rises` (from F1, F2, F3, F4): The larger a coin's absolute 3-day return, whether up or down, the more the coin rises over the next 3 days, only as far as that 3-day return exceeds the coin's typical absolute 3-day move over the past 60 days.
- `016-01_up-grind-price-continuation.g1_big-moves-precede-rises.d2_large-rises-keep-rising` (from F2, F3, F4): The larger a coin's 3-day rise relative to its typical absolute 3-day move over the past 60 days, the more the coin keeps rising over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
