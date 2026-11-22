---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: An hour in which the coin moves far more than its typical 30-day hourly move, being the first such hour in the past day, is followed over the next four to eight hours by a further move in the same direction as that hour, larger the higher that hour's volume against its 30-day average hourly volume.
Consequence: The first heavy-volume shock after a quiet day is a reason to trade with it, up or down, for four to eight hours, and a repeat shock inside the same burst is a reason not to.
Why:
- F3: A move of more than 2.5 usual hourly moves that is the first in 24 hours (1,784 events) is followed by more movement its own way the higher that hour's volume against its 30-day mean. Over 4 hours: +6.7 bp at under 2×, +14.5 bp at 2–4×, +32.9 bp at 4–8×, +44.0 bp above 8×. Over 8 hours: +8.1, +13.3, +34.1 and +62.9 bp.
- F4: The F3 gradient appears on both sides. For the 4–8× volume bucket over 4 hours, down hours give +31.5 bp in their direction (t 2.3, 258) and up hours +34.4 bp (t 2.7, 248). Over 12 hours it is positive in both coins (BTC +18.2 bp t 1.9, ETH +34.0 bp t 2.6) and in 6 of 8 years. The rank correlation with |move| × volume ratio is only 0.07.
- F5: Counting every large move on the fixed 4-bar grid instead, repeats inside a burst included, reverses the result. Large moves on volume above 4× are followed by −29.0 bp in their direction (t −1.8, 455 cases). The tested forecast, which fires on every up hour, measures −0.01 % per case (t −0.84, 13,276 cases). So the continuation belongs to the first surge, and later surges in a burst fade.
- F6: The book lost −9.4 bp a day and lost in 15 of 24 windows. It was in the market 65 % of the time with 24,971 trades of median length 4 hours. Its per-case move (+0.01 %) is 0.1 times the 0.11 % cost. By contrast, the F3 first-surge moves at 4× volume or more (+33 to +44 bp over 4 hours) are 3 to 4 times that cost.
