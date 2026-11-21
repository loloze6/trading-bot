---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the late-evening UTC hours, a coin keeps moving the way it moved over the past day. The stronger its 24-hour rise, the larger its excess return over the next 2 hours from the 21:00 close.
Consequence: A trader would lean long into 21:00–23:00 UTC in proportion to the coin's 24-hour rise, and refuse that long if the continuation is absent.
Why:
- F1: The 21:00 UTC 2-hour return rises with the coin's 24-hour return, not with its fall. The pooled slope of the excess 2-hour return on the vol-scaled 24-hour return is +5.3 bp per unit (t 4.4, n 17271), and it is positive in all six coins (t from 0.5 to 3.0). The top 24-hour-return quintile earns +11.0 bp (t 4.4), while the bottom quintile earns -0.9 bp (t -0.3). This is the opposite of the tested idea, which was rejected with slope t -3.73.
- F2: The evening hours rise on their own. The mean excess 1-hour return is +4.8 bp at 20:00 (t 6.0) and +3.7 bp at 21:00 (t 4.8), the two strongest of the 24 hours, each with about 17,400 cases. Pooled over 20–21h it is positive in 7 of 8 years (t from 1.3 to 5.2), and negative only in 2022 (-2.8 bp, t -1.8).
