---
line: 7.g patterns
backtest: 032-02.b1.e1.e1_tight-range-breakouts-continue_1d
idea tested: 032-02.b1.e1.e1_tight-range-breakouts-continue
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3538 USD
---
## Findings
- **F1:** Over all bars, the closer a coin's daily close sits to its prior 20-day closing high, the larger its excess return over the next 10 days, in non-overlapping cases. The rank correlation is 0.172 (t 4.63, 702 cases). Scaled by the coin's 20-day mean absolute move it is 0.174 (t 4.67).
- **F2:** The F1 gradient rises steadily across quintiles of distance from the 20-day high. Excess 10-day returns run from −1.95 % and −1.96 % in the two farthest quintiles to +1.29 % and then +4.94 % (t 2.96, 141 cases) in the quintile at the high.
- **F3:** The F1 gradient holds in every coin, with rank correlations from 0.099 (BTC) to 0.239 (XRP). It also holds on bars where the book held no position (0.140, 466 cases), so it is not only the tested breaks. Across windows it is mixed, positive in 6 of 12 (from −0.106 in w7 to +0.349 in w16).
- **F4:** The same nearness-to-high effect shows at 5 days for the 20-, 30- and 60-day highs. The rank correlations are 0.121 (t 4.58, 1422 cases), 0.115 (t 4.13) and 0.121 (t 3.55). At 20 days it is clear only for the 60-day high, at 0.188 (t 2.69, 198 cases).
- **F5:** The tested grade, narrowness of the 60-day range in usual moves, shows no gradient against the 20-day excess return. Its rank correlation is −0.074 (t −1.04, 198 cases), and step 5's slope t on the forecast was −0.57. The book's +4.83 % unusual move per case therefore comes from the break itself, not from how tight the range was.
- **F6:** The book trailed holding in most windows: it was below the coins' annualised mean in 9 of 12 windows and in all 6 coins (for example BTC +37 % against +58 %, ZEC +4 % against +32 %). Its 0.47 Sharpe edge over holding comes from being out in falling windows (w7 −20 % against −173 %, w14 −4 % against −157 %).
- **F7:** Next-day excess returns by weekday split as Wednesday closes −0.49 % (t −2.69, 1254 days) and Thursday closes +0.47 % (t 3.19). The 5-day returns from Thursday were negative (t −2.50), so the pattern is inconsistent and, after 7 groups and many angles, not a finding I act on.

## Ideas
- `032-02.b1.e1.e1.g1_nearness-to-high-momentum` (from F1, F2, F3, F4): The closer a coin's daily close is to the highest close of its prior 20 days, the larger its rise over the next 10 days, whether or not the close breaks above that high.
- `032-02.b1.e1.e1.g2_two-month-high-proximity-drift` (from F4, F5, F3): The closer a coin's daily close is to the highest close of its prior 60 days, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
