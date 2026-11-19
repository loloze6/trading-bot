---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return, the higher its return over the 4 hours following 16:00 UTC: a stronger 3-day rise is followed by a larger further rise over those hours, and a stronger 3-day fall by a larger further fall.
Consequence: A trader would follow the coin's 3-day trend from 16:00 to 20:00 UTC, the funding hour where the fade turns into continuation.
Why:
- F5: The fade is tied to the midday clock and reverses later in the day: the 4-hour sign-fade earns t 3.18, 5.16 and 4.25 when it starts at 10:00, 11:00 and 12:00 UTC, but t −5.16 and −6.72 when it starts at 15:00 and 16:00 UTC (trend continuation), and t −4.1 to −5.0 when it starts at 21:00 to 23:00 UTC.
