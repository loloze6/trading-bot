---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has made a large move over the past 24 hours, measured against its usual move, it rises over the next 3 days by more than its normal drift. The larger the absolute 24-hour move, whether up or down, the larger the rise.
Consequence: A trader takes the long side after outsized one-day moves of either sign, and refuses to fade large one-day rises.
Why:
- F3: Large 24-hour moves, in either direction, are followed by a larger-than-usual rise over the next 3 days, on the 18-bar grid. By size of the absolute 6-bar move in usual moves, the top three deciles show strengths of +0.088 (t 2.02), +0.098 (t 2.33) and +0.140 (t 2.75), about 515 cases each. Six of the seven lower deciles are between -0.02 and -0.06, and one is -0.11 (t -2.37).
- F4: The direction of a large 24-hour move does not decide what follows; both extremes rise more than usual over 3 days.
- F5: Fading volume does the opposite of what the brief expects. Among streaks of at least 3 falling bars, those with fading volume have strength -0.011 (t -0.16, 232 cases), against +0.080 (t 1.32, 263 cases) with rising volume. Rising streaks show the same order: fading +0.016, rising volume +0.114 (t 1.55). None of these differences is significant.
