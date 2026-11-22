---
idea: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: aaeaf3675030
---
Fidelity:
- Situation: an unbroken streak of falling 4h bars with a large loss in typical 30-day 4h moves -> kept
- Comparison: only while the coin's 30-day return is positive, and the stronger the rise, the larger the rebound -> kept
- Outcome: the coin rises over the next three days, more the deeper the streak -> kept
- Verdict transfer: yes: the forecast buys only down-streaks in coins up over 30 days, sized by the streak's loss in typical moves, so the test's result is the idea's.
Forecast: A regime gate first checks the 30-day (180-bar) percent return. When it is above 0 the bar is `mean_reversion`; otherwise the bar is `unknown`, which is flat. Inside the gate, one indicator is used: the current down-streak's summed loss, divided by the mean absolute 4h move over the last 180 bars (30 days). It is 0 unless the current bar closed down, and it grows with each further falling bar. It is standardised over its own past 181 values (min 45). It is then passed through a cubic graded dead zone (`signed_power`, exponent 3, pivot 10), so ordinary small streaks give almost no position and deep streaks a large long. The forecast is never negative: it is positive only during a down-streak in a month-rising coin, and 0 otherwise. The idea's second grading, a larger rebound the stronger the 30-day rise, is not sized in the forecast; it is tested by the supporting check.
Config: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a bet: the forecast rises by 2 or more on a bar, counted once per 18-bar grid cell. For each case, take the coin's 18-bar return from that bar's close, minus the coin's normal 18-bar drift over all its windows. The measure is the mean of these unusual moves and its t, pooled over coins and windows.
- Supporting check: Split the cases at the median of their 180-bar return at the signal bar. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The mean unusual move is above 0 with t >= 2 over at least 30 independent cases, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, or a confirm-sized main result whose supporting check fails, or fewer than 30 independent cases.
