---
line: 7.b inconclusive
backtest: 061-01.g1.d1.d1_calm-big-rise-convex-follow-through_1d
idea tested: 061-01.g1.d1.d1_calm-big-rise-convex-follow-through
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3729 USD
---
## Findings
- **F1:** Step 5's main measure is essentially zero and points the wrong way. The mean excess 5-day return is -0.20 % with t -0.32 over 314 cases on 228 days, which is -0.040 of a usual 5-day move (10.60 %). On the folds shown (B, C), the 135 bars in the regime earn +0.76 % excess over 5 days with t 0.76, so the result is near zero on both views.
- **F2:** The grading the idea claims is reversed rather than convex. On the bars in the regime in folds B and C, the excess 5-day return falls as the rise gets larger:
- **F3:** The effect changes sign with the year, so it is drowned by the market's own moves. On the bars in the regime, the excess 5-day return by year is:
- **F4:** The effect is mixed across coins. BTC gives +2.21 % (t 1.71, 30 cases), XRP +5.98 % (t 1.51), and ZEC +2.71 % (t 1.58). XMR gives -2.82 % (t -1.84, 31 cases) and LTC -1.64 % (t -0.93).
- **F5:** The choppy calm profile does not concentrate the effect, so the brief's claim that it lives only in calm markets is not supported. Big up days outside the profile earn +1.12 % excess over 5 days (t 1.80, 786 bars), more than the +0.76 % inside it (t 0.76, 135 bars). The only in-profile readings near t 2 rest on 19 to 23 grid cases: +6.2 % at 5 days (t 2.17) and a signed +5.1 % at 10 days (t 2.02).
- **F6:** The book does not pay even though the trades lose little before fees. The 174 trades average +0.94 % before fees and +0.84 % after, but only 47.7 % of them win. The book's Sharpe is -0.10 and its yearly return is -2.3 %. The total move per case (+0.42 %) covers the 0.19 % cost only through the coin's normal drift (+0.61 %), not through any unusual move.

## Ideas
- No ideas: The result is near zero (t -0.32 on 314 cases) and has no clear home. Its grading runs opposite to the idea (F2), its sign follows the year's market (F3) and the coin (F4), and it is no stronger inside the choppy calm profile than outside (F5), so no amendment would give a clear answer.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
