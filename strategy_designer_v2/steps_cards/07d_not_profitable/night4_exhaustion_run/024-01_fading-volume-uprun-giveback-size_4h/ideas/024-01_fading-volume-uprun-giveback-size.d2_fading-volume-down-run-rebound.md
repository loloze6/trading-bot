---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, and the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, the larger the rise.
Consequence: A 4-hour sell-off far larger than usual, made on fading volume, is a reason to buy for a partial rebound over three days.
Why:
- F8: The brief's "same holds for falls" appears only after the largest falls. After four or more down bars in the quartile of most negative scaled loss (-5.1), the coin's long unusual move over 3 days is +0.92 % (t 2.10, 436 cases) and the total move is +1.32 %. With fading volume the unusual move rises to +1.59 % (t 2.55, 131 cases), against +0.63 % (t 1.12, 305 cases) with rising volume.
- F9: The rebound after falls is graded by the fall's size. The long unusual move by quartile of scaled loss is +0.92 %, +0.12 %, -0.95 % (t -2.59) and -0.42 %, so small down-streaks keep falling. The rebound after the largest falls held in 6 of 8 years and in 4 of 6 coins, with BTC at -0.69 % and ETH at -1.64 %.
