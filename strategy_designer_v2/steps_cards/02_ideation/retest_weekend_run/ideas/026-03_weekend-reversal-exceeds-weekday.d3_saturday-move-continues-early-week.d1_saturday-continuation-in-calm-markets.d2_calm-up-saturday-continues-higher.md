---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's rise over Saturday's 24 hours is followed over the next two days, Monday and Tuesday, by a further rise that grows with the size of Saturday's rise, while the coin's 30-day volatility of hourly returns is low against its own past year, and the calmer the coin, the larger the rise.
Consequence: A trader would buy into Monday and Tuesday after an up Saturday in calm markets and take no short after a down Saturday, which keeps most of the gain with a shallower deepest fall.
Why:
- F5: By side, long trades summed +927 % (1161 trades) and short trades −320 % (781 trades). A long-only rebuild reaches a Calmar of 0.79 with a deepest fall of −11.4 % (Sharpe 1.02), and the deepest fall stays in w12.
- F6: The long side is not just the coin's drift. Being long on every calm Sunday regardless of Saturday's sign earns +0.02 % (t 0.13, 1424 cases), while calm up-Saturday cases earn +0.55 % (t 2.51, 803 cases).
- F1: The failing Calmar of 0.61 comes from one fall: the book dropped 18.5 % over 132 days from a peak in w11 to a trough in w12, both in 2021. 2021 is the book's worst year (summed daily return −0.111), and in that year the cases lost on both sides (de-drifted 48-hour return in the forecast's direction −0.66 % on shorts and −0.83 % on longs).
- F8: Cost is not the obstacle: the total move per case (+0.65 %) is 3.4 times the 0.19 % cost of a trade, so the failure is in the depth of the falls, not in the gain covering the fee.
