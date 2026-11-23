---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3662 USD
---
## Findings
- **F1:** The idea's gain comes entirely from wide days that close down. On non-overlapping 3-day grid cases, a down day with range above 1.7 times its 30-day mean range is followed by an excess 3-day return of +2.39 % (t 3.99, n 269). The same width on an up day is followed by −0.59 % (t −0.92, n 234). Over all wide days (range ratio above 1), down days give +0.71 % (t 2.26, n 936) and up days give −0.31 % (t −1.09, n 899).
- **F2:** On down days the effect grows with the range's width. The excess 3-day return is −0.54 % (t −1.15, n 388) at a ratio of 1–1.3, +0.81 % (t 1.43, n 279) at 1.3–1.7 and +2.39 % (t 3.99, n 269) above 1.7. On down days, the top quartile of fall size × width gives +0.93 % (t 2.36, n 599).
- **F3:** Wide down days are followed by a positive excess in five of six coins. XMR gives +1.19 % (n 154), ZEC +1.28 % (n 157), XRP +0.95 % (n 152), LTC +0.61 % (n 174) and BTC +0.19 % (n 149), while ETH is flat at −0.01 % (n 150). By year the effect is uneven: 2020 gives +3.12 % (t 3.23, n 110), and 2018 (−0.34 %) and 2022 (−0.51 %) are negative.
- **F4:** Strong recent rises continue, but only at the top. The 7-day return scaled by 30-day daily volatility (√7 × daily vol) has a top decile followed by an excess 3-day return of +1.40 % (t 3.13, n 501), and its ninth decile by +0.50 % (t 1.17). Deciles 0–7 lie between −0.61 % and +0.00 %, so the overall correlation is only 0.046.
- **F5:** The 14-day return grades the next 3 days more evenly. By quintile, the excess 3-day return rises from −0.30 % and −0.65 % (t −2.68) in the two lowest, through −0.34 %, to +0.38 % and +0.66 % (t 2.02) in the two highest, with about 1000 cases each.
- **F6:** The top-decile momentum cases are positive in six of eight years. They are strongest in 2024 at +2.10 % (t 3.08, n 144), 2021 at +1.93 % (t 2.25) and 2020 at +1.35 % (t 1.93), and negative in 2022 (−0.63 %) and 2023 (−0.11 %).
- **F7:** The book is mostly the market and a few days. Its daily returns correlate 0.72 with the coins' mean daily return. Its best 5 % of days sum to 298 % of its total gain and its worst 5 % to −275 %, which fits its Calmar failing at 0.64.
- **F8:** Other angles I looked at showed nothing clear given how many were examined. These were close location within the day's range (low-close days −0.34 %, t −1.56), the 1-day return quintiles (|t| < 0.9), volatility terciles (|t| < 0.5), weekday (largest is Saturday at +0.52 %, t 1.86) and per-coin forecast-positive cases (none with t above 1.6).

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only.g1_wide-down-days-rebound` (from F1, F2, F3): The more a coin's daily high-low range exceeds its 30-day average range on a day it closes lower, the higher its return over the next 3 days above its usual drift.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only.g2_strong-week-rises-continue` (from F4, F6): The larger a coin's 7-day rise measured against its daily volatility over the past 30 days, the higher its return over the next 3 days above its usual drift, the effect growing sharply among its strongest rises.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only.g3_two-week-return-carries-forward` (from F5, F4): The higher a coin's 14-day return, the higher its return over the next 3 days above its usual drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
