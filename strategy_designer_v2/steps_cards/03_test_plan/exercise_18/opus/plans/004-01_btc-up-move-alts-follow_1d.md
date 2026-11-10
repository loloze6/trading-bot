---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> kept
- Comparison: none -> kept
- Outcome: smaller altcoins drift up over the following bars -> replaced: the config sees only its own coin, so the only outcome it can measure is BTC's own next return
- Verdict transfer: no: the idea links bitcoin's past move to other coins' later returns, and a single-coin config on BTC/USDT cannot see an altcoin.
Reason: The situation is measured on bitcoin and the outcome on altcoins. The config sees only one symbol's bars, and the run covers only BTC/USDT, so no config can trade an altcoin on bitcoin's move. The guide lists another coin's prices as data the bars do not carry.
