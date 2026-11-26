---
line: 7.b inconclusive
backtest: 038-02_calm-swing-scaled-fall-continues_1d
idea tested: 038-02_calm-swing-scaled-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3430 USD
---
## Findings
- **F1:** In a calm market, the test's continuation shows on both sides together: the slope of the 5-day excess return on the swing-scaled 5-day move is +0.0085 with t 2.80 (904 cases, 200 days). The fall side alone, which the test measured, gives only +0.0090 with t 1.34 (432 cases, 133 days), and the rise side +0.0100 with t 1.95 (472 cases, 144 days). The test's result (t 1.48) is on the predicted side but uses half the cases.
- **F2:** The effect lives in the calm profile only. In an agitated market the same two-sided slope is flat at every horizon: t 0.17 over 3 days, -0.19 over 5, 0.96 over 7 and 0.29 over 10. The agitated quintiles even lean to reversal: the lowest quintile ends +1.15 % in excess and the highest -0.26 %.
- **F3:** In a calm market the effect is graded and sits in the extremes. The lowest quintile of the scaled move (mean -2.76) ends 5 days later at -3.35 % in excess, the highest (mean +3.63) at +2.93 %, and the three middle quintiles between -0.19 % and +0.16 %.
- **F4:** Calm cases whose 5-day move spans at least 2 daily swings continue in their own direction by +3.18 % over 5 days (t 2.85, 304 cases, 120 days). This holds on both sides: falls +3.59 % (t 2.27, 121 cases), rises +2.91 % (t 1.89, 183 cases). That is about 14 times the 0.22 % cost of a trade.
- **F5:** The calm two-sided slope over 5 days is positive in every year of folds B and C (2018 t 1.31, 2019 t 0.14, 2020 t 1.36, 2021 t 1.47). It is also positive on every coin with enough cases (BTC t 1.63, ETH 2.13, XMR 2.48, ZEC 2.05, ADA 1.95, XRP 1.73, LTC 0.87). It is a broad but small effect, not one coin's or one year's.
- **F6:** The tested idea already used every fold and all 19 coins, so no more data is available. Its short-only book also fights the coins' upward drift: the normal drift in the short direction is -0.69 % per case, the total move -0.32 % against an unusual move of +0.38 %, and the book's Sharpe is -0.008.

## Ideas
- `038-02.b1_calm-swing-scaled-move-continues` (from F1, F2, F3, F4, F5, F6): In a calm market, the more of its 20-day daily swings a coin's 5-day move spans, the further the coin keeps moving the same way over the next 5 days, for rises and falls alike.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
