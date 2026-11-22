---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return to 00:00 UTC is partly reversed over the following 24 hours, and the larger that day's move, the larger the opposite move the next day.
Consequence: A trader can fade a coin's large UTC-day move over the next day and should refuse to chase it.
Why:
- F4: A coin's 24-hour return to 00:00 UTC is partly reversed over the next 24 hours on most days of the week, in non-overlapping daily cases (about 2100 to 2240 per weekday).
