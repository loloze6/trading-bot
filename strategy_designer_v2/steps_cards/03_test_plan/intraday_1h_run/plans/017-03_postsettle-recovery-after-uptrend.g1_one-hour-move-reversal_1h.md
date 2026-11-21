---
idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's last-hour return, sized against its recent hourly volatility -> kept
- Comparison: the reversal is stronger when the coin's 30-day volatility is high -> kept: the criterion measures it from the closes, by the 720-bar volatility on each bar
- Outcome: the next 1-hour return runs against the last-hour move, and grows with that move's size -> kept
- Verdict transfer: yes: a fade that earns more with its size, and earns more in high 30-day volatility, is the idea; a significant loss from fading rejects it.
Forecast: The forecast starts from the last 1-hour return divided by the standard deviation of the last 20 hourly returns. This is the move in usual moves. It is standardised against its own past 60 values, so a typical move gives about 10, capped at ±20. Then it is negated. The forecast is short after an up-hour and long after a down-hour, and its size grows linearly with how sharp the move was against recent volatility. It is near zero after a quiet hour and never follows the move. No regime is used: the 30-day volatility claim is tested in the criterion, not in the sizing.
Config: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The excess gain on every bar, pooled over all coins and windows. It is postRebalance_current_allocation × (close[t+1]/close[t] − 1) minus the same allocation × the coin's mean hourly return over all its windows. The t of its mean is taken before costs.
- Supporting check: On each bar, compute the 30-day volatility from the closes: the standard deviation of the last 720 hourly returns, within the window. Then compare the mean excess gain on bars above the coin's median 30-day volatility with the mean on bars below it. The check passes when the high-volatility group minus the low-volatility group has a Welch t ≥ 2.
- Confirm: The main mean excess gain has t ≥ 2, and the supporting check passes.
- Reject: The main mean excess gain has t ≤ −2.
- Inconclusive: Inconclusive results are: - a main t between −2 and 2; - a main t ≥ 2 while the check's t is below 2. The minimum is 10,000 bars pooled, with at least 2,000 bars in each volatility group. Bars without a full 720-bar volatility inside their window are left out of the check.
