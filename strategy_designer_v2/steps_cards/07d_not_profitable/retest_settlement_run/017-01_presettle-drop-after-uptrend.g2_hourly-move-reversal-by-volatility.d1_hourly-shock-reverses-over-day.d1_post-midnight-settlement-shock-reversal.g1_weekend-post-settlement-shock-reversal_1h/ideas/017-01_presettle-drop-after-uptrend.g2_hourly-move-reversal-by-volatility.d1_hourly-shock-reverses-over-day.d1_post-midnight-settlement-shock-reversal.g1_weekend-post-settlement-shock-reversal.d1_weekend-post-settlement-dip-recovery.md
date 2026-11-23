---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall in the first hour after the 00:00 UTC funding settlement on a Saturday or Sunday, relative to its 24-hour volatility, the more its return over the next 24 hours rises.
Consequence: A trader would buy the coin after a weekend post-midnight down hour, sized by how large that hour's fall was, and would not fade weekend up hours in a rising market, which is where the book's deepest falls came from.
Why:
- F1: The short side alone causes the failing Calmar. Rebuilt from the recorded positions after a cost of 0.19 % per round trip, the long-only book has a yearly return of +9.9 %, a deepest fall of -11.0 %, a Calmar of 0.90 and a Sharpe of 0.91. The short-only book has a yearly return of -0.07 %, a deepest fall of -26.9 % and a Calmar of -0.003. The two together give Calmar 0.42 against a 0.75 rule. Per trade, longs net +0.44 % (t 5.6, 3913 trades) and shorts net -0.46 % (t -6.2, 4170 trades).
- F2: The book's deepest fall was -23.8 % over 205 days, from w16 to w18, during the 2020–2021 rise. In w17 the coins rose a summed +51 % and the book lost -12.5 %. In that window the short side lost -13.6 % gross while the long side made +3.3 %. In 2020 the short side lost -10.0 % and the long side made +23.3 %. So the falls come from fading up hours while the coins are rising.
- F3: The long side carries the real effect, and it is graded. On weekend 00:00 cases, the next 24 hours return +0.54 % after a down hour (t 6.4, 2337 cases), against +0.19 % on all weekend 00:00 bars (t 3.1, 4869 cases) and -0.14 % after an up hour. By the hour's move in units of 24-hour volatility, the next 24 hours return +0.39 % for 0 to -0.5, +0.33 % for -0.5 to -1 and +0.98 % for -1 to -2 (t 5.5, 581 cases).
- F6: The idea's measured size is +0.41 % per case, 2.1 times the 0.19 % cost of a trade. The cases kept by the repairs are larger:
