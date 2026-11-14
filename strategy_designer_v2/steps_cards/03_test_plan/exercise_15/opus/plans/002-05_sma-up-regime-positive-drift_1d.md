---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the stretch from an upward 50/200 SMA cross until the next downward cross -> adapted: "after the up-cross, until the down-cross" becomes "while SMA50 > SMA200", graded by the size of the spread.
- Comparison: random stretches of the same length -> kept: the in-trend bars are compared with all bars, which is the same as holding the coin.
- Outcome: price rises more often and further during the stretch -> kept: the coin's next-bar returns on in-trend bars.
- Verdict transfer: yes: the up-cross stretch is exactly the set of bars where the forecast is positive, so both a confirm and a reject carry over to the idea.
Forecast: The forecast uses the spread between the 50-day SMA and the 200-day SMA, as a percent of the 200-day SMA (50/200 is the usual daily convention; the brief gives no settings). The spread is standardised against its own past 200 values, then clipped at 0. It is positive, and grows with the spread, from the bar of an upward cross until the next downward cross. It is zero while the 50-day SMA is below the 200-day SMA. It is long only, because the idea concerns only the stretches that start with an upward cross.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar. Each bar's next-day return is counted once, so returns do not overlap.
- Main measure: The coin's mean next-bar return on bars with forecast > 0, minus its mean next-bar return on all bars. The bars are pooled over the 6 windows, and the measure is taken before costs.
- Supporting check: The share of up days on bars with forecast > 0, against the share of up days on all bars.
- Confirm: The in-trend mean next-bar return exceeds the all-bar mean, with a t-statistic of at least 2.0. The in-trend share of up days is also higher than the all-bar share.
- Reject: The in-trend mean return is at or below the all-bar mean. It is also a reject if in-trend returns are below out-of-trend returns with a t-statistic of -2.0 or lower, which would mean the moves reverse.
- Inconclusive: A positive difference with a t-statistic between 0 and 2, or a main measure and supporting check that disagree, neither confirms nor rejects. The test needs at least 100 in-trend bars and at least 3 distinct upward-cross stretches; fewer than that is also inconclusive.
