---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin trades a four-hour volume far above its 30-day average, it rises over the next three days, only while its own 30-day return is positive. The higher the volume against that average and the larger that 30-day rise, the larger the rise.
Consequence: Treat a volume surge as a long signal only in a coin that is in a monthly uptrend, and stand aside from surges in a coin that is falling over the month.
Why:
- F1: The book fails on its falls, not its gain: it earns 38.0 % a year, but its chained daily value falls 59.9 % at worst, giving a Calmar of 0.634 against 0.75. Its worst 5 % of days (145 days, mean −7.3 %) are all days when the coins fell (100 %, coin mean −9.4 %), and inside single windows it falls up to 55.3 % (w16), 52.8 % (w14) and 46.9 % (w2).
- F2: The book is almost always long, with a mean position of 0.71 after a falling 7 days and 0.79 after a rising one. Over about 105,000 bars on each side, its summed bar gain is 54.30 after a rising 7-day return and only 7.05 after a falling one. On the 30-day return it is 44.36 against 0.35.
- F5: The 30-day return shows the same split. Its two top fifths (above +6.4 %) give +0.99 % (t 3.56) and +0.96 % (t 3.38), with about 1,520 cases each. Its second fifth (−17.9 % to −4.9 %) gives −0.93 % (t −4.53).
- F7: Rebuilding the book before fees with positions kept only while the coin's 7-day return is positive changes the failing measure. The deepest fall drops from −58.4 % to −32.1 %, and the Calmar rises from 0.78 to 1.88, with Sharpe going from 0.94 to 1.50. Keeping positions only while the 30-day return is positive gives a Calmar of 1.44 and a deepest fall of −29.5 %.
