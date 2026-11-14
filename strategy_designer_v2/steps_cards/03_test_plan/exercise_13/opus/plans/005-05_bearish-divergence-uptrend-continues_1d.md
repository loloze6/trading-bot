---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new high over a recent window while RSI stays below its own prior high in that window (bearish divergence) -> replaced: the catalogue can measure where the close sits in its range (`DonchianBreakoutComponent`) and the RSI level (`RSIPullbackComponent`, 50 - RSI), but nothing measures RSI against its own recent peak. Using the RSI level instead of the RSI's prior high would be a different quantity.
- Comparison: the RSI's current value against its previous high made while price was lower, and, from the brief, price moves after a divergence against price moves after new highs without one -> replaced: no component holds RSI's prior peak. `percentile` on RSI cannot follow `standardise` (V15), and a veto percentile ranks RSI over its whole stored history, not against the last swing high.
- Outcome: price keeps rising to further highs after the divergence (long, continuation) -> kept: a positive forecast while the divergence is present, judged on the forward close-to-close return.
- Verdict transfer: no: built from the RSI level instead of RSI-versus-its-own-prior-high, the test would measure "new price high with a moderate RSI", which is not the divergence the idea names.
Reason: The divergence needs RSI compared with its own recent maximum (a lower RSI high while price makes a higher high). No catalogue component, alone or combined through weights, negation, centring or regimes, computes RSI's position relative to its own recent range or peak. The data is all in the coin's own closes, and a graded divergence score would fit the config's logic.
