---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d
idea tested: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3490 USD
---
## Findings
- **F1:** How near XMR closes to the day's low predicts the next day better than the day's return does. On all 2,897 bars, a regression of the next-day excess return on (0.5 minus the close's place in the day's range) has t 5.10. The lowest fifth of closes (n 577) is followed by +0.85 % (t 4.19), the highest fifth (n 581) by −0.60 % (t −3.31). Welch's t for lowest minus highest is 5.33, a gap of +1.45 %. On its own the lowest fifth's move is 0.18 of the usual daily move of 4.65 %, against 0.13 for the tested idea.
- **F2:** Once the day's return in usual moves (z) is in the regression, what carries the effect is the distance of the close below the day's high, in 30-day daily volatilities. That distance has t 3.31 (slope 0.0051, n 2,417), while z drops to t −0.40 and the distance above the low has t −1.65. So the tested fall-in-volatility signal mostly stands in for "closed far below the high."
- **F3:** The book cannot short, and its flat days hold a pattern it does not use. On up days closing in the top fifth of their range (n 568), the next day is −0.58 % (t −3.15). On all forecast-≤0 days in that fifth (n 565), it is −0.58 % (t −3.17). Up days closing in the bottom fifth (n 115) are followed by +1.10 % (t 1.94). For a short, the −0.58 % move minus the +0.11 % normal drift still exceeds the 0.31 % cost of a trade.
- **F4:** The close-location effect lasts one day only. On a non-overlapping grid, its t is 5.10 at one day, 1.91 at two days (n 1,202) and −0.45 at three days (n 786). It is also uneven over time: with z in the regression, its yearly t falls from 1.22 in 2018 to −1.03 in 2025, and by half the early windows give t 0.04 and the late ones t 1.82. So it is mostly shared with z rather than separate from it.
- **F5:** On down days, the rebound is concentrated in some conditions. It is +0.85 % (t 2.16) in the top volatility quartile against +0.03 % (t 0.12) in the lowest. It is +0.77 % (t 2.79) in the top volume tercile against +0.18 % in the lowest. It also appears at both ends of the 60-day return: +0.92 % (t 2.15) after the largest falls and +0.76 % (t 2.37) after the largest rises. With this many angles examined, none of these stands out enough to count alone.

## Ideas
- `031-03.g1.b1.d2.e2.g1.d1.g1_xmr-close-below-high-rebound` (from F1, F2, F4): The farther XMR's daily close sits below that day's high, measured in its 30-day daily volatility, the more its price rises over the next day.
- `031-03.g1.b1.d2.e2.g1.d1.g2_xmr-strong-close-next-day-fade` (from F1, F3): The closer an up day in XMR closes to its high, the more its price falls over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
