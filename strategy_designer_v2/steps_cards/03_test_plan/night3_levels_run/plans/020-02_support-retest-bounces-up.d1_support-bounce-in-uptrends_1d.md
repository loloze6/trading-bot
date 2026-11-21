---
idea: 020-02_support-retest-bounces-up.d1_support-bounce-in-uptrends
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e48527ec0eac
---
Fidelity:
- Situation: price falls back to a price where it turned up several times in the past 90 days, graded by the number of turns -> kept: SwingLowTouchNearnessComponent (period 90, fall_period 5) counts the swing lows near the close, weighted by nearness, only after a fall.
- Comparison: only while the 90-day return is positive, and more strongly the larger that return -> replaced: the config can gate on a positive return or add the return, but cannot scale the support reading by it.
- Outcome: the price rises over the next 5 days, more after more turns and a larger 90-day return -> kept: a long forecast with a 5-bar horizon.
- Verdict transfer: no: without the product, a test would credit or blame the idea for the return alone or the support alone, not their joint effect.
Reason: The idea is the product of a support-retest strength and the positive 90-day return. The config only takes weighted means of components, and a regime only switches the position on or off. A gated mean would still go long on a positive return with no retest at all, so no catalogue combination computes the interaction.
