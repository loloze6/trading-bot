---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next six hours, only while the coin's 24-hour return before that hour was flat or falling, and the larger that hour's rise relative to its typical 30-day hourly move and the deeper the prior 24-hour fall, the larger the further rise.
Consequence: A heavy-volume up-hour is a reason to go long for several hours when it breaks a falling day, and a reason to refuse the long when the coin had already run up over the day.
Why:
- F4: Strong up-hours do not continue as a group. Hours of 2.5–4 hourly standard deviations up are followed by +0.2 bp unusual move over 6 hours (n 222). Strong up-hours on more than 3 times the usual volume give +20 bp (t 0.88, n 167), while those on 1–2 times the usual volume give −55 bp (t −1.41, n 53).
- F5: Whether a strong up-hour continues depends on the 24 hours before it. When the prior 24-hour return was at or below zero, the 6-hour unusual move after the up-hour is +23 bp (t 0.68, n 146) and the 1-hour move is +22 bp (t 1.71). When the prior 24 hours had already risen more than 2 day-scaled standard deviations, the up-hour is followed by −43 bp over 6 hours (t −1.72) and −84 bp over 24 hours (t −1.73, n 109).
- F1: The tested effect is too small to pay for a trade: per case the total 6-hour move is +0.01 % and the unusual move is −0.03 % (strength −0.015, t −1.38, 11507 cases), against a cost of 0.11 % per trade. As a result the book fails every gain and fall measure: Sharpe −0.26, mean daily return −0.037 %, Calmar −0.25, and the lowest Sharpe with one window left out is −0.39.
