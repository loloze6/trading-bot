---
idea: 013-06_breakout-volume-drives-continuation
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: a coin closes above its prior 52-week high (the breakout day) -> kept: the regime fires while the close is above the highest of the prior 365 closes.
- Comparison: breakout-day volume against its own 90-day average volume -> adapted: an on/off "higher volume" judgement made graded, as the ratio of today's volume to the prior 90-day mean.
- Outcome: the 30-day return after the breakout is larger the higher that volume ratio -> adapted: the 30-day holding period is dropped from the config, and the 30-bar return is measured in the criterion.
- Verdict transfer: yes: the criterion relates each breakout's 30-bar return to its recorded volume ratio, which is exactly the idea's claim.
Forecast: A regime rule uses DistanceFromHighComponent (period 365, close, current bar excluded, percent). When the close is above the prior 365-close high, the bar is a breakout ("trending"). On every other bar the forecast is 0 (flat). On breakout bars the forecast is VolumeRatioComponent: today's volume divided by the mean of the prior 90 days' volume, standardised against its own last 90 values. The forecast is always positive (long only) on those bars. It is about +10 at usual volume, grows with heavier volume up to the cap of +20, and shrinks towards 0 on thin volume.
Config: 013-06_breakout-volume-drives-continuation_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The cases are breakout bars (regime "trending"), taken without overlap: in each window, the first breakout bar, then the next one at least 30 bars later. A case needs close[t+30] inside the same window. Each case's excess return is its 30-bar return minus the coin's mean 30-bar return over all its windows (holding the coin). The main measure is the pooled OLS slope of that excess return on the case's recorded volume ratio (`volratio` last_history_value), with its t-statistic.
- Supporting check: The mean excess 30-bar return of the cases in the top third by volume ratio is above zero.
- Confirm: The slope's t is 2 or more with at least 30 cases, and the supporting check passes.
- Reject: The slope's t is -2 or less with at least 30 cases, so heavier breakout volume goes with smaller 30-bar returns.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more while the top-third mean excess return is not above zero. Fewer than 30 non-overlapping breakout cases is also inconclusive.
