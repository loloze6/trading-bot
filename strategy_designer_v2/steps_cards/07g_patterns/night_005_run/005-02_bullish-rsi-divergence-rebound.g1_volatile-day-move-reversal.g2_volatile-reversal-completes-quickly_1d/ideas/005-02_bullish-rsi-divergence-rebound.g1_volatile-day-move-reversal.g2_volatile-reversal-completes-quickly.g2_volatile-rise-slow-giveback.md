---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, a sharp one-day rise gives back slowly, over the next 3 days rather than the next day. The larger the rise relative to the coin's 60-day mean absolute daily move, the larger the fall over those 3 days.
Consequence: A short against a sharp rise in a volatile stretch should be held for about 3 days and not judged on its first day.
Why:
- F2: The fade in the high-volatility regime lasts about 3 days, then fades out. The 3-day slopes on the move ratio are −0.0064 (t −2.47, n 181) in BTC and −0.0131 (t −3.75, n 167) in ETH. By 5 days they shrink to t −0.82 and −0.84 (n 101, 94). Outside the regime the 3-day slopes are slightly positive (t 0.32 and 1.57).
- F3: In the high-volatility regime, the reversal after down days is fast and the reversal after up days is slow. After down days, the slope of excess return on the size of the move is +0.0059 at 1 day (t 2.93, n 517) and +0.0107 at 3 days (t 2.05, n 157). After up days it is only −0.0023 at 1 day (t −1.44, n 523) but −0.0100 at 3 days (t −2.83, n 191).
