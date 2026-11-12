---
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
idea tested: 001-01_rsi-high-extreme-reversal-down
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3528 USD
---
## Findings
- **F1:** The idea's own bet loses before fees. All 7,700 short trades lose on average before fees (BTC −0.47%, ETH −0.57% per trade). The loss sits in trades held over 8 hours: −0.89% for 8–16h, −2.69% for 16–48h, −3.00% for over 48h. Trades closed within 2 hours win 82–95% of the time. So the runs that keep RSI above 50 for long go on rising instead of giving back.
- **F2:** High RSI is followed by more rise, not reversal, and the same holds in both coins. In the decile with the highest RSI (lowest 50−RSI), the next 12 hours beat the coin's drift by +10.4 bp pooled (BTC +8.3, ETH +12.4). The next decile down is −9.8 bp, so the step is not smooth. With overlapping 12-hour windows the true t is about 2.6/√12 ≈ 0.8.
- **F3:** Low RSI is followed by more fall, in both coins. In the lowest-RSI decile, the next 12 hours trail the drift by −24.0 bp pooled (BTC −20.3, ETH −27.7; t on overlapping bars −5.0, about −1.4 after correcting for overlap). On non-overlapping bars with RSI 35–40, the next 12 hours average −41.6 bp (n=61, t −1.3).
- **F4:** Past 12-hour returns rank the next 12 hours the same way. The top decile of past 12-hour return is followed by +19.3 bp over drift (t 4.15 on overlapping bars, about 1.2 corrected). Deciles 7–9 are all positive (+11.0, +9.2, +19.3), while deciles 0–2 are all negative (−8.2, −9.4, −12.5). The 24-hour non-overlapping version shows no ordering, so this rests on the 12-hour, overlapping view only.
- **F5:** The book bleeds whatever the volatility. When the short is active, the book's next-bar return is −2.2 to −4.4 bp in every 24-hour volatility quintile, against −0.1 to −0.4 bp when flat. The high-volatility quintile shows +15.8 bp forward excess on overlapping bars, but only t 1.34 on the grid, and its sign flips across windows and coins (BTC w3 −35, ETH w6 −33). It is not a stable pattern.
- **F6:** Hour-of-day returns line up in both coins but do not stand out from chance. Hours 19 and 21 UTC are positive in both coins (+4.6/+4.1 bp and +3.7/+3.8 bp; pooled t 2.3 and 2.2). Hours 0 and 16 are negative in both (pooled t −2.1 and −1.8). With 24 hours tested, about one |t|>2 is expected by chance, so I treat this as unconfirmed.

## Ideas
- `001-01_rsi-high-extreme-reversal-down.g1_hourly-strength-continues-upward` (from F1, F2, F4): In BTC and ETH on 1h bars, after the coin has made one of its largest 12-hour rises, or RSI(14) sits among its highest readings, the next 12 hours rise more than the coin's usual drift.
- `001-01_rsi-high-extreme-reversal-down.g2_hourly-weakness-continues-downward` (from F3, F4): In BTC and ETH on 1h bars, when RSI(14) sits among its lowest readings, the next 12 hours fall more than the coin's usual drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
