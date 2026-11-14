---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp upward move made on unusually low volume -> adapted: "low-volume up bar" is a regime condition; "sharp" is graded by the size of the one-bar rise.
- Comparison: volume against the coin's usual volume -> kept: volume at or below 0.75 times its 20-bar average.
- Outcome: price then falls back, giving up part of the rise -> adapted: "after the move" becomes "while the move is the latest bar", a short held for the next bar.
- Verdict transfer: yes: the test shorts exactly the thin up-moves and scores the next bar's fall, so a confirm or reject applies to the idea.
Forecast: A regime veto uses VolumeExpansionHedgeComponent (vol_period 20, sf 20). It fires on an up bar whose volume is at or below 0.75 times its 20-bar average (raw value ≤ -5), and sets the mean_reversion regime. Every other bar is flat. In that regime, the forecast is the one-bar percent return (PriceEvolutionComponent, period 1), with these steps: - standardised against its last 60 values; - passed through the strongest graded dead zone (signed_power, exponent 3, pivot 20); - negated; - clipped at 0, so the forecast is short only. The forecast is near zero for an ordinary rise and grows towards -20 as the rise becomes sharp. It is zero whenever the bar is not a thin-volume up bar.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's next-bar return after each bar with a non-zero forecast, minus the coin's mean one-bar return over all 24 windows pooled (holding). Cases are pooled over all coins and windows.
- Supporting check: Among active bars, those with forecast ≤ -10 (the sharpest thin rises) should show a more negative excess next-bar return than those with forecast between -10 and 0.
- Confirm: The mean excess next-bar return is negative with t ≤ -2, counting each active bar once (the 1-bar horizon gives no overlap).
- Reject: The mean excess next-bar return is positive with t ≥ +2: thin rises keep going rather than revert.
- Inconclusive: Any t between -2 and +2, including estimates near zero, is inconclusive. So is a result from fewer than 30 active bars pooled across coins and windows.
