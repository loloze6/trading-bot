---
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
idea tested: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3441 USD
---
## Findings
- **F1:** The Calmar failure comes from one long fall: the book's daily chain reached its deepest fall of −55.6 % by w10 against a yearly return of only 23.2 % over 7.9 years, and the fall built steadily from −22.8 % in w1 to −54.0 % in w8 and −53.2 % in w9, while its worst fall inside any single window was only −8.8 % to −27.5 %.
- **F2:** In w1–w9 the momentum effect was absent on both sides: longs earned −0.024 % per coin-bar (2915 bars) and shorts −0.015 % (3574 bars), against +0.291 % for longs in w10–w24 (5626 bars); summed per window, longs gave about −0.12 and shorts about −0.09 of book value over w1–w9.
- **F3:** The short side is a net drain over the whole record: it lost in 16 of 24 windows (for example −0.138 in w5 and −0.107 in w3), and it gained clearly in only two (+0.218 in w2, +0.284 in w14).
- **F4:** Shorts lose most when the coin is already deep below its 60-day high: in the deepest fifth (43 % to 70 % below it) shorts earned −0.243 % per bar (t −2.44, 868 bars); in the fifth 15 % to 24 % below it they earned +0.145 %. Likewise shorts after a 90-day fall of 40 % to 82 % earned −0.186 % (t −1.08, 427 bars).
- **F5:** Longs gain in step with closeness to the 60-day high: +0.512 % per bar within 1.5 % of it (t 2.92, 909 bars), +0.350 % at 1.5 % to 5 % below it (t 2.94), down to +0.026 % and +0.101 % in the two deepest fifths.
- **F6:** The book's gain fades as the coin's 20-day volatility rises: mean bar gain was +0.195 %, +0.203 % and +0.155 % in the three calmest fifths, against +0.014 % and +0.061 % in the two most volatile. Shorts in the most volatile fifth earned −0.087 % (t −1.45).
- **F7:** Cost does not cause the failure: the total move per case is +0.56 % over 5 days, 2.9 times the 0.19 % cost of a trade, and the book's Sharpe (0.75) beats holding the coins by 0.19. The problem is when the book is short or exposed, not the size of the edge.

## Ideas
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high` (from F1, F3, F4, F5): The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days.
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d2_deep-drawdown-rebounds` (from F3, F4): The further a coin's close stands below its highest close of the past 60 days, the larger its rise over the next 5 days.
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d3_momentum-stronger-when-calm` (from F2, F6): The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the lower the coin's 20-day volatility of daily returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
