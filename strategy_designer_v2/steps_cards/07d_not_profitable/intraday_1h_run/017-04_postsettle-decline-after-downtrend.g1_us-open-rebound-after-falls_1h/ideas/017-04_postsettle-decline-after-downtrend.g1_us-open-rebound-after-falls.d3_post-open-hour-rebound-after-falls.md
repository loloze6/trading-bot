---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a 3-day fall, the return over the hour from 13:00 UTC is positive, and the deeper the 3-day fall, the larger that rise.
Consequence: A trader would buy the post-open hour rather than the open itself, keeping most of the rebound while carrying the position for one hour instead of two.
Why:
- F2: The 2-hour rise is too small to pay that round trip in most cases: the forecast quintiles 1 to 4 (forecast 1.8 to 13.9) give mean 2-hour returns of −0.04%, 0.02%, 0.05% and 0.07%, and only the top quintile (forecast 19.3) gives 0.23%, across 8432 cases with a raw t of 3.57.
- F5: Nearly all the gain is in the 13:00 bar, not the 12:00 bar: summed gain before fees is 3.01 on positions held through the 13:00 bar against 0.77 through the 12:00 bar; in the top forecast quintile the 13:00 bar gives 0.19% of the 0.23%.
