---
idea: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 9111077ea370
---
Fidelity:
- Situation: an unbroken streak of falling 4h bars, its loss large against the typical 4h move over the past 30 days, while the 30-day return is positive -> adapted: the streak's loss in mean absolute 4h moves over 180 bars, graded, held while the streak lasts; the 180-bar return above 0 is a regime condition.
- Comparison: the streak's loss against the coin's typical 4h move over the past 30 days -> kept
- Outcome: the coin rises over the next three days, more after a larger loss -> kept: a long position sized by the loss and held 18 bars.
- Verdict transfer: yes: the forecast is the idea's own graded loss, gated by its own 30-day condition, and judged on its 3-day forward rise.
Forecast: The forecast uses one long-only component, DownStreakLossInUsualMovesComponent (window 180, max_bars 180, side "down", base "start"). It measures the current down-streak's loss divided by the mean absolute 4h return over the last 180 bars (30 days), and it is 0 on any bar that did not close down. The component is standardised over 180 past values (min_periods 45), passed through signed_power (exponent 3, pivot 20) so that small streaks give almost nothing and large losses grow steeply, and clipped at 0. The forecast is active only in the regime where the 180-bar return (PriceEvolutionComponent, period 180) is above 0. Elsewhere it is flat. It is never negative.
Config: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are the bets (forecast rises of at least 2 points on the long side), read once per cell of the non-overlapping 18-bar grid of each window. For each case, take the coin's 18-bar return from the signal bar minus the coin's normal 18-bar drift over all windows. The measure is the mean of this unusual move over the cases and its t.
- Supporting check: Split the cases at the median entry forecast. The mean unusual move of the top half minus that of the bottom half must be above 0.
- Confirm: The mean unusual move is positive with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, a positive t ≥ 2 whose supporting check fails, or fewer than 30 cases.
