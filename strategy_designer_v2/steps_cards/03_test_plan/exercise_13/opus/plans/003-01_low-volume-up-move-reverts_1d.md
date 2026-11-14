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
- Situation: a sharp upward move made on unusually low volume -> adapted: the move is the latest daily bar's percent change, used as a graded size (larger rise, larger position, zero on down days). "Low volume" is a regime condition: the bar's volume is below its 20-bar mean. Volume is graded nowhere in the catalogue except through this on/off comparison, which is allowed only in the detector.
- Comparison: volume judged against the coin's usual volume -> adapted: "unusually low" becomes "below its own 20-bar average volume" (the volume_filter convention), an on/off regime instead of a graded degree of thinness.
- Outcome: price falls back after the rise, giving up part of it -> adapted: the short position is held only on the bar after the low-volume up day (holding period dropped). The fall-back is measured by that next bar's return, which should be below the coin's normal daily return.
- Verdict transfer: yes: the test bets against exactly the low-volume rises, sized by how sharp they are, and is judged on whether price falls back right after them relative to holding; a confirmation or a rejection of that next-day drift speaks directly to the idea.
Forecast: On every daily bar, the detector checks whether today's volume is below its 20-bar mean. It does this with a constant +10 passed through volume_filter(20), which reads 0 when volume is below its mean. When the result is below 5, the bar is forced into the `mean_reversion` regime. On every other bar the regime is `unknown`, which is flat (forecast 0). In the `mean_reversion` regime the forecast comes from the 1-bar price change (PriceEvolutionComponent, period 1). It is standardised against the mean absolute daily move of the 60 bars before it (target 10, cap 20), then negated and clipped at a maximum of 0. This makes it a short-only bet against the rise: - On a low-volume up day the forecast is negative and proportional to the size of the rise relative to recent daily moves. An average-sized rise gives about -10 (100% short). A rise twice the usual size or more gives -20. - On a low-volume down day it is 0. - On a normal or high-volume day it is 0. Its size grows continuously with how sharp the up move is.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: For every bar with a negative forecast (a low-volume up day), take the next bar's return of BTC minus the mean daily return of BTC over the same window. That excess return is what the short earns relative to simply holding the coin. Average it weighted by |forecast|, pooled over the 6 windows. Each case covers one non-overlapping next bar. The t-statistic of the weighted mean is computed before costs.
- Supporting check: Split the active bars into terciles by |forecast|. The mean next-bar excess return in the top tercile (sharpest low-volume rises) should be lower than in the bottom tercile.
- Confirm: The |forecast|-weighted mean next-bar excess return after low-volume up days is negative with t ≤ -2.0, and the strategy's cumulative portfolio return, summed over the 6 windows before costs, is positive.
- Reject: The weighted mean next-bar excess return is zero or positive, meaning price after low-volume rises does as well as or better than BTC's normal daily drift, or the top tercile follows through more than the bottom tercile.
- Inconclusive: A negative weighted mean with t between -2.0 and 0 counts as inconclusive. Fewer than 60 active bars (low-volume up days) pooled across the 6 windows also makes the test inconclusive, whatever the sign.
