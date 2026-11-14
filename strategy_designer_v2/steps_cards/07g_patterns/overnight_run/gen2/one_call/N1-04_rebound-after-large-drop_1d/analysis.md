---
line: 7.g patterns
backtest: N1-04_rebound-after-large-drop_1d
idea tested: N1-04_rebound-after-large-drop
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3114 USD
---
## Findings
- **F1:** On down days the next-day rebound depends on where the bar closed within its range. Down days closing in the bottom 20% of the range were followed by a rise 57.6% of the time, with a mean of +0.49% (t 4.62, n 2163). Down days closing in the top 20% rose only 46.6% of the time, with a mean of -0.34% (t -0.88, n 116).
- **F2:** Within the forecast's own large drops (z ≤ -1.88) the same split holds. Drops that closed in the bottom 20% of the range rose next day 62.9% of the time, mean +1.01% (t 4.29, n 580). Drops that closed above mid-range rose only 47.3% of the time, mean -0.53% (t -0.78, n 55). The idea's drop size does not capture this.
- **F3:** The low-close rebound grows with range expansion against the prior 20 days.
- **F4:** Large drops rebound more in high-volatility regimes. In the top third of the coin's 120-day volatility rank they rose next day 65.1% of the time, mean +1.21% (t 2.27, n 146). In the bottom third they rose 56.5% of the time, with a negative mean of -0.40% (t -1.10, n 168).
- **F5:** The day after a Friday close is the strongest weekday.
- **F6:** The large-drop rebound has faded. Next-day hit after large drops was 62.5–67.0% in each year 2018–2023, but only 50.0% in 2024 (t 0.04, n 130) and 53.7% in 2025 (t 0.74, n 136).
- **F7:** Large up moves do not continue the next day.
- **F8:** The book loses on its worst days because it holds through continued crashes. On its worst 1% of days (n 173) the coin fell -9.7% on average. Mean net trade P&L is negative for every coin (-0.28% to -1.00%) despite trade hit rates of 46–53%.

## Ideas
- `N1-04_rebound-after-large-drop.g1_wide-range-weak-close-rebound` (from F1, F2, F3): When a coin's daily bar falls and closes in the bottom fifth of an unusually wide range (wide against its recent ranges), the next day's close is higher more often than on ordinary days.
- `N1-04_rebound-after-large-drop.g2_rebound-needs-high-volatility` (from F4, F6): A large one-day drop in a coin is followed by a higher next close more often when the coin's recent volatility is in the upper part of its own history.
- `N1-04_rebound-after-large-drop.g3_friday-to-saturday-weekend-drift` (from F5): A coin's close on the day after a Friday close (UTC) is higher than the Friday close more often than on other days of the week.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
