---
idea: 016-07_up-volume-burst-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: coin has risen over the past 3 days -> kept: a regime rule selects bars whose 72-bar return is above 0.
- Comparison: share of the period's volume traded in its few busiest hours -> kept: the top 3 hourly volumes' share of the last 72 hours' volume.
- Outcome: the coin gives back more of the rise over the next 3 days, the larger that share -> kept: a short position sized by the share, judged on the next 72 bars' return.
- Verdict transfer: yes: the test compares 72-bar forward returns of risen bars across volume-concentration levels, which is the idea's claim.
Forecast: A regime rule checks the 72-bar price change at each hourly close. When it is above 0, the bar is in `mean_reversion`; otherwise it is `unknown`, which is flat. In the risen regime, the forecast is the top-3 volume share of the last 72 bars (TopVolumesShare, period 72, top_k 3), standardised against its own past 72 values and then negated. It is always short in that regime. Its size is about 10 at the usual concentration, grows to 20 as a few hours carry more of the volume, and shrinks toward 0 as the volume spreads evenly. Outside the risen regime the forecast is zero.
Config: 016-07_up-volume-burst-reversal_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The sample is the risen-regime bars on each window's non-overlapping 72-bar grid. For each sample, take the coin's forward 72-bar return minus that coin's mean 72-bar return over all windows. The measure is Welch's t of this excess return for the top third of the size of `post_pipeline_value` (most concentrated volume) minus the bottom third.
- Supporting check: The top third's mean excess forward 72-bar return is below 0, meaning the concentrated rises actually give back.
- Confirm: The main measure is t ≤ -2, and the supporting check passes.
- Reject: The main measure is t ≥ +2, meaning more concentrated rises do better over the next 72 bars.
- Inconclusive: Anything else is inconclusive, including t between -2 and +2, or t ≤ -2 with a top-third mean at or above 0. The test needs at least 100 grid samples in each third, pooled over coins and windows.
