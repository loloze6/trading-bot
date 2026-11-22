---
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d
idea tested: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3461 USD
---
## Findings
- **F1:** The book's whole gain comes from its long side and its short side loses. Long bars earned a summed +12.08 (mean +0.146 % a bar over 8269 bars). Short bars lost a summed −3.22 (mean −0.035 % a bar over 9096 bars). The book was short more often than long.
- **F2:** The gain sits at the very top of the range. Bars with a forecast in (15, 20] carry +7.58 of the +8.86 total bar gain (mean +0.416 % a bar, 1821 bars). On the 10-day grid their unusual move is +5.27 % over 178 cases, about 28 times the 0.19 % cost of a trade. The (8, 15] bucket shows −0.86 % (351 cases) and the (2, 8] bucket +0.97 % (198 cases).
- **F3:** Below the middle of the range the coin rises back rather than falling further, so the shorts bet the wrong way.
- **F4:** The deepest fall, which fails the Calmar test (0.206), was driven by the shorts.
- **F5:** The upward continuation near the top holds whether or not the coin trended over 90 days.

## Ideas
- `023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only` (from F1, F2, F4, F5): The closer a coin's daily close sits to the top of its 30-day closing range, the more the coin rises over the next 10 days, only while the close is in the upper half of that range. The rise grows fastest in the last stretch just below the 30-day high.
- `023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d2_bottom-of-range-rebound` (from F3, F4): The closer a coin's daily close sits to the bottom of its 30-day closing range, the more the coin rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
