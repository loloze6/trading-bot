---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: A coin's return over the hour from 01:00 to 02:00 UTC is below its average hourly return.
Consequence: A trader could time entries for longs after that hour, or hold shorts through it.
Why:
- F11: One hour-of-day effect holds across both coins and both years. Returns at UTC hour 1 average -3.95 bp (t=-2.10) and are negative in all four coin-year cells (-1.4 to -6.3 bp). The positive effects at hour 20 (+4.39 bp, t=2.36) and hour 22 (+3.79 bp, t=2.17) are not consistent: hour 20 is -2.2 bp for ETH in 2023, and hour 22 is about 0 in 2022.
