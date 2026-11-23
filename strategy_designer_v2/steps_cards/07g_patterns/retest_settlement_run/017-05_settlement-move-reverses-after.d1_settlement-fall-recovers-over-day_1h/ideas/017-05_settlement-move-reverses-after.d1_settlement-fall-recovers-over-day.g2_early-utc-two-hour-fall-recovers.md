---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin that falls over the 2 hours ending at 00:00, 01:00 or 02:00 UTC rises over the following 24 hours, more strongly the larger that fall against its usual 2-hour move. The rise comes on top of the reversal of its 24-hour fall.
Consequence: A fall into the first hours of the UTC day, especially after a falling day, is a reason to be long for the following day.
Why:
- F5: The 2-hour move reverses over the next 24h most strongly on bars closing at 00:00, 01:00 and 02:00 UTC (t −6.32, −8.53, −7.83, about 15,900 bars each).
- F6: At the 00:00–02:00 UTC closes, the 2-hour move keeps its reversal when the 24h move is in the same regression: coefficients −13.5 bp (t −8.96) for the 2h move and −15.5 bp (t −9.63) for the 24h move. It is negative in all six coins (t −3.52 to −8.13) and in seven of eight years (2022: +0.7 bp, t 0.20).
