---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse
line: 7.b inconclusive
backtest: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the more its Saturday-Sunday rise is reversed, over the next 4 days.
Consequence: A trader would hold a short against a thin-volume weekend rise through Thursday rather than closing it after Tuesday, because the reversal keeps growing.
Why:
- F2: Thinness alone does grade the reversal, and only at Sunday's close. The 48-hour reversal regressed on log(weekday volume over weekend volume) has slope 0.0084 and t 3.02 on 2,099 cases. The thinnest quintile reverses +0.72 % (t 2.18) and the least thin -0.79 %, with top minus bottom t 2.76. On the other six weekday closes the same slope's t lies between -0.58 and 1.57, which is the weekend-only pattern the brief predicts.
- F4: The effect is on one side only.
- F6: The thinness effect holds across time and in most coins.
- F7: Where it shows, the move is large next to a trade's 0.19 % cost. The thinnest-quintile reversal after a weekend rise is 1.46 % over 48 hours, about 7.7 times the cost, and 2.55 % over 96 hours.
