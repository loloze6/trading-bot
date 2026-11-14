---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move -> replaced: the config sees only the traded coin's own bars, and bitcoin is the signal here.
- Comparison: altcoins versus the earlier bitcoin move -> replaced: no second coin's bars exist in one config.
- Outcome: smaller altcoins keep rising over the following bars -> replaced: the test runs on BTC/USDT only, so no altcoin price is traded.
- Verdict transfer: no: a test of BTC's own momentum says nothing about altcoins catching up to bitcoin.
Reason: The idea needs bitcoin's move as the signal and an altcoin's later return as the outcome. A config reads only one coin's own bars and feeds, so it cannot hold another coin's prices. The run also covers BTC/USDT alone, so there is no altcoin to trade.
