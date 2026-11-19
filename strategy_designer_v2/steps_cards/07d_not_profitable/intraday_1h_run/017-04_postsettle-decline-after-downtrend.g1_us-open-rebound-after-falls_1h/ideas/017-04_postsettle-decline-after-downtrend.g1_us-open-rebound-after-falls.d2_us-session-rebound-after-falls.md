---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a 3-day fall, the return over the 12 hours from 12:00 UTC is positive, and the deeper the 3-day fall, the larger that rise.
Consequence: A trader would hold the rebound after a 3-day fall through the US session, which spreads one round-trip fee over a rise several times larger than the 2-hour one.
Why:
- F1: Fees, not the forecast, sink the book: per coin the summed gain before fees on the held positions is 0.46 to 0.88, while the summed fees are 1.31 to 1.70, and the fees sit almost entirely on the entry at 11:00 (7256 fee bars, mean 0.058%) and the exit at 13:00 (7368 fee bars, mean 0.058%); that is about 0.1% per daily round trip.
- F3: The rise belongs to the deepest falls only: the deepest 3-day-fall quintile (mean fall −14.2%) gains 0.24% over the 2 hours, against 0.07%, 0.05%, 0.05% and −0.05% in the four shallower quintiles.
- F6: After the deepest 3-day falls the rise keeps building past 2 hours: the deepest quintile gains 0.52% over 12 hours and 0.25% over 24 hours from the 11:00 close, and over all cases the 12-hour return has a raw t of 2.48.
