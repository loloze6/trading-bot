---
line: 7.b inconclusive
backtest: N2-05_shock-up-continuation_1d
idea tested: N2-05_shock-up-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3065 USD
---
## Findings
- **F1:** The 601 independent big-up-day events have a mean 5-bar excess return of +0.88% (t 1.67), but the median is −0.22%, the hit rate is 48.9%, the skew is 2.4 and the 5%-trimmed mean is only +0.34%, so a few large winners lift the mean while the typical event goes nowhere.
- **F2:** Much of the drift is the market's own move: the other five coins rise +1.05% over the same 5 bars (t 2.92, n 601), and the coin's 5-bar return correlates 0.59 with theirs. Measured relative to that basket, the excess is +0.42% (t 0.99).
- **F3:** The effect changes sign across years. Events gain in 2021 (+2.97%, t 2.08, n 74) and 2024 (+3.35%, t 2.72, n 77) and lose in 2022 (−4.60%, t −2.82, n 67) and 2018 (−0.49%, hit 34%, n 62), so a pooled t near 1.7 averages opposing regimes.
- **F4:** The effect sits in coins that were already rising. Events in the top tercile of the prior 20-day return gain +2.97% over 5 bars (t 2.35, n 163). The low and mid terciles gain +0.08% (t 0.11) and −0.35% (t −0.49).
- **F5:** Measured from the bar after the event (bars t+1 to t+5), top-tercile prior-20-day events gain +2.68% (t 2.61, n 163, hit 58.9%). The next-bar excess over all events is −0.20% (t −0.88), so any continuation starts after the first day.
- **F6:** Big up days that close above the prior 20-day closing high gain +1.82% over 5 bars (t 2.01, n 245), against −0.02% (t −0.04, n 242) for those that do not. Similarly, events above the 50-bar average gain +1.27% (t 1.91, n 299), against +0.03% (t 0.04, n 157) below it.
- **F7:** The effect is not stronger for bigger shocks: the z-score quartiles give +1.37%, +1.22%, −0.17% and +1.20% with no ordering. It also varies by coin, from ZEC +3.14% (t 1.75, n 98) to XMR −1.33% (t −1.33, n 90).

## Ideas
- `N2-05_shock-up-continuation.b1_shock-up-inside-existing-uptrend` (from F4, F5, F1, F3): When a coin closes up by an outsized amount (about 2σ of its recent daily moves) while its close is already well above where it was 20 days earlier, it keeps rising over the next five days, beginning from the day after the shock.
- `N2-05_shock-up-continuation.b2_shock-up-new-high-breakout-continuation` (from F6, F1, F7): When a coin's outsized up day closes above its highest close of the prior 20 days, the coin keeps rising over the following five days.
- `N2-05_shock-up-continuation.b3_delayed-drift-above-trend` (from F5, F6, F2): After an outsized up day in a coin trading above its 50-day average, the coin rises from the next day's close to five days after the shock, more than its usual daily drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
