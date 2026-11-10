---
idea: 004-07_btc-leads-alts-not-reverse
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Untestable: The idea compares bitcoin's returns with later altcoin returns (and the reverse), so it needs a second coin's prices, but the config sees one coin at a time and the run covers only BTC/USDT. No component can read another coin's bars, so neither the lead nor the lag can be computed.
