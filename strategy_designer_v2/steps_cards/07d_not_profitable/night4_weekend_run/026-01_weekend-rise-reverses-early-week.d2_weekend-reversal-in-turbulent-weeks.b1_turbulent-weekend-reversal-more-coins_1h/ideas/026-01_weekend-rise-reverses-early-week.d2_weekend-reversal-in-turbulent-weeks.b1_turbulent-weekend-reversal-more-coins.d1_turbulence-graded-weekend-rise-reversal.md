---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), only while the coin's 30-day hourly volatility is high against its own last 6 months; the higher the coin's 30-day hourly volatility at Monday 00:00, the larger the fall.
Consequence: A trader would size the Monday fade by how turbulent the coin is, not by how far it rose over the weekend, and close it at the end of Tuesday.
Why:
- F4: The fall grows with the coin's 30-day hourly volatility. By volatility quintile, the 48-hour short move is -0.81 % (t -0.99), +0.80 %, +0.90 %, +1.09 % and +1.79 % (t 2.19), about 155 cases each.
- F3: The fall does not grow with the weekend gain; it shrinks as the forecast grows:
- F1: The book's short is not closed after Monday and Tuesday. Of 826,743 recorded bars, 70,135 carry a short outside the 48 hours after a Monday 00:00 bar, and none carry a long. Those out-of-window bars sum to a gain of -0.70, against +2.15 inside the window. Trades last a mean of 99 hours (median 48, maximum 2,833), and the leftover position most often sits on Wednesday (130 coin-windows).
- F2: Because of those overstays, the 1,586 trades average -1.22 % net (t -3.99, 28 % winners). This is against a mean short move of +0.90 % over the idea's own 48 hours on the 985 Monday cases (t 3.08).
