---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: In BTC and ETH on 1h bars, when RSI(14) sits among its lowest readings, the next 12 hours fall more than the coin's usual drift.
Consequence: A trader should refuse to buy hourly weakness at low RSI expecting a bounce, and lean short with it instead.
Why:
- F3: Low RSI is followed by more fall, in both coins. In the lowest-RSI decile, the next 12 hours trail the drift by −24.0 bp pooled (BTC −20.3, ETH −27.7; t on overlapping bars −5.0, about −1.4 after correcting for overlap). On non-overlapping bars with RSI 35–40, the next 12 hours average −41.6 bp (n=61, t −1.3).
- F4: Past 12-hour returns rank the next 12 hours the same way. The top decile of past 12-hour return is followed by +19.3 bp over drift (t 4.15 on overlapping bars, about 1.2 corrected). Deciles 7–9 are all positive (+11.0, +9.2, +19.3), while deciles 0–2 are all negative (−8.2, −9.4, −12.5). The 24-hour non-overlapping version shows no ordering, so this rests on the 12-hour, overlapping view only.
