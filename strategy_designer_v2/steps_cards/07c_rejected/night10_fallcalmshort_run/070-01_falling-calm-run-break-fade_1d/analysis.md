---
line: 7.c no effect
backtest: 070-01_falling-calm-run-break-fade_1d
idea tested: 070-01_falling-calm-run-break-fade
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3683 USD
---
## Findings
- **F1:** In the explore half (w1–w18), inside the falling calm profile, up days ending a down run of 2 or more days were followed by a next-day move 0.86 % below the coin's drift (t -2.04, 71 cases, plain t). That is the idea's direction. The step-5 verdict over all windows is a 0.03 % rise (t -0.18 in the short direction, 412 cases, 275 days), so the later windows must have gone the other way. The effect is not stable across periods.
- **F2:** The run's length does not grade the move. The Spearman correlation of run length with the next-day excess is -0.05 (p 0.71) over the 71 cases, and the in-profile means by run length are not monotone: 2 days -0.61 % (t -1.10, 33 cases), 3 days -0.45 % (23), 4 days -1.38 % (8), 5+ days -2.84 % (7). The few long runs are too thin to carry a grade.
- **F3:** How deep the run fell grades the move where its length does not. Among run-2+ cases the Spearman correlation of the run's cumulative return with the next-day excess is +0.27 (p 0.023), so a deeper decline goes with a larger next-day fall. Over all in-profile run-breaking up days (142), the deepest third saw -1.07 % next day (t -1.79), the middle third -0.18 % and the shallowest third +0.66 % (t 1.11).
- **F4:** A bounce that recovers little of the run's fall precedes the largest giveback. Over all in-profile run-breaking up days, split into thirds by the up day's return divided by the run's decline:
- **F5:** The fall is uneven across coins and years. By coin: BTC -1.52 % next day (t -2.15, 29 cases), XRP -0.99 % (t -1.58, 19), XMR +0.06 % (23). By year: 2018 -2.44 % (16 cases), 2019 -0.36 % (33), 2021 -0.59 % (19). By window, w12 alone holds 28 of the 71 cases at -0.37 %.
- **F6:** The profile itself has no drift to borrow. All in-profile days have a next-day excess of +0.01 % (t 0.04, 565 days). Days still inside a down run show nothing either: -0.04 % to -0.32 % after runs of 1 to 3 days, all |t| < 0.8. Whatever fall follows comes from the up day ending the run, not from the falling calm market as a whole.
- **F7:** The size is far below the cost of a trade. Over all windows the total move per case is -0.13 % against a 0.29 % round-trip cost (-0.4 times the cost). Even the explore-half -0.86 % rests on a t of about 2 that the later windows erase. Only a version with a much larger move per case, such as the deep-run or weak-bounce cases of F3 and F4 at -1 % to -2.4 %, could cover the cost.

## Ideas
- `070-01.c1_deep-run-bounce-fades` (from F3, F2, F1, F6): In a falling, calm market, the first up day after a run of consecutive down days is followed by a fall over the next day, and the deeper the run's total decline (its cumulative return from the run's start to its last down day), the larger the fall.
- `070-01.c2_weak-bounce-gives-back` (from F4, F3, F6, F7): In a falling, calm market, the first up day after a run of consecutive down days is followed by a fall over the next three days, and the smaller that up day's rise against the run's decline, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
