---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-03_close-below-breakout-bar-low
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 5 days, and the smaller the coin's 20-day rise into the breakout day, the larger the fall.
Consequence: A trader would short a failed breakout that came out of a quiet base and refuse one that capped a strong 20-day rally.
Why:
- F4: On the broader situation, 256 cases of a close back below the old 20-day high within 10 days of a breakout, the 5-day short outcome depends on the 20-day run-up into the breakout. The low run-up tercile gained +0.78 % (t 0.71, 87 cases), the middle −0.35 % and the high tercile −2.28 % (t −2.30, 86 cases). The overall Spearman is −0.149: after a big run-up, the failure is followed by a fresh rise.
- F6: The book's falls and weak Calmar (0.21) follow from shorting into rising coins. Over 60 days, the strongest tercile of prior returns gave the short −1.16 % per case and the weakest −0.03 %. The losing shorts sit where the coin was already trending up.
- F3: Recomputed from prices, the tested situation is a 20-day high, a 3-day failure and a close below the breakout day's low. It gave 46 non-overlapping 5-day cases with an unusual move of +0.09 % (t 0.06). All twelve variants of lookback (10 or 20 days), failure window (3, 5 or 10 days) and reference level (breakout low or old high) stay between −0.31 % and +0.62 %, with |t| ≤ 0.81 on 46 to 656 cases. The depth's Spearman with the outcome sits between −0.13 and +0.08 in every variant.
