---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day hourly volatility is high against its last 6 months, a rise from Saturday 00:00 to Monday 00:00 UTC is followed by a fall over Tuesday (Tuesday 00:00 to Wednesday 00:00 UTC): the larger the weekend gain, the larger the Tuesday fall.
Consequence: A trader would fade a turbulent-week weekend rise on Tuesday only, sparing the cost of carrying it through a flat Monday.
Why:
- F3: In the tested Monday cases (744 with a full 96-hour path), the reversal falls on Tuesday. The Monday 00:00 to Tuesday 00:00 return is +0.11 % (t 0.45), the Tuesday return is −0.62 % (t −2.74), and Wednesday–Thursday gives +0.77 % back (t 1.38).
- F4: The weekend reversal holds only in the high-volatility regime: the slope of the Monday–Tuesday move on the weekend move is −0.125 (t −4.3, 1 666 cases), and the top quintile of weekend rises is followed by −1.38 % unusual. In calm regimes the slope is +0.066 (t 2.25, 2 499 cases), and a weekend fall is followed by a further unusual −0.68 % (t −3.43).
