---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more evenly a coin's absolute hourly moves over the past 24 hours are spread across the hours, the larger its rise over the next 3 days.
Consequence: A trader would favour long exposure after days of evenly spread hourly moves and refuse it after days dominated by a single violent hour.
Why:
- F6: Days whose 24-hour move was spread evenly across hours are followed by larger 3-day returns than days dominated by one hour, whatever the move's direction. Grouped by the share of the day's absolute hourly moves taken by the largest hour, the next 72-hour return is 0.0061 (t 5.13), 0.0040 (t 3.42) and 0.0001 (t 0.11), n about 5317 each. High minus low is -0.0060, Welch t -3.72. Over 24 hours the same gap is weaker (t -1.39).
