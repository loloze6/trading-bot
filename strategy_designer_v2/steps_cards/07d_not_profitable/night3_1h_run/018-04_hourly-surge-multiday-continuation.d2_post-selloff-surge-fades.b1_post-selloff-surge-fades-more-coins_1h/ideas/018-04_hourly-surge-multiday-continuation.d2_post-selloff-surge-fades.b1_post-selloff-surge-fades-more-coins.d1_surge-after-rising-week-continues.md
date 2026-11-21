---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price rises more than the coin's usual 5-day return over the next 5 days. The larger the coin's 7-day return before that day, measured in its usual weekly moves, the larger the excess rise.
Consequence: A trader would buy a sharp up day that comes after a rising week and hold it for days, and would refuse to short it.
Why:
- F1: The book fails because the shortfall it bets on is not in the data, so its shorts sit against the coins' own rise. Per case the unusual move on the short side is -0.18 % (t -0.47, 1186 cases) and the total move is -1.03 %, which is -4.6 times the 0.22 % cost of a trade. Per hour the book's gain splits into -0.084 bps from the market's own rise and only +0.008 bps from timing.
- F3: After a sharp up day that follows a falling week, the coin does not fall more than usual. On the first bar of a 120-hour cell where the 24-hour return reaches 3 usual daily moves after a negative prior week, the raw 5-day return is +0.94 % (t 2.48, 1181 cases) and the 10-day return is +1.48 % (t 2.41). The drift-removed 5-day move is -0.40 % (t -0.73) after a fall of 1 to 2 usual moves, and -0.14 % (t -0.15, 125 cases) after a fall deeper than 2.
- F4: Taken over all prior weeks, such a first surge is followed by a 5-day rise beyond the coin's normal drift of +0.76 % (t 2.27, 2067 cases, strength 0.056). This continuation grows with the prior week's rise in usual moves:
- F6: The size of the surge itself does not grade the move that follows. The drift-removed 5-day move is +0.81 % (t 2.37) for surges of 3 to 4 usual daily moves, +0.59 % for 4 to 5, and -0.56 % for 5 to 7. The traded volume of the last 24 hours relative to its 30-day mean shows no order across its quartiles (+0.40 %, +1.41 %, +0.22 %, +1.03 %).
