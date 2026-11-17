---
line: 7.a not observable
backtest: 013-03_breakout-above-high-continues_1d
idea tested: 013-03_breakout-above-high-continues
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1975 USD
---
## Findings
- **F1:** Only 10 of the 526 non-overlapping 30-bar grid bars had a forecast above 0, against the plan's minimum of 30, because only 237 of 17,044 bars (1.4%) closed above the prior 365-bar high, spread over about 152 short break episodes.
- **F2:** Breaks are rare on every coin, so no one coin carries the sample: break bars are 2.4% of bars on BTC (69) and ETH (70) but only 0.7% to 1.1% on LTC (23), XMR (25), XRP (18) and ZEC (32), giving 2, 3, 1, 0, 1 and 3 grid cases.
- **F3:** Breaks cluster in bull years and vanish elsewhere: 0 grid cases in 2018, 2019 and 2022; 3 in 2020, 2 in 2021, 1 in 2023, 2 in 2024 and 2 in 2025. Nine of the 24 windows (w1–w4, w7–w9, w14, w16) have no break bar at all.
- **F4:** The windows average 122 bars, so the 30-day horizon allows only about 4 grid points per window, 526 in all. The grid count is set by calendar time, so another bar size would give the same number of cases.
- **F5:** The outcome varies widely from case to case: the excess 30-bar return on break grid bars has a mean of 0.229 and a standard deviation of 0.752, against 0.313 for all grid bars. With 10 cases, the slope t of 5.18 rests on very few points. The forecast on those bars has a mean of 2.07, a standard deviation of 3.21 and a maximum of 10.7, so a handful of large breaks dominate.
- **F6:** About 0.07 grid cases occur per coin-window (10 over 143). Fold D (w19–w24) runs a little higher, at about 0.11 (4 over about 36).
- **F7:** Adding every coin available still falls short of 30:

## Ideas
- No ideas: The plan needs at least 30 break grid cases. The default data gives 10 (F1), and adding every available coin on daily bars across all folds would give only about 21 to 27 (F6, F7). A finer bar size adds none, because the 30-day grid is fixed in calendar time (F4). So no available data can show this idea either way.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
