---
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3508 USD
---
## Findings
- **F1:** The tested effect points the way the idea predicts but is too small and too uneven to clear the bar. Over 413 cases the mean short-direction unusual 20-day move is +1.99 % (t 1.86, strength 0.076), the median is +4.2 % and 60 % of cases move the predicted way. The spread is wide (usual 20-day move 21 %), so 413 cases cannot pin a 2 % mean down.
- **F2:** The effect is mixed across years and rests on one of them. 2018 alone gives +10.5 % per case (t 3.83, 63 cases), and 2022 gives +5.9 % (t 2.58). 2020 (−4.5 %), 2023 (−2.4 %) and 2024 (−4.9 %, t −1.84) go the other way. On the 10-day grid, leaving out any single year moves t only between 0.75 and 1.55.
- **F3:** Coins split the effect. BTC (+3.5 %, t 1.76, 62 cases) and ZEC (+5.5 %, t 1.93, 71 cases) carry it. ETH, XMR and XRP show +0.3 % to +0.7 % with t below 0.3. With about 62 to 73 cases per coin and no coin above t 2, more coins would add cases where the shortage is.
- **F4:** The grading the idea claims is barely visible.
- **F5:** The test's horizon is not misplaced. Read on its own grid, the 5-day horizon gives +0.6 % (t 1.64, 804 cases) and the 10-day +0.8 % (t 1.30, 612 cases), no clearer than 20 days. The 40-day horizon fades to +0.3 % (t 0.17, 354 cases).
- **F6:** The book cannot pay even though the unusual move is 10.3 times the 0.19 % cost of a trade. The coins' normal drift is −2.51 % per 20 days in the short direction, which leaves a total move of −0.52 % per case (−2.7 times the cost). The book's Sharpe is −0.37.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails.b1_failed-breakout-after-falling-month` (from F1, F2, F3, F5): When a coin closes above a price where it turned down several times in the past 90 days after its 30-day return was negative, it tends to fall back over the next 20 days. The deeper that 30-day fall, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
