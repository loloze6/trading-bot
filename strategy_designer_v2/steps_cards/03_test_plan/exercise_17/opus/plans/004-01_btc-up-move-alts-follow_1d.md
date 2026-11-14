---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin up move -> replaced: a config on one coin cannot see bitcoin's bars while trading an altcoin.
- Comparison: altcoin's lagged response against bitcoin's earlier move -> replaced: needs two coins' returns side by side, which no config can hold.
- Outcome: smaller altcoins drift up over the following bars -> replaced: the test runs only on BTC/USDT, so no altcoin outcome exists.
- Verdict transfer: no: a test on BTC alone, or on an altcoin alone, cannot show altcoins lagging bitcoin.
Reason: The idea's signal is bitcoin's move and its outcome is an altcoin's later return, so it needs another coin's bars. The guide says a component sees only its own symbol's bars and feed columns, and the test runs only on BTC/USDT.
