---
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3813 USD
---
## Findings
- **F1:** The book loses before costs, so the cost is not what sinks it: its 3925 trades of about 45 hours average -0.41 % before fees and -0.51 % after; shorts lose -1.05 % and longs gain +0.37 %; the book loses most on Mondays (-6.2 bp a day) and Tuesdays (-9.2 bp); its Sharpe is -0.66, its mean daily return -0.029 % and its Calmar -0.16; the idea's size is -0.24 % per case against a cost of 0.19 % a trade.
- **F2:** The 48-hour weekend return joins two halves that act in opposite ways. Across 2387 Monday-00:00 cases, Saturday's 24-hour return correlates +0.071 with the next 48 hours (t 3.47), while Sunday's correlates -0.083 (t -4.06). The full 48-hour return the book trades on correlates only -0.013 (t -0.62), so the two halves cancel.
- **F3:** Sunday's own 24-hour return is reversed: over the next 24 hours the unusual move against it averages +0.38 % (t 3.42, 2387 cases, strength 0.077), and over the next 48 hours +0.58 % (t 3.85). That is about 2 and 3 times the 0.19 % cost of a trade.
- **F4:** Sunday's reversal grows with the size of Sunday's move. Over the next 24 hours it is -0.04 % in the smallest |z| quintile (mean |move| 0.34 %), then +0.34 %, +0.33 % and +0.40 %, and +0.86 % in the largest quintile (mean |move| 7.5 %, t 2.63, 478 cases). Over 48 hours the largest quintile reaches +1.09 %.
- **F5:** Saturday's move continues: at Monday 00:00, the next 48 hours in the direction of Saturday's 24-hour return average +0.45 % unusual move (t 2.99, 2387 cases).
- **F6:** Sunday's reversal is broad but not steady. It holds in all six coins over 24 hours (+0.14 % in BTC to +0.58 % in XMR, t 2.38). It is larger after rises (+0.52 %, t 3.48) than after falls (+0.22 %, t 1.38). It was strong in 2019 to 2020 (+0.78 % and +0.85 %) and near zero in 2023 and 2025 (-0.02 % and -0.00 %).
- **F7:** The reversal is not unique to the weekend: the day ending Wednesday 00:00 is reversed over the next 24 hours by +0.40 % (t 3.55). The day ending Tuesday 00:00 is not (-0.07 %, t -0.72), nor the day ending Friday 00:00 (-0.08 %).

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week` (from F1, F2, F3, F4, F6): A coin's 48-hour return over Saturday and Sunday is followed by a larger opposite move over the next two days than a 48-hour return of the same size that ends on any other weekday, only for the part made on Sunday: the larger the coin's 24-hour return over Sunday, the larger the opposite move over Monday and Tuesday.
- `026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday` (from F3, F4, F6): A coin's 24-hour return over Sunday is followed by an opposite move over the next 24 hours, and the larger Sunday's move, the larger that opposite move.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week` (from F2, F5): A coin's 24-hour return over Saturday is followed over the next two days by a move in the same direction, and the larger Saturday's move, the larger that continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
