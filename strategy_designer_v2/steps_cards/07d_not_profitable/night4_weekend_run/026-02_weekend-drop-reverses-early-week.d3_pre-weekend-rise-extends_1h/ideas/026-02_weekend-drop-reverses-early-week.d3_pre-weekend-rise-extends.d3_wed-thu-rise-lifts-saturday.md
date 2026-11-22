---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin rises over the two days before Friday 00:00 UTC, it keeps rising over Saturday, from Saturday 00:00 to Sunday 00:00. The larger that two-day rise, the larger Saturday's rise.
Consequence: A trader can take the pre-weekend long at Saturday 00:00 rather than Friday, avoiding Friday's partial pullback and freeing capital on Friday.
Why:
- F6: The extension shows on Saturday, not Friday. The 48-hour rise into Friday predicts Friday's own 24 hours negatively (slope t = −3.49) and Saturday's 24 hours positively (t = 7.91). Saturday's 24 hours are also predicted by the 48 hours before Friday (t = 7.10), not by Friday's own move (t = −0.01).
- F1: The book fails on size, not on edge: its mean daily return is 0.00032 against a 0.0005 floor and against holding's 0.00119, because it is in the market only 21–27 % of bars per coin, at a mean position of 0.34–0.69 when in. Its gain all comes on Friday (+0.00107 a day) and Saturday (+0.00160), while the other weekdays sit between −0.00027 and +0.00002. This is across 1969 trades netting +0.66 % each after fees, so cost is not the problem.
