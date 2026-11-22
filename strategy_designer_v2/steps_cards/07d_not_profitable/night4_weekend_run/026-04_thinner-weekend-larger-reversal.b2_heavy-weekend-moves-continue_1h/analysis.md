---
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3924 USD
---
## Findings
- **F1:** The book's gain is too thin because it is mostly flat. It holds a position on only 6–18 % of bars depending on the coin, is flat on 52 % of days, and holds a mean absolute allocation of 0.56 at the cases. Its mean daily return is 0.024 % against the 0.05 % required, while its mean on the days it is in a position is 0.050 %.
- **F2:** The weekend move keeps extending well past the 48-hour hold. On the 463 Sunday-23:00 cases the signed return is +1.15 % at 48 h (t 2.65) and +2.13 % at 120 h (t 3.44). The increment from 48 to 120 h is +0.93 % (t 1.96, 453 cases). On the volume-gated weekends the unusual move doubles from +1.14 % at 48 h (t 2.49, 432 cases) to +2.37 % at 120 h (t 3.74, 422 cases).
- **F3:** The continuation lives almost entirely in weekends that extend the preceding weekdays' move. Among gated weekends whose move has the same sign as the prior five weekdays' move, the unusual 120 h move is +3.83 % (t 4.71, 257 cases), against +0.10 % (t 0.10, 165 cases) when the weekend goes against the week. Across all weekends the same split is +0.89 % (t 2.46, 1086 cases) against −0.09 % (t −0.29, 1133 cases).
- **F4:** The Friday move points the same way. Cases where the Friday before the weekend moved in the weekend's direction gain +1.72 % over 48 h (t 2.83, 270 cases), against +0.20 % (t 0.31, 180 cases) otherwise.
- **F5:** Across all 2,219 Sunday-23:00 weekends, ungated, the effect is graded by weekend volume against the weekdays. The unusual 120 h move by volume-ratio quintile goes from −0.97 % (t −1.84) in the lowest to +2.46 % (t 3.72) in the highest. The ungated weekends together show nothing (u120 −0.08 %, t −0.30, 1797 cases).
- **F6:** Inside the gated cases, the size of the weekend move does not grade the outcome. The 48 h move by |move| quartile is +0.02 %, +2.81 %, +0.86 %, +0.81 %. Across all weekends, by vol-scaled move quintile, it is flat at about +0.4 % except −0.58 % in the fourth.
- **F7:** The Calmar failure comes from a deep fall late in the folds and from losing tails. The book's deepest fall is −14.2 % over 288 days, from w22 to w24, where five of six coins' trades lost (ZEC −63 %, XMR −38 %, XRP −30 % summed). XMR loses overall (−128 % summed over 135 trades, worst trade −62 %). The worst 1 % of trades lose more than 24.5 %, and the 10 worst days sum to −0.27 against a total of +0.70.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_weekend-extends-weekday-trend` (from F1, F2, F3, F4, F7): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 5 days, the more so the larger the move and the heavier the weekend volume against the weekdays, only while the weekend move extends the coin's move over the preceding five weekdays, and the more so the larger that weekday move in the same direction.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_weekend-volume-grades-continuation` (from F2, F5, F6): The heavier a coin's Saturday-Sunday volume against its mean volume over the preceding five weekdays, the further the coin continues its weekend move over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
