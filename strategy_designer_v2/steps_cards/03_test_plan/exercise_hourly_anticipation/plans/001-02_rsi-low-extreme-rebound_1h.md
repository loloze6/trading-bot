---
idea: 001-02_rsi-low-extreme-rebound
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a low extreme -> adapted: RSI(14) below 50 graded by depth, with a smooth dead zone (signed_power), instead of a fixed cutoff.
- Comparison: rebound after extreme readings vs. after neutral readings -> kept: forward returns after the largest positions are compared with returns after flat or neutral bars and with holding.
- Outcome: price rises over the following bars -> adapted: "after the extreme" becomes "while RSI is low"; no fixed holding period.
- Verdict transfer: yes: a long position sized by RSI depth earns from the rebound only if low RSI readings are followed by recoveries beyond what holding the coin gives.
Forecast: Wilder RSI(14) on 1h closes. The raw value is (50 − RSI) × 0.4 and is clamped at 0, so it is positive only when RSI is below 50. It is standardised against its own past 60 values (target 10, cap 20). It is then squared with signed_power (exponent 2, pivot 10), so mild dips get small positions and deep oversold readings get large ones. The forecast is 0 whenever RSI ≥ 50 and never negative. It grows smoothly as RSI falls further below 50.
Config: 001-02_rsi-low-extreme-rebound_1h_config.json
Criterion:
- Horizon: 12 bars
- Main measure: The forward 12-bar return after bars whose forecast is in the top decile of non-zero forecasts, per coin. It is measured minus the mean 12-bar return over all bars of the same window (buy-and-hold drift). Returns are taken on non-overlapping 12-bar blocks, so overlapping returns count once.
- Supporting check: The same 12-bar excess return after bars with forecast 0 (RSI ≥ 50). It should be lower than after the top-decile bars.
- Confirm: Mean top-decile excess return is above 0 with t ≥ 2 on the non-overlapping cases, in at least 2 of the 3 coins. The supporting check must point the same way.
- Reject: Mean top-decile excess return is ≤ 0 in at least 2 of the 3 coins, or significantly negative (t ≤ −2) in any coin, which would point to continuation.
- Inconclusive: Any result in between, such as a positive mean with t < 2 or a split across coins. The test also counts as inconclusive if a coin has fewer than 30 non-overlapping top-decile cases across its 6 windows.
