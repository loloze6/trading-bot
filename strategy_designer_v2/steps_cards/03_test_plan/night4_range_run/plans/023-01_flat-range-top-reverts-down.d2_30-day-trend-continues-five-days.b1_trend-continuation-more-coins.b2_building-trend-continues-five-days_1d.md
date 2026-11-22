---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: be08f97ea86e
---
Fidelity:
- Situation: 30-day net move a moderate share of the 30-day high-low range -> kept: `NetMoveToRangeRatioComponent` (period 30, high_low) measures the share.
- Comparison: larger 30-day return, effect rising toward the share's middle and fading near its top -> replaced: no catalogue component weights the 30-day return by a hump in the share, and the sums the config allows cannot form that product.
- Outcome: price continues in the 30-day direction over the next 5 days -> kept: a 5-bar horizon on daily bars.
- Verdict transfer: no: without the share-weighted return, a test would measure plain momentum, or momentum switched on and off by a regime band, not the idea's graded interaction.
Reason: The forecast must be the 30-day return multiplied by a weight that rises with the net-move share toward its middle and falls to zero near its top. Strategy components combine only by weighted sums, and products exist only in the regime detector's score_product mode. A regime band on the share would make the weight on/off rather than graded, and `FlatnessWeightedRangePositionComponent` multiplies range position by (1 - share), which is neither the return nor a hump.
