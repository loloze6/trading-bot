---
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d
idea tested: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6235 USD
---
## Findings
- **F1:** The check failed on Calmar (0.72 against the 0.75 rule) because of two deep falls: 42 % from w12 to w14, while holding the coins fell 79 % over the same stretch, and 42 % from w1 to w7, while holding fell 75 %; the book's yearly return is 30 % against holding's 13 %.
- **F2:** The book loses inside its falling legs and earns everywhere else. Those legs cover 1450 of 2898 days, where its daily returns sum to -1.85 (holding: -3.37); on the other days they sum to +4.46.
- **F3:** Inside the falling legs, nearness to the 90-day high is followed by falls instead of rises. The nearest quintile, held at a position of 1.05, loses 0.32 % per bar, and its 5-day return is -1.27 % (t -2.32, 253 cases); middle nearness is also followed by falls, -1.11 % to -1.79 % (t -2.4 to -3.1). Outside the legs, the nearest quintile is followed by +3.98 % (t 5.51, 449 cases).
- **F4:** In the bear years 2018 and 2022, closes at middle nearness are followed by the largest falls: quintile 2 by -3.82 % over 5 days (t -4.53, 119 cases), quintile 3 by -3.45 % (t -2.37, 57). The book still holds them at positions of 0.58 and 0.62, against 0.37 and 0.53 over all years. Its forecast is standardised against nearness's own last 90 values, so a partial rebound in a falling market reads as "near".
- **F5:** Across all bars, the gain is concentrated where nearness is high and climbing. The nearest quintile earns 0.35 % per bar (5-day return +2.09 %, t 4.08, 702 cases). The quintile whose nearness rose most over the past 10 days carries 11.4 of the book's 16.4 summed bar gain (5-day return +1.40 %, t 3.05, 632). Near-high closes that are also a 10-day closing high earn 0.66 % per bar (+2.88 % over 5 days, t 3.18, 274), against 0.15 % (+1.58 %, t 2.61, 428) for those that are not.
- **F6:** The year the book lost most, 2018, is also the year the move after its positions was most negative: it lost 0.155 % per bar, and the 5-day return after its bars was -1.71 % (t -2.54, 426 cases).
- **F7:** The idea is large enough for its cost: its total move is 1.19 % per case, 6.2 times a round trip, and its unusual move 3.1 times. The failure is in the falls, not in the cost.

## Ideas
- `020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high.d1_absolute-nearness-to-high` (from F3, F4, F6, F7): The closer a coin's daily close sits below its highest close of the past 90 days, the more it rises over the next 5 days, the rise growing with the percent distance of the close to that high itself. A close that is only nearer than it was over the past 90 days, but still far below the high, is followed by a fall over the next 5 days.
- `020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high.d2_rising-nearness-to-high` (from F1, F3, F5): The closer a coin's daily close sits below its highest close of the past 90 days, the more it rises over the next 5 days, and the more so the more that nearness has grown over the past 10 days.
- `020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high.d3_rebound-retest-in-downtrend` (from F2, F3, F4): After a coin's 90-day highest close has been falling over the past 20 days, the further the close has rebounded from its low back toward that falling high, the more the coin falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
