---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, the give-back after a large one-day move happens within the next 3 days. The larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over those 3 days.
Consequence: A fade of a sharp move in a volatile stretch should be held for days, not a week, and a fade still held after about 3 days is a reason to close it.
Why:
- F1: The direction of follow-through after a large daily move depends on the coin's 20-day volatility rank, and the rank works as a graded moderator: regressing the excess 3-day return on z × (vol rank − 0.5) gives slope −0.031 with t = −5.46 over 1091 non-overlapping 3-day cases. Here z is the day's return over its 60-day mean absolute daily return.
- F4: The high-volatility reversal the strategy trades is short-lived. Its 3-day slope is −0.0070 (t −3.99, n 414), positive... rather, still negative and significant, but the 7-day slope is +0.0007 (t 0.15, n 174), so the give-back is complete within about 3 days.
- F3: Fading the top 20% of daily moves loses when volatility is low and earns when it is high. In low volatility the fade loses −0.0077 after down days (t −1.09, n 79) and −0.0093 after up days (t −1.79, n 104). In high volatility it earns +0.0263 (t 2.10, n 50) and +0.0181 (t 2.56, n 81).
