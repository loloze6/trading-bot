---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour move relative to its usual 24-hour move, the more of it the coin gives back over the next 24 hours.
Consequence: A trader would fade unusually large daily moves for one day, from a situation that changes slowly enough for a held position to stay on its side, and would not carry the fade beyond the day.
Why:
- F1: The book's position does not follow its forecast. The position held has the forecast's sign on 49.9 % of bars, and its correlation with the forecast is 0.04. Sizing barely depends on the forecast: the mean |allocation| is 0.86 when |forecast| ≤ 0.5 and 0.91 when |forecast| > 14. Gain per bar is about 0 at every forecast level (-0.32 to +0.07 bps). The book's gross loss therefore comes before fees: -12.1 bps a day on BTC and -8.0 on ETH, against fees of 2.5 to 5.1 bps a day.
- F7: A slower situation carries a similar give-back. Scaled 24-hour moves in their 4th and 5th quintiles give back 33 and 22 bps over the next 24 hours (t 3.7, 2.5), but continue over 7 days (-84 and -132 bps). Scaled 72-hour moves do not reverse at all (-9 bps, t -1.0).
