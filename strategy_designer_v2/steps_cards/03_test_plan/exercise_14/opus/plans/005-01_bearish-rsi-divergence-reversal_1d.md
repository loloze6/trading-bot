---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high than it did at the previous price high -> replaced: no catalogue component, alone or combined, compares the RSI at the current price high with the RSI at the previous price high. `DonchianBreakoutComponent` shows that price is at the top of its range. `RSIPullbackComponent` gives only the current RSI level (50 - RSI). Taking one minus the other measures "price high while RSI is low", which is not the same as "RSI below its value at the prior peak". Ranking RSI against its own recent history would need `percentile` as a second history op beside `standardise`, which V15 refuses.
- Comparison: the RSI at the previous price high, and, from the brief, new highs that come without a divergence -> replaced: no component stores or retrieves the RSI value at an earlier swing high.
- Outcome: price falls after the divergent high and gives back part of the run-up (short side) -> adapted: the forecast is held while the divergence reading is present, and is judged on forward returns against holding the coin, with no fixed holding period.
- Verdict transfer: no: built from the catalogue, the test would measure price range position against RSI level, not divergence between peaks, so its result would not confirm or reject the idea.
Reason: The idea needs the RSI at the current price high compared with the RSI at the previous swing high. That value comes from the coin's own closes and could feed a graded forecast, but no catalogue component computes or remembers the RSI at a prior peak. The nearest compositions (Donchian position minus RSI level) measure a different quantity, and RSI ranked within its own window is blocked by the single-history-op rule.
