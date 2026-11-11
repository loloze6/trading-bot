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
- Situation: a sharp upward move on unusually low volume -> adapted: the bar's up-move is graded by its size, gated while the bar closes up on volume below its 20-day average.
- Comparison: none -> kept
- Outcome: price then falls back, giving up part of the rise -> adapted: short while the situation holds, holding period dropped, so it is judged on the next daily bar.
- Verdict transfer: yes: the test measures whether low-volume up-days are followed by declines, scaled by the size of the move, which is what the idea claims.
Forecast: The forecast is active only on an up day whose volume is below its 20-day average. That gate is a veto on `VolumeExpansionHedgeComponent(20)`, which is below 0 exactly on such bars. On every other bar the forecast is 0. On an active bar the forecast is the day's percentage move (`PriceEvolutionComponent`, period 1), standardised against its own past 60 values, then softened with `signed_power` (exponent 2, pivot 10), then negated. It is therefore always negative (short) when active, and grows with the size of the up-move: a small rise gives a small short, and a sharp rise gives a large short, up to the +/-20 cap.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take every bar where the forecast is not zero. Compute the coin's next-bar return minus that coin's mean daily return over all 24 windows together (holding), with the sign flipped for the short side. Pool these across coins and test whether the mean differs from zero (t-test, one case per active bar, no overlap at 1 bar).
- Supporting check: Regress the next-bar excess return on the forecast across active bars. The slope should be negative: larger shorts should be followed by larger declines relative to holding.
- Confirm: The pooled mean sign-adjusted excess return is above 0 with t >= 2.
- Reject: The pooled mean sign-adjusted excess return is below 0 with t <= -2, meaning low-volume up-days are followed by gains relative to holding.
- Inconclusive: Any t between -2 and 2 neither confirms nor rejects, including results near zero. Any result with fewer than 100 active bars pooled across coins is also inconclusive.
