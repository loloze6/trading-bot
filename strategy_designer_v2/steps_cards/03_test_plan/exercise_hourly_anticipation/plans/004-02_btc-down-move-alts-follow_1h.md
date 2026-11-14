---
idea: 004-02_btc-down-move-alts-follow
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp bitcoin down move -> kept
- Comparison: the altcoin's later move against the bitcoin move it lags -> replaced: the config only sees the traded coin's own bars, never bitcoin's
- Outcome: smaller altcoins keep falling over the following bars -> replaced: the test runs only on BTC/USDT, so altcoin returns cannot be traded or measured
- Verdict transfer: no: a forecast on BTC that trades BTC tests bitcoin's own continuation, not whether altcoins follow bitcoin.
Reason: The idea needs bitcoin's bars as the signal and an altcoin's price as the outcome, which is a cross-coin relation. A config sees only one symbol's own bars and feeds, and the run trades only BTC/USDT, so neither the lead-lag link nor the altcoin drift can be expressed.
