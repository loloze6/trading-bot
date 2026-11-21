---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a 3-day fall, the return over the 2 hours from 12:00 UTC is positive, and the deeper the 3-day fall, the larger that rise, only while the coin's 1-day return is also a fall, the rise growing with the depth of that 1-day fall.
Consequence: A trader would take the US-open rebound only on coins that are falling over both the last 3 days and the last day, so that the expected rise clears a round-trip fee of about 0.1%.
Why:
- F1: Fees, not the forecast, sink the book: per coin the summed gain before fees on the held positions is 0.46 to 0.88, while the summed fees are 1.31 to 1.70, and the fees sit almost entirely on the entry at 11:00 (7256 fee bars, mean 0.058%) and the exit at 13:00 (7368 fee bars, mean 0.058%); that is about 0.1% per daily round trip.
- F2: The 2-hour rise is too small to pay that round trip in most cases: the forecast quintiles 1 to 4 (forecast 1.8 to 13.9) give mean 2-hour returns of −0.04%, 0.02%, 0.05% and 0.07%, and only the top quintile (forecast 19.3) gives 0.23%, across 8432 cases with a raw t of 3.57.
- F3: The rise belongs to the deepest falls only: the deepest 3-day-fall quintile (mean fall −14.2%) gains 0.24% over the 2 hours, against 0.07%, 0.05%, 0.05% and −0.05% in the four shallower quintiles.
- F4: The 1-day fall sorts the cases at least as well: the quintile with the deepest 24-hour fall (−8.3%) gains 0.26% over the 2 hours, and the other four quintiles gain between −0.06% and 0.09%.
