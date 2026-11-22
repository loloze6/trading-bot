---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next two hours to one day, and the larger that hour's fall in typical hourly moves and the deeper the coin's 24-hour fall before it, the larger the rebound.
Consequence: A heavy-volume capitulation hour after a falling day is a reason to buy the rebound for up to a day rather than sell it.
Why:
- F6: Heavy-volume falls are followed by rises, not continuation. Hours with a volume-weighted scaled return of −10 to −3 are followed by +19.7 bp over 2 hours (t 2.71, n 607) and +36.5 bp over 24 hours (t 1.67). Strong down-hours (below −2 standard deviations) that come after a prior 24-hour fall of more than 2 day-scaled standard deviations are followed by +111 bp over 2 hours (t 2.65), +100 bp over 6 hours and +252 bp over 24 hours (t 2.66, n 95). That 6-hour move is about nine times the cost of a trade.
- F2: The fees eat everything the book gains before costs. The forecast is positive on 49 % of all hours, and the book trades 3.6 times a day. Per bar, the gain before costs is 0.24 bp on BTC against 0.53 bp of fees, and 0.46 bp on ETH against 0.45 bp. So the signal fires on ordinary up-hours, not on rare surges.
- F1: The tested effect is too small to pay for a trade: per case the total 6-hour move is +0.01 % and the unusual move is −0.03 % (strength −0.015, t −1.38, 11507 cases), against a cost of 0.11 % per trade. As a result the book fails every gain and fall measure: Sharpe −0.26, mean daily return −0.037 %, Calmar −0.25, and the lowest Sharpe with one window left out is −0.39.
