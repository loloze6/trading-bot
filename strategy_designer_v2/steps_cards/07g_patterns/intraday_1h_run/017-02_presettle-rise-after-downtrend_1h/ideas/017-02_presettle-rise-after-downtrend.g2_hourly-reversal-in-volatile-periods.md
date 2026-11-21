---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next hour, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly when the coin's 24-hour volatility is high.
Consequence: A trader would fade sharp single-hour moves, mostly in volatile periods, and would stop fading if the reversal is not confirmed.
Why:
- F3: A coin's next hour reverses its last hour, and the reversal grows with the size of the move. The next-hour excess slope on the last hour's volatility-scaled move is negative in all six coins, from −0.69 to −4.21 bp per z, t −1.7 to −7.0, about 52,000 bars each. Buckets run from +14.2 bp (t 3.38) after moves of −3 z or worse to −3.3 bp (t −4.29) after moves of +1 to +2 z.
- F4: The one-hour reversal sits in high-volatility periods. Its slope is −5.19 bp per z (t −10.1) in the top quintile of 24-hour volatility, against +0.44 bp (t 1.19) in the lowest quintile and −0.6 to −0.9 bp in the middle quintiles.
