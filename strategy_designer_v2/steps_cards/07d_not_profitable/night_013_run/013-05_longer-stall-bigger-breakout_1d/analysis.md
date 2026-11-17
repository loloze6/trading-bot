---
line: 7.d not profitable
backtest: 013-05_longer-stall-bigger-breakout_1d
idea tested: 013-05_longer-stall-bigger-breakout
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2805 USD
---
## Findings
- **F1:** The book fails on mean daily return, 0.000232 against the 0.0005 floor. The cause is how rarely it is in the market: only 2.64% of all bars are in the trending regime (close above the prior 365-day closing high), and 2.61% of bars hold a position. The share by coin runs from 1.0% (XRPUSD) to 4.9% (BTCUSD).
- **F2:** When it is in, the situation pays. On the 439 trending bars the coin's next-day return beats its own mean by 0.99% a day (t = 3.27), and the mean allocation there is 0.94. The edge is real but present on too few days to lift the book's daily mean.
- **F3:** The edge does not come from the stall count that grades the position. Raw stalls of 0–5 days give a mean 30-bar forward return of 64.1% (n = 45), but 15–30 days give −0.3% (n = 165) and 30–60 days give 10.1% (n = 130). The forecast's grading does not line up with what follows, yet it sizes the largest positions (allocation 1.20) on the longer stalls.
- **F4:** A close above a shorter recent high carries the same follow-through and happens far more often. 7.4% of bars close above their prior 30-day closing high, against 2.6% for the 365-day high. On a non-overlapping 10-bar grid the next-10-bar excess return is +5.39% above the 30-day high (n = 132, t = 2.59) and +4.16% above the 20-day high (n = 163, t = 2.36). In daily excess return it is +0.32% (t = 2.07) for the 30-day high and +0.73% (t = 2.93) for the 60-day high.
- **F5:** The follow-through is graded by closeness to the 60-day high, though not across the whole range. On the 10-bar grid, coins 20–30% below their 60-day high return −2.80% excess (t = −2.78), 5–10% below +0.30%, within 5% below +2.21% (t = 1.72) and above it +3.81% (t = 1.69). On the 30-day high, the bins from 5% to 30% below all return between −0.3% and −0.8%, against +5.4% above it.
- **F6:** The book's yearly daily mean never reaches the floor in any full year except 2024 (0.000725). 2021 sits at 0.000496, and 2022 and 2023 are around zero. That is consistent with a signal too sparse to carry the book in most years.

## Ideas
- `013-05_longer-stall-bigger-breakout.d1_stall-under-monthly-high` (from F1, F2, F4): When a coin closes above its prior 30-day closing high, the more days of the past 20 days it spent closing just under that high, the larger its return over the next 10 days.
- `013-05_longer-stall-bigger-breakout.d2_closeness-to-monthly-high` (from F3, F4, F5): The closer a coin's close is to its prior 30-day closing high, and the further it sits above it, the larger the coin's return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
