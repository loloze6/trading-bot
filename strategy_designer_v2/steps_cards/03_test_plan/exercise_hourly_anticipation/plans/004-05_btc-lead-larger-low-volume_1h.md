---
idea: 004-05_btc-lead-larger-low-volume
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin move -> replaced: the config sees only the traded coin's own bars, so an altcoin config cannot read bitcoin's move.
- Comparison: low-volume altcoins against high-volume altcoins -> replaced: it needs several coins compared with each other, and the config runs on one coin.
- Outcome: the altcoin follows through in bitcoin's direction over the next bars -> replaced: the only coin given is BTC/USDT, so no altcoin outcome can be measured.
- Verdict transfer: no: no config built from one coin's own bars can show that bitcoin leads altcoins, or that thinly traded altcoins lag more.
Reason: The idea needs bitcoin's returns as the signal and altcoin returns as the outcome, compared across altcoins by volume. A config sees only one coin's own bars and feeds, and the test runs on BTC/USDT alone.
