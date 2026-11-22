---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin trades a four-hour volume far above its 30-day average on a bar whose own move is large against the coin's usual four-hour move, it rises over the next three days. The larger that bar's move in either direction, the larger the rise.
Consequence: The size of the price move on the surge bar, rather than the size of the volume, says how much of a rise to expect over the next three days.
Why:
- F5: The rise after a surge grows with the size of the surge bar's own move against the coin's usual 4h move, whichever its direction. By quintile of the absolute body z, the excess runs from -0.35 % (t -1.37) through -0.24 %, +0.44 % and +0.50 % to +1.23 % (t 3.75), with 802 to 803 cases each. Large down bodies (z -2.7) give +0.81 % (t 2.59) and large up bodies (z +2.6) give +0.86 % (t 2.64).
- F6: The forecast's own grading carries no information. By forecast level (3.4, 9.3, 19.7) the excess is +0.35 %, +0.23 % and +0.25 %, and the step-5 Spearman is -0.014. Overall, the unusual move of +0.21 % per case is only 1.1 times the 0.19 % cost of a trade.
