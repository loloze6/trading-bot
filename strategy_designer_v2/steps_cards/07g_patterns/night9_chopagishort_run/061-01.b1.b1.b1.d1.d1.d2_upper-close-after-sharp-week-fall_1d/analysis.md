---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6327 USD
---
## Findings
- **F1:** After a deep 5-day fall (5-day return of -1 usual move or less), the close's place in the day's range splits what follows in two. Closes in the top quarter of the range were followed by a further fall: -5.1 % against the coin's normal 3-day drift (t -2.5, 55 cases on 22 days). Closes in the 0.5–0.75 band showed no fall: +0.2 % (t 0.09, 84 cases). Closes in the lower half showed none either: -0.5 % (t -0.31, 227 cases).
- **F2:** The same split shows on the 5×5 grid of 5-day return quintile against close-location quintile (2,712 cases). The cell with the deepest 5-day fall and the highest close is the most negative of the 25 cells: -0.34 of a usual move (t -3.39, 76 cases). The deepest-fall cell with the lowest close goes the other way: +0.12 (t +1.94, 213 cases).
- **F3:** Grading by the depth of the fall, as the tested book does, does not carry the effect. The verdict's supporting check came out at -0.59 % (deeper falls did worse), and the main measure was +0.44 % with t 0.78 over 1,255 cases. The tested situation's 0.5 location cut-off mixes in the 0.5–0.75 band, which holds no effect (+0.2 %, F1).
- **F4:** The fall after a high close following a deep 5-day fall grows with the horizon. It is -5.1 % over 3 days (t -2.5) and -9.3 % over 5 days (t -1.78, 23 cases on 11 days). The book's trades show the same: trades held 4–6 days earned +7.4 % on average (97 trades) and trades held 6–10 days +12.5 % (20 trades). Trades closed within 3 days lost -1.8 % (465 trades).
- **F5:** The high-close effect after a deep fall is not confined to the brief's choppy market. It was -4.3 % in choppy markets (10 cases) and -4.6 % in falling markets (t -1.81, 35 cases). The agitation split could not be measured on these windows, because the 365-day swing rank needs more history than a window holds.
- **F6:** No other angle stood out once day clustering and the number of angles tried are counted:
- **F7:** The book itself earned little: Sharpe 0.24 against a holding Sharpe about 0.37 higher, Calmar 0.07, and window means of daily returns between -0.04 % and +0.29 %. It lost on most coins: LINK -3.7 % and AAVE -5.6 % mean per trade.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.d1.d2.g1_high-close-inside-weekly-drop` (from F1, F2, F3, F5): After a coin's 5-day return has been a deep fall, a daily close near the top of that day's high-low range is followed by a further fall over the next three days, and the nearer the close sits to the day's high, the larger that fall.
- `061-01.b1.b1.b1.d1.d1.d2.g2_high-close-drop-five-days` (from F1, F4): After a coin's 5-day return has been a deep fall, a daily close near the top of that day's high-low range is followed by a further fall over the next five days, and the nearer the close sits to the day's high, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
