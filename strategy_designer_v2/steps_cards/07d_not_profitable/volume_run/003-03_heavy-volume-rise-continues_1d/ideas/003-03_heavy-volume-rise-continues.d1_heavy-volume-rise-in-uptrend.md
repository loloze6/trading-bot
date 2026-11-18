---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-03_heavy-volume-rise-continues
line: 7.d not profitable
backtest: 003-03_heavy-volume-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days, but only while its 30-day return is positive. The larger the rise, the heavier its volume against that average and the stronger the prior 30-day rise, the larger the further gain.
Consequence: A trader would follow heavy-volume rises only inside a coin's month-long uptrend and refuse them after a 30-day decline, where they do not continue.
Why:
- F4: The 5-day continuation exists only when the coin has risen over the past 30 days. The 5-day excess return is -0.0045 (t -0.59, n 129) in the lowest 30-day-return tercile (median -13.6 %). It is +0.0237 (t 2.38) in the middle tercile (median +7.0 %) and +0.0287 (t 2.26) in the top tercile (median +31.7 %). Split by sign, it is +0.0245 (t 2.99, n 252) when the 30-day return is positive against +0.0093 (t 1.19, n 259) when it is negative.
- F5: The continuation grows with the size of the rise and less clearly with its volume. By terciles of the scaled one-day rise it is 0.0118 (t 1.07), 0.0181 (t 1.88) and 0.0320 (t 3.08). By terciles of the volume ratio it is 0.0185, 0.0165 and 0.0269.
- F6: The book's result depends on the window, and it loses where the coins fell. Pooled window Sharpes run from -1.85 (w2) to +1.77 (w11). In w2 and w14, where holding returned -0.0036 and -0.0043 a day, the book returned -0.0015 and -0.0008 a day.
- F3: The book therefore earns almost nothing. Its mean daily return is 4.9e-05 against 0.0012 for holding. The part it gets from the market's own rise is only 0.00007 to 0.00017 per coin. Fees take 1 to 5 % of the book per window, and the 2988 trades last 3.3 days on average with a 49 % win rate.
