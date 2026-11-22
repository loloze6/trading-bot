---
idea: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken streak of falling 4h bars whose loss is large against the 30-day typical 4h move -> adapted: the streak's loss in usual one-bar moves (180 bars) is graded, not thresholded, and "after the streak" becomes "while the streak lasts"; the bet is held 18 bars.
- Comparison: only while the coin's 30-day return is negative, and a more negative return gives a larger fall -> kept: a regime gate on the 180-bar return below 0, with the grading by that return checked in the criterion.
- Outcome: the coin keeps falling over the next three days -> kept: short, horizon 18 bars of 4h.
- Verdict transfer: yes: the forecast shorts graded streak losses only in negative-month regimes, and the criterion tests both the further fall and its growth with the 30-day decline.
Forecast: The regime detector computes the 180-bar (30-day) percent return. When that return is below 0, the bar is "trending"; on every other bar the forecast is 0 (flat). In "trending" there is one component, DownStreakLossInUsualMovesComponent (window 180, side "down", base "start"). It measures the loss of the current unbroken run of down closes, counted in the coin's mean absolute 4h move over the last 180 bars. It is 0 whenever the current bar did not close down. The component is standardised against its own past 180 values (min_periods 45), then negated so that it gives a short. It then goes through signed_power with exponent 3 and pivot 10, so that ordinary streaks stay near 0 and large ones grow steeply. The forecast is never positive. It is 0 off a down streak or when the month is up, and grows more negative as the streak's loss gets larger against the usual move.
Config: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Take the cases: short bets (a fall of the forecast of at least 2 points), read once per 18-bar grid cell of each window. For each case, compute the coin's 18-bar return after the signal's close, minus the coin's normal 18-bar drift over all windows, taken on the short side and divided by the coin's usual 18-bar move. Measure the mean of this strength and its ordinary t.
- Supporting check: Across the cases, take the slope of the drift-adjusted 18-bar return on the 30-day return at the signal bar. The 30-day return is recomputed from the recorded closes, as close[t]/close[t-180]-1 inside the window. The check passes if that slope is positive with t ≥ 2: a more negative month is followed by a deeper fall.
- Confirm: The mean strength is above 0 with t ≥ 2, over at least 30 cases, and the supporting slope is positive with t ≥ 2.
- Reject: Either the mean strength is below 0 with t ≤ -2 (the coin rises more than its drift after such streaks), or the supporting slope has t ≤ -2, over at least 30 cases.
- Inconclusive: Any result with t between -2 and 2 on the main measure. Also a main confirm whose slope t lies between -2 and 2. Also any result with fewer than 30 cases in total across coins and windows.
