---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move -> replaced: the config sees only the traded coin's bars, so bitcoin's move cannot be measured.
- Comparison: the altcoin catching up to the bitcoin move, a later response -> replaced: the gap between bitcoin's move and the altcoin's move needs both coins' bars.
- Outcome: smaller altcoins keep rising over the following bars -> kept: the coin's own forward return, long side.
- Verdict transfer: no: a forecast built from the altcoin's own bars tests that coin's own momentum, not a lagged response to bitcoin.
Reason: The situation is a move in bitcoin, and the outcome is in a different coin. A strategy config sees only its own symbol's bars and feeds, and the guide says it has no access to another coin's prices. A lead-lag between bitcoin and altcoins therefore cannot be expressed.
