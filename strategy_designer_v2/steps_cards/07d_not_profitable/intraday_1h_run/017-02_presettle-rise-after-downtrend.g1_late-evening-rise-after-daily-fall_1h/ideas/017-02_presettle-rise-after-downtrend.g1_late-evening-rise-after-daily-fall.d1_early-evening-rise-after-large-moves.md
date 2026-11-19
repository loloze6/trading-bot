---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 2 hours from the 20:00 UTC bar, a coin's return is positive, and the larger the size of its 24-hour move, the larger that late-evening rise.
Consequence: A trader would lean long from 20:00 to 22:00 UTC, more after a large daily move in either direction, because that is when the evening rise is large enough to cover a daily round trip's fee.
Why:
- F1: Fees, not the forecast, sink the book: summed over all bars the fees came to 9.26 against a gross position gain of -1.51, which is 0.000533 fee against -0.000087 gross per coin-day, leaving the book's mean daily return at -0.000621 while holding the coins made +0.001190.
- F3: The late-evening rise is real but sits earlier and around the trade window, not inside it: the mean 1-hour return across all coins is +0.000545 (t 6.75) on the 20:00 bar and +0.000436 (t 5.66) on the 21:00 bar, but -0.000039 (t -0.49) on the 22:00 bar, among the highest-t hours of the day.
- F6: From the 20:00 bar the 2-hour return is positive in four of the five 24-hour-return quintiles, and largest after the deepest 24-hour falls (+0.002171, t 6.65), next after the strongest rises (+0.001323, t 4.81), and near zero in the fourth quintile (-0.000006). That is about four times the 21:00 deepest-fall quintile's +0.000060.
