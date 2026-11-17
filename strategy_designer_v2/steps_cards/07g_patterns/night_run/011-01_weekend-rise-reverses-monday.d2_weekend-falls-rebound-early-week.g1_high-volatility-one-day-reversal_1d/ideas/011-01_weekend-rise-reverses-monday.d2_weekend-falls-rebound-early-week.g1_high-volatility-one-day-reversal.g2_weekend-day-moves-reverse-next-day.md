---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's move on a Saturday or Sunday that was large relative to its usual daily move over the past 60 days is followed by a move the opposite way over the next 1 day. The reversal is larger the larger that scaled weekend-day move.
Consequence: Concentrate one-day fades on weekend-day moves and skip the fade after Friday and Monday moves.
Why:
- F4: Large moves made on weekend days reverse more than weekday ones. The largest third of down days on Saturday or Sunday were followed by +0.0118 (t 3.87, n 432), against +0.0039 (t 3.34, n 1920) on weekdays. The largest third of weekend up days were followed by −0.0056 (t −2.38, n 557), against +0.0003 (t 0.28, n 1877) on weekdays.
- F5: By weekday, the fade of the top 30% of scaled moves earned most on Saturday (+0.0073, t 2.78, n 367) and Sunday (+0.0089, t 2.94, n 500). It earned nothing on Monday (−0.0004, t −0.25, n 773) and Friday (−0.0018, t −0.93, n 637). The book's gain per bar follows the same pattern: Sunday +0.0018 (t 2.78) and Saturday +0.0010 (t 2.32), against Monday −0.0001 and Friday −0.0005.
