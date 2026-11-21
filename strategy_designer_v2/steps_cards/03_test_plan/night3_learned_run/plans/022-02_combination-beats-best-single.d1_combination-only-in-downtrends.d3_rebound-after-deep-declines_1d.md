---
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the coin's 90-day return is negative -> adapted: on/off condition kept as a regime rule (90-bar return below 0), active "while" it holds.
- Comparison: the further below the 90-day high, the higher the return -> kept: graded distance of the close below its 90-bar closing high.
- Outcome: higher return over the next 5 days, long rebound side -> kept: long position sized by depth, held 5 bars.
- Verdict transfer: yes: the regime is the idea's own condition and the forecast grows with the idea's own depth measure.
Forecast: A regime rule makes the forecast active only on bars where the 90-bar price change (PriceEvolutionComponent, period 90) is below 0. On all other bars the forecast is 0. On active bars the forecast is the close's percent distance below its highest close of the last 90 bars, bar t included (DistanceFromHighComponent, period 90, close, percent). That distance is standardised over a 90-bar window with min_periods 22, then negated. The forecast is therefore 0 at the 90-day high and grows in proportion to the depth below it, near +10 at the usual depth. It is never negative, so there are no shorts.
Config: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use bars where the regime is mean_reversion, sampled on the non-overlapping 5-bar grid of each window. On those bars, regress the coin's 5-bar forward return minus its normal 5-bar drift (all windows pooled, per coin) on the forecast (post_pipeline_value of depth). Report the slope's t across all coins.
- Supporting check: none
- Confirm: The slope is positive with t >= 2 over at least 100 independent grid cases: deeper positions are followed by larger excess 5-bar returns.
- Reject: The slope is negative with t <= -2 over at least 100 independent grid cases: deeper positions are followed by smaller excess returns.
- Inconclusive: Any t between -2 and 2, or fewer than 100 grid cases in the regime, is neither a confirm nor a reject.
