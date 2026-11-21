---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, and the more such past turning-up lows lie within a few percent above the close, the larger the fall, only while the close is below its 50-day average price.
Consequence: A close under a tight cluster of past lows in a coin already below its 50-day average is a reason to be short for 5 days, and a single or distant past low above the close is no reason to be short at all.
Why:
- F1: The book loses because it is short most of the time in coins that rise. It is short on 69 % to 80 % of bars, with a mean position of -0.41 to -0.58. Its gain from the market's own rise is negative on every coin (-0.031 % to -0.069 % per bar). Its timing gain is positive on 5 of 6 coins (+0.018 % to +0.060 % per bar) but smaller. So the idea's total move per case is -0.47 % over 5 days, against a cost of 0.19 %.
- F2: The book stays short even where no cluster of past lows sits near the close. On bars with no swing low within 3 % above the close, its mean position is -0.36 and it is short 68 % of the time (13,384 bars), losing 0.039 % per bar. The standardised, negated forecast turns any low above the close, however far, into a short.
- F4: The count of swing lows within 3 % above the close grades the next 5 days' move (unusual move, non-overlapping cases):
- F5: The graded fall is broad. With 3 or more such lows, the 5-day unusual move is negative on all 6 coins (-0.8 % to -6.1 %) and in 7 of 8 years (-1.7 % to -7.2 %; 2020 is the exception at +4.5 %).
- F6: The fall is concentrated when the close is below its 50-day average.
