---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend
line: 7.d not profitable
backtest: 017-03_postsettle-recovery-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run up, the return over the 8 hours after the 08:00 UTC funding settlement (measured from the close of the hour before it) is negative, and the stronger the 3-day rise, the larger that fall.
Consequence: A trader would refuse to be long a rising coin through the 08:00 settlement, and could test a short there as a book of its own.
Why:
- F4: The 08:00 UTC settlement runs the other way: up-trend entries at the 07:00 bar lose 3.7 bp over 2 bars (t −2.46) and 11.4 bp over 8 bars (t −3.86, 8,678 cases). At the book level the 07:00 bar costs 2.6e-4 in fees a coin-day for −4.3e-5 of gross gain.
