---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return at Friday 00:00 UTC, the more it rises over Friday and Saturday.
Consequence: A trader can size a Friday-to-Sunday long by the coin's 30-day return, which gives a weekly bet on most weeks instead of only after two-day rises.
Why:
- F3: The 30-day return predicts the Friday–Saturday move better than the two-day rise does. At Friday 00:00, the slope of the 48-hour return on the 720-hour return has t = 7.76 (1818 cases), against t = 2.57 for the 48-hour rise. By 720-hour-return quintile, the 48-hour return climbs steadily from −0.42 % to +0.09 %, +0.72 %, +0.80 % and +2.08 %.
- F4: This 30-day effect is tied to the weekend days. The slope t of the next 48 hours on the 720-hour return is 7.76 from Friday 00:00 and 5.08 from Saturday 00:00, but between −1.72 and +0.90 from Sunday through Wednesday 00:00.
- F1: The book fails on size, not on edge: its mean daily return is 0.00032 against a 0.0005 floor and against holding's 0.00119, because it is in the market only 21–27 % of bars per coin, at a mean position of 0.34–0.69 when in. Its gain all comes on Friday (+0.00107 a day) and Saturday (+0.00160), while the other weekdays sit between −0.00027 and +0.00002. This is across 1969 trades netting +0.66 % each after fees, so cost is not the problem.
