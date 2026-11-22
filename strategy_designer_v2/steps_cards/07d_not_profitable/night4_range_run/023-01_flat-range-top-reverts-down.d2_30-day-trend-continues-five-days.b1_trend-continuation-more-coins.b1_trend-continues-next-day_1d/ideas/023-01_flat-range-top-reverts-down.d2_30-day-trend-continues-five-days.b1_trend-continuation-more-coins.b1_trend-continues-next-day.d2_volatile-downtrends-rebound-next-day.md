---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next day, except after a 30-day fall, where the higher its 30-day volatility against its own last 60 days, the more the coin rises over the next day.
Consequence: A trader would follow a coin's 30-day rise, and would buy rather than short a coin that is falling while volatile against its own past, more so the higher that volatility.
Why:
- F2: Short losses come from falling coins whose volatility is high. Shorts in the top quartile of 30-day daily volatility move −0.517 % per day in their direction (t −3.12, n 1,452). Shorts in the three lower quartiles move between +0.09 % and +0.14 % (t about 0.9 each).
- F3: The same reversal grows with volatility against the coin's own recent level, measured as 30-day volatility over its 60-day median. In falling coins the next-day move in the short's direction falls steadily across the quartiles: +0.329 % (t 2.70, n 1,363), −0.070 %, −0.003 %, then −0.773 % in the top quartile (t −3.38, n 718).
- F4: Rising coins keep rising at every volatility level, and most strongly when volatility is high against its own past. Longs in the top relative-volatility quartile move +0.724 % (t 4.06, n 1,659), and longs in the top absolute-volatility quartile move +0.507 % (t 2.80).
