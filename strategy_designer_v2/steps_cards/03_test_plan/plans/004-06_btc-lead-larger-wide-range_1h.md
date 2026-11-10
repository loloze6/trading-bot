---
idea: 004-06_btc-lead-larger-wide-range
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Untestable: The idea needs bitcoin's returns as the signal and altcoins (sorted by their bar ranges) as the coins traded, but the config sees one coin at a time with no other coin's prices, and the test runs only on BTC/USDT, so there are no altcoins to compare. Dropping the cross-coin lead and the wide-versus-narrow range comparison would remove what the idea is about.
