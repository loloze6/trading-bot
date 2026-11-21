---
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4407 USD
---
## Findings
- **F1:** The short side is what loses. On the 8824 short bars the book lost -0.000255 per bar, and -0.000260 of that is simply the coin's own rise against the position, because the coins rose +0.087 % a day while it was short. Shorts carried -54 % of the book's total gain. On the 8458 long bars the book gained +0.000756 per bar, of which only 0.000328 came from the market's rise, so timing was about +0.00043.
- **F2:** The forecast's short side works only when the coin's 60-day return is not in its lowest tercile. In the middle and top terciles, short grid cases were followed by 5-day excess returns of -1.49 % and -1.22 %, with slope t of 2.91 and 1.79 (563 and 564 cases). In the lowest tercile, 84 % of the 564 cases were short, those shorts were followed by only -0.22 %, the few longs by +1.66 %, and the slope t was 0.58.
- **F3:** The unscaled 20-day return predicts the next 5 days better than the components the book uses. Its slope t is 2.69 (2843 non-overlapping cases), against 2.31 for the standardised nearness to the 90-day high, 1.40 for the 20-day return standardised over 60 days, and 1.90 for the combined forecast (3419 cases).
- **F4:** The cost of trading is not what fails. Per case the total move is +0.47 % against a 0.19 % round trip, 2.5 times the cost. Fees were 0.0038 % of the book per bar against a gain before costs of 0.024 % per bar.
- **F5:** The book is too small and too split to beat holding:
- **F6:** Most of the forecast's spread sits at its top. Across forecast quintiles the 5-day excess return goes from -0.35 % and -0.37 % in the two lowest quintiles to +0.27 % and +0.61 % in the two highest, so the long end carries the larger move.
- **F7:** The book lost in 2022 (-0.000158 per bar) and in 2023 (-0.000280 per bar). In 2023 the coins rose +0.15 % a day, so the book lost in a rising year as well as a falling one.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising.d1_near-high-momentum-outside-falls` (from F1, F2, F6, F7): The nearer a coin's close sits to its 90-day high and the larger its 20-day return, the higher its return over the next 5 days. This holds only while the coin's 60-day return is not in a fall; within that state, the further the close sits below its 90-day high after a 20-day fall, the lower the next 5 days' return.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising.d2_raw-20-day-momentum-persists` (from F3, F4, F6): The larger a coin's 20-day return, measured as a plain percentage change, the higher its return over the next 5 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising.d3_closeness-to-high-lifts-returns` (from F1, F3, F5, F6): The nearer a coin's close sits to its 90-day high, the larger its rise over the next 5 days above its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
