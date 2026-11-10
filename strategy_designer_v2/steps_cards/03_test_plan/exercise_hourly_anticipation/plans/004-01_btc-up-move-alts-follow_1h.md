---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> replaced: an altcoin config cannot see bitcoin's bars, and on BTC/USDT there is no altcoin to trade
- Comparison: altcoin response against bitcoin's earlier move -> replaced: needs two coins' prices in one config, which no component reads
- Outcome: smaller altcoins rise over the following bars -> replaced: the only tradable coin here is bitcoin itself, not an altcoin
- Verdict transfer: no: a test on bitcoin's own bars says nothing about whether altcoins lag bitcoin.
Reason: The idea's situation is one coin (bitcoin) and its outcome is the price of other coins (altcoins). The config sees only its own symbol's bars and feeds, and the guide says other coins' prices cannot be expressed. The test also runs only on BTC/USDT, so there is no altcoin whose later drift could be measured.
