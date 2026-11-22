---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin rises over the two days before Friday 00:00 UTC, it keeps rising over Friday and Saturday, only while its 30-day return is positive. The larger that two-day rise and the larger the 30-day return, the larger the further rise.
Consequence: A trader keeps the pre-weekend long when the month is up and refuses it when the month is down, adding size as both rises grow.
Why:
- F2: The Friday rise works only inside a 30-day uptrend. Among Friday 00:00 cases after a 48-hour rise, those with a positive 720-hour return gain +1.64 % over 48 hours (500 cases), and the slope on the two-day rise has t = 4.72. Those with a non-positive 30-day return gain only +0.21 % (345 cases), with a slope t of −0.85.
- F5: Inside the uptrend, the two-day rise still grades the move. Among Friday cases with a positive 720-hour return (918 cases), the slope of the next 48 hours on the 48-hour rise has t = 3.95, and of Saturday's 24 hours t = 5.06.
- F1: The book fails on size, not on edge: its mean daily return is 0.00032 against a 0.0005 floor and against holding's 0.00119, because it is in the market only 21–27 % of bars per coin, at a mean position of 0.34–0.69 when in. Its gain all comes on Friday (+0.00107 a day) and Saturday (+0.00160), while the other weekdays sit between −0.00027 and +0.00002. This is across 1969 trades netting +0.66 % each after fees, so cost is not the problem.
