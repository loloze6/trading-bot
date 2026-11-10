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
- Situation: a sharp up move on unusually low volume -> adapted: low volume becomes a regime veto (bar volume below its 20-bar mean), and the size of the move is graded.
- Comparison: none in the idea (the brief's contrast with high-volume moves belongs to a sibling idea) -> kept
- Outcome: price falls back after the move, so it goes down -> adapted: "after the move" becomes a short held over the next bar, sized by the move.
- Verdict transfer: yes: the short earns before costs only if low-volume up bars are followed by falls, and it loses if they hold.
Forecast: The forecast is zero unless the bar's volume is below its 20-bar mean. Volume is the idea's condition, so it is set in the regime detector. The detector uses a constant +10, passed through `volume_filter(20)`. A low-volume bar reads below 5, which selects `mean_reversion`. Every other bar falls back to the null `unknown` regime, so the position is flat. On a selected bar, the component is the 1-bar percent move (`PriceEvolutionComponent`, period 1). It is first standardised over its last 60 values (min 20). It is then clipped at 0, so only up moves count, and damped with `signed_power` (exponent 2, pivot 10) so small moves give little and sharp moves give a lot. Last, it is negated. The result is a short of 0 to 20, growing with the square of how large the up move was against recent moves. It is zero on down bars and on bars with normal or high volume, and never long.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take every bar with a non-zero forecast. Measure BTC's close-to-close return over the next bar, minus BTC's mean 1-bar return over all bars of the same window. Weight each by |forecast|, pool across the 6 windows, and give the t-statistic of that weighted mean.
- Supporting check: Split active bars into terciles of |forecast|. Compare the mean next-bar excess return of the top tercile with the bottom tercile; the top should be the more negative.
- Confirm: The weighted mean excess return is negative with t ≤ -2, and the top tercile's mean is below the bottom tercile's. That means the short beats holding the coin, before costs.
- Reject: The weighted mean excess return is ≥ 0, or the top tercile's mean is ≥ 0 and above the bottom tercile's.
- Inconclusive: A negative mean with -2 < t < 0, or a negative mean whose terciles are not ordered. The test needs at least 60 active bars pooled across windows, and at least 20 in the top tercile; with fewer, it is inconclusive.
