---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return), with its Sunday close below its 50-day average price, rises over the next 3 days (Monday to Wednesday), and the larger the weekend fall and the deeper its 30-day decline, the larger the rise.
Consequence: Weight Monday rebound trades towards coins whose weekend fall comes at the end of a deep month-long decline.
Why:
- F5: A deep 30-day decline strengthens the same situation, and the decline alone earns nothing. Cases in the lowest quartile of the 30-day return earn +2.45 % (t 4.22, 269 cases), against +0.90 %, +0.52 % and +1.28 % in the others. Non-Sunday falls below the SMA50 in that same 30-day quartile earn -0.04 % (t -0.08, 319 cases). With a falling SMA50 as well, the cell reaches +5.15 % (87 cases).
- F1: The weekend fall carries the effect and the depth term does not. By quartile of the weekend-fall part of the forecast, the 3-day excess return runs -0.40 % (t -0.81), +0.50 %, +1.14 % (t 2.68), +2.57 % (t 4.22), 373 to 374 cases each, and the top quartile makes 5.77 of the book's 9.09 summed case gain. By quartile of the depth-below-SMA50 part (standardised over 60 bars) it is flat at +0.72 %, +1.01 %, +1.08 % and +1.01 %.
- F3: Both failing measures come from the book's weak years. The deepest fall, -22.3 %, ran 54 days from a peak in w1 to a trough in w2 (2018). Sunday cases in w1 and w2 earned -0.15 % excess (t -0.19, 204 cases) against +1.13 % (t 4.29, 1289) in the other windows, and 2018 cases averaged -1.62 % (t -1.80, 112 cases). The book was in a position on only 22 % of coin-days and summed +3 % in 2023 while holding summed +115 %, so it trails holding's Sharpe by 0.093 and has a Calmar of 0.26.
