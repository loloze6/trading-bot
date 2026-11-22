---
idea: 029-02_breakout-volume-trapped-decline.d2_failed-breakout-in-calm-volatility
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a daily close above the prior 20-day high, then within 3 days a close back below that high -> kept: `FailedBreakoutDepthComponent` with `period` 20, `fail_window` 3 and `exclude_current` 1 measures it as written.
- Comparison: the calmer the last 20 days of daily moves against the last 60 days, the larger the fall -> replaced: no config step can scale the failure's size by the volatility ratio, so this would become a fixed on/off cut or be dropped.
- Outcome: the coin falls over the next 5 days, more when calmer -> kept: a short held for 5 bars on daily bars.
- Verdict transfer: no: without the graded calmness weighting, the test cannot confirm or reject the claim that the fall grows as volatility contracts.
Reason: The idea's forecast is a product: the failed-breakout depth times how calm the last 20 daily moves are against the last 60. The config's weighted mean can only add components, so a volatility term would open shorts with no failed breakout, and a regime cut on the ratio would turn the graded comparison into on/off. The only product in the catalogue, `FailedBreakoutDepthInUsualMovesComponent`, divides by the absolute 20-day volatility, not by its ratio to the 60-day volatility.
