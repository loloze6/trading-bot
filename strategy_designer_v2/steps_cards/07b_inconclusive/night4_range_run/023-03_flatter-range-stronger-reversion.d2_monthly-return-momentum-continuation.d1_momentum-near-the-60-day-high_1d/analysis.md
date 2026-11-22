---
line: 7.b inconclusive
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
idea tested: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3111 USD
---
## Findings
- **F1:** On the plan's 5-day grid the forecast's slope is on the predicted side but small and noisy (slope 0.000273, t 1.30, 3,419 cases). The same forecast is clear over shorter horizons (t 2.30 at 1 day on 17,380 cases, t 2.51 at 3 days on 5,723) and fades over longer ones (t 0.46 at 10 days, t −0.11 at 20 days), so the plan read the idea past the horizon where it shows.
- **F2:** Over 3 days, the idea's own product of 30-day return and nearness to the 60-day high is clearer than at 5 days. The raw product has t 3.42 (2,843 cases) against t 1.47 at 5 days (1,691 cases), and the recorded raw component has t 3.26 against t 1.80. The standardisation over the past 60 values weakens it (post-pipeline t 2.51 at 3 days, 1.30 at 5 days; correlation of post-pipeline with raw 0.30).
- **F3:** The effect is mixed across years and coins, which keeps a pooled 5-day t short of the bar. By year the 5-day slopes run from t −2.07 in 2022 and −1.51 in 2018 to +1.79 in 2020 and +1.67 in 2025. By coin they range from t +1.44 (ETH) and +1.34 (XRP) to −0.77 (LTC), with no coin above t 2 on about 570 cases each.
- **F4:** The gain sits on the long side near the high. Five-day excess returns in the forecast's direction are +1.35 % (t 2.78, 516 cases) after a 30-day rise in the third of cases nearest the 60-day high, and −0.10 % (t −0.16, 370 cases) after a rise further from it. Within the forecast's short side the slope is the wrong way (t −1.44, 1,703 cases), against t +0.44 on the long side.
- **F5:** The 30-day return alone already predicts the 5-day excess move (slope 0.0163, t 2.76, 2,555 cases). Its slope is positive only in the nearest-to-high third (t 1.38) and zero in the middle and far thirds (t −0.12, −0.08), so the nearness grading points the right way. The idea's per-case size is 0.087 of a usual move, with a total move of 1.13 % per case, 5.8 times the 0.19 % cost of a trade.

## Ideas
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins` (from F1, F3, F5): The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days.
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days` (from F1, F2, F4): The larger a coin's 30-day return, the larger its rise over the next 3 days, the more so the closer the coin's close stands to its highest close of the past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
