---
line: 7.b inconclusive
backtest: 067-01.b1_choppy-down-stretch-keeps-falling_1d
idea tested: 067-01.b1_choppy-down-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3838 USD
---
## Findings
- **F1:** Step 5's measure was not what failed. On the choppy grid's 128 below-average 5-day cases, the slope on the plan's 60-bar standardised forecast has a t of only 0.92, while the slope on the raw stretch it is built from has a t of 1.93, though the two correlate 0.91. Standardising the stretch against its own recent size blurs its grading.
- **F2:** In a choppy market, a close below the 20-day average is followed over 5 days by a clear fall against the coin's drift: -3.2 % excess, t -3.62, 128 cases. The fall is a level, not a grade. By stretch band (≤-3, -3..-2, -2..-1, -1..-0.5, -0.5..0) the excess is -4.9 %, -7.3 %, -1.0 %, -4.8 % and -0.8 %, which is not monotonic.
- **F3:** The below-side grading is mixed across periods. Its 5-day slope t is -1.61 in 2018, +1.06 in 2019, +6.16 in 2020 and -0.90 in 2021, so one year carries it. All six coins have a positive slope with t under 2 (0.17 to 1.92).
- **F4:** In a choppy market the grade shows when both sides of the average are read together. The 5-day excess return rises with the raw stretch with slope t 3.29 over 249 cases. The octiles of the stretch run from -7.7 % at the deepest below (stretch -3.2) to +1.2 % at the highest above (stretch +4.1).
- **F5:** The above side alone is weak in a choppy market (5-day slope t 1.11, mean excess +0.0 %, 121 cases). The both-sides grade of F4 therefore rests mostly on below-average closes doing worse than above-average ones.
- **F6:** The both-sides grade is not specific to choppy markets. Outside the choppy profile it has a 5-day slope t of 3.52 over 1,173 cases, and over all bars 4.31 over 1,422 cases. It also holds at 10 days in a choppy market (t 2.33, 126 cases).
- **F7:** Agitation does not localise the below-side effect clearly. Agitated choppy cases fall more (-5.6 % excess, slope t 1.68, 40 cases) than calm ones (-2.1 %, slope t 0.75, 88 cases), but neither slope reaches 2.
- **F8:** The tested book's average 5-day trade cannot pay. The total move per case is +0.03 % against a 0.19 % round-trip cost (0.1 times the cost), and the unusual move is +0.60 % (t 1.50, 449 days). The down-stretch fall in a choppy market lies in the coin's own falling drift (-0.57 % in the short direction), not on top of it.

## Ideas
- `067-01.b1.b1_choppy-stretch-carries-both-ways` (from F4, F1, F2, F5): In a choppy market, the further a coin's close stands from its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin keeps moving the same way over the next 5 days, rising after closes above the average and falling after closes below it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
