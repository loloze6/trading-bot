---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday return (Saturday close to Sunday close) is reversed over the next 3 days, falls followed by rises and rises followed by falls, and the larger the Sunday move the larger the reversal. The reversal is larger the lower the weekend's volume stands against the coin's 20-day average volume.
Consequence: Trade against both weekend rises and weekend falls, leaning hardest on large moves made on thin weekend volume, and refuse such trades after heavy-volume weekends.
Why:
- F1: On Sunday bars, the Sunday return predicts the next 3 days in the opposite direction, with a coefficient of -1.90 % excess 3-day return per standard deviation of Sunday return (t -4.96, about 830 weekly cases). Across all days on the 3-day grid the same reversal is only -0.41 % per standard deviation (t -2.03, 2288 cases), so weekend moves reverse several times more than weekday moves.
- F2: The Sunday reversal is graded both ways: the bottom Sunday-return quintile is followed by +1.49 % excess over 3 days (t 1.97) and the top quintile by -1.29 % (t -1.81). The tested idea kept only the long side and weighted it by the volatility ratio, and the volatility-ratio quintiles on the 3-day grid show no ordered pattern (-0.51 %, -0.18 %, +0.03 %, +0.98 %, +0.07 %; regression slope t 1.36).
- F3: The Sunday reversal weakens as weekend volume rises against the coin's 20-day volume. The interaction of Sunday return with weekend volume surprise is +0.95 % per standard deviation squared (t 3.17), so low-volume weekends reverse most, as the brief's second prediction says.
