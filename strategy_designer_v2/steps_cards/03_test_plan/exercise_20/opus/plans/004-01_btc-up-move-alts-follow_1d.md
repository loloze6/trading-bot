---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> replaced: the test runs on BTC/USDT only, and a component sees only its own coin's bars, so the trade cannot be on bitcoin's own past.
- Comparison: altcoin returns against bitcoin's earlier returns, net of their own past -> replaced: no second coin is available.
- Outcome: smaller altcoins drift up afterwards -> replaced: the altcoin's price is not in BTC's bars or feeds; only BTC's own price could be traded.
- Verdict transfer: no: the idea needs the bitcoin signal and the altcoin outcome together, and one coin's config cannot hold both.
Reason: The idea pairs a bitcoin move with a later altcoin price move, which needs a second coin's bars. The guide says a component sees only its own symbol's bars and feeds, so the cross-coin link cannot be built.
