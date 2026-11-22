---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its 30-day average, the price rises back over the next 24 hours, and the larger that hour's fall in typical moves and the higher its volume against its 30-day average, the larger the rise.
Consequence: A heavy-volume hourly sell-off is a reason to buy, or to close a short, for the next day, and not to follow it down.
Why:
- F4: Heavy-volume falls are followed by a rebound, not by the continuation the brief expects. After hours falling more than 2 typical moves on volume more than twice the 30-day mean (n 926), the unusual return in the fall's direction was −30 bp over 2 hours (t −4.22) and −65 bp over 24 hours (t −3.47). Heavy-volume rises of the same size show nothing comparable: −1.4 bp over 4 hours (t −0.16) and +24 bp over 24 hours (t 1.48, n 874).
- F5: The rebound grows with the size of the fall times the log of its volume ratio, but only in the top quintile. That quintile (n 1014, mean score 6.8) is followed by +27 bp over 6 hours (t 2.61, strength 0.14) and +62 bp over 24 hours (t 3.41). The four lower quintiles lie between −8 and +8 bp over 6 hours, none with |t| above 1.
- F6: The rebound is strongest at the extreme and holds in every sub-period of both coins. Falls over 5 typical moves on volume over 4 times the mean are followed by +48 bp over 4 hours (t 1.61) and +130 bp over 24 hours (t 2.41, n 184). After heavy falls, the 24-hour unusual return is positive in all 8 coin × window-group cells, from +11 bp (BTC w1–6) to +152 bp (BTC w13–18). At 24 hours the move is about 5–12 times the 0.11 % cost of a trade.
- F2: Fees cause most of the book's loss. It made 19464 trades, all short, with a median holding of 4 hours. Each trade averaged −0.25 % gross and −0.35 % net, against a cost of 0.11 % per buy and sell. Per day, turnover was 1.73, fees took −0.091 % and the gross gain was only −0.016 %. That explains the −0.105 % mean daily return and the Sharpe of −1.93.
