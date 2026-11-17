---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high against its own volatility over the past 60 days, its Saturday or Sunday vol-scaled move is reversed more strongly over the next day, in proportion to the move's size.
Consequence: Lean harder into weekend fades in turbulent stretches and scale them down when the coin is calm.
Why:
- F3: The weekend fade is larger when the coin's 20-day volatility is high against its own 60-day median. It is 0.0056 (t 3.96, n 2377) in the wildest third, against 0.0024 (t 2.88) in the calmest. The same weekday fade in the calm third is -0.0018 (t -2.71).
- F2: The weekend size-grading survives the volume weighting. Regressing the next-day excess return on z x relative volume gives a slope of -0.0017 (t -5.80), close in strength to z alone (slope -0.0041, t -6.31). The largest weekend rises (z>2) are followed by -1.52% (t -3.09, n 210), and z in 1 to 2 by -0.37% (t -1.86).
