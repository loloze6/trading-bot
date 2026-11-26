---
line: 7.d confirmed, not profitable
backtest: 060-01.b1_agitated-decline-rally-fades-next-day_1d
idea tested: 060-01.b1_agitated-decline-rally-fades-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4273 USD
---
## Findings
- **F1:** The giveback lives almost entirely in up days that come after a 5-day fall. In folds B and C, in-profile up days whose prior 5-day return was in the lowest quartile (below -4.6 %) were followed by a short-side return of +1.82 % over the next day (t 3.23, 160 cases), +1.85 % over two days and +1.51 % over three days. Up days after a 5-day rise of +0.9 % to +8.8 % lost -0.63 % the next day (t -1.32) and -1.31 % over three days. All 637 cases together earned only +0.67 % next day, and their effect is gone by day 3 (-0.04 %).
- **F2:** The prior 5-day fall is not an effect of its own on the short side. In-profile down days with the same lowest-quartile 5-day return were followed by a short-side return of -1.13 % the next day (t -4.15, 382 days) and -1.42 % over three days. These coins rebound when there is no up day. The condition earns the short only together with the idea's rise, which fits the brief's theory: a squeeze up day inside a running decline is the overshoot that trapped holders sell into.
- **F3:** The book's deepest fall, -5.7 % in w14, and its worst days came on days when the coins rose strongly. Its worst days lost -5.2 %, -3.5 % and -2.1 % while the coins' mean return was +11.0 %, +5.9 % and +12.5 %. Across days, the book's mean return falls steadily from +0.14 % on the coins' worst-day quintile to -0.11 % on their best-day quintile. These losses on squeeze continuations are what hold the Calmar at 0.33.
- **F4:** The sizing puts its weight where the effect fails, and holding on costs money.
- **F5:** The effect points the same way in every year explored but is weak in 2020. Next-day short-side returns were +1.40 % (t 2.90) in 2018, +0.68 % in 2019, +0.14 % in 2020 and +0.65 % in 2021. The book earned +2.2 % a year against the coins' much larger swings, with nine of twelve windows within ±1.2 %.

## Ideas
- `060-01.b1.d1_bounce-inside-fresh-slide-fades` (from F1, F2, F3, F4): In a falling, agitated market, a coin's one-day rise that comes after a fall over its last 5 days is followed by a fall over the next 3 days that grows with the size of the rise against the standard deviation of its daily returns over the past 30 days and with the depth of that 5-day fall.
- `060-01.b1.d2_post-slide-bounce-next-day-giveback` (from F1, F2, F4, F5): In a falling, agitated market, a coin's one-day rise is followed by a larger fall over the next 1 day the deeper the coin's 5-day return before the rise, graded by the rise against the standard deviation of its daily returns over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
