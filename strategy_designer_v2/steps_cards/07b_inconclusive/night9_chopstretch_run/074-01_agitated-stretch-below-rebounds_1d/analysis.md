---
line: 7.b inconclusive
backtest: 074-01_agitated-stretch-below-rebounds_1d
idea tested: 074-01_agitated-stretch-below-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2032 USD
---
## Findings
- **F1:** In folds B and C, the 172 non-overlapping 10-day agitated cases below the average show no grading: their mean unusual move is +0.24 % (t 0.17) and the slope of that move on the depth is -0.0058 (t -0.54). Step 5's slope over all folds is on the predicted side but small (t 1.03, 405 cases on 152 days), and the size cannot be told from 0 (+0.05 % per case, t 0.06 over 329 days, strength 0.017).
- **F2:** The depth quartiles of the agitated cases do not rise in order. Over 10 days the shallowest quartile gives +0.69 %, the second +3.33 %, the third -4.15 % (t -1.92) and the deepest +0.92 %, so the deepest stretches do not rebound more than the shallow ones.
- **F3:** The brief's contrast with calm markets is in the data even though the grading is not. Over 10 days, calm cases below the average lose 3.38 % of unusual move (t -3.38, 183 cases) while agitated cases gain +0.24 %. Over 20 days the calm cases lose 6.38 % (t -3.01, 93 cases) and the agitated cases gain +5.38 % (t 1.89, 102 cases).
- **F4:** The agitated rebound sits in one period.
- **F5:** No single coin carries the effect. The mean unusual 10-day moves of the agitated cases range from +4.2 % for BTC (t 1.31, 29 cases) to -2.2 % for XRP (t -0.43, 24 cases), and every coin's slope on depth has |t| ≤ 0.82.
- **F6:** The market's own rise drowns the effect. The total move per case is +1.36 %, almost all of it normal drift (+1.30 %), against an unusual move of +0.05 %. That unusual move is 0.3 times the 0.19 % cost of a trade, while the coin's usual 10-day move is 14.49 %.

## Ideas
- `074-01.b1_agitated-stretch-all-coins` (from F1, F4, F5): In an agitated market, the further a coin's close sits below its 20-day average, measured in units of the standard deviation of its daily returns over the same 20 days, the more it rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
