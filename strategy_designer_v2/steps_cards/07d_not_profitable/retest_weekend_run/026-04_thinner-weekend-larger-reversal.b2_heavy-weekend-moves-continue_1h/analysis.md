---
line: 7.d confirmed, not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6327 USD
---
## Findings
- **F1:** The Calmar fails (0.67 against 0.75) because of one long fall: the book's deepest fall is −12.5 %, running 304 days from w22 to w24. All three windows lost (−4.4 %, −3.9 %, −3.2 %, each falling 4.9–6.5 % inside the window). In those windows the 43 cases ran against the signal: mean directional 48-hour return −2.6 % for longs (t −2.04, 28 cases) and −0.7 % for shorts (15 cases). By year, 2025 has a mean of −1.9 % (t −1.53, 43 cases) and the deepest mean adverse excursion, −6.9 %.
- **F2:** The effect lives in calm coins. Cases in the coin's lowest tercile of 30-day volatility earn +1.94 % per 48 hours (t 3.11, 115 cases) with a mean adverse excursion of −3.1 %. The highest tercile earns +0.96 % (t 0.82, 118 cases) with −6.6 %. In the w22–w24 fall the high-volatility cases account for −0.48 of the −0.71 summed position gain. Chaining the weekly case gains for the low and middle terciles only roughly halves the deepest fall, from −12.9 % to −6.0 %, and raises total gain over deepest fall from 4.7 to 8.3.
- **F3:** Calm volatility is not an effect on its own. Following any 48-hour move on the plain 48-bar grid in the lowest volatility tercile earns +0.24 % (t 2.08, 2,138 cases), about an eighth of the +1.94 % on signal cases. It belongs to the brief's theory: a coin that is usually calm is one where a heavy-volume weekend move is informed flow rather than noise.
- **F4:** Weekend moves in the direction of the coin's prior 30-day trend carry the effect, and moves against it barely do:
- **F5:** The case gain grows with the weekend-to-weekday volume ratio: +1.92 % (t 1.96) in the top quarter against −0.08 % in the bottom quarter, 87 cases each. But inside the w22–w24 fall the top half of the volume ratio lost the most: −4.0 % per case (t −2.37, 18 cases, summed gain −0.63). So heavier volume alone does not protect against the falls.
- **F6:** XMR is the one coin where heavy weekend moves reversed: −1.22 % per case (t −1.19, 68 cases), and −4.2 % (t −3.19, 9 cases) in the fall windows. Without XMR the chained cases earn +1.55 % per case (t 2.78, 278 cases), with the deepest fall at −10.4 % instead of −12.9 %.
- **F7:** A stop would hurt the book. Cases that went 3 % or more against the signal in their first 12 hours gained +3.57 % over the remaining 36 hours (t 2.63, 38 cases). Cases already 3 % or more in favour gave back −1.06 % (t −0.75, 75 cases).

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins` (from F1, F2, F3): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 48 hours. The continuation is the larger the larger the move, the heavier the weekend volume against the weekdays, and the calmer the coin's hourly moves over the past 30 days against its own usual level.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation` (from F1, F4, F5): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 48 hours, the more so the larger the move and the heavier the weekend volume. The continuation is larger the more the weekend move goes the same way as the coin's 30-day return before the weekend.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr` (from F1, F6): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 48 hours, the more so the larger the move and the heavier the weekend volume against the weekdays.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
