---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close return, measured against its 20-day volatility of daily returns, is followed by a move the other way over the next 3 days. After a Sunday fall the coin beats its normal drift, after a Sunday rise it falls behind, and the larger the Sunday move, the larger the move back.
Consequence: Lean against the Sunday move on both sides for the first three days of the week: buy after a Sunday fall and lighten or short after a Sunday rise.
Why:
- F1: Sunday is the only day whose move clearly reverses over the next 3 days. The correlation of the Sunday bar's vol-scaled return with the next 3 days' excess over drift is -0.094 (p < 0.0001, n = 4320). Every other weekday lies between -0.021 and +0.051.
- F2: The Sunday reversal works on both sides of the move. Sunday rises are followed by -1.02 % against drift over 3 days (t -5.48). Sunday falls are followed by +0.97 % (t +4.67).
- F3: Across Sunday quintiles of the scaled return, the next 3 days' excess falls from +1.37 % (t 3.86) through +1.11 %, -0.54 % and -1.17 % to -0.97 % (t -3.05) at the top. The effect is graded across the whole range but flattens among the largest rises, which matches the tested short-only plan's weighted correlation of -0.001.
- F4: The Fri-to-Sun two-day weekend move, scaled the same way, predicts nothing. Its quintiles give +0.43 %, -0.07 %, -0.56 %, -0.14 % and +0.13 %, all with |t| ≤ 2.1. The reversal belongs to Sunday's own bar.
