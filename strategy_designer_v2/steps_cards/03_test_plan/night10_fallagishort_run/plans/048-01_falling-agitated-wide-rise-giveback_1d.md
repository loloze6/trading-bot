---
idea: 048-01_falling-agitated-wide-rise-giveback
brief: 048_falling-agitated-wide-rise-giveback
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, agitated market, an up day whose rise against the 30-day daily swing, times its range against the 30-day usual range, is large -> adapted: the profile is added by code, and the product is graded (zero on down days, growing with both factors), but no catalogue component computes that product.
- Comparison: rise in 30-day return standard deviations, range in 30-day mean high-to-low ranges -> kept: both bases exist inside separate components, but the config cannot multiply them.
- Outcome: the coin falls over the next day, more the larger the product -> kept: a graded short with a 1-bar horizon.
- Verdict transfer: no: without the product, a test would measure a different quantity, such as a rise in percent or a sum of the two factors.
Reason: The idea needs the day's rise in 30-day return standard deviations multiplied by the day's range in 30-day mean ranges, on up days only. `ScaledFallRangeMultipleComponent` computes only the falling-day version. `RiseTimesRangeMultipleComponent` measures the rise in percent, not against the swing. The config's weighted mean can add components but cannot multiply them.
