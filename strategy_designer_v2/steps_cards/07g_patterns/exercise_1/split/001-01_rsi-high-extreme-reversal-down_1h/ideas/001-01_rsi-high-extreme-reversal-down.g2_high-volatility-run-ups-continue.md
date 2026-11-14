---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: When a coin has risen over the past 12 hours while its 24-hour volatility is high relative to its own recent median, it keeps rising over the next 12 hours more than its usual drift.
Consequence: A trader would buy, or refuse to short, a coin that has run up during a relative-volatility spike.
Why:
- F5: The past 12 hours' move points weakly toward continuation. The top past-12h decile is followed by +19.5 / +19.0 bp of 12-bar excess return (BTC / ETH). The bottom decile is followed by -3.4 / -13.0 bp. The top-minus-bottom spread is positive in 10 of 12 coin-windows (up to +91 bp) but strongly negative in w6 for both coins (-57, -75 bp), and no single decile reaches non-overlapping |t| > 2.1.
- F6: Volatility conditions this continuation. When 24h volatility is in its top tercile relative to its own recent median, bars after a 12h rise see +24.9 bp of 12-bar excess return, versus +5.4 bp in the low-volatility tercile. In the low-volatility tercile, falls continue (-16.9 bp). In absolute volatility terms, the top tercile shows +11.6 / +8.8 bp excess for BTC / ETH, against -8.5 / -9.1 bp in the middle tercile.
- F8: The book's largest 1% bar losses and gains come from the same setup: allocation about -1.9 (beyond full size), after a +296 / +355 bp 12h run-up, in relative volatility of 1.32 / 1.34. The coin then moves +188 bp or -160 bp in the next bar, so the tails are symmetric coin flips taken with leverage.
