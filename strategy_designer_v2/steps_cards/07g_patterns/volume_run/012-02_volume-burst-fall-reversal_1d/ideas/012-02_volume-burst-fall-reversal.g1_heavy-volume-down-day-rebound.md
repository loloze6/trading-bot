---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.g patterns
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day the coin closes lower, the larger that day's volume relative to its 30-day average volume, the larger the coin's rise over the next 3 days, whatever the size of the fall.
Consequence: A down day on unusually heavy volume is a reason to buy for a few days, sized up with the volume burst, rather than to wait for a sharp fall.
Why:
- F1: On down days of any size, the next 3 days' excess return rises with the day's volume against its 30-day average. Pooled log-volume-ratio slope 0.0129, t 4.05, controlling for the fall's size, whose own coefficient is 0.0003 (t 0.16). Non-overlapping 3-day grid, 2023 cases.
- F2: The effect sits in the top fifth of volume among down days. Those cases gain +2.26% in excess over 3 days (t 4.35, n 405); the lower four fifths average between -0.19% and -0.38%.
- F3: Fall size does not gate the effect. The log-volume slope is positive for falls of 2 or more usual moves (0.032, t 3.02, n 157), for falls of 1 to 2 (0.043, t 4.28, n 373) and for falls under 1 (0.0076, t 2.24, n 1493). So the plan's sharp-fall gate threw away most of the signal.
- F4: The same volume ratio on up days predicts nothing. The slope is -0.0005 (t -0.27, n 2260), and the top volume fifth of up days averages -0.33%. The pattern is specific to heavy-volume selling.
- F5: The down-day volume effect is positive in all 6 coins: slopes 0.002 to 0.019, t from 0.38 for BTC to 2.41 for ZEC. It is positive in 7 of 8 years, with 2023 flat at -0.0001. It already shows over the next day: slope 0.0042, t 4.57, n 6478.
- F6: The brief's long lower wick does not add to the rebound. Among falls of 2 or more usual moves, the 3-day excess return falls with wick share (slope -0.022, t -0.85, n 432). The deepest-wick third averages -0.18%, against +0.74% for the shallowest.
