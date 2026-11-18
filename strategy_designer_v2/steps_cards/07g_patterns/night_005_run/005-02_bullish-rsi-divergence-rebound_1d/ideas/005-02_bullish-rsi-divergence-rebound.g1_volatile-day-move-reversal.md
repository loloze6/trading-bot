---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high, a large one-day move is partly given back over the next 1 to 3 days. The larger the day's move and the higher the coin's 20-day volatility relative to its usual level, the larger the opposite move that follows.
Consequence: In volatile stretches, fading a coin's sharp daily move for a few days earns money, and chasing such a move is a reason to refuse the trade.
Why:
- F1: When a coin's 20-day volatility is in its top third, the next day's return runs against today's: the most negative fifth of days (mean −7.0%) is followed by +1.12% above the coin's average (t 3.55, n 324), and the most positive fifth (mean +7.4%) by −0.49% (t −2.08, n 324); the low-minus-high gap is 1.64% (Welch t 4.18, Spearman −0.168, p 1e-11).
- F2: The reversal grows with volatility. In one regression the term "1-day return × volatility relative to the coin's mean" has beta −0.142 (t −6.43). In the lowest volatility third the low-minus-high gap is −0.43% (t −1.65), and over all bars it is only 0.54% (t 2.88).
- F3: The high-volatility reversal holds in each coin on its own: BTC 1.41% (Welch t 3.08, Spearman −0.163) and ETH 1.79% (t 2.82, Spearman −0.170). The gap is positive in every year with high-volatility days, from 0.53% in 2021 to 4.08% in 2020; Welch t is above 2 in 2018, 2020, 2024 and 2025.
- F4: The reversal lasts beyond one day. On a non-overlapping 3-day grid in high volatility, the lowest fifth of 1-day returns outruns the highest fifth by 4.27% over the next 3 days (Welch t 3.94, 106 cases each, Spearman −0.175).
