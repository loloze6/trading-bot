---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
instruments: BTC/USDT
bar: 1d
period: fold A
---
Idea: On a single coin's daily bars, while the 50-day SMA is above the 200-day SMA, the next day's close-to-close return is negative on average and down days outnumber up days, from the first bar after the up cross onward.
Consequence: A trader should refuse to treat a 50-over-200 stretch as a reason to hold long, and could treat it as a short-side context instead.
Why:
- F1: On BTCUSD daily bars, the 290 bars inside the 50-over-200 SMA stretch had a mean next-bar return of -0.85% against -0.03% on the 434 bars outside it (Welch t -4.14). Only 27% of in-stretch next bars closed up, against 48% outside, and the in-stretch median next bar was -1.06% against -0.06%.
- F2: The negative drift holds in every window that has in-stretch bars. The in-stretch mean was -1.76% in w1 (13 bars), -0.68% in w4 (82), -1.05% in w5 (122) and -0.70% in w6 (73). The out-of-stretch bars of the same windows averaged +0.94% (w4) and +0.62% (w6).
- F3: By year, the in-stretch mean was -1.76% in 2022 (13 bars) and -0.85% in 2023 (277 bars). The 2023 out-of-stretch bars averaged +0.76%, so the stretch underperformed even in a rising year.
- F5: The stretch's age does not change the effect either. Mean next-bar returns were -0.96% in its first 10 bars, -1.31% at bars 11–30, -0.32% at bars 31–60 and -1.14% after 60, so the drift is present from the cross onward.
