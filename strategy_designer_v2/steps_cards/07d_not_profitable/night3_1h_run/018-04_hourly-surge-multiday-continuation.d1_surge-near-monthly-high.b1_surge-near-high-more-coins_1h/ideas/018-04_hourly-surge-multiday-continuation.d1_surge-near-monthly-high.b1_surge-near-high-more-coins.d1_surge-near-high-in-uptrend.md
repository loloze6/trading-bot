---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while the close stands near its 30-day high and its 30-day return is positive: the closer the close to its 30-day high, measured as a plain percentage distance, and the larger its 30-day return at that hour, the larger the rise.
Consequence: A trader would take surges near the month's high in coins already rising over the month, and refuse surges inside a month-long decline, which carry the book through the coins' shared falls.
Why:
- F1: The book failed only on Calmar (0.71 against 0.75 needed). Its deepest fall, −54.5 %, outweighs its yearly return of 38.7 %. That fall ran from w1 to a trough in w3, taking 309 days to reach bottom and 936 days to recover. Holding the coins fell 71.9 % over the same stretch. The next deepest falls were also shared declines: −37.0 % in w21–w22 (holding −57.2 %), −36.0 % in w23–w24 (holding −31.5 %) and −27.1 % in w17–w18 (holding −56.4 %).
- F2: During the deepest fall the book lost more than the coin itself on several coins. Summed daily returns over the 309 days were BTC −1.48 against the coin's −0.92, ETH −1.24 against −0.95, UNI −1.19 against −0.89 and TRX −0.64 against −0.28. Only DOGE gained (+0.55 against −0.41). So the book stayed long, at a vol-targeted size of up to 2×, through the shared decline.
- F3: The trades' net result rises steadily with the coin's 30-day return at entry. Over 8,376 trades the mean net result by quintile was:
- F4: The trades' net result also rises steadily with nearness to the 30-day high at entry, from +0.62 % (t 0.78) when the close was 29 % to 64 % below the high, to +6.40 % (t 7.51) within 2.6 % of it. Yet 1,400 of the 8,376 trades (a fifth) were entered 29 % or more below the high. The forecast is standardised against its own past 500 hours, which lets surges deep inside a month-long decline still reach full size despite the nearness weight.
- F6: The idea is large enough to pay its costs. The total move is +1.18 % per case over 5 days, 5.3 times the 0.22 % cost of a trade, and the unusual move is +0.35 %, 1.6 times the cost. Trades held 426 hours on average, with a mean net result of +3.29 %, a median of −1.97 % and a 41 % win rate. The failure is the depth of the falls, not the cost of trading.
