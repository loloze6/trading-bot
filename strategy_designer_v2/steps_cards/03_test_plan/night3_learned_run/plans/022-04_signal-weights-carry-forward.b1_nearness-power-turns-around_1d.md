---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: af2e424c34f8
---
Fidelity:
- Situation: a coin's nearness to its 90-day high has had high predictive power for its 5-day returns over the past 365 days -> kept: `SignalPredictivePowerComponent` (signal "high", high_period 90, corr_lookback 365, horizon 5) measures it as stated.
- Comparison: the higher that past power, the lower the power over the following 90 days -> replaced: the catalogue only allows a bet against the signal in proportion to w (`PastPredictivePowerWeightedCompositeComponent` "single", negated), and that bet's gain mixes the w-to-future-power slope with the average level of power.
- Outcome: the same signal's predictive power for 5-day returns is lower over the next 90 days -> replaced: the counter-bet's gains show a sign reversal of power, not a power that is merely lower (a decay from 0.3 to 0.1 would lose money and still fit the idea).
- Verdict transfer: no: a losing counter-bet would not reject an idea that claims only lower, not reversed, power, and a winning one could come from the average level of power rather than its relation to past power.
Reason: The idea's outcome needs the past power centred on its usual level and multiplied by the signal, so that the position's gain follows the future power relative to the past power. Components combine only by weighted sums, with no product, and `standardise` does not centre, so no catalogue component or combination computes this.
