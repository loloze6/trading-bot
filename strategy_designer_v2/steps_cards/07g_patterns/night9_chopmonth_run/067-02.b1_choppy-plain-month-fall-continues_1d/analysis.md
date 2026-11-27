---
line: 7.g patterns
backtest: 067-02.b1_choppy-plain-month-fall-continues_1d
idea tested: 067-02.b1_choppy-plain-month-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4454 USD
---
## Findings
- **F1:** In the choppy regime, the 7-day move after the coin's own drift is removed falls step by step with the plain 30-day return: -9.39 % in its lowest fifth (30-day return -26 %, t -2.80, 43 cases on 23 days) and -4.40 % in the next fifth (t -1.97, 28 days). It is +0.49 %, +2.32 % and +1.82 % in the upper three fifths, each with t under 1.1, so the fall side carries the effect and the rise side does not show.
- **F2:** Outside the choppy regime the same falls are not followed by more falling (calm -0.09 %, t -0.04, 39 days; agitated -0.46 %, t -0.14, 24 days). The month-fall continuation lives in the choppy market only, which is the brief's situation.
- **F3:** The tested config's standardised forecast also shorted 48 choppy cells whose 30-day return was above zero; those moved +2.73 % against the short (t 0.81). The 111 cells it shorted after a real 30-day fall moved -5.14 % (t -2.80, 54 days). The book therefore diluted its plain-fall cases with cases where the month was up.
- **F4:** The deep-versus-shallow gap holds on all seven starting offsets of the 7-day grid. The deepest third of choppy 30-day falls moved between -5.7 % and -11.0 %, the shallower two thirds between -1.2 % and -2.8 %, so the grading does not depend on where the grid starts.
- **F5:** The effect is uneven across windows. Choppy falls were strongly negative in w9, w12 and w15 (calm cases -5.9 %, -12.2 % and -8.6 %, t -6.6, -7.9 and -5.6). They were positive in w7, w8 and w10 (+3.7 % agitated, +6.5 % and +15.8 % calm, t about +3).
- **F6:** Splitting choppy falls by agitation gives contradictory answers, so the effect does not show in one agitation level.
- **F7:** The book behaves as a short on the coins. Its daily return correlates -0.53 with the coins' mean daily return. On its worst 2 % of days the coins rose +9.0 %, and on its best 2 % they fell -9.1 %.
- **F8:** That explains the size line. The unusual move of +1.13 % per case (5.0 times the 0.22 % cost) is cancelled by the coins' upward drift of 1.13 % against the short, leaving a total move of -0.01 %.
- **F9:** Two other angles did not stand out from chance after this many cuts.

## Ideas
- `067-02.b1.g1_choppy-swing-scaled-month-fall` (from F1, F2, F3, F4, F8): In a choppy market, the further a coin's close sits below its close of 30 days earlier, measured in units of its usual 30-day swing, the more it falls over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
