---
line: 7.g patterns
backtest: 043-01_falling-agitated-intraday-drop-rebound_1d
idea tested: 043-01_falling-agitated-intraday-drop-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4065 USD
---
## Findings
- **F1:** In the falling-agitated profile, the next-day excess return falls in steps across the deciles of the day's open-to-close return: +2.69 % (t 5.41, 208 days) in the largest-drop decile, +1.31 % (t 3.89) in the second and +1.02 % (t 2.28) in the third. It reaches about 0 in the fourth, and is −0.78 % to −1.50 % in deciles 5 to 9 (t −1.57 to −2.80), the small-drop to moderate-rise days. Out of the profile the same deciles run only from +0.41 % (t 1.55) to −0.31 %.
- **F2:** The idea's long-only book does not use one half of this pattern. In the profile, up days are followed by a next-day excess of about −1.1 % (constant −1.13 %, t −2.39, 622 cases on 265 days). The lower two rise terciles give −1.07 % (t −2.91) and −1.13 % (t −3.23). The top tercile gives −0.46 % (t −0.99), so on up days the fall does not grow with the size of the rise (slope 0.057, t 0.75).
- **F3:** In the profile, the down-day relation is to the raw drop, as the brief claims. The next-day excess on the drop has a slope of 0.399 (day-clustered t 4.20, 675 cases, 288 days). The same drop measured against the coin's 20-day swing has a slope of −0.017 (t −1.77). Adding the 20-day return leaves the drop's slope at 0.356 (t 3.51).
- **F4:** The rebound is not reversed or extended after the next day. The day-after-next excess in the largest-drop decile is −0.40 % (t −0.97). The 3-day excess on the drop has a slope of 0.350 (t 3.69), against 0.399 for one day.
- **F5:** Out of the profile, the next-day excess on the drop has a slope of only 0.129 (t 2.05, 3,405 cases). Split by 60-day trend, no part is separable from 0 (falling 0.051, t 0.39; choppy 0.276, t 1.37; rising −0.007, t −0.06). The effect lives in the profile.
- **F6:** The book's gain is concentrated. Its 10 best days carry 68 % of its total return, only 41 % of its non-zero days are positive, and its 10 worst days sum to −24.5 %.

## Ideas
- `043-01.g1_falling-agitated-day-move-reversal` (from F1, F2, F3, F5): In a falling, agitated market, the higher a coin's open-to-close return on a day, from a large drop up to a moderate rise, the lower its return over the next day: large drops rise the next day and up days fall the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
