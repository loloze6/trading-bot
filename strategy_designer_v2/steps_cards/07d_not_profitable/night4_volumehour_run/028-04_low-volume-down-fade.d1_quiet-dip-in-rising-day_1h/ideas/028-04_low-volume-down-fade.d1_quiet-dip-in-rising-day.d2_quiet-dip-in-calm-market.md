---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day
line: 7.d not profitable
backtest: 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price recovers part of that fall over the next two to six hours, only while the coin's 24-hour return before that hour is a rise and its hourly volatility over the past 7 days is below its hourly volatility over the past 30 days; the calmer the past 7 days against the past 30, the larger the recovery.
Consequence: A trader buys quiet-volume dips in rising days only when the market has been calming, and stands aside when recent volatility is swelling.
Why:
- F1: The move per case is too small to pay for the book's turnover. A case's 6-hour total move is +0.09 % (unusual +0.06 %, t 2.27, 5857 cases), against 0.11 % per buy and sell. Over the record the book's gross gain was 1.47 on BTC and 2.89 on ETH, against fees of 2.58 and 2.11, from 6872 and 6659 rebalances and a summed turnover of 5054 and 3841. The book loses on fees, mostly on BTC.
- F4: Calm recent volatility strengthens the effect, and agitation reverses it. Calm means the 7-day hourly volatility is low against the 30-day one; agitated means it is high. In calm conditions with a 7-day rise, the unusual 6-hour move is +0.20 % (t 3.87, n 1233; total +0.23 %). In agitated conditions with a 7-day fall, it is −0.20 % (t −2.39, n 897). Over all cases, the quintiles of this volatility ratio fall steadily, from +0.16 % (calmest) to −0.05 % (most agitated).
- F5: The forecast does not grade the effect it trades. 4685 of 5857 cases sit at the cap of 20 because of the cubic transform, and they earn less (+0.05 % unusual) than the uncapped cases (+0.08 %).
