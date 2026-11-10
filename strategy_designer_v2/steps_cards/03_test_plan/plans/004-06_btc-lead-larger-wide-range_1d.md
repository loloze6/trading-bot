---
idea: 004-06_btc-lead-larger-wide-range
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: sharp bitcoin move, seen by an altcoin -> replaced: a config sees only one coin's bars, and the test coin is BTC itself, so no altcoin is measured.
- Comparison: wide-range altcoins versus narrow-range altcoins -> replaced: this needs several altcoins at once, which a single-coin config cannot see.
- Outcome: altcoin follows through in the direction of BTC's move -> replaced: it needs altcoin returns after BTC's move, which are not in BTC's bars.
- Verdict transfer: no: a test on BTC's own bars says nothing about how altcoins respond to BTC, or about wide-range versus narrow-range altcoins.
Reason: The idea links one coin's (BTC's) earlier move to other coins' (altcoins') later returns, and compares altcoins with each other. A config sees only one symbol's own bars and feeds, so it cannot read another coin's prices or rank coins against each other.
