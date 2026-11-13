---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-01_weekday-of-coming-bar
line: 7.g patterns
backtest: N2-01_weekday-of-coming-bar_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily bar falls more than its usual one-day move on volume well above its recent average, the next daily bar returns more than the coin's average day, because forced or panicked sellers exhaust themselves and price snaps back.
Consequence: A trader would take longs after high-volume selloff bars rather than refusing them as trend breaks.
Why:
- F1: After a down bar that falls more than one 20-bar standard deviation, the next bar beats the coin's mean daily return: +0.0048 (t 3.29, n 1302) for z in (-2,-1] and +0.0069 (t 2.58, n 476) for z ≤ -2. After a small up bar (z in (0,1]) the next bar lags the mean by -0.0021 (t -3.36, n 5275), and all six coins show that lag.
- F2: Heavy volume sharpens the rebound. A down bar of z ≤ -1 with volume above 1.5x its 20-bar average is followed by +0.0097 excess (t 4.05, n 677), against +0.0027 (t 1.86, n 1101) without the surge. Any down bar on a volume surge gives +0.0083 (t 4.82, n 1218), while an up bar on a surge gives -0.0007 (t -0.45, n 1282).
- F7: The rebound comes and goes by year: z ≤ -1 rebounds were strongest in 2020 (+0.0137, t 3.05) and 2021 (+0.0145, t 3.36) and near zero in 2019, 2024 and 2025. By coin it ranges from XMR at +0.0102 (t 3.51) to BTC at +0.0022 (t 0.89).
