---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has fallen far over the past 24 hours against its usual move while it has risen over the past 30 days, it rises over the next 3 days by more than its normal drift. The rise is larger the deeper the 24-hour fall and the larger the 30-day rise, whatever the volume behind the fall.
Consequence: A trader buys sharp one-day dips inside 30-day uptrends without waiting for a streak of falling bars or for fading volume.
Why:
- F4: The direction of a large 24-hour move does not decide what follows; both extremes rise more than usual over 3 days.
- F5: Fading volume does the opposite of what the brief expects. Among streaks of at least 3 falling bars, those with fading volume have strength -0.011 (t -0.16, 232 cases), against +0.080 (t 1.32, 263 cases) with rising volume. Rising streaks show the same order: fading +0.016, rising volume +0.114 (t 1.55). None of these differences is significant.
- F6: The book's forecast is graded where it is active. Its terciles of positive forecast give strengths of -0.066, +0.167 and +0.233 (t -0.83, 1.70, 1.91; about 99 cases each). The flat bars give -0.006 (t -0.45, 5,428 cases).
