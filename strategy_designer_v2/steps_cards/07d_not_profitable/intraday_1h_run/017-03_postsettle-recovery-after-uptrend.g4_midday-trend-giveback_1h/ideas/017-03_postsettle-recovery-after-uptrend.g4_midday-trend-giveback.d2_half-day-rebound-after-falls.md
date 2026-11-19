---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback
line: 7.d not profitable
backtest: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a 3-day fall, a coin rises over the 12 hours from 11:00 UTC, and the larger the 3-day fall, the larger that rise.
Consequence: A trader could hold the midday rebound in a fallen coin for half a day instead of three hours, so the same single round trip is paid against a larger move.
Why:
- F1: The forecast's edge is real but smaller than the cost of trading it: trades earn +0.065% before fees (t 5.98, n 26111, 53% winners) but pay a 0.100% fee gap each, leaving −0.035% per trade, and per coin-day the book makes 0.028% gross against 0.117% in fees.
- F2: The fee comes from the daily round trip: the position is opened on the 10:00 bar (mean change 0.48 of the book, fee 0.051%) and closed on the 13:00 bar (change 0.48, fee 0.051%). That is about 1.49 trades per day, and it pushes the book below zero in every year from 2018 to 2025 (daily −0.028% to −0.12%).
- F4: Almost all of the gain is on the long side. Longs after a 3-day fall earn +0.107% gross per trade (net +0.007%) and a +0.113% 3-hour move. Shorts after a 3-day rise earn +0.025% (net −0.075%) and +0.008%, and over 12 and 24 hours the coin keeps rising against the short (−0.17% signed).
