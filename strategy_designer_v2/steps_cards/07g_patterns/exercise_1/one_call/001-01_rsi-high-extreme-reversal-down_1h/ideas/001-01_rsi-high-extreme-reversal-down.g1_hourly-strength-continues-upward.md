---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: In BTC and ETH on 1h bars, after the coin has made one of its largest 12-hour rises, or RSI(14) sits among its highest readings, the next 12 hours rise more than the coin's usual drift.
Consequence: A trader should refuse to short hourly strength at high RSI and instead lean with it over the next half-day.
Why:
- F1: The idea's own bet loses before fees. All 7,700 short trades lose on average before fees (BTC −0.47%, ETH −0.57% per trade). The loss sits in trades held over 8 hours: −0.89% for 8–16h, −2.69% for 16–48h, −3.00% for over 48h. Trades closed within 2 hours win 82–95% of the time. So the runs that keep RSI above 50 for long go on rising instead of giving back.
- F2: High RSI is followed by more rise, not reversal, and the same holds in both coins. In the decile with the highest RSI (lowest 50−RSI), the next 12 hours beat the coin's drift by +10.4 bp pooled (BTC +8.3, ETH +12.4). The next decile down is −9.8 bp, so the step is not smooth. With overlapping 12-hour windows the true t is about 2.6/√12 ≈ 0.8.
- F4: Past 12-hour returns rank the next 12 hours the same way. The top decile of past 12-hour return is followed by +19.3 bp over drift (t 4.15 on overlapping bars, about 1.2 corrected). Deciles 7–9 are all positive (+11.0, +9.2, +19.3), while deciles 0–2 are all negative (−8.2, −9.4, −12.5). The 24-hour non-overlapping version shows no ordering, so this rests on the 12-hour, overlapping view only.
