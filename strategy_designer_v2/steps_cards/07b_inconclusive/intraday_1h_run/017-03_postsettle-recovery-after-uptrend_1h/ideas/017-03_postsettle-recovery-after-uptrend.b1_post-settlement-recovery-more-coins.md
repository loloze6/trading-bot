---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend
line: 7.b inconclusive
backtest: 017-03_postsettle-recovery-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run up, the return over the 2 hours after each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the stronger the 3-day rise, the larger that post-settlement recovery.
Consequence: Longs who closed to avoid funding reopen after the payment, so the timing-driven dip reverses.
Why:
- F1: The test's own result points the way the idea predicts but falls short of the bar. On the 25,701 settlement entry cases, the slope t on the forecast is 1.52 and the forecast-weighted mean excess 2-hour return is +3.5 bp. The forecast quintiles rise almost steadily, from +1.4 bp (t 0.79) in the lowest to +5.0 bp (t 2.09) in the highest.
- F6: The test used only the 6 default coins. Hourly bars exist for 13 more coins, in folds A and D in full and partly in B and C, so the unchanged idea can be run on more independent cases.
