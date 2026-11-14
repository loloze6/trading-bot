---
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
idea tested: N4-04_dip-rebound-spans-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3461 USD
---
## Findings
- **F1:** The book fails on its falls, not its gain: the book's daily returns (each day, the mean over coins of `book_return`) earn about 21% a year, but the deepest fall chained across windows is -35.6%, and single windows fall far: w17 -21.7%, w13 -19.5%, w11 -17.7%, w19 -15.9%. In those windows nearly the whole fall sits in one to four book days below -2% (w17: one day carried -0.209 of a 3-day, -21.7% fall; w13: two days carried -0.205; w19: two days carried -0.163).
- **F2:** The loss comes from positions the dip does not repay quickly. Of 1432 trades, the 1017 closed within 1.5 days average +1.11% after fees. The 251 that lasted 1.5 to 3.5 days average -4.35% (worst -28.9%), and the 86 that lasted 3.5 to 7.5 days average -3.59%. A dip that keeps falling after entry is what the book holds into its falls.
- **F3:** The rebound exists only after large standardised drops. Over non-overlapping long-forecast events, the 3-bar excess return against the coin's all-window mean is +1.94% (t=3.58, n=288) when the drop's z is below -1.06, and +1.05% (t=1.64, n=288) for z between -1.06 and -0.64. It is -0.12% (t=-0.27, n=288) and -0.17% (t=-0.38, n=288) for the two milder quartiles. Half the events the book takes carry no edge but still carry crash risk: 6-8% of events in every quartile fall more than 10% in 3 bars.
- **F4:** The rebound needs a real uptrend, not the regime's bare "above 0". When the 20-day rise is under 6.2%, the 3-bar excess is -0.07% (t=-0.18, n=288). When the 20-day rise is 14.8-27%, it is +1.06% (t=2.23, n=288).
- **F5:** The rebound weakens when volatility is calm. In the lowest quartile of 20-day to 60-day volatility (ratio below 0.84), the 3-bar excess is -0.19% (t=-0.32, n=182). In the higher three quartiles it is +1.0% to +1.5% (t 1.39 to 1.96, n=182 each).
- **F6:** Once a dip has rebounded, the edge is spent. On held days that follow an up-close above +0.97%, the coin's next-day return averages -0.24% (n=590). On held days that follow drops below -2.55%, it averages +0.47% to +0.83% (n=590 and 589).

## Ideas
- `N4-04_dip-rebound-spans-days.d1_failed-dip-keeps-falling` (from F1, F2): In a coin whose 20-day and 60-day changes are positive, a day that closes lower right after a sharp-drop day is followed by further decline over the next several days: the drop is the start of a fall, not a dip.
- `N4-04_dip-rebound-spans-days.d2_only-large-dips-rebound` (from F3, F1): In an uptrending coin, a rise over the next three days follows only a one-day drop that is large against the coin's last 60 daily moves, about one standard deviation or more. Milder down days are followed by the coin's ordinary drift.
- `N4-04_dip-rebound-spans-days.d3_rebound-needs-strong-trend` (from F4, F5): A sharp one-day drop is followed by a three-day rise mainly when the coin has risen strongly over the previous 20 days and its recent volatility is at or above its 60-day level. In a barely positive or calm trend, the drop is followed by no rise.
- `N4-04_dip-rebound-spans-days.d4_rebound-ends-on-first-up-close` (from F6, F2): After a sharp dip in an uptrend, the first up-close above about one percent marks the end of the rebound, and the coin's next days return below its average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
