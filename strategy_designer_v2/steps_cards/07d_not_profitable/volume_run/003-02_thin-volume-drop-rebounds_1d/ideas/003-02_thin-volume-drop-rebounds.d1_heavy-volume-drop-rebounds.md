---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds
line: 7.d not profitable
backtest: 003-02_thin-volume-drop-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin falls over one day on volume above its own 30-day average daily volume, it wins back part of that fall over the next 3 days. The larger the fall and the heavier its volume against that average, the larger the rebound.
Consequence: A trader would buy sharp one-day drops that come with heavy volume, read as capitulation selling that gets absorbed, rather than waiting for thin-volume drops, which are rare and do not rebound.
Why:
- F1: The book barely trades because its situation almost never happens: of 488 one-day falls of at least 2 usual moves, only 1.2 % came on volume at or below half the 30-day average (6.4 % below 0.8, 12.1 % below 1), and the median volume ratio on such falls is 1.70. The book therefore held a position on 0.03 % of bars, with 5 bars of forecast above 0, which fails both the trades-per-bar test (0.0003) and the mean daily return test (3.6e-06).
- F2: Over all falls of at least 1 usual move, the rebound runs the opposite way to the tested idea: heavy-volume falls (ratio ≥ 1.5) had a mean 5-day excess return of +0.0151 (n 325), against −0.0068 for thin-volume falls (ratio < 1, n 377). Welch t for heavy minus thin is 2.42.
- F3: The excess return after a fall rises with the log of the volume ratio at every horizon: slope 0.0162 (t 3.99, n 1286) over 3 days, 0.0131 (t 2.09, n 1027) over 5 days, and 0.0269 (t 2.53, n 702) over 10 days.
- F4: Fall size times log volume ratio grades the rebound over 3 days (slope 0.0038, t 3.33, n 1286), but not over 5 days (t −0.11). The graded effect is strongest in the first few days.
- F5: The thinnest-volume quartile of falls (mean ratio 0.63) was followed by a negative 5-day excess of −0.0077 (t −1.26, n 257). The heaviest quartile (mean ratio 2.51) was followed by +0.0163 (t 1.78, n 257). Thin-volume falls do not rebound in this data.
- F6: The heavy-volume advantage is broad but not universal. Heavy beat non-heavy falls in 5 of 8 years (2020 +0.037 vs −0.014, 2025 +0.056 vs −0.012) and in 4 of 6 coins (ZEC +0.042 vs −0.008, XRP +0.032 vs −0.008), but not in BTC (−0.015 vs +0.002).
