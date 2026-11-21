---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the 2 hours after the 16:00 UTC funding settlement, a coin moves in the direction of its own 3-day return, and the larger that 3-day return, the larger the move with it.
Consequence: Trade with the 3-day trend just after the 16:00 UTC settlement instead of expecting a recovery against it.
Why:
- F4: In the two hours after the 16:00 UTC settlement, the coin keeps moving with its 3-day trend instead of recovering against it. The trend-signed excess return for the bars stamped 15:00 and 16:00 is +5.0 bp (t 5.4) and +3.8 bp (t 4.7). It is positive in all six coins (ETH t 4.3, ZEC t 4.9) and in 7 of 8 years.
- F7: Fees, not direction, sink the book. The mean gross gain is 0.19 bp per bar against 0.72 bp of fees per bar, which comes to about 5.6% gross against 20.9% in fees per coin and window. The gain sits in the bars stamped 15:00 (+4.6 bp per active bar) and 16:00 (+2.2 bp), while the 07:00 bar loses -0.9 bp.
