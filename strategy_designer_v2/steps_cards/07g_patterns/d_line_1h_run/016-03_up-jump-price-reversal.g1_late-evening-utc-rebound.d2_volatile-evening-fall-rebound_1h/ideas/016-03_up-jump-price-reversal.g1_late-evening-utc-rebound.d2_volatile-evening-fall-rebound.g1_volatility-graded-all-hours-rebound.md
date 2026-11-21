---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours, at any hour of the day, and the effect grows larger the higher its 10-day hourly volatility ranks against its past 30 days.
Consequence: A trader can hold the 24-hour rebound after high-volatility falls for the full day from any hour, sized up with the volatility rank, instead of closing it after one hour.
Why:
- F1: The book misses the effect it was built on: of 3,310 trades the median and mean hold are about 1.0 hour, and 3,306 of the held bars sit on the 20:00 UTC close; that one hour earns -0.17 bp excess (t -0.21, n 17,404), so trades average -0.08 % before fees and -0.18 % after (0.53 % commission each), while the 24-bar rebound after a 20:00 fall in high volatility is about +34 bp per standard deviation of fall (t 5.12, n 6,069).
- F2: The 24-hour rebound after a 24-hour fall in high volatility (volatility rank ≥ 0.5) is not specific to 20:00 UTC; one non-overlapping sample per day at every close hour shows a positive slope: 54–92 bp per standard deviation of fall at closes 00:00–13:00 (t 7.9–13.3, about 6,000 cases each) and 12–34 bp at 14:00–19:00 (t 1.9–5.1).
- F3: At the 20:00 close the 24-hour response to a 24-hour fall rises steadily with the 10-day volatility rank across five bins: -42.3 bp (t -5.01, n 4,624) in the calmest fifth, -2.9 (t -0.28), +20.4 (t 2.06), +29.2 (t 2.89), and +43.1 bp (t 5.63, n 2,938) in the most volatile fifth.
- F5: The high-volatility rebound at 20:00 is positive in all six coins (20–61 bp per standard deviation, t 1.15–5.04) and in 7 of 8 years, with 2020 the exception (-2 bp, t -0.13).
