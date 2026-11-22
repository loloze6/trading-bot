---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its 30-day average, the price rises over the next six hours, and the larger the fall in typical moves times the log of its volume ratio, the larger the rise.
Consequence: Shorting into a heavy-volume hourly drop is a reason to refuse the trade, and a long leaning against it can be held for a few hours.
Why:
- F4: Heavy-volume falls are followed by a rebound, not by the continuation the brief expects. After hours falling more than 2 typical moves on volume more than twice the 30-day mean (n 926), the unusual return in the fall's direction was −30 bp over 2 hours (t −4.22) and −65 bp over 24 hours (t −3.47). Heavy-volume rises of the same size show nothing comparable: −1.4 bp over 4 hours (t −0.16) and +24 bp over 24 hours (t 1.48, n 874).
- F5: The rebound grows with the size of the fall times the log of its volume ratio, but only in the top quintile. That quintile (n 1014, mean score 6.8) is followed by +27 bp over 6 hours (t 2.61, strength 0.14) and +62 bp over 24 hours (t 3.41). The four lower quintiles lie between −8 and +8 bp over 6 hours, none with |t| above 1.
