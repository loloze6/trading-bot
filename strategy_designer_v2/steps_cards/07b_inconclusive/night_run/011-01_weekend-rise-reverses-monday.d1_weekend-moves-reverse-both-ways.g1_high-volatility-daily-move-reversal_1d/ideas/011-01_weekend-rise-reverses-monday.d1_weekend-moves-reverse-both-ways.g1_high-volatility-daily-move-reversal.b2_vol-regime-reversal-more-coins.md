---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high relative to its own 120-day volatility, its last day's move reverses over the next 1 day. The larger that day's return measured in its 20-day volatility, the larger the move back, and the reversal is stronger after down days than after up days.
Consequence: Fade daily moves in proportion to their volatility-scaled size only while the coin's volatility is elevated, and stay out of daily reversal trades in calm periods, where there is none.
Why:
- F6: The pooled down-minus-up gap is on the side the idea predicts, at 0.0015 (Welch t 1.23 on 3922 vs 4149 bars). It would need roughly 2.6 times as many cases to reach t 2 at the same size, and the backtest used only 6 of the 19 coins available.
- F1: The verdict's check fails because the down-minus-up gap is concentrated in large moves. On active bars with |vol-scaled move| ≥ 1, down days reverse more than up days by 0.0121 (Welch t 4.03; 722 down, 846 up). On smaller moves the gap is −0.0010 (t −0.74; 3200 down, 3303 up). Pooled, this gives the verdict's 0.0015 at Welch t 1.23.
