---
line: 7.d confirmed, not profitable
backtest: 032-02.b2.g2_volatile-close-near-low-rebound_1d
idea tested: 032-02.b2.g2_volatile-close-near-low-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4027 USD
---
## Findings
- **F1:** The deepest falls happen in rising months. On the book's worst 5 % of days, held bars with a positive 30-day return made 303 of 399 cases, summing −12.70 against −4.21 for those with a negative 30-day return, and the windows with the deepest book falls (w16 −30.9 %, w17 −29.7 %) are ones where the coins rose overall (summed returns +0.54 and +0.51).
- **F2:** Inside the regime, the idea's effect sits in coins already falling over 30 days. Among regime bars in the lowest quarter of 30-day return, closes near the low were followed by +1.83 % excess next day (t 3.88, n 255), against −1.18 % (t −2.28, n 212) for mid closes and −0.60 % (n 197) near the high. That lowest quarter alone averages about +0.15 %, so the falling-month condition is not an effect of its own.
- **F3:** In the highest quarter of 30-day return, closes near the low earned −0.12 % excess (n 174) while being held at the largest allocation (0.64), so the rising-month part of the book carries risk without gain.
- **F4:** The book loses on its mid-range closes, which the long-only forecast still holds at about 0.4 of the book. Regime bars with an up day and a mid close lost −0.75 % excess next day (t −2.99, n 377), and in the lowest 30-day quarter mid closes lost −1.18 %. Only the near-low third carries the rise (+0.63 %, t 2.63, n 645, on down days).
- **F5:** The effect grows with how wide the 30-day ranges are against the 90-day ones. In the widest third of the range ratio, near-low closes gained +1.40 % excess (t 2.26, n 134) against −1.41 % for mid closes, while the widest third alone averages about −0.17 %, and the mildest third shows +0.80 % near the low (t 1.52).
- **F6:** A down day explains much of the effect on its own, so it is not a repair. Regime bars after a down day earn +0.49 % excess (t 2.67, n 1291) against +0.63 % when the close is also near the low. Bars after a deep down day earn about the same with near-low closes (+1.11 %, n 318) as with mid closes (+1.06 %).
- **F7:** The size is thin against cost. The total move is +0.35 % per case against a 0.19 % trade cost (unusual move t 1.43), so the repair must come from a stronger case of the situation, as in F2 and F5, rather than from more trading.

## Ideas
- `032-02.b2.g2.d1_near-low-rebound-in-falling-months` (from F1, F2, F3, F7): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days and its 30-day return is negative, the lower its close sits within the day's high-low range, the larger its rise over the next 1 day, and the more so the deeper its 30-day fall.
- `032-02.b2.g2.d2_below-midrange-close-rebound` (from F4, F7): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days, the further its close sits below the middle of the day's high-low range, the larger its rise over the next 1 day.
- `032-02.b2.g2.d3_rebound-scaled-by-range-widening` (from F5, F7): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days, the lower its close sits within the day's high-low range, the larger its rise over the next 1 day, and the wider the past 30 days' ranges are against the past 90 days', the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
