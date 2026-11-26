---
line: 7.g patterns
backtest: 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d
idea tested: 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4491 USD
---
## Findings
- **F1:** In the falling agitated profile, an up day is followed by a next-day move 0.98 % below the coin's normal drift (t −4.24, 613 days) and a down day by one 1.25 % above it (t 5.37, 675 days); outside the profile both are near zero (−0.14 %, t −1.55, 3,572; +0.07 %, t 0.73, 3,395), so the one-day reversal lives in this profile only.
- **F2:** Within the profile, the next-day fade after an up day grows with the length of the down run just before it: after no down day −0.20 % (t −0.35, 126 days), after one −1.02 % (t −1.76, 101 days), after two −2.93 % (t −3.24, 50 days), after three or more −1.06 % (t −1.21, 49 days).
- **F3:** The fade belongs to the first up day of a move: in the profile an up streak of 1 is followed by −1.55 % (t −5.84, 370), a streak of 2 by +0.39 % (t 0.62, 131) and a streak of 3 by +0.01 % (59), so a second up day is not faded.
- **F4:** The fade does not grow with the up day's own size against the 30-day swing: up-day quartiles by return/s30 give −1.15 %, −0.59 %, −1.59 % and −0.15 % (day-clustered t −1.93, −0.89, −3.06, −0.18). Where the day closed in its range grades it only slightly (low, middle and high close terciles −1.22 %, −1.05 %, −0.67 %).
- **F5:** The brief's multi-day give-back is weak. In the profile, after a 2-day rise the next 2 days are flat in every tercile of the rise against the swing (+0.07 %, −0.09 %, +0.45 %, all |t| < 0.3). After a 3-day rise only the top tercile gives back over the next 3 days (−3.10 %, t −1.93, 28 days), which cannot be told from chance.
- **F6:** The book's gain is concentrated in w14 and w16: their cases fall −2.39 % (t −3.81, 87) and −1.46 % (t −2.87, 85) and their book sums are 0.086 and 0.036, against at most 0.012 in any other window. Cases are weaker in the early half of the explored windows (−0.80 %, t −1.04, 72 days) than in the late half (−1.02 %, t −2.32, 186 days), which fits the failed Calmar.
- **F7:** The long-side mirror is graded in the profile but already held. The next-day move after down days rises with the down streak (+0.92 %, +1.21 %, +2.01 %, +3.31 % for streaks of 1, 2, 3 and 4 or more, t 3.04 to 2.96), but the falling agitated long cell already holds 12 strategies.

## Ideas
- `058-01.g2.g1.g1.d1.d1.g1_agitated-decline-first-bounce-fade` (from F2, F3, F1, F4): In a falling, agitated market, the first up day after a run of down days is followed by a fall over the next day, and the more consecutive down days came before it, the larger that next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
