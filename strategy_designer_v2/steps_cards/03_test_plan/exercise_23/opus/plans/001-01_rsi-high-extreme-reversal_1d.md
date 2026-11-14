---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme -> adapted: RSI above 50 is graded, with the strongest dead zone (cubed), so the position is near zero away from the extreme; "after" becomes "while".
- Comparison: behaviour after extreme readings versus after neutral readings -> adapted: in the criterion, returns after the largest short positions are compared with the coin's average return over the same windows.
- Outcome: price falls back over the following bars -> adapted: the holding period is dropped; the short position is held only while RSI stays high, and a fixed horizon is used in the criterion.
- Verdict transfer: yes: the test measures how price moves after high RSI readings compared with all bars, in both directions, so a confirm or a reject carries over to the idea.
Forecast: Wilder RSI(14) on daily closes, taken as 50 − RSI. Each value is standardised against the 60 bars before it (an average reading gives 10, capped at 20), then cubed around a pivot of 10, so readings near 50 give almost nothing and readings far above 50 give large values. Only the negative side is kept, so the forecast is never positive. It is zero when RSI ≤ 50, slightly negative when RSI is mildly above 50, and grows steeply more negative (short) as RSI rises toward an extreme.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after bars with forecast ≤ −10, minus the coin's mean 5-bar forward return over all bars of the same window. Cases are pooled over coins and windows, and overlapping 5-bar spans are counted once.
- Supporting check: Before costs, the strategy's cumulative return minus 0 (it is short only). It should be positive if the idea holds, and should not be explained by the windows' market drift.
- Confirm: The mean excess 5-bar return after forecast ≤ −10 is negative, with t ≤ −2 on non-overlapping cases.
- Reject: The mean excess 5-bar return after forecast ≤ −10 is positive, with t ≥ +2 (price keeps rising after high RSI).
- Inconclusive: Any t between −2 and +2 is inconclusive, including an estimate near zero. Fewer than 30 non-overlapping cases pooled is also inconclusive.
