---
idea: 012-01_liquidation-flush-rebound
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a bar closes sharply lower, on volume far above its 30-day average, with a long lower wick below its close -> replaced: no component measures the lower wick (close minus low), so this part has no catalogue measure.
- Comparison: volume against its own 30-day average volume -> kept: VolumeRatioComponent with period 30.
- Outcome: price rises over the next 3 days, more for bigger bursts and longer wicks -> kept: a long forecast held while the situation lasts, judged over 3 bars on daily bars.
- Verdict transfer: no: without the wick, a test of sharp high-volume falls alone cannot confirm or reject a theory that needs buyers to have absorbed the flow inside the bar.
Reason: The lower wick is the distance between the bar's low and its close. Only high/low-reading components exist (ADXDirectionalComponent, KeltnerBreakoutComponent, regime measures), and none of them, alone or combined, outputs that distance. The sharp fall (VolatilityScaledReturnComponent, period 1) and the volume burst (VolumeRatioComponent, period 30) are available, but the wick cannot be built.
