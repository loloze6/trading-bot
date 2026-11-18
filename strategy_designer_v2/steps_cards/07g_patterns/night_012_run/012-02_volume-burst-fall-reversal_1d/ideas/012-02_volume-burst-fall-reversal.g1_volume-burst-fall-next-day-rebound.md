---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.g patterns
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among days on which a coin falls sharply, the larger that day's volume relative to its 30-day average volume, the larger the coin's rise over the next day.
Consequence: The rebound after a heavy-volume fall comes within the first day or so, so a trader who wants it must hold briefly and not carry the position for a week.
Why:
- F1: Among daily falls of more than one usual move, a higher volume ratio (volume over its 30-day mean) is followed by a larger excess return, but only over short horizons: the slope is 0.0056 (t 4.48, n 1666) at 1 day and 0.0206 (t 5.06, n 526) at 3 days, then -0.0016 (t -0.32, n 345) at 5 days, -0.0069 (t -0.63, n 197) at 7 days and -0.043 (t -1.82, n 87) at 14 days, so the rebound is over within about 3 days.
- F4: Over all bars, the day's volume ratio alone predicts the 3-day excess return with slope 0.0054 (t 3.60, n 4283), but among up days of more than one usual move the slope is only 0.0036 (t 1.30, n 609), so the volume effect comes mainly from falls.
