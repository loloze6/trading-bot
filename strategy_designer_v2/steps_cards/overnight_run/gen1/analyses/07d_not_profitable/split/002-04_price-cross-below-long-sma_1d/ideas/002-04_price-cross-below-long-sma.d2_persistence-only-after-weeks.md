---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the first days after a coin's close drops below its 200-day average, the coin tends to rise back rather than keep falling. A downward drift shows up only after the close has stayed below the average for more than about two months.
Consequence: A trader should hold off shorting a fresh break below the long average and short only after the close has stayed under it for many weeks.
Why:
- F5: The early part of each short loses most: in the first 1-5 bars after the forecast turns negative the coin rose +0.30% per day (gross -0.0032 per bar), in bars 6-60 it rose about +0.16 to +0.18% (gross about -0.0016 to -0.0017), and only after 61-150 bars did it fall (-0.04% per day, gross -0.0003).
- F6: The 2488 short trades win only 23.8% of the time and average -3.89% gross against about 0.1% in fees; every duration bucket up to 30 days loses about -6% gross per trade (333 one-day trades at -6.53%, 640 trades of 11-30 days at -5.94%), and only the 500 trades held over 30 days gain (+4.96%, summed +2482).
