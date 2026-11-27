---
idea: 072-02_choppy-deep-up-day-fade
brief: 072_choppy-deep-below-high-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a choppy market, a day that closed up, close below the 20-day high in 20-day return standard deviations -> kept: choppy is the profile, the up close is a regime, and the depth is measured directly.
- Comparison: the further below the high, the larger the fall (deeper against shallower) -> kept: the short grows with the depth.
- Outcome: the price falls over the next day -> kept: short, held 1 bar.
- Verdict transfer: yes: the forecast is the idea's depth on its up days only, measured on the next day's move.
Forecast: A regime rule uses the day's 1-bar return, in percent (`PriceEvolutionComponent`, period 1). When it is above 0, the bar is in `mean_reversion`. Every other bar is in `unknown`, which is flat. Step 3's code adds the choppy profile. In `mean_reversion`, the forecast is `VolatilityScaledDistanceFromHighComponent` with period 20, vol_period 20, source close, the current bar included and base level. That component gives (close − highest of the last 20 closes) / that high / std of the last 20 daily returns, which is never positive. It is standardised over 60 bars (min 20) and then clipped at max 0. The forecast is 0 when an up day closes at its 20-day high. It grows more negative, so the short grows, as the close sits more usual daily moves below the high. It is never positive, which keeps the book short only.
Config: 072-02_choppy-deep-up-day-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Take each bar with a forecast below 0. Compute (|forecast| / 10) x −(next-day return − the coin's mean daily return over all its windows). Report the mean of these values and its t, with cases on the same day summed into one. This is the depth-weighted short gain before costs, measured against holding the coin.
- Supporting check: Split the cases into thirds by the depth value (`post_pipeline_value`). The deepest third's mean excess next-day return minus the shallowest third's must be below 0.
- Confirm: The main-measure t is 2 or more and the supporting check is below 0.
- Reject: The main-measure t is −2 or less, meaning deep up-day closes are followed by rises in proportion to depth.
- Inconclusive: A t between −2 and 2, or a t of 2 or more with the check at or above 0. At least 200 cases on at least 150 distinct days are needed; with fewer, the result is inconclusive.
