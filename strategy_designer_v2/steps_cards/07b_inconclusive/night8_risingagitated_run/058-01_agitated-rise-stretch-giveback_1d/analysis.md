---
line: 7.b inconclusive
backtest: 058-01_agitated-rise-stretch-giveback_1d
idea tested: 058-01_agitated-rise-stretch-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3380 USD
---
## Findings
- **F1:** The test's own forecast showed no graded giveback at any horizon: in the rising agitated profile, the slope of the excess return on the size of the short forecast had t of +0.84 at 3 days (288 cases), -0.81 at 5 days (171), -0.01 at 10 days (80) and -1.37 at 20 days (27). Step 5's pooled slope t of +0.39 on 436 cases fits this.
- **F2:** The effect runs the other way from the idea. In the profile, closes above the 20-day average were followed by a rise beyond the coin's normal drift: the mean excess over 5 days was +2.37 % (t 2.14, 171 cases in folds B and C). Step 5's mean unusual move in the short direction was -1.08 % on all folds.
- **F3:** The larger distance does not bring a larger fall. Over 5 days, the five raw-distance quintiles in the profile had mean excess returns of +4.06 %, +2.38 %, +2.85 %, +2.88 % and -0.36 % (about 34 cases each). Only the top fifth turned negative, against +3.10 % for the rest (Welch t -1.28, 35 cases), and the forecast's quartiles fell only from +3.82 % to +1.47 %, all with t under 1.6.
- **F4:** The top-distance giveback does not hold at other horizons. The top fifth minus the rest had a Welch t of +0.00 at 3 days and -0.38 at 10 days. At 10 days the top vol-scaled quintile even rose +9.19 % beyond drift (t 2.04, 16 cases), so no horizon or scaling shows the effect clearly.
- **F5:** The effect is not specific to agitation, and it is not in most coins. In rising calm markets, closes above the average were also followed by rises beyond drift at 5 days (quintile means +1.7 % to +5.5 %, the fourth with t 3.41), as in the agitated profile. By coin, only LTC had a slope near the bar (t -1.83, 39 cases), while BTC, XMR and XRP had mean excess returns of +2.9 % to +3.6 %.
- **F6:** Even the idea's total move cannot pay for trading. The total move per case is -1.44 % in the short direction, -7.5 times the 0.19 % cost of a trade, and the book had a Sharpe of -0.92.

## Ideas
- No ideas: The theme's effect is not in the data. In rising agitated markets a close far above its 20-day average is followed by a further rise beyond drift, not a giveback (F2), and no graded fall shows at any horizon, coin or distance band (F1, F3, F4, F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
