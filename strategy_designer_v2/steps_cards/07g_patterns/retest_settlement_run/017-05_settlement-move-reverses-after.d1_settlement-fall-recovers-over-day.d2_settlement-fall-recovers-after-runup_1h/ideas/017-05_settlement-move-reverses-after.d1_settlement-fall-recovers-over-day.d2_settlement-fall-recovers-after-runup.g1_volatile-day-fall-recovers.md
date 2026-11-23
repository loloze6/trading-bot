---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a fall over its past 24 hours, and the rise is larger the deeper that fall is against the coin's usual 24-hour move. The rise grows further the higher the coin's volatility of hourly returns over the past 30 days.
Consequence: A deep one-day fall in a volatile coin is a reason to be long for the next day, sized by the depth of the fall and by the coin's volatility, while the same fall in a calm coin gives little reason.
Why:
- F1: Over the next 24 hours, a coin's excess return grows with the depth of its past 24-hour fall measured against its usual 24-hour move (z24). Bins from shallow to deep falls run -0.26 %, -0.12 %, +0.32 % (t 2.3), +0.50 % (t 2.6), +0.41 %, and +2.15 % (t 4.8, 329 non-overlapping cases) beyond 3 usual moves. The graded product (-z24, floored at 0) × next-24h excess return has t 4.88, and the Spearman correlation on the 7,486 falling cases is -0.098.
- F2: That 24-hour fall reversal sits almost entirely in high volatility. For falls beyond 1.5 usual moves, the top 30-day volatility tercile returns +2.34 % (t 6.2, 544 cases), the middle +0.14 % (t 0.7) and the bottom -0.09 % (t -0.6). The same move per case is 12 times the 0.19 % cost of a trade.
- F3: The fall reversal is stronger when the coin's 7-day return is negative (+0.88 %, t 4.7, 1,269 cases) than when it is positive (+0.51 %, t 2.1, 362 cases). This is the opposite of the run-up condition the tested idea used.
- F4: The fall reversal is not even across coins or years. It is strong in the smaller coins (ZEC +1.51 % t 3.2, XRP +1.26 % t 3.2, XMR +1.03 % t 2.7) and weak in BTC (+0.23 %, t 0.9). It is heaviest in 2018 (+1.85 %, t 3.8) and 2021 (+2.88 %, t 4.2), and it is positive in 18 of 24 windows.
