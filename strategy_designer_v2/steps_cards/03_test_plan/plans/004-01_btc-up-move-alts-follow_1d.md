---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> kept: the BTC/USDT bars hold bitcoin's own return.
- Comparison: the altcoin's later move against bitcoin's earlier move -> replaced: the config cannot read a second coin's bars.
- Outcome: smaller altcoins drift up over the following bars -> replaced: only BTC's own next return can be traded on BTC/USDT.
- Verdict transfer: no: a test that trades BTC on BTC's own past move measures bitcoin momentum, not altcoins lagging bitcoin.
Reason: The idea needs bitcoin's move as the signal and an altcoin's later return as the outcome. A config sees only one coin's bars and feeds, and the guide says another coin's prices cannot be expressed. The test also runs only on BTC/USDT, so no altcoin is traded.
