---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
instruments: BTC/USDT
bar: 1d
period: fold A
---
Idea: In stretches where the 50-day SMA is below the 200-day SMA but has been above it within the same recent period (a down-cross that interrupts an up-trending phase), BTC's next daily bar closes up more often than in long, unbroken stretches below the 200-day SMA.
Consequence: A trader can treat a fresh down-cross after a recent up-stretch as a buyable dip rather than as the end of the trend.
Why:
- F5: Out-of-stretch next-bar returns are positive in the windows that also contain stretches: w4 +0.0094 with up-share 0.59, and w6 +0.0062 with up-share 0.54. In the windows with no stretch they are negative: w2 -0.0046 and w3 -0.0012. By year, out-of-stretch bars return +0.0076 in 2023 against -0.0022 in 2022.
- F3: The gap is tied to the bar on which the forecast is positive, not to the bar that follows. Transitions from in-stretch to out-of-stretch (1->0, n=2) still carry a gap of -0.0098. Transitions from out to in (0->1, n=2) carry -0.00002. Bars inside the stretch (1->1, n=288) carry -0.00999.
- F10: The coin falls in every window, from -0.18 in w3 to -0.73 in w5, the window that is 100% in-stretch. Yet the book beats it by +0.47 in w4 (+0.249 vs -0.226) and by +0.47 in w6 (+0.260 vs -0.213), and loses only -0.089 in w5 against the coin's -0.729. The book's value and the bar-close series diverge on the gapped bars.
