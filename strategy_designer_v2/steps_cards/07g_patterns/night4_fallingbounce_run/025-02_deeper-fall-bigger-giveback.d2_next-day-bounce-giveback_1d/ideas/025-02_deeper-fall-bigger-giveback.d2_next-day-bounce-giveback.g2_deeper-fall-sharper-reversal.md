---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, the deeper that 90-day fall, the more the next day reverses the size of the day's move in usual daily moves.
Consequence: One-day fades of a falling coin's moves deserve more weight the deeper the coin's 90-day fall, and little weight when the fall is shallow.
Why:
- F1: In the falling regime (90-day return below 0), the next-day move runs against the day's scaled move across the whole range: the slope of next-day strength on the scaled one-day return is -0.066 (t -6.08, 7335 days), against -0.019 (t -1.65, 7885 days) outside the regime, and it is negative on all six coins (t from -1.63 to -4.28).
- F4: The reversal grows with the depth of the 90-day fall: the slope is -0.134 (t -3.55, 734 days) in the deepest third of 90-day returns, -0.057 (t -1.90) in the middle third and -0.037 (t -1.24) in the shallowest third.
- F5: The effect is one day long and uneven over the years: over two days on non-overlapping cases the falling-regime slope drops to -0.014 (t -0.95, 3614 cases), and the one-day slope is strong in 2018 (t -3.57), 2020 (t -8.63) and 2021 (t -3.43) but near zero from 2022 to 2025 (t between -0.26 and -1.42).
