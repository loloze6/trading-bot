---
idea: 004-07_btc-leads-alts-not-reverse
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin's past returns -> replaced: the config sees only one coin's bars, so it cannot pair bitcoin's moves with an altcoin's.
- Comparison: bitcoin leading altcoins vs altcoins leading bitcoin -> replaced: no second coin's returns exist in the config, so neither direction of the lead can be measured.
- Outcome: later altcoin returns in bitcoin's direction -> replaced: the only coin under test is BTC/USDT; altcoin prices are not in its bars or feeds.
- Verdict transfer: no: a single-coin forecast on BTC cannot measure a lead from one coin to another, so no result on it bears on the idea.
Reason: The idea is a lead-lag relation between two coins: bitcoin's earlier returns compared with later altcoin returns, and the reverse. The config sees only one symbol's own bars and feeds, and the guide states that another coin's prices are data it cannot use.
