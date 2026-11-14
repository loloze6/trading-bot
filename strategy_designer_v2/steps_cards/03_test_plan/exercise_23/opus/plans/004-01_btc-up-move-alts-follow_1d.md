---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: bitcoin makes a sharp up move -> replaced: no config on an altcoin can see bitcoin's bars
- Comparison: altcoin's later move against the bitcoin move it catches up to -> replaced: needs bitcoin's and the altcoin's bars at once
- Outcome: smaller altcoins keep rising over the following bars -> replaced: the test runs on BTC/USDT only, so no altcoin price is traded
- Verdict transfer: no: a forecast built from one coin's own bars cannot link bitcoin's move to another coin's later return.
Reason: The idea links one coin's sharp move to another coin's later returns, but a config sees only its own symbol's bars and feeds, and the guide says it cannot read another coin's prices. Here the test also runs on BTC/USDT alone, so there is no altcoin whose drift could be traded.
