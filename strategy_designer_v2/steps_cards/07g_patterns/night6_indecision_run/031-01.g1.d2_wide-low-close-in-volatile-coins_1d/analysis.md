---
line: 7.g patterns
backtest: 031-01.g1.d2_wide-low-close-in-volatile-coins_1d
idea tested: 031-01.g1.d2_wide-low-close-in-volatile-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4163 USD
---
## Findings
- **F1:** The book's gain is concentrated in a few days: it is in a position on 12.1 % of its 2898 book-days, its 10 best days sum to +54.3 % against a total of +76.4 % summed daily return, and its 10 worst days sum to −29.6 %. Nearly all trades last one day (286 trades, mean +2.30 % net); the 3 trades that lasted two days lost a mean of −8.5 %.
- **F2:** Across all coin-days, the next-day unusual move rises in the top octile of the day's (high − close) measured against the prior 20-day mean range. That octile (above 0.95 of a mean range) shows +0.64 % (t 2.92, 1812 cases on 715 days), while the octiles below 0.64 lie between −0.28 % and +0.01 % with no t beyond −1.8. Outside the tested regime the top octile still shows +0.40 % (t 1.92, 1586 cases on 686 days).
- **F3:** Among days closing in the lowest quarter of their range, the next-day unusual move grows with the range multiple:
- **F4:** My own volatility split does not carry the effect, so the regime filter's contribution is unclear. Wide low-close days with recomputed 20-day vol below its 60-day mean still give +1.14 % next day (t 2.60, 220 days), against +1.47 % (t 1.43, 60 days) when vol is high. The detector's own regime days give +2.22 % (t 2.97, 149 days) against +0.39 % (t 1.12, 164 days) for the other wide low-close days. My recomputation and the detector's condition disagree on which days are "volatile".
- **F5:** The prior run barely matters, against the brief's run-ending story. Wide low-close days after the lowest prior-5-day-return tercile give +1.75 % (t 1.83, 89 days), after the highest tercile +1.40 % (t 3.10, 130 days), and after the middle tercile +0.44 % (t 0.95).
- **F6:** On the regime's wide low-close days, the rise continues past day 1 on non-overlapping grids. The unusual move is +2.98 % over 2 days (t 2.80, 76 days) and +3.41 % over 3 days (t 2.22, 50 days). The other wide low-close days show +0.90 % (t 1.56) over 2 days and −0.06 % (t −0.07) over 3 days.

## Ideas
- `031-01.g1.d2.g1_close-far-below-high` (from F2, F3, F4): The further a coin's daily close sits below that day's high, measured in units of its mean daily range over the past 20 days, the larger its rise over the next 1 day, whatever its recent volatility.
- `031-01.g1.d2.g2_wide-low-close-three-day-rebound` (from F6, F1): After a day whose range is wide against its 20-day average and whose close lands near the low, in a coin whose 20-day volatility is high against its usual level, the coin keeps rising over the next 3 days. The wider that day's range and the closer its close to the low, the larger the 3-day rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
