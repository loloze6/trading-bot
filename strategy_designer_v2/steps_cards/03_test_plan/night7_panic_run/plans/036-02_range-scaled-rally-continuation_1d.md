---
idea: 036-02_range-scaled-rally-continuation
brief: 036_scaled-rallies-continue-next-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a coin's 3-day return is large against its usual daily range, graded by size -> replaced: no component divides a 3-day return by a mean high-to-low range; the nearest ones scale by the standard deviation or mean absolute size of returns.
- Comparison: the average daily high-to-low range over the past 30 days -> replaced: only return-based usual moves exist, not the mean bar range as a divisor of a return.
- Outcome: the price keeps rising over the next 7 days, more after larger scaled rallies -> kept.
- Verdict transfer: no: a test on return-scaled rallies would judge a different measure of "unusual" from the one the idea names.
Reason: The idea scales the 3-day rise by the coin's mean daily high-to-low range over 30 days. No component computes a return divided by a mean bar range. No composition gives it either: weights only add, and `standardise` divides by the component's own past values, not by the range. Every bar column it needs (close, high, low) is in the coin's own bars, so only the component is missing.
