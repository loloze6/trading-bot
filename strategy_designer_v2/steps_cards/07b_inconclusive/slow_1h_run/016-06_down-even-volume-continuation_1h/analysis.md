---
line: 7.b inconclusive
backtest: 016-06_down-even-volume-continuation_1h
idea tested: 016-06_down-even-volume-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3521 USD
---
## Findings
- **F1:** Among the 2,669 to 2,762 non-overlapping 72-hour grid cases where the coin had fallen over the past 3 days, the volume evenness measure ln(mean/median) has no link to the next 3 days' excess return, so the forecast's slope of 0.00134 (t 0.94) is effectively zero rather than a small effect on the predicted side. The concentration slope alone has t 0.05, and t −0.30 once the size of the fall is controlled. It also has no link at 24 hours (t 0.95) or 168 hours (t −0.10).
- **F2:** The forecast's small positive slope does not come from volume evenness. Its quintiles are not monotone (excess 72h returns of −0.50 %, +0.02 %, −0.24 %, +0.38 % and −0.43 % from most to least short), and its correlation with concentration is only 0.34. The concentration quintiles are flat too: −0.24 %, −0.45 %, −0.19 %, −0.41 % and −0.05 % from most even to most bursty.
- **F3:** No subset clearly shows the effect, so there is nowhere to narrow the idea to. By coin the slope's t ranges from −0.45 to 1.57, by year only 2023 passes 2 (t 2.26, 1 of 8 years), and by fall size every third has |t| < 1.5.
- **F4:** What does carry the next 3 days after a fall is the fall's size, which works against continuation. Over all 2,669 fallen cases the past 72h return has a slope of −0.10 on the next 72h excess return (t −3.53; t −8.21 at 24 hours, n 2,732; t −2.56 at 168 hours). The largest-fall quintile (mean −14.4 %) earns +0.60 % excess over the next 3 days, while the smallest-fall quintile (−0.6 %) earns −1.12 %. This rebound in the biggest falls drowns any evenness effect and explains why the short book lost money (Sharpe −1.31).
- **F5:** How smooth the fall was in price, rather than in volume, shows a borderline link to continuation at the plan's horizon. Path efficiency is |net 72h log move| / sum of |hourly log moves|. Controlling for the fall's size, higher efficiency is followed by lower 72h excess returns (t −2.06, n 2,669). The link is weaker at 24 hours (t −1.17) and 168 hours (t −0.85).

## Ideas
- `016-06_down-even-volume-continuation.b1_three-day-fall-size-rebound` (from F4): When a coin has fallen over the past 3 days, the larger its 3-day fall, the more it rises over the next 3 days.
- `016-06_down-even-volume-continuation.b2_smooth-falls-keep-falling` (from F5, F1): When a coin has fallen over the past 3 days, the more of its hourly price path went in the fall's direction (its 3-day net move as a share of its summed hourly moves), the more it keeps falling over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
