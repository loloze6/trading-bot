---
line: 7.b inconclusive
backtest: 058-02.g1_choppy-agitated-deep-fall-continues_1d
idea tested: 058-02.g1_choppy-agitated-deep-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3179 USD
---
## Findings
- **F1:** Step 5's slope lies on the side the idea predicts but is far short of the bar: 0.0011 with t 0.77 over 160 grid bars with a falling forecast. In folds B and C it is again positive, 0.0033 with t 0.94 on 56 cases on 37 days, and it is positive at every horizon tried (1, 3, 5, 10 and 20 days, t 0.33 to 1.28).
- **F2:** The fall does carry on in this profile as a level. In B and C the mean 5-day excess return on falling-forecast grid bars is -4.9 %, with 66 % of cases negative, t -2.95 plain and -1.74 with each day's cases taken together. It is negative on all six coins, from -2.1 % on ZEC to -11.5 % on BTC. Over all folds step 5's mean is -2.0 %, and its unusual move is +0.62 % in the short direction (t 0.98, 191 days).
- **F3:** The grading on depth is weak and uneven, which is what keeps the slope's t low. By forecast tercile the 5-day excess is -6.5 % for the deepest, -3.4 % for the middle and -4.7 % for the shallowest, so it is not monotonic. ETH's slope is negative (t -0.64) while the other five coins are positive (t 0.17 to 1.18).
- **F4:** The slope is mixed across periods. Without 2021 it is 0.0063 with t 1.46 on 32 cases, against -0.0048 with t -0.96 on 24 cases in 2021. 2020 carries most of it (0.016, t 1.85, 16 cases), and window means range from +6.0 % in w11 to -33 % in w13 and w16.
- **F5:** The volume split the brief names cannot be read on these cases, because two splits disagree. Against the 30-day volume, quiet falls give -6.5 % and heavy falls -13.3 % (17 and 16 cases). Against the 90-day volume, quiet falls give -17.5 % and heavy falls -7.5 % (9 cases each).
- **F6:** Too few cases is the binding limit: the choppy agitated profile is rare (about 3 % of coin-days) and gives only 56 falling cases in B and C on six coins. More data exists: 13 more coins have daily bars in folds A and D, and some of them in parts of B and C.

## Ideas
- `058-02.g1.b1_choppy-agitated-fall-all-coins` (from F1, F2, F6): In a choppy, agitated market, the deeper a coin's 30-day fall measured against its usual 30-day move, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
