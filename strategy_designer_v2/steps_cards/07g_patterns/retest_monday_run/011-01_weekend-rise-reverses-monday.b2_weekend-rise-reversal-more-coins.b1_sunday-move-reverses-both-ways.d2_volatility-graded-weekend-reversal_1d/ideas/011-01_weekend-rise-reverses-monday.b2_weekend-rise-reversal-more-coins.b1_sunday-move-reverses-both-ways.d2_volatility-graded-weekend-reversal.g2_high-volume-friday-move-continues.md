---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Friday return continues in the same direction over the next day (Saturday), and the continuation is larger the higher Friday's volume is relative to the coin's 20-day average volume.
Consequence: A trader would follow a heavy-volume Friday move into Saturday rather than fade it, and would refuse to fade such Friday moves.
Why:
- F7: Friday's move carries on into Saturday, graded by volume and size, but much of it is common to all coins on the same date. The signed next-day return rises with Friday volume quartile (0.009, 0.023, 0.050, 0.138; top quartile t 3.55) and with |Friday move| quartile (top quartile 0.177, t 4.74). 16 of 19 coins have a positive slope, yet the per-date cross-coin slope has t 1.27 for one day and 2.64 for three days.
