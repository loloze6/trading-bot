---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose from Saturday close to Sunday close, measured against its 20-day volatility of daily returns, falls behind its normal drift over the next 2 days: the larger the Sunday rise against the coin's recent Sunday moves, the larger the shortfall.
Consequence: Do not buy a coin at the Sunday close after it rose on Sunday, and treat the rise as a reason to stay out or lightly short through Tuesday.
Why:
- F1: The test's main measure is on the predicted side, with a |forecast|-weighted 3-day shortfall of +0.92 % and t 3.56 over 2559 Sunday rises, but its grading check failed (correlation -0.001); the shortfall is flat across forecast quintiles (+0.76 %, +1.59 %, +0.75 %, +0.88 %, +1.10 %, about 437 cases each, mean |forecast| rising from 1.3 to 18.4), so the cases reverse by about the same amount whatever the size of the rise.
- F2: Weighed by the raw scaled Sunday rise, the picture is the same: the 3-day shortfall is +0.97 % for rises of 0 to 0.5 vol (n 1040, t 3.8), +0.96 % for 0.5 to 1 (n 637, t 3.1) and +1.39 % for 1 to 1.5 (n 284, t 2.9), with no growth above that (t under 0.8); the effect is the sign of Sunday's move, not its size.
- F4: The reversal is specific to Sunday's own bar. Rises on Tuesday to Saturday do not reverse (3-day excess from -0.49 % to +0.11 %, Thursday and Friday rises continue at t -2.2 and -2.9); only Monday rises reverse a little (+0.59 %, t 3.1). Taken over the 2-day Saturday-plus-Sunday return, the reversal disappears (quintiles of its size from -0.02 % to +0.27 %, all |t| < 0.8).
