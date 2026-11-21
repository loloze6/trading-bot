---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 10 days, only while that 28-day return is a rise; the larger the rise, the larger the 10-day gain that follows.
Consequence: A trader would lean long in proportion to a coin's 28-day rise and refuse to short a coin only because it fell over 28 days, so the losing short side that drives the deepest falls is removed.
Why:
- F1: The Calmar fails because of one long fall, not because the gain is too small. The book's yearly return is 18.8 %, its deepest fall is 60.9 %, and Calmar comes out at 0.31. That fall ran from w2 to w8: 741 days to the trough and 1,102 more to recover. Over those days the book's daily returns summed to -0.85 while holding the coins summed to +0.20.
- F2: Only the long side earns. Overall, long days earn +15.5 bps a day (8,657 days) and short days -1.1 bps (8,671 days). Outside w2-w8, longs earn +21.7 bps a day (t 5.07, 6,322 days) and shorts +0.4 bps (t 0.13, 5,946 days). Inside w2-w8, both sides lose: longs -1.3 bps (t -0.23), shorts -4.5 bps (t -0.87).
- F3: Shorts did most of the damage in the falls. Their summed daily gains were -1.23 in w2-w8 and -1.08 in w19-w21, which hold the two deepest falls (-61 % and -37 %). Longs summed -0.31 in w2-w8 but +8.28 in w9-w18 and +3.96 in w19-w21.
- F5: Longs are graded by the 28-day rise and by nearness to the 60-day high.
