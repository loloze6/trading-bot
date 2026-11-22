---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls in an unbroken streak of 4-hour periods while its volume over the last 8 hours shrinks against its last 24 hours, it keeps falling over the next 3 days, and the more the volume fades, the larger the further fall.
Consequence: A falling streak on drying volume is a reason to stay short or out for three days rather than to buy the dip.
Why:
- F2: Down-streaks of at least two 4h bars where the last 8 hours' volume has faded against the last 24 hours fall further over the next 3 days, the reverse of the brief's give-back. Fading minus rising volume is -0.186 standard deviations (Welch t -3.09, n 1117). The slope on the size of the fade has t -2.85, and the fading half is lower in all 6 coins and in 6 of 8 years.
