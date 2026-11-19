---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run down, the return over the 24 hours after each funding settlement time (00:00 and 16:00 UTC) is negative, only while the coin's 7-day hourly volatility is low, and the stronger the 3-day fall, the larger that decline.
Consequence: A trader would short calm, falling coins once at the 00:00 and 16:00 settlements and hold a full day, so that one fee is paid against a decline several times larger. They would refuse the trade at 08:00 and in turbulent falls, which rebound.
Why:
- F1: Fees, not the forecast, sink the book. The positions earn about +0.000255 a day before costs (+0.000011 per bar), but fees cost about 0.00181 a day (0.000076 per bar), seven times the gain. That leaves the book's mean daily return at -0.00154, which fails both the Sharpe test (-2.74) and the mean-daily-return test.
- F2: The fees come from the trading pattern. The book takes a short at each settlement and drops it 4 hours later, about 2.6 trades a day. Each entry hour (07, 15, 23) and each exit hour (03, 11, 19) costs about 0.00024 in fees. The hold hours add another 0.000035–0.000042 per bar from resizing. One 4-hour episode therefore costs about 0.0006 in fees, while the hold bars after the 23:00 entry gross only about +0.00008 together.
- F3: The decline after settlement is real but too small for the fees. Among the 3-day falls, only the largest quintile (mean 3-day fall -14%) falls 4 hours later by -0.0012. The other quintiles fall only -0.0001 to -0.0006, and the fee is about 0.001 a round trip (net minus gross per trade is -0.10%).
- F4: The 08:00 settlement carries nothing. After falls, the 4-hour return after the 07:00-stamped close is -0.000005, against -0.00075 after the 15:00 close and -0.0008 after the 23:00 close. Yet the 08:00 hold is entered as often (about 52% of those bars are held), so it pays fees for no gain.
- F5: How the move plays out over the next day depends on volatility.
