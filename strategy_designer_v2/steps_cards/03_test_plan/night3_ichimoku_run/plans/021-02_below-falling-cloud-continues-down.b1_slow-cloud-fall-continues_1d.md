---
idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: coin closes below its Ichimoku cloud and the cloud is falling -> kept: a regime rule selects bars where the close is below the cloud bottom and the cloud's 26-bar slope is below 0.
- Comparison: a cloud falling more slowly over the past 26 days against one that collapsed fast -> kept: the cloud-slope proximity 1/(1+fall%) over 26 bars, larger the slower the fall, sizes the short.
- Outcome: the return over the next 26 days is negative, more negative the slower the fall -> kept: the book holds a short for 26 daily bars.
- Verdict transfer: yes: the condition, the slowness dose and the 26-day short outcome are measured as stated.
Forecast: The forecast is active only on bars where the close is below the cloud bottom and the cloud's mid level has fallen over the last 26 bars. On every other bar it is 0. On active bars it is short. The size is the cloud-slope proximity 1/(1+fall%), measured over 26 bars with Ichimoku settings 9/26/52/26. That value is standardised against its own past 104 values and negated. So the short is largest, about -10 or more, when the cloud has only drifted down. It shrinks toward 0 as the cloud's fall becomes a collapse, and it never goes positive. The size cannot grow gradually at the moment the coin enters this situation: the idea's strongest short sits right at a gentle fall, so the position starts at its largest there.
Config: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: The cases are the bars of a non-overlapping 26-bar grid in each window where the regime is trending and the forecast is below 0. For each case, take the coin's 26-bar return minus its normal drift, in the short direction. The measure is the mean of this unusual move, with its t, before costs.
- Supporting check: Among the cases, split at the median of slow_fall's raw value. Take the excess return (26-bar return minus drift) of the slow-fall half minus that of the fast-fall half. This difference must be below 0.
- Confirm: The main mean unusual move is positive with t >= 2, and the slow-minus-fast excess-return difference is below 0.
- Reject: The main mean unusual move has t <= -2, meaning the cases rise more than the drift. Or the slow-minus-fast difference is positive with Welch t >= 2.
- Inconclusive: Any other result, including a main t between -2 and 2, is inconclusive. A confirming main t with a dose difference at or above 0 (but Welch t below 2) is also inconclusive. Fewer than 30 cases over all coins and windows is inconclusive.
