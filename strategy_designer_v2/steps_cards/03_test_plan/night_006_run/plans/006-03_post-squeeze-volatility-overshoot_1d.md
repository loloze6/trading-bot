---
idea: 006-03_post-squeeze-volatility-overshoot
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: the coin's 20-day range is compressed against its 100-day range -> replaced: no catalogue component measures range width, and the nearest are std-based volatility measures.
- Comparison: realised volatility over the next 7 days against its own 100-day average, beyond a mere return to that average -> kept: both are computable from the coin's closes.
- Outcome: volatility over the next 7 days rises above its 100-day average, direction unknown -> replaced: a long or short spot position earns only from price direction, not from volatility size.
- Verdict transfer: no: a directional position's gains would not show whether volatility overshoots its average, so neither a confirm nor a reject would carry over to the idea.
Reason: The idea predicts how large moves will be, not which way they go. The config can only hold a long or short spot position whose gain follows price direction, and it cannot express a direction-free volatility bet such as a straddle, so the outcome cannot be turned into a forecast whose gains test it.
