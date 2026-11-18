---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the higher its 5-day average volume against its 30-day average, the higher its return over the next 7 days, whatever the direction of its last 5 days.
Consequence: A trader would lean long on coins whose recent volume runs above its monthly norm, and would not hold coins whose volume has dried up.
Why:
- F1: Across all bars, not only after falls, the log of a coin's 5-day over 30-day average volume predicts its excess 3-day return. The pooled slope is 0.0124 with t 4.30 over 4283 non-overlapping cases. It still holds after controlling for the 5-day return (slope 0.0120, t 4.16; the 5-day return's own t is only 1.26). So the tested idea's volume effect is not limited to declines.
- F2: The same volume ratio predicts more strongly over 7 days. On a sparser non-overlapping grid of 2064 cases the slope on the excess 7-day return is 0.0346, t 5.24.
- F4: The volume slope is positive in 7 of 8 years and largest in 2024 (t 5.01). It is positive in all six coins, but only XRP (t 3.75) and ZEC (t 2.36) are individually above 2; BTC, ETH, LTC and XMR are between 0.36 and 1.32.
