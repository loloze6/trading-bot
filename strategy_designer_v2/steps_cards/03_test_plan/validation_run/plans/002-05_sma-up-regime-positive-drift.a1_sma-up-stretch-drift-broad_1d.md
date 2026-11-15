---
idea: 002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the stretch from the short average's upward cross over the long average until the next downward cross -> adapted: the on/off "short above long" state is made graded as the positive SMA50/SMA200 spread, and is 0 while short is below long.
- Comparison: random stretches of the same length -> kept: judged against simply holding the coin, its mean return over all windows.
- Outcome: price rises more often and further over the stretch, upward -> adapted: the stretch has no fixed length, so it is measured as the next 1-bar return on every bar inside the stretch (no holding period).
- Verdict transfer: yes: a long held only while the 50-SMA is above the 200-SMA gains beyond holding exactly when up-cross stretches rise more often and further than random ones.
Forecast: The forecast uses the SMA spread (SMA50 - SMA200) / SMA200, standardised over its last 200 values (min 50), then clipped at 0. It is positive and grows with the spread while the 50-SMA is above the 200-SMA, which is the stretch after an upward cross. It falls smoothly to 0 at the downward cross and stays 0 (flat) while the 50-SMA is below. It is never short.
Config: 002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, the next 1-bar return minus the coin's mean 1-bar return over all windows. Pooled over coins and windows, it is tested with the t of the mean.
- Supporting check: The share of up bars (next return > 0) among bars with forecast > 0, compared with the coin's share of up bars over all bars of all windows.
- Confirm: The mean excess return has t >= 2, and the up-bar share on forecast > 0 bars is above the coin's overall share.
- Reject: The mean excess return has t <= -2 (crosses mark exhaustion, so moves reverse).
- Inconclusive: Any t between -2 and 2, or t >= 2 with an up-bar share not above the coin's. At least 300 bars with forecast > 0 are needed; with fewer the result is inconclusive.
