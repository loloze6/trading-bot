---
idea: 002-02_sma-downcross-downward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short average has crossed below the long average -> adapted: "after the cross" becomes "while SMA50 is below SMA200", sized by the gap between them.
- Comparison: price after random points -> kept: forward returns on short bars are compared with the coin's unconditional forward returns over the same windows.
- Outcome: price keeps falling, more often and further -> kept: the forward 10-bar return and the share of falling outcomes on short-position bars.
- Verdict transfer: yes: "while below the long average" is the allowed adaptation of "after a downward cross", so a short that pays more than random points confirms the idea and one that does not rejects it.
Forecast: The forecast uses one indicator, the spread (SMA50 − SMA200) / SMA200 on daily closes, which is the usual 50/200 convention because the brief gives no lengths. The spread is standardised against its own past 200 values (min_periods 50) and then negated. It is clipped at a maximum of 0, so the forecast is never long. It is zero while SMA50 is at or above SMA200. Once SMA50 falls below SMA200 the forecast turns negative, a short. The short grows smoothly as the 50-day average sinks further under the 200-day one, and reaches −20 at the cap.
Config: 002-02_sma-downcross-downward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The mean 10-bar forward return of BTC on bars with a forecast below 0, minus the mean 10-bar forward return over all bars, pooled across the 6 windows. Returns are taken from non-overlapping 10-bar blocks, so overlapping returns are counted once. The test is judged before costs.
- Supporting check: Among short bars, the share of 10-bar blocks with a negative forward return, compared with that share over all bars.
- Confirm: The idea is confirmed if all of the following hold: - The conditional-minus-unconditional difference is at most −1.0% per 10 bars. - That difference has a t-stat of −2 or lower on the non-overlapping blocks. - The falling share on short bars exceeds the unconditional share by at least 10 points.
- Reject: The idea is rejected if either of the following holds: - The difference is 0 or above, meaning price does not fall further than after random points or moves after the cross reverse. - The falling share on short bars is not above the unconditional share.
- Inconclusive: Any difference between −1.0% and 0, or a difference with a |t| below 2, is inconclusive. It is also inconclusive with fewer than 12 non-overlapping 10-bar short blocks, or with fewer than 2 distinct downward crosses across the windows.
