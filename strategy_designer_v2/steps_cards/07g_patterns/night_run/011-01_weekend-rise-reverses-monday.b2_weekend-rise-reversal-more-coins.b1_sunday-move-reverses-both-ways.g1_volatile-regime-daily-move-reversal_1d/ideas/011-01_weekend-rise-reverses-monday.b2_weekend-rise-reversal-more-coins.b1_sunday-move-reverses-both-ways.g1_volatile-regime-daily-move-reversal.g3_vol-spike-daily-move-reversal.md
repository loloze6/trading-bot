---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily move is followed by a move the other way over the next day, and the higher its 20-day volatility relative to its 120-day volatility, the larger the move back.
Consequence: A trader would fade daily moves only in proportion to how far short-term volatility has risen above its longer-run level, and would leave most days untraded.
Why:
- F3: The reversal sits only where 20-day volatility is high against its 120-day level: in the top tercile of vol20/vol120 the fade gain is 0.00296 (t 4.04, n 6056), against −0.00023 (t −0.36) and 0.00026 (t 0.41) in the lower two terciles.
- F5: The edge is real before costs but smaller than the cost of trading it: mean timing gain is 0.000452 per bar against a mean fee of 0.000647 per bar, so the book's mean daily return is −2.7e-05 (Sharpe −0.03).
