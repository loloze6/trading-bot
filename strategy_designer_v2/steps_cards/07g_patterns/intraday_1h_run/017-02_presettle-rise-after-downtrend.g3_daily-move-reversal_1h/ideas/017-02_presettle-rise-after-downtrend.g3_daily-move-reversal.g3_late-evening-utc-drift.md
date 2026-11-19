---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin rises over the two hours from 20:00 to 22:00 UTC, and the rise is larger the higher its one-week hourly volatility.
Consequence: A trader would hold the coin long through the 20:00–22:00 UTC hours, scaled by its current volatility, rather than through other evening hours.
Why:
- F4: Coins rise in the hours starting 20:00 and 21:00 UTC: +5.45 bp (t=6.75) and +4.36 bp (t=5.66) per hour. These are the largest of the 24 hours, so they stand out even after testing every hour. In volatility units the rise is positive in all six coins (t from 2.11 for XRP to 4.43 for BTC), on all seven weekdays, and in 7 of 8 years. 2022 is the exception (t=-3.57).
- F5: The funding clock times show no distinctive behaviour. The hours just before and after 00, 08 and 16 UTC have normalised mean returns between -0.021 and +0.023, with |t| ≤ 2.8. That is no larger than at non-funding hours such as 02 (-2.77 bp, t=-3.80) or 13 (-3.56 bp, t=-3.80), so it does not support the brief's settlement mechanism.
