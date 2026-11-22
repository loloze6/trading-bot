---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), mostly over Tuesday, only while the coin's 30-day hourly volatility is high against its own last 6 months; the higher that volatility, the larger Tuesday's fall.
Consequence: A trader would fade a weekend rise mainly across Tuesday in turbulent weeks, holding it no longer than to Wednesday 00:00 UTC.
Why:
- F6: Most of the fall comes on Tuesday. The short move is +0.18 % over the first 24 hours and +0.72 % over the second 24 hours (985 cases).
- F4: The fall grows with the coin's 30-day hourly volatility. By volatility quintile, the 48-hour short move is -0.81 % (t -0.99), +0.80 %, +0.90 %, +1.09 % and +1.79 % (t 2.19), about 155 cases each.
- F1: The book's short is not closed after Monday and Tuesday. Of 826,743 recorded bars, 70,135 carry a short outside the 48 hours after a Monday 00:00 bar, and none carry a long. Those out-of-window bars sum to a gain of -0.70, against +2.15 inside the window. Trades last a mean of 99 hours (median 48, maximum 2,833), and the leftover position most often sits on Wednesday (130 coin-windows).
