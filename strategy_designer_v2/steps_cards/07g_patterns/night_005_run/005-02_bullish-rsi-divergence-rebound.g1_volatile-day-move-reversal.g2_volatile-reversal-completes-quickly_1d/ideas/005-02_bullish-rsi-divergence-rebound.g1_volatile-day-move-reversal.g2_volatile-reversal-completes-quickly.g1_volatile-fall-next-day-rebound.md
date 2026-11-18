---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, a sharp one-day fall is followed by a rebound over the next day. The larger the fall relative to the coin's 60-day mean absolute daily move, the larger that next-day rise.
Consequence: A trader buying a sharp fall in a volatile stretch should expect most of the rebound on the next day and take it then, rather than wait for more.
Why:
- F1: In the high-volatility regime (20-day volatility rank over 100 days ≥ 0.8), the next day's excess return falls with the day's move over its 60-day mean absolute move: slope −0.0034 (t −3.28, n 542) in BTC and −0.0058 (t −4.02, n 498) in ETH. Outside the regime the slope is flat (t −0.09 and −0.08, n 1851 and 1895).
- F3: In the high-volatility regime, the reversal after down days is fast and the reversal after up days is slow. After down days, the slope of excess return on the size of the move is +0.0059 at 1 day (t 2.93, n 517) and +0.0107 at 3 days (t 2.05, n 157). After up days it is only −0.0023 at 1 day (t −1.44, n 523) but −0.0100 at 3 days (t −2.83, n 191).
- F4: The book's trades earn on quick turns and lose when held. Trades held ≤1.5 days average +1.86% net (n 597). Trades held 1.5–3.5 days average −1.77% (n 232), and 3.5–7.5 days −5.25% (n 80). BTC shorts lose −0.75% per trade (n 244) while BTC longs gain +0.63% (n 240).
