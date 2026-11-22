---
idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 9111077ea370
---
Fidelity:
- Situation: a coin falls in a streak of 4h bars on rising volume, with more volume rise counting more -> adapted: graded by the volume trend across the current down streak, with no fixed on/off cut.
- Comparison: the coin's 30-day return is positive -> kept: a regime rule that the 180-bar return is above 0.
- Outcome: the coin rises over the next seven days, more when volume rose more -> kept: long, held 42 bars.
- Verdict transfer: yes: the test measures the same streak, the same volume rise, the same uptrend condition and the same 7-day rise.
Forecast: The forecast is active only while the 180-bar (30-day) return is positive (regime `trending`) and is flat otherwise. In that regime it reads how volume changes across the current run of down-closing 4h bars: the least-squares slope of volume on bar index over the streak, divided by the streak's mean volume (`DownStreakVolumeFadeComponent`, `side` "down", `statistic` "slope"). That value is standardised against its own past 181 values and negated, so rising volume reads positive. It is then clipped at 0, which keeps the book long only. The forecast is 0 when bar t closed up or flat, when the streak is a single bar, or when volume fades across the streak. It is positive and grows as volume rises more steeply across the falling streak, up to the +20 cap.
Config: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h_config.json
Criterion:
- Horizon: 42 bars
- Main measure: A case is a bet: a rise of the forecast of at least 2 points, read once per cell of a 42-bar grid in each window. For each case, take the coin's 42-bar return from the signal bar's close minus the coin's normal 42-bar drift (holding the coin, all windows). The measure is the mean of this unusual move over all cases, before costs, with its t over the independent cases.
- Supporting check: The mean unusual move of cases whose forecast is above the cases' median, minus that of cases at or below it, is above 0.
- Confirm: The main measure is positive with t >= 2, and the supporting check is above 0.
- Reject: The main measure is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose supporting check is at or below 0 is also inconclusive. So is any result with fewer than 30 independent cases over all coins and windows.
