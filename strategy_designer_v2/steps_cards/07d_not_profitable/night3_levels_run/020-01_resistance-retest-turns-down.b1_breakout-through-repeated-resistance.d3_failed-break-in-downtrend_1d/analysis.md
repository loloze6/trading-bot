---
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend_1d
idea tested: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3609 USD
---
## Findings
- **F1:** The book loses on the moves it holds, not on its costs: 1148 trades, all short, held about 10.8 days, lose 3.05 % each before fees and 3.15 % after, against a cost of about 0.19 % per round trip, with 34 % winners, so fees explain only about 0.1 point of the loss.
- **F2:** The shorts bet against the coins' rise: the unusual short-side move per case is +0.58 % over 10 days (t 0.90, 620 cases), smaller than the normal 10-day drift of 1.17 % that a short pays, so the total move is -0.60 % per case and the book's mean daily return is -0.00025 (Sharpe -0.44) while holding the coins earned positive daily means in 6 of 8 years.
- **F3:** The forecast's grading runs the wrong way. The smallest-|forecast| fifth of cases has an unusual short move of +2.65 % (t 2.15, 124 cases), and the two largest fifths have -2.31 % (t -1.50) and -0.27 %. The trades show the same: gross losses grow from -2.03 % in the smallest |entry forecast| quarter to -4.48 % in the largest, so the bigger positions lose the most.
- **F4:** The size of the break carries the inversion. Cases whose close is only just above the broken level (smallest fifth of the touches × excess reading, median 0.27) are followed by a +3.05 % unusual short move (t 2.57, 124 cases), while the other four fifths have -0.44 % to +0.89 %, all with |t| below 0.8.
- **F5:** The depth of the 20-day fall, which the idea grades on, does not grade the move. Across its fifths the unusual short move is -0.18 %, +3.13 %, +0.68 %, +0.49 % and -1.09 % from deepest to shallowest, with no rise toward the deeper falls.
- **F6:** What does grade the decline is the coin's 60-day rise before the 20-day pullback. The fifth with the largest 60-day return (median +41 %) is followed by an unusual short move of +7.05 % (t 2.58, 52 cases), against -2.3 % to +0.6 % in the other fifths (correlation of 60-day return with the move 0.15). Among the just-above-level breaks, the top 60-day tercile shows +5.0 % (t 1.90, 39 cases, strength 0.34).
- **F7:** The losses are concentrated in years when the coins rose. In 2023 and 2024 the book's mean daily return was -0.0012 and -0.0011 while the coins gained 0.0015 and 0.0024 a day, and those years' cases have unusual short moves of -1.98 % and -2.69 %. The loss per coin is largest on XRP (-0.00075 a day), ZEC (-0.00052) and XMR (-0.00036).

## Ideas
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend.d1_failed-break-after-run-up` (from F3, F4, F5, F6, F2): When a coin closes above a price where it turned down several times in the past 90 days after falling over the past 20 days, it tends to fall over the next 10 days, and the larger its 60-day rise before that fall and the closer its close stays to the broken level, the larger the decline.
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend.d2_resistance-break-exhaustion` (from F6, F5, F7, F2): When a coin closes above a price where it turned down several times in the past 90 days after falling over the past 20 days, it tends to fall over the next 10 days, and the larger its 60-day return, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
