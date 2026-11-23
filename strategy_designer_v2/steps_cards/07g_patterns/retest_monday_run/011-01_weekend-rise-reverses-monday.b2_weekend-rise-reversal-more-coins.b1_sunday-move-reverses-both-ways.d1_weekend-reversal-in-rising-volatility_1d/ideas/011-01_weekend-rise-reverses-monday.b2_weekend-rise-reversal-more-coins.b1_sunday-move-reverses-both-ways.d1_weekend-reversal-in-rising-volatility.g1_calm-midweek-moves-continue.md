---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a calm market, where a coin's 20-day daily volatility is below its 60-day volatility, the coin's Wednesday move (its Tuesday-to-Wednesday close-to-close return) continues in the same direction over the next 2 days, and the larger the Wednesday move, the larger the continuation.
Consequence: A trader would follow a coin's Wednesday move into the end of the week in settled markets, and refuse to fade it.
Why:
- F1: In calm markets, where the 20-day volatility is below the 60-day volatility, a coin's Wednesday move continues over Thursday and Friday rather than reversing: the mean continuation is +0.98 % in excess of drift (t 5.47, 1436 cases), and it is the strongest of the 14 weekday-by-regime cells.
- F2: That Wednesday continuation in calm markets shows on both days (Thursday +0.42 %, t 3.17; Friday +0.54 %, t 4.23), after both rises (+0.59 %, t 2.35) and falls (+1.36 %, t 5.30), and in 7 of 8 years (2018 +2.69 % t 3.68, 2022 +1.49 % t 4.08, 2025 +1.36 % t 3.29; only 2020 negative at −0.39 %).
- F3: The Wednesday continuation is not cleanly graded by move size: its quartiles of |z| give +0.58 % (t 1.79), +1.13 % (t 2.74), +0.33 % (t 0.98) and +1.90 % (t 5.34), so only the largest quarter stands clearly apart.
- F4: Across all Wednesdays, the continuation fades as volatility rises: the four lower quintiles of the 20/60 volatility ratio give +0.78 % to +1.16 % (t 2.26 to 3.78), and the top quintile gives −0.08 % (t −0.16).
- F5: The calm-market continuation also holds after Thursday's move: the contrarian measure there is −0.56 % (t −3.45, 1444 cases), and −1.58 % (t −4.04) for moves above one 60-day standard deviation.
