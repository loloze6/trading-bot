---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's rise in the first hour after the 00:00 UTC funding settlement on a Saturday or Sunday, relative to its 24-hour volatility, the more its return over the next 24 hours falls, while its 7-day return is negative.
Consequence: A trader would fade a weekend post-midnight up hour by going short only while the coin's past week has been falling, which keeps the reversal and drops the shorts that lost in rising markets.
Why:
- F1: The short side alone causes the failing Calmar. Rebuilt from the recorded positions after a cost of 0.19 % per round trip, the long-only book has a yearly return of +9.9 %, a deepest fall of -11.0 %, a Calmar of 0.90 and a Sharpe of 0.91. The short-only book has a yearly return of -0.07 %, a deepest fall of -26.9 % and a Calmar of -0.003. The two together give Calmar 0.42 against a 0.75 rule. Per trade, longs net +0.44 % (t 5.6, 3913 trades) and shorts net -0.46 % (t -6.2, 4170 trades).
- F2: The book's deepest fall was -23.8 % over 205 days, from w16 to w18, during the 2020–2021 rise. In w17 the coins rose a summed +51 % and the book lost -12.5 %. In that window the short side lost -13.6 % gross while the long side made +3.3 %. In 2020 the short side lost -10.0 % and the long side made +23.3 %. So the falls come from fading up hours while the coins are rising.
- F4: Fading weekend up hours earns only when the hour is large and the coin's 7-day return is negative. For up hours above 1 volatility unit with a negative 7-day return, a short captures +1.17 % over 24 hours (t 5.05, 349 cases). With a positive 7-day return it captures +0.34 % (t 1.41, 453 cases). Shorting small up hours (0 to 1 unit) loses -0.09 % and -0.16 %.
- F5: The 7-day downtrend is not an effect of its own. Shorting every weekend 00:00 bar with a negative 7-day return, with no signal, captures -0.11 % over 24 hours (t -1.21, 2245 cases); with the signal it captures +1.17 %. This fits the brief's theory: after a run down, shorts are the crowded side paying funding. They would cover into the settlement and reopen after it, so a post-settlement up hour in a downtrend is the timing flow that reverses.
- F6: The idea's measured size is +0.41 % per case, 2.1 times the 0.19 % cost of a trade. The cases kept by the repairs are larger:
