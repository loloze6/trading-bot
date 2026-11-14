---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
instruments: BTC/USDT
bar: 1d
period: fold A
---
Idea: While the 50-day SMA sits above the 200-day SMA, BTC's next daily bar has a smaller high-low range and a smaller spread of returns than bars where the 50-day SMA is below the 200-day SMA.
Consequence: A trader can take larger positions in the up-regime for the same risk, because the regime marks calmer bars rather than a directional edge.
Why:
- F9: In-stretch bars are quieter than out-of-stretch bars. The standard deviation of next-bar returns is 0.0235 against 0.0320, and the mean next-bar high-low range in w5/w6 is 0.029-0.033, against 0.035-0.060 in the out-of-stretch windows w2/w3.
- F2: With the gap removed, the next bar's open-to-close return in-stretch is +0.00113 against -0.00030 out-of-stretch, a difference of +0.00143 with Welch t = 0.69. The up-share is 0.476 in-stretch against 0.475 out. Intraday, the regime neither persists nor reverses.
- F4: The negative close-to-close drift shows the same size in every window that has in-stretch bars: w1 -0.0176 (n=13), w4 -0.0068, w5 -0.0105, w6 -0.0070. The gap is about -0.0100 in each. Open-to-close in-stretch varies by window: w1 -0.0076, w4 +0.0032, w5 -0.0005, w6 +0.0030.
