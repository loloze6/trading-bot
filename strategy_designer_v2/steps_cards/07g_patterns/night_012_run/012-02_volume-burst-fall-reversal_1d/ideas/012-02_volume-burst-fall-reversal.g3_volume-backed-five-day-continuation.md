---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.g patterns
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's 5-day return, measured in its usual daily moves, is followed by a larger move in the same direction over the next 7 days the higher its 5-day average volume is relative to its 30-day average volume.
Consequence: Strong five-day moves that come on rising volume are the ones to follow for a week, and those on thin volume deserve less weight.
Why:
- F3: That 7-day continuation grows with recent volume: by tercile of 5-day mean volume over 30-day mean volume the m5 slope is 0.0069 (t 0.93), 0.0117 (t 2.19) and 0.0137 (t 3.05), and the product m5 × volume ratio gives slope 0.0090 (t 4.48, n 1723).
- F2: The coin's 5-day return measured in usual moves (5-day return over the 20-day daily standard deviation times √5) predicts the coin's next 7-day excess return with slope 0.0119 (t 4.23, n 2011 non-overlapping cases), the opposite of reversal; the slope is positive at every horizon from 2 to 14 days (t 2.31 to 4.23) and for all six coins (XRP t 3.28, the others t 0.89 to 1.79).
