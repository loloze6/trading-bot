---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's one-day return on a Saturday or a Sunday, measured against its own recent daily volatility, is reversed over the next day. The larger the weekend day's rise, the larger the next day's fall, and the larger its fall, the larger the next day's rise. A Sunday's move keeps being reversed over the following two days, in proportion to its size.
Consequence: Hold the fade of a Sunday move through Tuesday's close rather than unwinding it on Monday, so one round of fees buys two days of reversal.
Why:
- F5: The reversal of a Sunday move keeps running past Monday.
- F2: Fees cost about half the weekend gain. Saturday bars earn 0.000756 gross against 0.000384 in fees. Sunday bars earn 0.001200 gross against 0.000612 in fees. Monday's unwind adds another 0.000449 per bar in fees.
- F1: The book misses its gain targets mostly because of fees and because it is flat most of the time. It holds almost nothing from Monday to Friday (mean absolute position about 0.005, against 0.32 to 0.39 on weekend bars). Its gross gain is 0.000278 per bar, of which fees take 0.000207. This leaves a daily mean of 0.000194, against 0.001389 for holding the coins, with a daily standard deviation of 0.0079 and 24% of days at exactly zero.
