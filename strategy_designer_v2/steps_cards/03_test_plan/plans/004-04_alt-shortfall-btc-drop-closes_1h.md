---
idea: 004-04_alt-shortfall-btc-drop-closes
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Untestable: The idea compares an altcoin's move with the move bitcoin's same-bar drop implies, so it needs bitcoin's bars and the altcoin's bars together, but the config sees one coin at a time and the coin here is BTC/USDT itself. No catalogue component reads another coin's prices, so neither the gap nor bitcoin's sharp move can be computed for an altcoin.
