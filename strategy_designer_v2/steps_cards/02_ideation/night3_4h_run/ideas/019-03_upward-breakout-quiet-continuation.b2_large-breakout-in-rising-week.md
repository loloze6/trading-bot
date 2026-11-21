---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive, the coin rises over the next three days, and the farther that close sits above the two-day high, measured in the coin's 30-day average four-hour range, the larger the rise.
Consequence: A trader would buy large upward breaks in units of the coin's usual 4h range during a rising week and refuse breaks that follow a falling week, where the move is large enough per case to cover the cost of a trade.
Why:
- F3: The narrowness of the two-day stretch, the core of the idea's grading, does not order the outcome. The narrowness quintiles give +0.60, +0.35, −0.11, +0.46 and −0.20 %, none with |t| above 1.35, and the Spearman correlation of narrowness with the 18-bar excess return is −0.017.
- F4: The size of the break does order the outcome, measured as the close's distance above the two-day high in units of the 30-day average 4h range. The top quintile (median 1.35 ranges) earns +1.46 % excess over 3 days (t 3.24, 569 cases), about 7.7 times the cost of a trade. The other four quintiles sit between −0.37 % and +0.03 %. The raw break in percent shows the same pattern, with its top quintile at +1.00 % (t 2.09).
- F5: The coin's prior 7-day return splits the cases cleanly and in grades. Its quintiles give −0.75 % (t −2.37), −0.27 %, +0.41 %, +0.61 % and +1.12 % (t 2.17) over 18 bars, and −0.74 % up to +1.89 % (t 2.53) over 36 bars. Breakouts after a falling week lose (−0.51 %, t −2.07, 903 cases), while those after a rising week gain (+0.57 %, t 2.68, 1949 cases).
- F6: The two conditions together carry the effect. Large breaks (top tercile) after a rising week earn +1.44 % over 3 days (t 3.12, 696 cases), while every tercile after a falling week is negative (−0.25 to −0.85 %).
