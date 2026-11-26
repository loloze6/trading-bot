---
line: 7.d confirmed, not profitable
backtest: 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d
idea tested: 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3577 USD
---
## Findings
- **F1:** The Calmar failed (0.291) because of two long falls: −69.5 % from w20 to w24 (491 days to the trough) and −58.4 % from w3 to w6 (439 days). Inside them the short side lost while the long side still earned: net summed gain −0.75 (342 bars) and −0.63 (259 bars) on shorts, against +0.27 (255 bars) and +0.12 (223 bars) on longs.
- **F2:** Over all bars the short side carries little and the long side carries the gain: mean gain per bar is +0.070 % on 1523 short bars against +0.311 % on 1361 long bars. Rebuilt with costs, the short-only book has Sharpe −0.13 and Calmar −0.15, while the long-only book has Sharpe 1.07, deepest fall −33.9 % and Calmar 1.04 (as tested: 0.63, −69.5 %, 0.30).
- **F3:** XMR's reversal is lopsided, measured on XMR's next-day return by decile of the day's return over its 30-day volatility, against the coin's mean of +0.136 %:
- **F4:** The gain grows with the size of the day's move, and small moves only pay fees:
- **F5:** The 5-day to 30-day volatility ratio grades the gain as the idea says: +0.001 % per bar in its lowest quintile and +0.578 % (t 3.05, n 436) in its highest. The rebound side is therefore graded by both of the idea's own measures.

## Ideas
- `031-03.g1.b1.d2.e2.g1.g2.d1_rebound-after-turbulent-falls` (from F1, F2, F3, F5): The larger XMR's one-day fall against its 30-day daily volatility, the more it rises back over the next day, and this rebound grows with how high its volatility over the past 5 days stands against its 30-day volatility.
- `031-03.g1.b1.d2.e2.g1.g2.d2_rebound-grows-with-fall` (from F2, F3, F4): The larger XMR's one-day fall measured in its 30-day daily volatility, the larger its rise over the next day, with the rebound growing faster than the fall, so that falls of more than a usual day carry most of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
