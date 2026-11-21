---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend
line: 7.b inconclusive
backtest: 017-03_postsettle-recovery-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a 3-day rise, the return over the next 8 hours from each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the larger the coin's 3-day return, the larger that return.
Consequence: If confirmed, a trader would hold a rising coin through a settlement for 8 hours rather than 2, where the recovery shows more clearly.
Why:
- F1: The test's own result points the way the idea predicts but falls short of the bar. On the 25,701 settlement entry cases, the slope t on the forecast is 1.52 and the forecast-weighted mean excess 2-hour return is +3.5 bp. The forecast quintiles rise almost steadily, from +1.4 bp (t 0.79) in the lowest to +5.0 bp (t 2.09) in the highest.
- F5: The effect strengthens with a longer horizon than the plan's 2 hours. On the same cases the forecast slope t goes 0.20, 1.52, 1.97 and 2.20 at 1, 2, 4 and 8 hours, and the raw-rise slope t is 2.23 at 8 hours. It runs against the market in one year: in 2022 the slope t is -3.00 on the forecast and the mean is -7.4 bp.
