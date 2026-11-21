---
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2463 USD
---
## Findings
- **F1:** The book loses because it shorts coins that rise in most windows. Measured on the step 5 cases, the idea's unusual move is +1.99 % per case over 20 days, but the coin's normal drift in the short direction is -2.51 %. So the total move is -0.52 % per case, which is -2.7 times the 0.19 % cost of a round trip. On the book's own 239 short entries, the mean 20-day short gain is -1.32 % (t -0.86, 54 % winners).
- **F2:** The short entries pay only in falling years. In 2018 they earned +9.4 % per entry (t 2.45, 27 entries, coin 20-day drift -9.6 %), and in 2022 +7.0 % (t 2.32, 33 entries, drift -3.5 %). They lose in the rising years, for example 2024 at -6.4 % (t -2.13, drift +5.2 %) and 2023 at -5.2 % (t -1.51). The book's mean daily return is above 0 only in 2018 (+0.00043), 2022 (+0.00063) and 2025 (+0.00049).
- **F3:** The depth of the 30-day fall grades the outcome as the idea says. In the deepest quartile (mean 30-day return -50 %) the short gain is +3.8 % (t 1.74, 60 entries). In the shallowest quartile (-2.8 %) it is -5.6 % (t -1.48). Spearman rho between the 30-day return and the short gain is -0.13.
- **F4:** The size of the break day's own rise grades the reversal. In the largest one-day-rise quartile (mean +10.8 %) the short gain is +4.7 % (t 1.62, 56 entries). In the smallest quartile (+1.3 %) it is -7.9 % (t -2.08). Spearman rho is +0.15.
- **F5:** The level's strength (touch count times margin) carries no grading. Its quartiles give short gains of +1.1 %, -2.9 %, -5.2 % and +1.8 %, and Spearman rho is 0.04.
- **F6:** Shorts entered in calm coins lose. In the lowest 30-day volatility quartile (daily standard deviation 1.5 %) the short gain is -7.1 % (t -2.13, 56 entries). In the third quartile (4.4 %) it is +4.9 % (t 1.76). Spearman rho is +0.16.
- **F7:** Shorts entered at the top of the 60-day range lose. Where the break closes at 0.98 of that range, the short gain is -7.4 % (t -1.84, 56 entries), against +0.6 % to +1.7 % in the lower three quartiles.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails.d1_breakout-fails-in-downtrend` (from F1, F2, F3): When a coin closes above a price where it turned down several times in the past 90 days after its 30-day return was negative, it tends to fall back over the next 20 days, only while its 90-day return is also negative. The deeper that 30-day fall, the larger the decline.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails.d2_spike-break-after-falling-month` (from F1, F3, F4, F6): When a coin closes above a price where it turned down several times in the past 90 days after its 30-day return was negative, it tends to fall back over the next 20 days. The larger that day's own rise against the coin's 30-day daily volatility, and the deeper the 30-day fall, the larger the decline.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails.d3_oversized-bounce-in-falling-month` (from F3, F4, F5, F6): When a coin rises sharply in one day while its 30-day return is negative, it tends to fall back over the next 20 days. The larger that one-day rise against its 30-day daily volatility, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
