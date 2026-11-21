---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: At any hour of the day, a coin's 2-hour return runs opposite to its return over the next 24 hours. The larger that 2-hour move relative to the coin's usual 2-hour move, and the higher the coin's hourly volatility over the past 20 hours against its usual level, the larger the move back.
Consequence: A trader would fade large volatility-scaled 2-hour moves on volatile days at any clock hour, which gives several times more cases than the settlement hour alone.
Why:
- F2: The reversal sits almost entirely in volatile conditions. Settlement cases in each coin's top third by 20-hour volatility gain 34 bps of excess over 24 hours (t 4.1, 5755 cases). The bottom and middle thirds gain 2.1 and 2.2 bps (t 0.4). Inside the volatile third, the largest third of pre-settlement moves gains 61 bps (t 4.0, 1955 cases), about 3 times a trade's cost, while the quiet, smallest-move cell loses 21 bps (t -2.6).
- F3: The size of the pre-settlement move grades the reversal. By quintile of |move| in usual 2-hour moves, the 24-hour excess is 1, 3, 4, 30 and 26 bps (t 3.6 and 2.9 in the top two quintiles), so the lower 60 % of cases carry under a quarter of the cost each.
- F5: The effect is not specific to the funding clock. The 17 UTC placebo hour reverses as much as 00 UTC over 24 hours (12.0 vs 12.9 bps, t 3.3 vs 3.4). Among high-volatility, large-move cases, 05 UTC gives 51 bps (t 2.7) and 11 UTC 36 bps (t 2.1), against 61 bps at 00 UTC.
