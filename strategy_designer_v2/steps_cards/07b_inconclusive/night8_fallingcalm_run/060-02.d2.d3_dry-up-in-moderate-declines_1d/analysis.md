---
line: 7.b inconclusive
backtest: 060-02.d2.d3_dry-up-in-moderate-declines_1d
idea tested: 060-02.d2.d3_dry-up-in-moderate-declines
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2069 USD
---
## Findings
- **F1:** On the backtest's own 5-bar grid, the short signal's sign-flipped excess return in folds B and C is +2.12 % per case, with t 1.84 over 98 days (266 cases). This is on the predicted side and matches step 5's +1.31 % (t 1.76, 202 days), but it falls short of t 2 because the cases fall on few independent days.
- **F2:** The effect points the same way on all six coins: BTC +0.52 %, ETH +2.88 %, LTC +1.89 %, XMR +2.73 %, XRP +2.67 % and ZEC +1.78 %. Each coin alone has only 30 to 56 days, and only XRP reaches t 2.11. The effect is broad but thin per coin, so the test is short of cases, not short of an effect.
- **F3:** The result is mixed across periods, which drowns part of it. 2018 gives +4.21 % (t 2.12, 39 days) and 2019 gives +2.28 % (t 2.03, 35 days). 2020 goes the other way at -4.74 % (t -3.21, 13 days), and w16 and w17 give -8.12 % and -3.42 % on just 3 and 7 days.
- **F4:** The dry-up grading itself is clean inside the falling market. Ranking all falling-regime grid bars by 30-day volume shrinkage, the excess fall rises from -1.82 % (most growing volume, t -0.46) through +0.86 % and +1.88 % to +5.48 % (strongest dry-up, t 2.47, 28 days). Shrinking volume gives +3.71 % (t 2.24) and growing volume gives -1.09 % (t -0.43), as the brief predicts.
- **F5:** The effect grows with the horizon. The signal's excess fall is +0.65 % over 3 days (t 0.80), +2.12 % over 5 days (t 1.84) and +3.45 % over 10 days (t 2.19, 96 days). The plan's 5-day horizon is not where the effect is weakest, but it is not yet where it is clearest either.
- **F6:** Step 5's size is +1.72 % unusual move per case (t 3.27 over 351 days, strength 0.154) and +1.13 % total. That is 8.9 and 5.9 times the 0.19 % cost of a trade, so the move is large enough to pay. The open question is only whether the main measure can clear t 2 with more independent days.

## Ideas
- `060-02.d2.d3.b1_dry-up-moderate-declines-more-coins` (from F1, F2, F4, F6): In a falling market, while the coin's 10-day return is negative but its fall is still moderate, the more its trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
