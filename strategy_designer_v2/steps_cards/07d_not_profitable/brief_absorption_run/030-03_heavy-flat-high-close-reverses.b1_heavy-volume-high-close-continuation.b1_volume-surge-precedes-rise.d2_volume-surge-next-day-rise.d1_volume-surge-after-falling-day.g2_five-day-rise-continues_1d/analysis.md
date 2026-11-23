---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4761 USD
---
## Findings
- **F1:** The Calmar failed because of one long fall: the book fell 33.7 % over 1114 days, from w1 to its trough in w10, while the coins fell 68.3 %. That fall alone sets the deepest fall against a yearly return of +25.0 %, giving a Calmar of 0.742 against a rule of 0.75.
- **F2:** The book's gain while held depends on the coin's own longer trend. On bars held when the coin's 60-day return was positive, the mean daily gain was +0.219 % (3095 bars, sum +6.79); when it was not, it was −0.020 % (2566 bars, sum −0.51). Above versus below the 50-day average it was +0.209 % (3829 bars) against −0.005 % (2851 bars).
- **F3:** The idea's grading exists only inside a rising 20-day trend. On the 3-day grid among signal cases, the slope of excess return on the forecast is 0.00083 when the 20-day return is positive (1508 cases, forecast-weighted excess +0.65 %). When it is not, the slope is 0.00014 (820 cases, weighted excess +0.14 %).
- **F4:** The weak half of the forecast carries no gain. By forecast quartile, the 3-day excess is −0.17 %, −0.09 %, +0.25 % and +0.96 % (about 712 cases each). With a positive 20-day return, the top half earns +0.66 % (t 2.13, 881 cases) and the bottom half −0.25 % (t −0.92, 627 cases).
- **F5:** Held gain in the losing stretch w1–w10 shows where the fall came from. With the 20-day return at or below zero and a strong forecast, the mean daily gain was −0.045 % (285 bars). With a positive 20-day return and a strong forecast it was +0.075 % (980 bars). In w11–w24, the strong-forecast, positive-trend bars earned +0.582 % a day (1631 bars, sum +9.49), almost all of the book's gain.
- **F6:** The trend condition alone is only part of the 3-day effect, and none of the 9-day effect.
- **F7:** Rebuilt books with costs show how much a trend filter improves the falls.
- **F8:** The idea's size clears the cost. Per case the total move is +0.63 %, 3.3 times the 0.19 % cost of a trade, and the unusual move 1.2 times it. The book's problem is its falls in down-trends, not cost.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues.d1_five-day-rise-in-uptrend` (from F1, F2, F3, F5, F7): The larger a coin's 5-day rise, measured in its usual 5-day moves, the more it rises over the next 3 days, only while the coin's 20-day return is positive.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues.d2_five-day-rise-held-longer` (from F3, F6, F8): The larger a coin's 5-day rise, measured in its usual 5-day moves, the more it rises over the next 9 days, only while the coin's 20-day return is positive.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues.d3_strong-advance-in-uptrend` (from F4, F5, F7): The larger a coin's 5-day rise, measured in its usual 5-day moves, beyond its typical 5-day advance, the more it rises over the next 3 days while its 20-day return is positive, with the move growing fastest among the strongest advances.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
