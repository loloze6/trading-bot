---
idea: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: a31b77de3651
---
Fidelity:
- Situation: the coin closes below its Ichimoku cloud and the cloud is falling -> adapted: the two on/off conditions select a regime, and the cloud's 26-day slope is measured as the idea states it.
- Comparison: the return is more negative the slower the cloud fell over 26 days and the calmer the daily moves were over 30 days -> kept: the short is sized up as the cloud's 26-day fall and the 30-return volatility shrink against their own past sizes.
- Outcome: the return over the next 26 days is negative -> kept: each short bet is held for 26 daily bars.
- Verdict transfer: yes: the test measures the same condition, the same two size drivers and the same 26-day forward return, so its verdict is the idea's verdict.
Forecast: The forecast is flat unless the close is below the cloud's nearest edge (Ichimoku 9/26/52/26) and the cloud's mid level has fallen over the last 26 bars. On those bars the forecast is (s + v − 40) / 6: - s is the size of the cloud's 26-bar fall, standardised against its own past (window 104), with the sign flipped. It is about 10 at a usual fall and capped at 20. - v is the standard deviation of the last 30 daily returns, standardised (window 60). It is about 10 at usual calm and capped at 20. - The constant −10 carries weight 4. The forecast is always zero or below, so the book is only ever short. It is about −6.7 when the fall is barely visible and the coin is very calm, about −3.3 at usual levels, and it shrinks toward 0 as the fall steepens or the swings grow.
Config: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: Use the non-overlapping 26-bar grid of each window and keep the cells whose bar has a forecast below 0. For each cell, take the short's gain: minus (the coin's 26-bar return minus its normal 26-bar drift over all windows). Average these gains weighted by |forecast| and give the t of that mean.
- Supporting check: Split the cases at the median |forecast|. The mean drift-adjusted 26-bar return of the larger half minus that of the smaller half must be below 0.
- Confirm: The weighted mean short gain is above 0 with t ≥ 2, on at least 30 cases, and the supporting check passes.
- Reject: The weighted mean short gain is below 0 with t ≤ −2, on at least 30 cases.
- Inconclusive: Any t between −2 and 2, a confirming t with a failed supporting check, or fewer than 30 independent cases.
