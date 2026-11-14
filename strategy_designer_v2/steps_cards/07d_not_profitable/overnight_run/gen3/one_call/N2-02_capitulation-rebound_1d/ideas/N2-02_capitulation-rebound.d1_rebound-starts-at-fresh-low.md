---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-02_capitulation-rebound
line: 7.d not profitable
backtest: N2-02_capitulation-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is extremely far below its 200-day average, it rises over the next one to two weeks while the close is still within a few percent of its 5-day low. Once the close has already bounced well off that low, it tends to fall instead.
Consequence: Take the capitulation long only at extreme depth and while price sits near its recent low, and refuse it after the first sharp bounce.
Why:
- F2: A larger forecast earns more. Trade gross gain rises with entry forecast: 1.52% for forecasts 1–5 (n=113), 3.16% for 5–10 (n=173) and 5.74% for 10 and above (n=307). On non-overlapping 10-bar excess returns, forecasts 0–5 are negative (−0.0145, t −1.36, n=137; −0.0134, t −1.10, n=87) and forecasts of 10 and above are positive (+0.0206, t 0.90, n=69).
- F4: The rebound pays only near a fresh low. Active bars within 3% of their 5-day low have a mean 10-bar excess return of +0.0061 (t 0.49, n=170). Bars already more than 8% above that low have −0.0234 (t −1.96, n=93). Bars after a rising 3-day close have −0.0117 (t −1.17, n=145), against +0.0008 after a falling 3-day close (n=191).
