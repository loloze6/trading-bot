---
line: 7.d confirmed, not profitable
backtest: 060-01.g1.d2.d1.g3_wide-high-close-fade_1d
idea tested: 060-01.g1.d2.d1.g3_wide-high-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4245 USD
---
## Findings
- **F1:** The effect lives on the next day only: the signal's short excess return is +0.67 % at 1 day (t 3.00, 624 cases) but -0.07 % at 2 days, -0.24 % at 3 days and -0.37 % at 5 days (t -0.21 to -0.80). A longer hold would give the gain back, so the book's weak Sharpe against holding (-0.13) and its Calmar (0.24) cannot be fixed by holding longer.
- **F2:** The book's losses sit where the coin had already fallen hard over its last 10 days. Signals with a 10-day return below -15 % earn -1.42 % on narrow days (64 cases, t -1.61) and +0.57 % on wide days (86 cases, t 0.83). Signals without such a fall earn +0.59 % on narrow days (270 cases, t 2.05) and +1.47 % on wide days (204 cases, t 3.78). The 10-day return quartiles agree: the deepest quartile (below -15.4 %) earns -0.26 % (t -0.47), against +0.40 % to +1.29 % in the others.
- **F3:** The same deep-fall signals lose in the windows that drag the book, at -0.94 % in w16 (32 cases) and -2.22 % in w18 (42 cases); w18 is the window of the book's deepest fall (-3.9 %) and its only losing large window (-0.66 %). In w18 the not-deep, wide signals earn +3.51 % (40 cases).
- **F4:** The not-deep-fall condition is not an effect of its own. On in-profile bars without the signal (close in the lower half), the not-deep, wide bars give a short excess of -1.29 % (233 cases, t -3.09). With the signal the same condition gives +1.47 %. The condition alone points the other way, so it belongs to the idea's theory: after a deep sell-off, a strong close is capitulation buying meeting exhausted supply, not short-lived covering into an ongoing downtrend.
- **F5:** The book's 25 worst trades came on unusually wide days after deep falls, and their positions were larger than average:
- **F6:** The range grading itself holds. The short excess rises from -0.08 % in the narrowest range quartile to +1.38 % in the widest (t 2.89, 147 cases).
- **F7:** Closes pinned at the very top of the range fade less: close location above 0.855 earns +0.30 % (t 0.66, 156 cases), against +0.98 % and +0.97 % for 0.63 to 0.855 (t 2.08 and 2.30).
- **F8:** In a cost-applied rebuild on folds B and C, excluding signals after a 10-day fall below -15 % raises the Sharpe from 0.76 to 0.87 and cuts the deepest fall from -4.0 % to -3.3 %. The rebuild does not reproduce the record's Calmar (1.16 here against 0.24 recorded on all folds), so most of the recorded fall lies in folds A and D, which step 7 cannot see.

## Ideas
- `060-01.g1.d2.d1.g3.d1_wide-high-close-fade-no-capitulation` (from F2, F3, F4, F5, F1): In a falling, agitated market, a coin that closes in the upper part of its day's high-low range falls over the next day, and the wider that day's range against its average range of the last 20 days, the larger the next-day fall, except when the coin's 10-day return already shows a deep fall.
- `060-01.g1.d2.d1.g3.d2_wide-shallow-fall-high-close-fade` (from F2, F6, F4, F5): In a falling, agitated market, a coin that closes in the upper part of its day's high-low range falls over the next day, and the wider that day's range against its average range of the last 20 days and the smaller the coin's fall over the last 10 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
