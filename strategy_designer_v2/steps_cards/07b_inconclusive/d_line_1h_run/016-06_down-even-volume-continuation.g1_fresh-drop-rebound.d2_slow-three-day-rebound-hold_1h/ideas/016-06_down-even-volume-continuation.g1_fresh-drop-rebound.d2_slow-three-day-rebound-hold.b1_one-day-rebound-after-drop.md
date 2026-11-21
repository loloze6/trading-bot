---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.b inconclusive
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 1 day.
Consequence: Buy a fresh drop inside a 3-day decline for a one-day rebound, sized by the depth of that drop, rather than holding it for three days, when the extra days add nothing.
Why:
- F1: The tested idea's rebound arrives almost entirely in the first day. On the plan's 72-bar grid in `mean_reversion` (2762 cases), the forecast's slope on the excess return is t 4.10 over hours 0–24, with t 2.26 for hours 0–6 and t 3.62 for hours 6–24. Over hours 24–72 it is only t 0.37 (slope 0.000060 against 0.000510 for 0–24). So the main 72-bar t of 2.75 is carried by day one, and the "builds across 3 days" check fails.
- F2: Days two and three add nothing consistent. The slope is t −1.28 over hours 24–48 and t 1.82 over hours 48–72, and the supporting 24–72 slope was 6.0e-05, short of half the main slope.
- F3: Measured at the 1-day horizon on a non-overlapping 24-bar grid in `mean_reversion` (8482 cases), the forecast predicts the next day's excess return with t 4.95. The effect is graded: the mean next-day excess rises steadily by forecast bucket, from −0.0030 at forecast 0 and −0.0028 at 0–5, through −0.0021 at 5–10 and +0.0008 at 10–15, to +0.0031 at 15–20 and +0.0039 at the +20 cap.
- F4: The 1-day effect is broad but weakening. Five of six coins have a positive 24-bar slope with t between 1.78 and 3.61 (LTC t 0.01), and all eight years are positive. It is strongest in 2018 (t 4.54) and 2021 (t 2.30), and only t 0.54 to 1.14 in 2022–2025.
- F5: On the raw prices, the last day's fall predicts the next day's excess return more strongly when the coin also fell over 3 days. Inside a 3-day fall the slope is 0.226 (t 15.0, 8272 cases), against 0.131 (t 3.77, 8542 cases) after a 3-day rise. The deepest quintile of 1-day falls (mean −8.4%) is followed by +0.74% excess over the next day, against −0.51% after the top quintile (mean +3.7%).
- F6: The book cannot keep this edge because it re-sizes hour by hour. Its summed bar-by-bar gross gain is +1.80, set against 58,401 trades (3.3 per day), a summed turnover of 19,201 and a mean daily book return of −0.0011.
