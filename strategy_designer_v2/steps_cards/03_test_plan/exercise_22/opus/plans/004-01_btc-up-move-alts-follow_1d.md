---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> kept: BTC's own past return is in its bars.
- Comparison: altcoin's delayed response versus bitcoin's earlier move -> replaced: no other coin's bars are visible to the config.
- Outcome: smaller altcoins drift up over the following bars -> replaced: the only tradable price is BTC's own, not an altcoin's.
- Verdict transfer: no: a test on BTC's own bars cannot see whether altcoins follow bitcoin.
Reason: The idea links bitcoin's move to later altcoin returns, so it needs one coin's signal to trade another coin. A component sees only its own coin's bars and feeds, and the guide lists another coin's prices as data the config cannot use. The run also covers only BTC/USDT, so there is no altcoin to trade.
