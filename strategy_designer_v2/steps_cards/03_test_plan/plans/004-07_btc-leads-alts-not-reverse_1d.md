---
idea: 004-07_btc-leads-alts-not-reverse
brief: 004_bitcoin-leads-altcoins-lagged-response
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: an earlier bitcoin return -> replaced: a config sees only one coin, so this cannot be paired with any other coin's later return.
- Comparison: BTC leading alts versus alts leading BTC -> replaced: this needs altcoin bars, which the config never sees.
- Outcome: later altcoin returns in the same direction -> replaced: the run trades only BTC/USDT, so altcoin returns are not in the record.
- Verdict transfer: no: no single-coin BTC forecast can measure a lead-lag between two coins.
Reason: The idea relates bitcoin's past returns to later altcoin returns, and the reverse, so it needs two coins' bars at once. The config sees only one symbol's bars and feeds, and the run here covers only BTC/USDT.
