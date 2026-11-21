---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price rises more than the coin's usual 5-day return over the next 5 days. The larger the coin's 30-day return before the surge, measured in its usual 30-day moves, the larger the excess rise.
Consequence: A trader would hold a sharp up day for five days when it comes inside a month-long rise, and give it little weight when the month was flat or falling.
Why:
- F1: The book fails because the shortfall it bets on is not in the data, so its shorts sit against the coins' own rise. Per case the unusual move on the short side is -0.18 % (t -0.47, 1186 cases) and the total move is -1.03 %, which is -4.6 times the 0.22 % cost of a trade. Per hour the book's gain splits into -0.084 bps from the market's own rise and only +0.008 bps from timing.
- F4: Taken over all prior weeks, such a first surge is followed by a 5-day rise beyond the coin's normal drift of +0.76 % (t 2.27, 2067 cases, strength 0.056). This continuation grows with the prior week's rise in usual moves:
- F5: The continuation after a surge is graded by the coin's 30-day return in usual 30-day moves. The drift-removed 5-day move is:
- F7: The after-fall cases change sign from year to year, so no stable fade exists to rescue. Their drift-removed 5-day move is -4.2 % in 2021 (t -2.34) and -2.5 % in 2025 (t -3.87), but +1.6 % in 2023 (t 2.47) and +3.2 % in 2024 (t 3.95).
