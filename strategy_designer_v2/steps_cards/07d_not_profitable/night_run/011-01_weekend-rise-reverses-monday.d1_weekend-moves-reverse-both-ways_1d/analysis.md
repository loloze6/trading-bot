---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways_1d
idea tested: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3511 USD
---
## Findings
- **F1:** The book is only exposed from Sunday close to Monday close, so it is flat about 71% of days (active share 28.6%). Its mean daily return is 5.6e-05 against the required 5e-04, and only Mondays earn anything: the book's mean is 7.97e-04 on Mondays and about 0 on every other weekday. That gives a yearly return of 1.2% against a deepest fall of 24.5% (Calmar 0.06), with falls of 20–24% in w9, w6, w7, w8 and w13.
- **F2:** The reversal the book bets on is real and specific to the weekend. On Sundays the 2-day fade return is 0.79% (t 4.83, n 2021). On the other six days it ranges from -0.33% to +0.08% (t -2.44 to 0.55).
- **F3:** The book holds only one day of a reversal that runs on into Tuesday. The fade earns 0.45% over Monday (t 4.13), 0.23% more on Tuesday (t 2.39) and 0.64% over the two days (t 4.29, n 2441). Each Sunday's fee of 0.045% of the book takes about 36% of the mean Monday gain of position × return (0.125%).
- **F4:** The reversal is not graded at the top, and the forecast is largest exactly where there is no edge. By quartile of |weekend z|, the 2-day fade is:
- **F5:** The reversal sits in coins whose 20-day return is negative and is weak in rising coins:
- **F6:** Low weekend volume does not strengthen the reversal, unlike what the brief expects. The 2-day fade is 0.70%, 0.81% and 0.89% for low, mid and high Sunday relative volume.

## Ideas
- `011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.d1_weekend-reversal-in-downtrends` (from F2, F3, F5, F1): A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and a coin that fell over the weekend rises over those 2 days, only while the coin's 20-day return is negative. The more negative that 20-day return and the larger the weekend move relative to the coin's usual daily move, the larger the move back.
- `011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.d2_moderate-weekend-moves-reverse` (from F4, F2, F1): A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and a coin that fell over the weekend rises over those 2 days. The move back grows with the weekend move up to the size of the coin's usual daily move and shrinks as the weekend move grows further beyond it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
