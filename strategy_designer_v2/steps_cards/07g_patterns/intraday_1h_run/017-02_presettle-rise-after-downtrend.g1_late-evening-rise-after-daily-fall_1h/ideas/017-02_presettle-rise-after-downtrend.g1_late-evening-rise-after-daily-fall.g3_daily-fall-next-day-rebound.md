---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 24 hours runs against its past 24-hour return. The deeper its 24-hour fall relative to its recent volatility, the larger the rebound over the following day.
Consequence: A trader would buy coins after sharp daily falls for a one-day hold, sized by the depth of the fall, and refuse that buy if no rebound appears.
Why:
- F4: On a non-overlapping daily grid, the bottom quintile of vol-scaled 24-hour return is followed by +34.5 bp excess over the next 24 hours (t 3.7, n 3421). The top two quintiles are followed by -16.1 bp (t -2.0) and -15.6 bp (t -1.9).
