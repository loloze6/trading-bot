---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) while its Sunday close sits below its 50-day average price rises over the next 3 days (Monday to Wednesday), and the larger the weekend fall measured against the coin's own recent daily moves, the larger the rise.
Consequence: Size weekend-fall rebounds by the size of the fall alone, so the small falls that lose stop diluting the book and stop carrying its falls.
Why:
- F1: The weekend fall carries the effect and the depth term does not. By quartile of the weekend-fall part of the forecast, the 3-day excess return runs -0.40 % (t -0.81), +0.50 %, +1.14 % (t 2.68), +2.57 % (t 4.22), 373 to 374 cases each, and the top quartile makes 5.77 of the book's 9.09 summed case gain. By quartile of the depth-below-SMA50 part (standardised over 60 bars) it is flat at +0.72 %, +1.01 %, +1.08 % and +1.01 %.
- F2: The Sunday timing is the effect, not the falling-below-average condition. Non-Sunday grid bars with a one-day fall and a close below the 50-day average earn -0.30 % excess over 3 days (t -1.34, 1580 cases), against +1.02 % on the Sunday cases (t 4.12, 1493 cases). Sunday falls above the 50-day average earn +0.06 % (t 0.16, 650 cases).
- F3: Both failing measures come from the book's weak years. The deepest fall, -22.3 %, ran 54 days from a peak in w1 to a trough in w2 (2018). Sunday cases in w1 and w2 earned -0.15 % excess (t -0.19, 204 cases) against +1.13 % (t 4.29, 1289) in the other windows, and 2018 cases averaged -1.62 % (t -1.80, 112 cases). The book was in a position on only 22 % of coin-days and summed +3 % in 2023 while holding summed +115 %, so it trails holding's Sharpe by 0.093 and has a Calmar of 0.26.
- F8: Cost does not explain the shortfall. The total move per case, +1.50 %, is 6.7 times the 0.22 % cost of a trade, so the problem lies in how the cases are weighted, not in fees.
