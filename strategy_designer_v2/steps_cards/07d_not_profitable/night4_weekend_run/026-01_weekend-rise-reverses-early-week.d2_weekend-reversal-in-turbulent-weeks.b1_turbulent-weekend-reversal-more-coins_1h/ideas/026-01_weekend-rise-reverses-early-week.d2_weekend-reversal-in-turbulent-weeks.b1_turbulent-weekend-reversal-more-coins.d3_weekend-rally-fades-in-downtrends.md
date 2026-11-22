---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days (Monday and Tuesday), only while the coin's 30-day hourly volatility is high against its own last 6 months and its 30-day return is negative; the deeper its 30-day fall, the larger the fall after the weekend rise.
Consequence: A trader would fade weekend rises in turbulent coins that are in a monthly decline, and do it more strongly the deeper that decline.
Why:
- F7: The fall is largest after a 30-day decline. It is +1.68 % (t 2.54) when the 30-day return is in its lowest quintile (-60 % to -21 %) and +1.31 % (t 2.27) in the next. It is -0.97 % (t -1.66) when the 30-day return is near flat (-4 % to +17 %).
- F5: The effect rests on a few periods, which is why the leave-one-window-out Sharpe fails (-0.188):
- F4: The fall grows with the coin's 30-day hourly volatility. By volatility quintile, the 48-hour short move is -0.81 % (t -0.99), +0.80 %, +0.90 %, +1.09 % and +1.79 % (t 2.19), about 155 cases each.
