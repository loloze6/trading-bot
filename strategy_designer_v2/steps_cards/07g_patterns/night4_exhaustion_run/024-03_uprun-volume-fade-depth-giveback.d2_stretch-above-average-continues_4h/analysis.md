---
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3754 USD
---
## Findings
- **F1:** The coin's recent volume against its usual volume ranks what follows. The volume of the last day (6 bars) over the mean of the last 6 days (36 bars) sorts the next 3 days' excess return over the coin's drift from -0.55 % (lowest fifth, t -2.25, 1092 non-overlapping cases) through -0.37 %, -0.40 % and +0.20 % to +0.73 % (highest fifth, t 2.66, 1086 cases). That spread of 1.28 % is about three times the tested idea's unusual move of 0.44 %.
- **F2:** Volatility expansion shows a similar but uneven pattern. Cells where the last 6 days' 4h-return volatility runs highest against the last 60 days (top fifth, ratio about 1.49) are followed by +1.05 % excess over 3 days (t 3.17, 942 cases). The lowest fifth (ratio about 0.55) is followed by -0.67 % (t -2.67, 942 cases), but the middle fifths do not rise in order (+0.14 %, 0.00 %, -0.46 %).
- **F3:** The brief's volume-fade mechanism runs the other way. Among strong 3-day up-runs (top fifth of the past 3-day return over usual move), runs with rising volume were followed by +0.99 % excess (595 cases) and runs with fading volume by +0.45 % (347 cases). The gap of about 0.5 % is only about one standard error.
- **F4:** The tested distance-above-average effect is narrow and stops at the average. Above the 30-day average its slope has t 2.18 (2113 cases). It carries in XRP (t 2.02) and ZEC (t 2.00) only and is negative in LTC (-1.02) and XMR (-0.52). It is weaker when volatility is high (t 1.35) than when it is low (t 2.39). Positive-forecast cells lost in 2018 (-1.24 %) and 2022 (-1.25 %).
- **F5:** The book earns on days that extend an ongoing rally. Its best 1 % of days (174) came after the coin had already risen 22.9 % over the previous 3 days, against 0.3 % on all days. Its worst 1 % came after a 3-day change of -2.5 %.
- **F6:** Several angles showed nothing that stands out after about ten groupings:

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues.g1_volume-surge-precedes-rise` (from F1, F3): The more a coin's traded volume over the last day exceeds its average daily volume of the past 6 days, the more the coin rises over the next three days.
- `024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues.g2_volatility-expansion-precedes-rise` (from F2, F5): The more a coin's volatility of 4-hour returns over the past 6 days exceeds its volatility over the past 60 days, the more the coin rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
