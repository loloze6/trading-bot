---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
line: 7.b inconclusive
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves.
Consequence: A flat coin sliding moderately below the middle of its range is a short to take, while its most extreme slides are left alone.
Why:
- F1: The main measure is on the side the idea predicts, a mean short-side unusual 5-day move of +1.09 % with t 2.32 over 436 cases, but the grading fails: the larger-|forecast| half beats the smaller half by -0.77 %, and Spearman's rho between |forecast| and the unusual move is -0.09 (p 0.06).
- F2: The grading is hump-shaped, not monotone: by |forecast| quartile the unusual move is +0.66 % (t 0.59), +2.30 % (t 2.31), +1.13 % (t 1.26) and +0.29 % (t 0.39) from the weakest to the strongest. By raw 10-day return quartile it is +1.94 % (deepest), +2.78 %, -1.20 % and +1.31 % (shallowest), so a deeper slide does not reliably give a larger follow-through.
- F4: ZEC carries much of the pooled t: ZEC alone gives +3.42 % with t 2.99 over 73 cases. Without ZEC, the 5-day measure drops to +0.63 % with t 1.22 over 363 cases. The other coins lie between +0.23 % and +0.87 %, all with t below 0.81.
