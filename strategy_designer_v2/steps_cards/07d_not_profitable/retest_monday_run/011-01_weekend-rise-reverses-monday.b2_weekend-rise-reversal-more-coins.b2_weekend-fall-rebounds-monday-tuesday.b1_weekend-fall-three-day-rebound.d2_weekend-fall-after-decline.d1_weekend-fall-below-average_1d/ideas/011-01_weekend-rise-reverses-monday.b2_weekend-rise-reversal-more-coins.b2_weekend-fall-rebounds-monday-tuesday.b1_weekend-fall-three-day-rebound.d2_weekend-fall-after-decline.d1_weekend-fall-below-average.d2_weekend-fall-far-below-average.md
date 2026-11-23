---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the larger the weekend fall and the further in percent its Sunday close sits below its 50-day average price, the larger the rise.
Consequence: Put the largest weekend-fall bets on coins far below their 50-day average in percent, and small ones on coins only slightly below it.
Why:
- F1: The weekend fall carries the effect and the depth term does not. By quartile of the weekend-fall part of the forecast, the 3-day excess return runs -0.40 % (t -0.81), +0.50 %, +1.14 % (t 2.68), +2.57 % (t 4.22), 373 to 374 cases each, and the top quartile makes 5.77 of the book's 9.09 summed case gain. By quartile of the depth-below-SMA50 part (standardised over 60 bars) it is flat at +0.72 %, +1.01 %, +1.08 % and +1.01 %.
- F4: The raw depth below the 50-day average matters at its extreme, even though the standardised depth term does not (F1). Cases in the deepest quartile of the percent distance below the SMA50 earn +2.49 % excess (t 4.06, 208 cases), against +0.01 %, +1.16 % and +1.19 % in the other three quartiles.
- F2: The Sunday timing is the effect, not the falling-below-average condition. Non-Sunday grid bars with a one-day fall and a close below the 50-day average earn -0.30 % excess over 3 days (t -1.34, 1580 cases), against +1.02 % on the Sunday cases (t 4.12, 1493 cases). Sunday falls above the 50-day average earn +0.06 % (t 0.16, 650 cases).
