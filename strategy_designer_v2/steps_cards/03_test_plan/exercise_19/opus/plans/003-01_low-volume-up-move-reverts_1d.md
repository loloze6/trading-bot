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
- Situation: a sharp up move on unusually low volume -> adapted: a veto selects up days with volume at most 75 % of the 20-day average, and the size of the 1-day rise grades the position.
- Comparison: volume against its usual level -> adapted: "unusually low" becomes a fixed cut at 75 % of the 20-bar mean volume.
- Outcome: price falls back, giving up part of the rise -> adapted: "after" becomes the next bar, with no holding period.
- Verdict transfer: yes: a short sized by the thin-volume rise either earns the next-day give-back or it does not.
Forecast: The regime detector reads VolumeExpansionHedgeComponent (vol_period 20, sf 20). Its value is -(1 - volume/avg) x 20, but only on an up day with volume below its 20-bar average. A veto fires when that value is at or below -5, which means an up day on 75 % or less of average volume. The veto sets the regime to mean_reversion; every other bar is flat. In mean_reversion, the 1-bar percent return (PriceEvolutionComponent, period 1) is standardised over its past 60 values. It is then negated, so the position is always short on these up days. signed_power (exponent 2, pivot 10) damps small rises toward zero and enlarges sharp ones. The forecast is 0 on every other bar, and it grows more negative the sharper the thin-volume rise.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars where the forecast is non-zero, the next-bar return is computed as (forecast/10) x next-bar close-to-close return. Its mean is compared with the same short held on all bars, (forecast/10) x the unconditional mean next-bar return. This is a t-test pooled over the 6 windows; there is no overlap at a 1-bar horizon.
- Supporting check: Among active bars, regress the strategy's next-bar return on |forecast|; the slope should be positive.
- Confirm: The excess next-bar strategy return over the hold-adjusted baseline is positive with t >= 2, with at least 30 active bars.
- Reject: The excess return is negative with t <= -2: thin-volume rises carry on rather than revert.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is any result with fewer than 30 active bars across all windows.
