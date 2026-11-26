---
line: 7.b inconclusive
backtest: 065-02_falling-agitated-prior-slide-rebound_1d
idea tested: 065-02_falling-agitated-prior-slide-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3800 USD
---
## Findings
- **F1:** The result points the way the idea predicts but falls short of the bar. Step 5's pooled slope is +0.00060 with a day-clustered t of 1.77 (3,092 bars, 875 days), and its size is +0.38 % per case with t 1.36 (529 days). In folds B and C alone the same slope is +0.00072 with t 1.06 (807 bars). The test already used every coin and every fold of 1d data, so no more data is available to add.
- **F2:** In folds B and C, the forecast's slope comes entirely from bars where the latest day also fell, and it reverses where the latest day rose. On down latest days the slope is +0.0028, t 3.15, mean next-day excess return +1.49 %, 404 bars. On up latest days it is −0.0016, t −2.45, mean −0.94 %, 403 bars. A deep prior slide ending in a small or up day does not rebound, against the idea's "even when the latest day's own fall is small".
- **F3:** When the five-day fall is split into its two parts, the four days before the latest day add nothing. Their slope has t 0.32 at 1 day, 0.27 at 2 days and 0.58 at 3 days. The latest day's own fall has t 2.87, 3.55 and 3.76 at the same horizons (690, 685 and 678 cases in the profile, 279 days).
- **F4:** The deeper the whole five-day fall ending at the latest close, scaled by the coin's 20-day swing, the larger the rise, and the effect grows with the horizon.
- **F5:** The effect lives in the falling agitated profile only. Outside it, the same five-day depth has a slope of −0.00006 with t −0.03 (3,189 cases).

## Ideas
- `065-02.b1_five-day-slide-three-day-rebound` (from F2, F3, F4, F5): In a falling, agitated market, the deeper a coin's fall over the five days up to and including the latest day, measured against its usual daily swing, the larger its rise over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
