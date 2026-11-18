---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4658 USD
---
## Findings
- **F1:** The direction of follow-through after a large daily move depends on the coin's 20-day volatility rank, and the rank works as a graded moderator: regressing the excess 3-day return on z × (vol rank − 0.5) gives slope −0.031 with t = −5.46 over 1091 non-overlapping 3-day cases. Here z is the day's return over its 60-day mean absolute daily return.
- **F2:** In low-volatility stretches (20-day vol rank below 0.5 of its last 100 days), a large daily move continues rather than reverses, which the tested idea does not explain. On 3 days the excess-return slope on z is +0.0052 (t = 2.60, n = 677), positive in both coins (BTC +0.0032, t 1.25; ETH +0.0069, t 2.27) and in both halves of the windows (t 2.34 and 1.27). On 7 days the slope is +0.0109 (t = 2.01, n = 305).
- **F3:** Fading the top 20% of daily moves loses when volatility is low and earns when it is high. In low volatility the fade loses −0.0077 after down days (t −1.09, n 79) and −0.0093 after up days (t −1.79, n 104). In high volatility it earns +0.0263 (t 2.10, n 50) and +0.0181 (t 2.56, n 81).
- **F4:** The high-volatility reversal the strategy trades is short-lived. Its 3-day slope is −0.0070 (t −3.99, n 414), positive... rather, still negative and significant, but the 7-day slope is +0.0007 (t 0.15, n 174), so the give-back is complete within about 3 days.
- **F5:** The book earns from timing, not from the market, yet trails holding. Its timing gain is 0.000712 per bar against a market gain of −0.000018, but its daily Sharpe is 0.43 against 0.64 for holding. Its long positions earn 0.00169 per bar against 0.00052 for its shorts.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation` (from F1, F2, F3): In a coin whose 20-day volatility is low relative to its last 100 days, a large one-day move continues in the same direction over the next 3 to 7 days. The larger the day's move relative to the coin's 60-day mean absolute daily move, and the lower the 20-day volatility rank, the larger the continuation.
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly` (from F1, F4, F3): In a coin whose 20-day volatility is high relative to its last 100 days, the give-back after a large one-day move happens within the next 3 days. The larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over those 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
