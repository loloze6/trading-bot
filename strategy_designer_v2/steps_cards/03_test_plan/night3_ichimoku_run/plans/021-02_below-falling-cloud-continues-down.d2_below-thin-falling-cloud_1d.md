---
idea: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: coin closes below its Ichimoku cloud and the cloud is falling -> kept: regime rule needs close below cloud bottom and a negative 26-bar cloud slope.
- Comparison: thinner cloud relative to price versus a thicker one -> kept: cloud proximity 1/(1+width in % of close) grades the short.
- Outcome: return over the next 26 days is negative, more so under a thinner cloud -> kept: 26-bar forward return, short side.
- Verdict transfer: yes: the test bets short exactly in the stated situation, sized by thinness, over the stated 26-day horizon.
Forecast: A regime is set when two conditions hold together. The close must sit below the cloud's lower edge (IchimokuCloudPositionComponent, edge "nearest", below 0). The cloud's mid level must have fallen over the last 26 bars (IchimokuCloudSlopeComponent, lookback 26, below 0). Both use the standard 9/26/52 settings with a 26-bar displacement. Only in that regime is the forecast non-zero. It is the cloud proximity 1/(1+W), where W is the cloud width in percent of the close. That proximity is standardised over its past 78 values and negated. The forecast is therefore always negative or zero: about -10 under a cloud of usual thickness, larger in size (to -20) under a thinner cloud, smaller under a thicker one. It is 0 above the cloud, inside it, or when the cloud is not falling.
Config: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Cases are the bars where the forecast is below 0, taken on a non-overlapping 26-bar grid within each window. For each case, take the coin's 26-bar return from the case's close, minus the coin's mean 26-bar return over all windows (its normal drift), and sign it in the short direction. The measure is the mean of these values, with the ordinary t of the mean.
- Supporting check: Across those same cases, the Spearman correlation between the absolute forecast (thinness) and the short-direction excess return must be above 0.
- Confirm: Main t ≥ 2 (short-direction excess return positive) with at least 30 cases, and the supporting correlation above 0.
- Reject: Main t ≤ -2 (coins below a falling cloud rise more than their drift over 26 bars) with at least 30 cases.
- Inconclusive: Any main t between -2 and 2, or t ≥ 2 with a correlation of 0 or below, or fewer than 30 non-overlapping cases.
