---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin whose 3-day return is negative while its 7-day hourly volatility is low keeps falling over the next 24 hours, and the larger the 3-day fall relative to that volatility, the larger the next day's decline.
Consequence: A trader would hold a slow short on calm, steadily falling coins and turn it over rarely, rather than paying fees on every 4-hour clock window.
Why:
- F1: Fees, not the forecast, sink the book. The positions earn about +0.000255 a day before costs (+0.000011 per bar), but fees cost about 0.00181 a day (0.000076 per bar), seven times the gain. That leaves the book's mean daily return at -0.00154, which fails both the Sharpe test (-2.74) and the mean-daily-return test.
- F3: The decline after settlement is real but too small for the fees. Among the 3-day falls, only the largest quintile (mean 3-day fall -14%) falls 4 hours later by -0.0012. The other quintiles fall only -0.0001 to -0.0006, and the fee is about 0.001 a round trip (net minus gross per trade is -0.10%).
- F5: How the move plays out over the next day depends on volatility.
- F6: The forecast does sort the moves. Held bars in the strongest-forecast third gross +0.000092 per bar, against -0.000003 in the weakest third. The weakest third still holds positions averaging 0.05 of the book and pays to rebalance them.
