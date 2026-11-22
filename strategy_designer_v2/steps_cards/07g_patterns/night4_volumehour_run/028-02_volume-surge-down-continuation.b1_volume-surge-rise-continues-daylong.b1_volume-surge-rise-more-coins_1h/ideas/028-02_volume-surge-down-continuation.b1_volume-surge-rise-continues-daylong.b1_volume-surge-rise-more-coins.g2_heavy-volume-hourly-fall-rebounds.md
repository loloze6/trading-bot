---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which a coin falls far more than its usual hourly move over the past 30 days, the price rises over the next 2 hours, and more the larger that hour's fall times its volume relative to its 30-day average hourly volume.
Consequence: A trader would buy after a sharp hourly fall on heavy volume for a couple of hours, and refuse to short into such an hour.
Why:
- F4: An hour falling more than 2.5 usual moves is followed by a rebound over the next 2 hours, and the larger its fall times its volume ratio, the larger the rebound (slope t 3.24, 2515 cases). Falls of more than 4 usual moves on more than 4 times the usual volume are followed by +0.65 % (t 3.15, 472 cases). The rebound is positive in all six coins (ZEC +0.59 %, t 3.68; XRP +0.39 %, t 2.66; BTC +0.04 %) and in 7 of 8 years. Rises of the same size are followed by -0.03 % (t -0.68, 2597 cases).
- F1: The tested idea finds nothing in the bars: its 14681 cases end 24 hours later +0.01 % above drift (t 0.21), its top half does worse than its bottom half (-0.002 %), and the hours it bets on most (a rise of more than 4 usual moves on more than 4 times the usual volume) are followed by -0.15 % over 2 hours (t -0.98, 459 cases) and -0.65 % over 24 hours (t -0.56, 43 cases).
