---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 60 days, the more it falls over the next 5 days.
Consequence: A flat coin below mid-range is shorted in proportion to its 60-day decline, not to its latest 10-day drop.
Why:
- F3: Among the active shorts with 60 days of history, the next 5 days fall more than drift only when the coin's 60-day return is down. Below -20 % the excess is -4.19 % (t -4.9, n=95); between -20 % and -5 % it is -2.19 % (t -2.2, n=78). Between -5 % and +5 % it is +0.06 % (t 0.06, n=51), and above +20 % it is -1.59 % (t -1.0, n=81). The r60 slope is +0.032 (p 0.064).
- F4: Once the 60-day return is known, the 10-day fall adds nothing. With a 60-day return below -20 %, forecasts below -10 give -4.36 % against -4.05 % for milder ones. With a 60-day return above +20 %, the stronger forecasts are followed by +1.34 % against drift, a rebound against the short, versus -2.43 % for milder ones.
- F6: Being short coins that drift up costs the book about 0.023 % a day; the drift part runs from -0.013 % to -0.025 % a day across coins. The total move per case is -0.04 %, so the trade earns nothing before a 0.19 % cost. Mean daily return is -0.026 %, and timing is negative in 13 of 24 windows (for example -0.10 % a day in w10 and w11).
