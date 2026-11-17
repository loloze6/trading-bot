---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's move over the weekend (Saturday and Sunday, UTC) is followed by a move the other way over the next day, and the larger the weekend move, the larger the move back.
Consequence: A trader would fade weekend moves into Monday only, sized by the size of the move, and trade far less often than a daily fade so fees no longer eat the edge.
Why:
- F1: The fade's next-day gain beyond the coin's mean daily return depends mostly on the day of the move: after Sunday moves it is 0.00424 (t 4.89, n 4304), after Saturday moves 0.00177 (t 2.60, n 4303), and after Tuesday moves 0.00307 (t 3.65, n 4314), while Wednesday, Thursday and Monday sit near zero (|t| ≤ 0.33).
- F5: The edge is real before costs but smaller than the cost of trading it: mean timing gain is 0.000452 per bar against a mean fee of 0.000647 per bar, so the book's mean daily return is −2.7e-05 (Sharpe −0.03).
