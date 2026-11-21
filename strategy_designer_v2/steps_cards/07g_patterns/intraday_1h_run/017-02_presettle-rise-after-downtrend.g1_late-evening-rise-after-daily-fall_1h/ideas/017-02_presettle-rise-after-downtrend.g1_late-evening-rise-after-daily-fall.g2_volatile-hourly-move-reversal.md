---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next hour runs against its last hour's return. The larger the last hour's move relative to its recent volatility, the larger the reversal, and the reversal is stronger when the coin's 24-hour volatility is high against its own past month.
Consequence: A trader would fade sharp single-hour moves, sizing up with the move's size in volatile spells, and refuse the fade if no reversal appears.
Why:
- F3: A coin's next hour reverses its last hour, graded by the size of that move. Next-hour excess runs from +4.6 bp (t 7.0) in the lowest decile of the vol-scaled last-hour return to -3.1 bp (t -6.3) in the 9th decile. The reversal slope is -4.5 bp per unit (t -11.7) in the highest tercile of volatility relative to its 30-day median, against -0.2 bp (t -1.0) in the lowest tercile. It shows in every year (t -0.6 to -7.5) and is strongest in LTC, XMR, XRP and ZEC (t -5.0 to -7.5).
