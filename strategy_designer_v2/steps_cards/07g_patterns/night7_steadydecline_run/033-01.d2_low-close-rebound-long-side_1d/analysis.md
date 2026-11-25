---
line: 7.g patterns
backtest: 033-01.d2_low-close-rebound-long-side_1d
idea tested: 033-01.d2_low-close-rebound-long-side
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4111 USD
---
## Findings
- **F1:** On low-half closes, the next-day excess return is predicted by how far the close sits below the day's high as a share of price, (high−close)/close: slope 0.170, t 3.79 (day-clustered), 3949 bars on 1025 days. The relative position in the range (nearness to the low, 0 to 1) is not significant on the same bars: slope 0.0126, t 1.21. On all bars, the distance measure still has t 3.67 (8688 bars, 1448 days). After the day's own return is removed, it keeps t 2.00, while nearness to the low drops to t −0.02.
- **F2:** The rebound after a low close depends on how agitated the coin is. Closes in the bottom fifth of the range are followed by an excess next-day return of −0.37 % (t −1.44, 392 bars) in the calmest volatility tercile, +0.58 % (t 2.06) in the middle tercile and +1.56 % (t 4.92, 396 bars) in the most agitated. The slope on nearness to the low is 0.0259 (t 3.55, 713 days) in the agitated tercile and −0.0043 (t −0.77) in the calm one.
- **F3:** The book earns only in agitated markets. Its gain per bar in a position is −0.002 % (t −0.12, 1029 bars) in the calm tercile, +0.062 % (t 2.90) in the middle one and +0.135 % (t 5.58, 945 bars) in the agitated one. Its overall total move per case is 0.37 %, against a trade cost of 0.19 %.
- **F4:** Wide days drive the low-close rebound. Bottom-fifth closes on a range wide relative to the coin's last 20 days are followed by +1.28 % (t 4.92, 508 bars). On narrow-range days the same closes are followed by −0.61 % (t −1.85, 312 bars). The product of nearness to the low and relative range predicts with t 3.19 (1340 days).
- **F5:** Bottom-fifth closes rebound mostly in a falling 60-day trend: +1.21 % (t 4.06, 398 bars) against +0.17 % (t 0.47, 199 bars) in a rising one. The graded slope is weaker: t 1.94 in falling markets and −0.08 in rising ones.
- **F6:** The day's own return carries much of the effect. The lowest quintile of daily returns is followed by +0.71 % (t 4.56, 1722 bars), and the slope of the next day on the day's return is −0.087 (t −2.94, 1437 days). Low-half closes on down days are followed by +0.42 %, against −0.03 % on the 633 low-half up days.
- **F7:** The effect does not last past a day. On the 2-day non-overlapping grid, the lowest close-location decile is followed by −0.02 % (t −0.05, 263 cases). On the 3-day grid the deciles alternate in sign with no order.
- **F8:** High closes are followed by a fall only in agitated markets. Top-fifth closes are followed by −0.87 % (t −3.93, 564 bars) in the agitated tercile and +0.18 % (t 0.77) in the calm one. However, within the high half, the slope on close location is not significant in any tercile (agitated t 1.12), so this side is not graded.
- **F9:** The Thursday excess of +0.47 % (t 3.19) and the Friday excess of +0.39 % (t 2.87) are not used here. They come from one of many angles looked at, with no reason behind them, so they are not taken as findings for ideas.

## Ideas
- `033-01.d2.g1_give-back-below-high-rebounds` (from F1, F4, F7): The further below its day's high a coin closes, measured as a share of its price, the larger its rise over the next day.
- `033-01.d2.g2_agitated-low-close-rebound` (from F2, F3, F7): In an agitated market, the nearer a coin's close sits to its day's low, the larger its rise over the next day.
- `033-01.d2.g3_falling-market-low-close-rebound` (from F5, F2): In a falling market, the nearer a coin's close sits to its day's low, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `033-01.d2.g4_agitated-one-day-fall-reverses` (from F6, F2): In an agitated market, the larger a coin's one-day fall, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
