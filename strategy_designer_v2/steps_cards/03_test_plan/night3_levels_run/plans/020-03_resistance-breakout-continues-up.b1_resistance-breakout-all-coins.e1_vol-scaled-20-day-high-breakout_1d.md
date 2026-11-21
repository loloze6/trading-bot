---
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: d79aab634da6
---
Fidelity:
- Situation: the daily close's distance above its highest close of the previous 20 days, in units of its 20-day daily volatility -> replaced: no component divides that distance by return volatility, and `vol_normalize` divides by price-level std x close instead.
- Comparison: a farther break versus a smaller one, graded -> kept
- Outcome: the coin rises more over the next 10 days -> kept
- Verdict transfer: no: with the volatility scaling replaced, the test would judge a different break measure.
Reason: `DistanceFromHighComponent` (period 20, exclude_current 1) gives the break in percent, but the config cannot divide it by the coin's 20-day return volatility. The weighted mean only adds components and cannot multiply or divide them. `vol_normalize` divides by the 24-bar std of price levels times close, which is a different quantity that drifts with the price. Everything needed is in the coin's own closes, so only the component is missing.
