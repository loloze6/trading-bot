---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close return, measured against its 20-day volatility of daily returns, is followed by a move the opposite way over the next 3 days: the larger the Sunday rise, the further the coin falls behind its normal drift, and the larger the Sunday fall, the further it runs ahead of its normal drift.
Consequence: Lean against the direction of a coin's Sunday move for the first three days of the week, short after a Sunday rise and long after a Sunday fall, more so the larger the move.
Why:
- F1: The test's main measure is on the predicted side, with a |forecast|-weighted 3-day shortfall of +0.92 % and t 3.56 over 2559 Sunday rises, but its grading check failed (correlation -0.001); the shortfall is flat across forecast quintiles (+0.76 %, +1.59 %, +0.75 %, +0.88 %, +1.10 %, about 437 cases each, mean |forecast| rising from 1.3 to 18.4), so the cases reverse by about the same amount whatever the size of the rise.
- F3: The reversal also holds on the other side: Sunday falls are followed by a 3-day gain over drift of +0.97 % (n 2125, t 4.67), against +1.02 % shortfall after Sunday rises (n 2186, t 5.48); across all Sundays the scaled Sunday return correlates -0.088 with the next 3-day excess return (about 4320 cases), against +0.013 on the other weekdays.
- F4: The reversal is specific to Sunday's own bar. Rises on Tuesday to Saturday do not reverse (3-day excess from -0.49 % to +0.11 %, Thursday and Friday rises continue at t -2.2 and -2.9); only Monday rises reverse a little (+0.59 %, t 3.1). Taken over the 2-day Saturday-plus-Sunday return, the reversal disappears (quintiles of its size from -0.02 % to +0.27 %, all |t| < 0.8).
- F5: The two-sided Sunday reversal is present in every year, with 3-day reversal +1.60 % (2018, t 2.5), +1.22 % (2019), +1.49 % (2020), +1.92 % (2021), +0.19 % (2022, t 0.6), +0.34 % (2023, t 1.4), +1.67 % (2024, t 5.1) and +0.50 % (2025, t 1.8). It is weakest only on the smallest Sunday moves (+0.34 %, t 1.2, lowest |scaled| quintile, against +1.05 % to +1.26 % in the others).
