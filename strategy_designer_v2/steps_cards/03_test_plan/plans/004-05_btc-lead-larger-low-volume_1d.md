---
idea: 004-05_btc-lead-larger-low-volume
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin move seen from an altcoin -> replaced: an altcoin config cannot see bitcoin's bars, and the test runs only on BTC/USDT.
- Comparison: low-volume altcoins against high-volume altcoins -> replaced: this needs several coins' results ranked by volume, but the config runs on one coin at a time.
- Outcome: the altcoin follows through in bitcoin's direction over the next bars -> replaced: the test coin is bitcoin itself, so there is no altcoin response to measure.
- Verdict transfer: no: any single-coin BTC test measures bitcoin's own autocorrelation, not altcoins lagging bitcoin.
Reason: The idea needs bitcoin's returns as the signal for a different coin, and a comparison across altcoins grouped by volume. A config sees only its own coin's bars and cannot read another coin's prices, so the guide puts this outside what a config can express. The test universe is also only BTC/USDT.
