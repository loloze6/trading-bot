---
line: 7.d confirmed, not profitable
backtest: 031-01.g1.b2_next-day-down-close-rebound_1d
idea tested: 031-01.g1.b2_next-day-down-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3774 USD
---
## Findings
- **F1:** The failed measure is Calmar at 0.73 against 0.75, and it fails on one long fall: the deepest fall of the chained book is −27.6 % over 119 days in w8–w9 (2019), while the coins fell −43 % (summed daily returns) and the book −29 %; my rebuilt book of all signals gives Calmar 0.74, Sharpe 0.80, yearly +20.5 % and a deepest fall of −27.5 %.
- **F2:** The rebound lives only in falls that come while the coin's short-term volatility is rising: on signal bars, by quartile of the 20-day over 60-day volatility ratio, the excess next-day return is −0.28 % (t −1.80), +0.02 % (t 0.18), +0.10 % (t 0.67) and +0.76 % (t 4.74), with 1080 cases each; with the ratio above 1.2 it is +0.99 % (t 5.42, 880 cases), and at or below 1.2 it is −0.06 % (t −0.72, 3439 cases).
- **F3:** The volatility condition is not an effect of its own: on bars without the signal where the ratio is above 1.2, the coin's excess next-day return is −0.44 % (t −2.40, 937 bars), against +0.99 % where both hold; this fits the brief's crowding theory, in which a fall inside a burst of volatility is forced, one-sided selling that is then paid back.
- **F4:** Inside the rising-volatility regime the effect stays graded by the depth of the fall: in the top volatility-ratio quartile, the shallower half of the signals earns +0.58 % (t 2.72) and the deeper half +0.94 % (t 3.88); in the third quartile, the shallower half earns −0.41 % and the deeper half +0.59 % (t 2.88).
- **F5:** The calm-volatility signals carry the bear-year losses behind the deep fall: with the ratio at or below 1, the signals lost −0.93 % (t −3.39, 325 cases) in 2018 and −0.64 % (t −3.03, 359) in 2019, while with the ratio above 1 they earned +0.65 % and +0.37 % in those years; with the ratio above 1, the rebound is positive in 7 of 8 years and on all 6 coins (+0.21 % to +0.79 %).
- **F6:** Trading only signals with the volatility ratio above 1.2 (my rebuild, cost 0.095 % per side) lifts Calmar from 0.74 to 0.91 and Sharpe from 0.80 to 0.90, and cuts the deepest fall from −27.5 % to −10.1 %, at a yearly +9.2 % with 5 % of coin-days in a position; its excess move of +0.99 % per case is about 5 times the 0.19 % cost of a trade, against 1.0 times for the idea as tested.
- **F7:** A trend filter does not repair the falls: signals with a non-negative 20-day return earn +0.30 % (t 2.92) against +0.03 % (t 0.31) with a negative one, and the condition alone earns +0.07 % (t 0.78), but that book's Calmar is 0.40 with a deepest fall of −22.2 %.

## Ideas
- `031-01.g1.b2.d1_rebound-inside-volatility-bursts` (from F1, F2, F3, F4, F5, F6): The larger a coin's one-day fall, measured against its own daily volatility over the past 60 days, the more it rises above its normal drift over the next 1 day, only while its daily volatility over the past 20 days is above its daily volatility over the past 60 days.
- `031-01.g1.b2.d2_volatility-surge-graded-down-close-rebound` (from F2, F3, F4, F6): The larger a coin's one-day fall, measured against its own daily volatility over the past 60 days, the more it rises above its normal drift over the next 1 day, and the more so the further its daily volatility over the past 20 days stands above its daily volatility over the past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
