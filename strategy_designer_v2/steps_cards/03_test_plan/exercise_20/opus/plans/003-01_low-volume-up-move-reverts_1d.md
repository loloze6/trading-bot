---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: sharp up move on unusually low volume -> adapted: an up close on volume below 70 % of its 24-bar mean starts a regime, and position size grows with the size of the day's rise.
- Comparison: volume against its usual level -> kept
- Outcome: price falls back after the rise -> adapted: the fall is measured over the next bar, while the situation holds; the holding period is dropped.
- Verdict transfer: yes
Forecast: A veto uses the thin-volume up-bar reading `-(1 - volume/avg24) x 20`. The reading is non-zero only on up closes whose volume is below the 24-bar average. The veto selects the `mean_reversion` regime when that reading is -6 or lower, which means volume is under 70 % of its average. On every other bar the forecast is 0, so the position is flat. Inside the regime, the forecast is minus the 1-bar percent rise, standardised against its own last 60 values. A `signed_power` with exponent 2 is then applied, so the forecast is close to zero after small rises and grows steeply after sharp ones. The forecast is always short, and it is larger the sharper the thin-volume rise.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with a non-zero forecast, the next-bar coin return minus the coin's mean daily return in the same window, weighted by |forecast|. The bars are pooled across all windows, with each bar counted once.
- Supporting check: The same excess return, measured only on the half of active bars with the largest |forecast|.
- Confirm: The weighted mean excess return is negative with t ≤ -2, so the short strategy beats holding.
- Reject: The weighted mean excess return is positive with t ≥ +2, meaning thin-volume rises carry on.
- Inconclusive: Any t between -2 and +2 is inconclusive. Fewer than 30 active bars pooled across the windows is also inconclusive, whatever t is.
