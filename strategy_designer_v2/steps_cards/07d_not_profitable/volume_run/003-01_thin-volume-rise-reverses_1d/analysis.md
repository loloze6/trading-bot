---
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses_1d
idea tested: 003-01_thin-volume-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3581 USD
---
## Findings
- **F1:** The book's gain is lost in the moderately thin band (volume 0.5 to 0.75 of its 30-day average, regime chop): its 854 signal bars average -0.001019 per bar and its 682 trades average -1.51 % after fees, while the very-thin band (0.5 or less, regime mean_reversion) earns +0.000891 per bar on 955 signal bars and -0.44 % per trade.
- **F2:** Inside the very-thin band the giveback is graded the way the idea says: next-day excess return is -0.0036 for forecasts of 8 to 15 (111 bars) and -0.0064 for 15 to 20 (191 bars). In the moderately thin band the same forecast sizes are followed by rises, +0.0034 (121 bars) and +0.0041 (104 bars), so the larger short there loses more.
- **F3:** Signal bars that come after a 30-day fall of more than 10 % are followed by a next-day excess return of -0.0043 (t -2.74, 942 bars). After flat or rising 30-day returns it is near zero: +0.0005 (563), -0.0009 (551) and -0.0003 (865).
- **F4:** The book earns in falling years and loses in rising ones: per-active-bar gain is +0.00042, +0.00076 and +0.00091 in 2018, 2019 and 2022 (coin next-day means -0.0043, -0.0018, -0.0040), against -0.00063, -0.00173 and -0.00068 in 2020, 2021 and 2025 (coin means +0.0043, +0.0048, +0.0050).
- **F5:** Being short against the coins' rise (coin daily mean +0.00119) costs -0.000042 per bar. Timing adds only +0.000024 and fees take 0.000069 per bar, which leaves a mean daily book return of -0.0000885 and a Sharpe of -0.58.
- **F6:** On the non-overlapping 5-day grid, rises above 2 usual daily moves on volume over 1.25 times the 30-day average carry on, with a 5-day excess of +0.032 (t 1.94, 80 cases). Thin rises of 1 to 1.5 usual moves show no giveback: +0.033 (17 cases) at volume 0.5 or less, and +0.021 (45 cases) at 0.5 to 0.75.

## Ideas
- `003-01_thin-volume-rise-reverses.d1_thin-rise-reverses-in-downtrend` (from F3, F4, F5): When a coin rises sharply over one day on volume well below its own 30-day average daily volume, it gives back part of that rise over the next 5 days, only while the coin has fallen over the past 30 days. The larger the rise, the thinner its volume against that average and the deeper the 30-day fall, the larger the giveback.
- `003-01_thin-volume-rise-reverses.d2_giveback-scales-with-thinness` (from F1, F2): When a coin rises sharply over one day on volume well below its own 30-day average daily volume, it gives back part of that rise over the next day. The giveback grows the further below that average the volume lies, and it is largest for the sharpest rises on the very thinnest volume.
- `003-01_thin-volume-rise-reverses.d3_heavy-volume-rise-continues` (from F6, F5): When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days. The larger the rise and the heavier its volume against that average, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
