---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the closer the coin's close on that day to its lowest close of the past 90 days, the larger the fall.
Consequence: A trader would short bounces that leave a falling coin still near its 90-day low, and refuse to short bounces from coins that have already climbed well off it.
Why:
- F1: The main measure is on the side the idea predicts but too small to show: the mean unusual 5-day move in the short direction is +0.29 % per case (t 1.08, 1,337 cases, strength 0.029). That is about half the 0.05 strength of real ideas measured so far, and after the coins' normal drift of -0.59 % the total move is -0.30 % per case, against a trade cost of 0.19 %.
- F3: The effect is mixed across coins and none of the six shows it clearly. ETH (+1.13 %, t 1.55), LTC (+0.85 %, t 1.56) and ZEC (+0.73 %, t 1.10) lean toward a fall, while XRP (-0.94 %, t -1.15) and XMR (-0.38 %, t -0.59) lean the other way.
