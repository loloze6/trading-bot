---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> replaced: the config sees only the traded coin's own bars, so bitcoin's move cannot be read when trading an altcoin.
- Comparison: altcoin's later drift versus bitcoin's earlier move -> replaced: needs two coins' returns side by side, which the config cannot hold.
- Outcome: smaller altcoins drift up over the following bars -> replaced: the test coin is BTC/USDT only, so no altcoin price is traded.
- Verdict transfer: no: a test on BTC's own bars cannot show altcoins catching up to bitcoin.
Reason: The idea links bitcoin's move to later altcoin returns, which needs another coin's prices. The config sees only one symbol's bars and has no cross-symbol data, and the run trades only BTC/USDT, so there is no altcoin outcome to measure.
