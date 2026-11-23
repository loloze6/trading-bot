---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 10 days. The closer the fall of that closing day stays to the coin's usual daily move, rather than a crash several times larger, the larger the fall that follows.
Consequence: A trader would short the failure that slips back on an ordinary down day and refuse the one that collapses through the breakout low in a single crash bar.
Why:
- F5: Failures that arrive on a crash day bounce instead of falling, and the depth grading points the wrong way. The quintile with the largest one-day fall on the signal day (−10.8 % on average) is followed by a short-side move of −4.25 % (t −2.21, 73 cases), meaning the coin rose. The deepest-depth quintile (8.3 % under the breakout low) moved −2.71 % (t −1.51). The next fall quintiles (−6.2 % and −2.6 % that day) do continue: +0.91 % (t 1.12) and +1.11 % (t 1.16) over 5 days, and +3.27 % (t 2.45) and +2.72 % (t 1.94) over 10 days.
- F1: Most failed breakouts do not fall further. Recomputed from prices, a close below the breakout day's low within 3 days of a close above the prior 20-day high gives 361 cases with a short-side unusual 5-day move of −0.60 % (t −1.10). The broader close back below the old high gives −0.48 % (t −1.18, 619 cases) within 3 days, −0.64 % (t −1.73, 770 cases) within 5 days and −0.34 % (t −1.09, 1040 cases) within 10 days. The confirmed +2.83 % rests on 50 cases and does not hold for the situation at large.
- F4: The idea's grading by the run-up is absent. The Spearman correlation between the 20-day run-up into the breakout day and the short-side move is 0.038. Run-up quintiles from the smallest (4.4 % average) to the largest (71 %) all lose, between −0.30 % and −1.23 %, with every |t| below 0.62.
