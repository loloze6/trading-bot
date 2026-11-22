---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise in usual daily moves, the larger its fall over the next day.
Consequence: The giveback is a next-day event, so the short should cover the day after the bounce rather than ride the old fall.
Why:
- F2: The fade is a one-day effect. After a one-day rise of at least 2 usual moves with a negative 90-day return (66 cases), the coin's unusual move is −1.48 % over 1 day (t −2.36), −0.46 % over 2 days (t −0.62), −1.32 % over 5 days (t −1.10) and +2.28 % over 10 days (t 1.28). The book's short bars match this: +0.56 % gain on the situation's own next bar (t 1.99, 62 bars), then −0.33 % the bar after (t −1.70).
- F3: The tested gradient runs the wrong way. Over 5 days, the deepest quartile of 90-day falls gives −0.77 % unusual (n 17, t −0.29), while the shallowest gives −5.40 % (n 17, t −2.79). The deepest quartile even rises +8.19 % over 10 days (t 1.94). This matches step 5's slope t of 0.86 and its mean unusual move of −0.25 % per case, which is 1.3 times the 0.19 % cost of a trade, in the losing direction.
- F5: The next-day fade grows slightly with the size of the bounce. By tercile of the one-day rise in usual moves, the 1-day unusual move is −1.11 % (small), −1.61 % (mid) and −1.73 % (big), 22 cases each, with t from −0.87 to −1.78.
