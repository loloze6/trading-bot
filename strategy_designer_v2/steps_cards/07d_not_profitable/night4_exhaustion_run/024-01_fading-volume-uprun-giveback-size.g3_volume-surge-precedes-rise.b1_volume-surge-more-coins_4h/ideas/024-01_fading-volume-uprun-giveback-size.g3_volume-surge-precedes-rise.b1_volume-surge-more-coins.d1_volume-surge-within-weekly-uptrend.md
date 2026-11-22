---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin trades a four-hour volume far above its 30-day average, it rises over the next three days, only while its own 7-day return is positive. The higher the volume against that average and the larger that 7-day rise against the coin's usual 7-day move, the larger the rise.
Consequence: Lean long on a volume surge only when the coin has been rising over the past week, and refuse the long when it has been falling, where the book took its deepest falls.
Why:
- F1: The book fails on its falls, not its gain: it earns 38.0 % a year, but its chained daily value falls 59.9 % at worst, giving a Calmar of 0.634 against 0.75. Its worst 5 % of days (145 days, mean −7.3 %) are all days when the coins fell (100 %, coin mean −9.4 %), and inside single windows it falls up to 55.3 % (w16), 52.8 % (w14) and 46.9 % (w2).
- F2: The book is almost always long, with a mean position of 0.71 after a falling 7 days and 0.79 after a rising one. Over about 105,000 bars on each side, its summed bar gain is 54.30 after a rising 7-day return and only 7.05 after a falling one. On the 30-day return it is 44.36 against 0.35.
- F3: The surge's cases depend on the coin's own recent path. After a 7-day return in the top fifth (above +10.4 %), the 3-day excess return is +1.23 % (t 4.07, 1,914 cases). In the second-lowest fifth (−8.7 % to −1.9 %) it is −0.71 % (t −4.01, 1,914 cases).
- F4: Measured in the coin's own usual move units, the 7-day return grades the effect. The 3-day excess return is −0.86 % (t −4.48), −0.02 %, +0.52 % (t 2.30) and +1.15 % (t 4.19) from the second to the top fifth, each fifth with about 1,914 cases.
- F6: Across years, surges after a falling 7 days lost most in falling markets (−2.77 % in 2018 and −1.70 % in 2022). Surges after a rising 7 days were positive in 5 of 8 years, up to +2.30 % in 2021, but negative in 2022 (−0.79 %) and 2025 (−0.55 %).
- F7: Rebuilding the book before fees with positions kept only while the coin's 7-day return is positive changes the failing measure. The deepest fall drops from −58.4 % to −32.1 %, and the Calmar rises from 0.78 to 1.88, with Sharpe going from 0.94 to 1.50. Keeping positions only while the 30-day return is positive gives a Calmar of 1.44 and a deepest fall of −29.5 %.
- F8: Taken as a whole, the idea is too small for this book. Its unusual move is +0.14 % per case, against a cost of 0.22 % per trade. After a strong 7-day rise the unusual move per case (+1.23 %, F3) is about 5.6 times that cost.
