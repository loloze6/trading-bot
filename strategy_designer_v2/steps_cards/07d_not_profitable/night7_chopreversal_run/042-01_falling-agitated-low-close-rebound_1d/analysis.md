---
line: 7.d confirmed, not profitable
backtest: 042-01_falling-agitated-low-close-rebound_1d
idea tested: 042-01_falling-agitated-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3697 USD
---
## Findings
- **F1:** The book loses its money on the closes in the upper half of the day's range: in the falling agitated profile, closes in the top two fifths of the range (raw 0–0.2 and 0.2–0.4, n 231 and 270) were followed by next-day excess returns of −0.49 % and −0.84 %, and middle closes (0.4–0.6, n 254) by −0.06 %; the book still held positions of 0.07, 0.20 and 0.35 there and lost 0.09, 0.45 and 0.05 in summed bar gain, while closes in the bottom fifth (n 243) were followed by +2.17 % and earned 2.85.
- **F2:** The deepest fall (−14.4 %, the Calmar's denominator) came in w14 over 16 days, while the coins' daily returns summed to −37 %; in w14 the in-profile closes in the top three fifths of the range lost 0.03, 0.18 and 0.39 in bar gain (excess −1.2 %, −1.1 %, −2.4 %), while the bottom two fifths gained 0.29 and 0.68 (excess +0.5 %, +1.7 %), so the fall came from the long positions on high and middle closes.
- **F3:** Rebuilt from the recorded positions with the cost applied, a book that keeps only the lower half of the range has a Calmar of 1.52 against 0.82 for the rebuilt original, a deepest fall of −9.8 % against −14.4 %, a Sharpe of 1.22 against 0.91 and a yearly return of 14.9 % against 11.8 %, in a position on 8.0 % of coin-days; graded from the mid-range (zero at mid, largest at the low), it reaches a Calmar of 1.51 with a yearly return of 20.4 %. The rebuild reads higher than step 6's Calmar of 0.376, so these numbers compare the variants with each other, not with the reported value.
- **F4:** Adding the day's own fall (a down day) to the lower-half close gives a Calmar of 2.10, a deepest fall of −7.9 % and a Sharpe of 1.46 (graded version: Calmar 1.64, yearly 20.6 %). Measured as a condition: in the profile, a down day without a low close earns +0.51 % next day (n 111), a low close on an up day earns −0.82 % (n 108), and both together earn +1.40 % (n 564). The down day alone carries about a third of the joint move, and the low close alone carries none. It belongs to the theory: selling that presses into the close is a day that falls.
- **F5:** The day's own fall grades the move: in-profile bars in the lowest quintile of the day's return (mean −9.1 %) are followed by +2.37 % excess (bar gain 3.17), the second quintile (−2.9 %) by +1.12 %, and the three upper quintiles by −0.72 %, −1.21 % and −0.59 %; low-range closes in the lowest quintile still earn +2.03 % (n 239).
- **F6:** Outside the profile the effect is graded but small: excess next-day return runs from −0.34 % (raw 0–0.2, n 1540) to +0.23 % (raw 0.8–1, n 954), and a down day with a low close earns +0.20 % (n 2608) against +1.40 % inside the profile, so the effect lives in the falling agitated profile.
- **F7:** Cost is not the obstacle: the unusual move per case is +0.77 % (t 3.08, 656 days), 4.0 times the 0.19 % cost of a trade, and the failing measure is the falls, which come from the positions in F1–F2.

## Ideas
- `042-01.d1_lower-half-close-rebound` (from F1, F2, F3, F7): In a falling, agitated market, the lower a coin's close sits below the middle of that day's high-low range, the larger its rise over the next day, with a close at the very bottom of the range followed by the strongest rise, and closes in the upper half of the range followed by no rise.
- `042-01.d2_down-day-low-close-rebound` (from F4, F5, F2, F6): In a falling, agitated market, on a day the coin closes lower than the day before, the lower its close sits within that day's high-low range and the larger that day's fall, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
