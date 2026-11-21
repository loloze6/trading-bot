---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high relative to its past 120 days, its 1-day return relative to its usual daily move is followed by a move the opposite way over the next day. The larger the day's move, the larger the move back.
Consequence: In turbulent periods a trader would fade a coin's large daily moves for one day and leave calm periods alone.
Why:
- F3: The daily (00:00 to 00:00) 1-day vol-scaled return reverses over the next day (slope t -4.0, top third -22 bps, 14310 cases). This comes entirely from high-volatility periods: in the top tercile of 20-day volatility against its past 120 days, the largest moves reverse by 54 bps (t 2.7, 938 cases), against -6 bps (t -0.4) in the lowest tercile.
