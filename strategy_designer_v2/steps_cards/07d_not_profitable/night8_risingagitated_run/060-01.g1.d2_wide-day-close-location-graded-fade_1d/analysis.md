---
line: 7.d confirmed, not profitable
backtest: 060-01.g1.d2_wide-day-close-location-graded-fade_1d
idea tested: 060-01.g1.d2_wide-day-close-location-graded-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4586 USD
---
## Findings
- **F1:** The book fails only on Calmar (0.668 against 0.75), and on folds B and C the loss comes from a small set of cases: those whose close sits in the lowest third of the upper half of the range (close position 0 to 0.33 on a -1 to +1 scale) lose 1.40 % on the next day (33 cases, t -1.27, 64 % losing). Cases from 0.33 to 0.66 gain 2.35 % (74 cases, t 3.63, 31 % losing), and cases from 0.66 to 1 gain 1.30 % (53 cases, t 1.84).
- **F2:** The losing low cases reach the book because the forecast standardises the close position against its own last 60 values. A wide day whose close is barely above the middle still counts as a short whenever recent closes sat lower. Of the 160 cases, a quarter have a close position under 0.39, and the lowest is 0.001.
- **F3:** Keeping only the cases with a close position above 0.33 makes the book steadier. In a rebuilt book of the cases (absolute allocation × short return, minus 0.19 % cost), the deepest fall shrinks from -2.23 % to -1.94 % while the yearly return holds at 3.8 %. Calmar rises from 1.70 to 1.97 and Sharpe from 1.00 to 1.01, on 127 cases instead of 160.
- **F4:** The fall is a one-day effect. Over two days the short return of the cases is about 0 (s2: -0.39 % for closes from 0.66 to 1, +1.86 % for closes from 0.33 to 0.66, -3.29 % for the lowest cases), so a longer holding adds nothing.
- **F5:** Within the profile, how high the close sits matters only on wide days. Wide days closing in the upper half fall 1.40 % the next day (133, t 2.74), while narrow days closing in the upper half fall 0.28 % (414, t 1.03). Wide days closing in the lower half rise 2.91 % (177, t -4.93). The width alone carries no fall, since it amplifies whichever side the close is on.
- **F6:** The fall grows with how wide the day is against its 20-day average range: +1.10 % in the lowest third of cases (t 1.13), +0.76 % in the middle third and +2.35 % in the top third (ratio above 1.57, t 2.47). Wide-range days that close low instead rise 4.20 % (53, t -2.86), so the width is not an effect of its own. Cutting the book to range ratios of 1.3 or more lowered its Calmar to 1.52, so width belongs in the sizing, not as a filter.
- **F7:** The effect varies by coin and by year. It is near zero on BTC (+0.09 %, 36 cases) and LTC (-0.08 %, 23), and strongest in 2018 (+2.01 %, t 2.82, 58 cases). The 2021 cases reach only +0.79 % (t 0.42, 58 % losing).

## Ideas
- `060-01.g1.d2.d1_own-range-close-height-fade` (from F1, F2, F3, F4): In a falling, agitated market, a coin whose day's high-low range is at least as wide as its average range of the last 20 days falls over the next day when it closes in the upper part of that range, and the nearer the close sits to the day's high, measured within that day's own range rather than against its recent closes, the larger the next-day fall.
- `060-01.g1.d2.d2_wider-squeeze-day-fades-harder` (from F5, F6, F4): In a falling, agitated market, a coin that closes above the middle of its day's high-low range falls over the next day, and the wider that day's range against its average range of the last 20 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
