---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour fall that is large against the coin's usual 24-hour move, while its bar range over those 24 hours is wide against its 30-day average, the coin earns more than its usual drift over the next 3 days. The larger the fall times the range expansion, the larger that excess.
Consequence: A trader would buy sharp, wide-range sell-offs for a few days only, sizing up with the depth and width of the panic, rather than holding for two weeks.
Why:
- F1: The premium after a wide-range fall is real but short: among non-overlapping 3-day cases, a 24-hour fall of more than one usual 24-hour move with the 24-hour bar range above 1.3 times its 30-day average is followed by an excess of +2.37 % over the coin's 3-day drift (t 4.53, n 299), against +0.66 % (t 1.84, n 480) for the same falls without a wide range. At 14 days the same cases show +2.53 % with t 0.96 (n 48), so the 14-day horizon the idea was tested on dilutes the move into noise.
- F2: The excess grows with the fall times the range expansion, measured as the score (−z6, clipped at 0) × range ratio. At 3 days the score buckets 0 / 0–0.5 / 0.5–1 / 1–1.5 / 1.5–2.5 / >2.5 give −0.13 %, −0.38 %, −0.52 %, +0.14 %, +1.70 % (t 2.88, n 250) and +2.10 % (t 3.97, n 256). At 1 day the top bucket gives +1.02 % (t 5.02, n 862) and at 5 days +1.91 % (t 2.37, n 173).
- F3: The 3-day rebound after wide-range falls is positive in all six coins: BTC +1.00 %, ETH +1.64 %, LTC +4.07 % (t 3.18), XMR +1.88 %, XRP +1.67 %, ZEC +3.96 % (t 2.19), about 50 cases each. At 1 day it is positive in all six, with t from 1.82 to 3.56.
- F8: The 3-day move in the strongest situations is far larger than the cost of a trade. The top score bucket's excess of +2.10 % is about 11 times the 0.19 % cost, and the 1-day +1.02 % about 5 times. The size problem of the tested idea (unusual move 0.3 times the cost) comes from its 14-day horizon and long holding, not from the situation itself.
