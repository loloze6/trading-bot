---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: A coin rises over the 4 hours starting at 20:00 UTC, by an amount that grows with its typical 4-hour move over the past 30 days.
Consequence: A trader would time long entries or the closing of shorts before 20:00 UTC, and expect the evening lift to be larger in more volatile coins.
Why:
- F6: The 4h bar starting at 20:00 UTC rises more than any other bar of the day. Its pooled mean is +9.1 bp (t 5.78, 16066 bars), against −4.1 bp for the 00:00 bar (t −2.55). In return scaled by the usual move, the 20:00 bar is positive in all 6 coins (t 1.26 to 3.26) and in 7 of 8 years (t −0.69 to 4.27).
