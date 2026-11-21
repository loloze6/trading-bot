---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down in the past 90 days while its 30-day return is clearly negative, it tends to fall back over the next 10 days, and the deeper its 30-day decline (up to about a quarter of its price), the larger the fall.
Consequence: A trader should fade fresh closes above a recent turning high in a coin that has lost a large part of its month, rather than wait for a level that held three or more times, which comes too rarely to trade.
Why:
- F1: The book's failure comes from the ≥3-touch filter, not from the falling-month fade. Breaks of a 90-day turning high after a 30-day decline of 12 to 25 % fell 4.0 % more than the coin's drift over the next 10 days (t -4.3, 248 cases), but only 15 to 80 cases had 3 or more touches, and those show no fall (+1.4 % at exactly 3 touches, t 0.57, 53 cases).
- F2: The idea as tested is too small to pay and too rare to trade. Per case its unusual move is +0.30 % and its total move is -1.01 %, which is -4.5 times the 0.22 % cost of a trade. The book made 187 shorts at a mean net -3.86 %, won only 28 % of them, and traded 0.0045 times a day.
- F3: Among breaks after a deep fall, fewer touches gave the larger fall, the reverse of the brief's grading. A level touched twice was followed by a 5.6 % excess fall (t -4.6, 77 cases), a level touched once by 2.7 % (t -2.8, 288 cases), and 3 or more touches by 1.5 % (t -0.37, 15 cases).
- F4: The break adds to the falling month's own effect. On all grid bars with a 30-day return of -12 to -25 %, the excess 10-day move is -2.2 % (t -3.6, 471 cases), against -4.0 % on breaks in the same band.
- F5: The depth grading holds only in part. Breaks after a 30-day return of 0 to -12 % show no fall (+0.9 %, t 0.87, 201 cases; -0.05 %, t -0.04, 178 cases). Breaks after a fall deeper than 25 % fall less (-1.8 %, t -1.3, 132 cases). The correlation of the 30-day return with the excess move is only +0.05 (758 breaks).
- F6: The deep-decline break effect is broad across coins but leans on certain years. 17 of 19 coins show a fall on average. By year, 2025 gives -8.4 % (t -6.3, 91 cases) and 2021 gives -5.2 % (t -2.6), while 2018 gives +3.0 % (46 cases).
