---
idea: 004-01_btc-up-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Untestable: The idea needs bitcoin's past return as the signal and an altcoin's later return as the outcome, but the config sees only one coin's bars at a time and the test runs only on BTC/USDT. No config can read bitcoin's move while trading an altcoin, and a BTC-only run contains no altcoin whose catching-up could be measured.
