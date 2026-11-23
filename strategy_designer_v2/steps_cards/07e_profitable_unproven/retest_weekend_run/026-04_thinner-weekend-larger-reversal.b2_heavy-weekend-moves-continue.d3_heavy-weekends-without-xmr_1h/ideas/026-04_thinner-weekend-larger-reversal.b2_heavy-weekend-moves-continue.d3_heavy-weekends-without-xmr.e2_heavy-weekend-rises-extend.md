---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
line: 7.e profitable but not proven
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
instruments: BTC, ETH, LTC, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's rise over Saturday and Sunday is followed by a further rise over the next 48 hours. The further rise is larger the heavier the weekend's volume is against its mean over the preceding five weekdays.
Consequence: A heavy-volume weekend rise is a reason to be long into Monday and Tuesday, more so than a heavy-volume weekend fall is a reason to be short.
Why:
- F4: The book's profit is concentrated in a few long holds and in longs.
- F5: The continuation is clearest after heavy weekend rises with the heaviest volume. Up-moves in the top volume tercile reach a strength of 0.357 (t 2.21, 75 cases), against 0.056 (t 0.44, 41) for down-moves in the same tercile. Across all heavy weekends both sides continue: down +1.56 % (t 2.15) and up +1.69 % (t 2.35).
- F1: Inside the heavy-volume weekends, the move that follows grows with the volume ratio and not with the move's size. On 1,905 weekends, regressing the 48-hour strength on log(volume ratio) and the weekend move in usual moves gives +0.261 (t 5.76) on log volume ratio and −0.186 (t −4.08) on move size. Strength by move tercile within heavy weekends is flat: small 0.18, mid 0.29, large 0.21. This is why the plan's size check, ranked on |forecast| = move × ratio, failed (−0.0025).
