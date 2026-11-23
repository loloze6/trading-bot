---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower its power over the following 90 days. The larger both the excess past power and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a fall, the larger the coin's rise over the next 5 days.
Consequence: A trader should take only the long side of the nearness-power reversal, sized by the joint reading, and refuse its shorts, which pay the coin's rise without an edge.
Why:
- F1: The book loses on its short side and earns on its long side. Bars held short gained −0.043 % a bar (10,133 bars, mean allocation 0.39), while bars held long gained +0.124 % a bar (11,104 bars, mean allocation 0.46), with fees of only 0.006 % a bar on each side. The short side's loss comes from the coins' rise, not from a missing effect: on the 5-day grid the unusual move is almost the same on both sides (shorts +0.40 %, t 1.74, n 2275; longs +0.37 %, t 1.73, n 2454), but the total move is −0.34 % for shorts and +1.09 % for longs.
- F2: Keeping only the long side of the recorded positions fixes the measures that failed in my rebuilt book (round-trip cost 0.22 %). Sharpe rises to 0.95 against 0.54 for holding the coins and 0.56 for the original book. The mean daily return on days in a position rises to 0.124 %, against 0.045 % for the original and a 0.05 % bar. Calmar rises to 0.57 against 0.27 (deepest fall −36 % against −44 %), and the lowest Sharpe with one window left out rises to 0.82 against 0.42. Calmar still stays under the 0.75 bar.
- F4: Squaring the forecast buys nothing. On the 5-day grid, strength stays about 0.04 from the second quintile of |forecast| to the top (0.039, 0.041, 0.039), and the top quintile's unusual move (+0.41 %) equals that of the middle quintiles. Fees therefore spread over readings that are no stronger than the small ones.
