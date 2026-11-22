---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour fall over Sunday is followed by a rise over the next two days, Monday and Tuesday: the larger Sunday's fall, the larger the rise.
Consequence: A trader would keep the long side of the Sunday fade and drop the short side, which loses after Sunday's largest rises.
Why:
- F5: The reversal works after Sunday falls but not after Sunday's largest rises. Over the next 48 hours, the two most negative Sunday quintiles are followed by +1.07 % and +0.69 %, and the fourth quintile by -1.44 %. The largest Sunday rises (z +1.16) are followed by only -0.06 %. In the trades, longs net +0.63 % with a 61 % win rate (1980 trades), while shorts net -0.68 % with a 29 % win rate (2074 trades).
