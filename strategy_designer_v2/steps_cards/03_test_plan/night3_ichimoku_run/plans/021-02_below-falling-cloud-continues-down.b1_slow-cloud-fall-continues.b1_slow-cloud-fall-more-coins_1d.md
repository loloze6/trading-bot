---
idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: the coin closes below its Ichimoku cloud and the cloud is falling -> kept: a regime rule needs both the close-to-cloud distance (nearest edge) below 0 and the cloud mid-level's 26-bar slope below 0.
- Comparison: a slower 26-day fall of the cloud means a more negative return -> kept: the short is sized by the cloud-slope proximity, 1/(1+fall%) over 26 bars, so it grows as the fall slows.
- Outcome: the return over the next 26 days is negative -> kept: each short is held for 26 daily bars.
- Verdict transfer: yes: the regime is the idea's two conditions, the size follows the idea's slow-fall gradient, and the horizon is its 26 days.
Forecast: On bars where the close is below the cloud's lower edge (IchimokuCloudPositionComponent, 9/26/52/26, edge "nearest", base "close", below 0) and the cloud's mid level has fallen over the last 26 bars (IchimokuCloudSlopeComponent, percent form, below 0), the forecast is short. Its size comes from IchimokuCloudSlopeComponent in proximity form (9/26/52/26, lookback 26), equal to 1/(1+fall%). This value is standardised over its past 104 values and negated. It is largest, about -10, when the cloud is barely falling, and it shrinks toward 0 as the fall gets faster. On all other bars the forecast is 0 (flat). It is never positive.
Config: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Use the non-overlapping 26-bar grid of each window, on grid bars in regime "trending". Measure the forecast/10 times the coin's 26-bar forward return minus its normal 26-bar drift (the coin's mean 26-bar return over all windows). Take the mean and its t, so that a positive value means the short beats the drift.
- Supporting check: Within those cases, compare the excess 26-bar return (forward return minus drift) of the slower-fall half with that of the faster-fall half, split at the median `slow_fall.last_history_value`. The difference is slow minus fast, and Welch's t is taken on it.
- Confirm: The main mean is above 0 with t >= 2, and the slow-minus-fast difference is below 0 with t <= -1.
- Reject: The main mean is below 0 with t <= -2, or the slow-minus-fast difference is above 0 with t >= +2.
- Inconclusive: Any other result is inconclusive, including a main t between -2 and 2 and a main confirm whose check fails without reaching t >= +2. Fewer than 30 independent grid cases in the regime, or fewer than 15 per half, is also inconclusive.
