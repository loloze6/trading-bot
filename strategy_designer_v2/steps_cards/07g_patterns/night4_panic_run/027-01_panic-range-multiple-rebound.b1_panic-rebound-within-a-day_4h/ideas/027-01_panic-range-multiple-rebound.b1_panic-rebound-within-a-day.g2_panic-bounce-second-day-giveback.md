---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day
line: 7.g patterns
backtest: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a panic (a coin falling over 24 hours with a range several times its 30-day average 24-hour range), the more the coin rebounds over the next 24 hours, the lower its return over the 24 hours after that.
Consequence: A trader buying panics would take the first-day rebound and exit, rather than hold into the second day once the price has bounced.
Why:
- F3: After a panic (a 24h fall with the 24h range in the top quintile of its 30-day multiple), the following 24–48 hours depend on the first day's outcome. When the first 24 hours rose, the next 24 hours return −0.482 % against the drift (t −2.91, 1045 cases). When they fell, the next 24 hours return +0.518 % (t 2.32, 652 cases). The rebound is paid within a day, and a first-day bounce is partly reversed on the second day.
- F5: The book's trades lose once they last more than a day. Trades of up to 16 hours make +1.567 % gross (4150 trades) and trades of 16–24 hours +1.823 % (4432). Trades of 1–1.7 days make −0.873 % (2862) and trades over 1.7 days −2.518 % (3255).
- F4: Within these panics, the deepest quartile of falls carries most of the next-24h excess, +1.786 % (t 5.52, 427 cases), against +0.42 % to +0.93 % for the other three quartiles. The panic premium is positive in every year from 2018 to 2025 (+0.23 % to +1.69 %).
