---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
line: 7.e profitable but not proven
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin whose 30-day return is positive has a 24-hour fall that is large in units of its 30-day average absolute daily return, its price rises over the next 4 days by more than its usual 4-day drift, and the deeper that fall in usual daily moves, the larger the rise.
Consequence: The depth of a plunge in a rising coin, measured against its usual daily move, tells a trader how strongly to buy it for a rebound of a few days, and a shallow dip is no reason to buy.
Why:
- F4: The idea is graded where the test could not see it: by tercile of the raw fall-times-rise value, the unusual 96-hour move is +1.63 % (t 3.67, 773 cases) in the top tercile against +0.10 % in the middle and +0.56 % in the bottom; the supporting check could not be computed because 58 % of cases have the forecast at its cap of 20 (median 20), so the median split is empty.
- F5: The depth of the 24-hour fall carries the grading: the deepest tercile of 24-hour returns is followed by +1.47 % unusual move over 96 hours (t 3.18, 761 cases), against +0.22 % for the middle tercile and +0.34 % for the shallowest.
- F6: An ordinary dip in a rising month is not enough: on the non-overlapping 96-hour grid, bars with a positive 30-day return and a negative 24-hour return are followed by only +0.23 % unusual move (t 0.61, 717 cases), against +0.76 % for the signal's cases (t 3.63, 2330 cases).
- F7: The 30-day rise matters, but it gates the move rather than grading it: the lowest 30-day tercile of cases gives +0.04 % (t 0.12), while the middle and top terciles give +1.12 % (t 3.2) and +1.14 % (t 2.5).
- F8: The rebound is complete in about 2 to 4 days and does not grow after that: the unusual move is +0.24 % at 24 hours (t 2.4), +0.49 % at 48 hours (t 3.2), +0.76 % at 96 hours (t 3.6) and +0.74 % at 192 hours (t 2.3).
- F9: The rebound comes from the altcoins, not BTC: ETH, XRP and ZEC give +1.20 % to +1.61 % over 96 hours (t 1.8 to 2.6), while BTC gives +0.01 % (t 0.03, 416 cases).
