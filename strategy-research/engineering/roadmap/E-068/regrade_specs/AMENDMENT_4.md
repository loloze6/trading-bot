# Amendment 4: A8.5.1a with its episode gap in time (2 days). One bounded try.

Written and committed 2026-10-03, **before the method code below exists,
before its calibration, and before any run_065 effect size or verdict is
computed**. Operator decision of 2026-10-03. It amends amendment 3 section 4A
(method A) and section 6 (choosing the method). Everything else in amendment 3
stands: the verdict rule, the operator rules, and the gate.

## 1. The change: A8.5.1a's gap G is expressed in time, G = 2 days

New method id: `a851a_episode_timegap_v1`.

- **The rule:** `gap_bars = 2 days / bar step`. That is **2 bars on daily
  data** and 48 bars on hourly data, so hourly is unchanged.
- **Everything else in A8.5.1a stays as it is**, and the function
  `tools/episode_significance.py::compute_a851a_significance` is unchanged:
  - the 8-episode floor;
  - resampling whole episodes with replacement (2,000 resamples);
  - the pooled rank IC statistic among the event bars;
  - the 50% density fallback;
  - eras close episodes and are otherwise reporting only (the bootstrap pools
    across eras);
  - seed 20261003.
- Feeding is as in amendment 3, section 4A, except for the gap. The claimed
  direction is IC > 0 for both sides. One-sided p is `p2 / 2` if the IC points
  the claimed way, else `1 - p2 / 2`.

## 2. Why this is the method's own intent, not a new invention

- A8.5.1a's pre-registration defines the gap as a duration:
  "`G` configurable, `campaign_config.yaml: episode_significance.gap_bars`,
  **default 48 bars @ 1h ≈ 2 days**" (`engineering/improvements/done/
  design_and_docs/AMENDMENTS_01-06.md`, A8.5.1a-spec, rule 1). The code
  comment says the same ("48 bars @ 1h ~= 2 days").
- The method was built and tuned on hourly data. Its intent is "events closer
  than about 2 days belong to one episode".
- The units finding (`REGRADE_run065.md`, method A, "Why no answer"): passing
  the bar count unchanged to daily data turns 2 days into **48 days**.
  run_065's breakout days then merge into 1-5 episodes, below the floor of 8,
  and the method declines in 100% of the gate's simulations.
- Expressing the gap in time restores the stated 2 days on daily data. No
  other rule changes.

## 3. Calibration gate: unchanged

The gate is exactly amendment 3, section 5:
- no-edge prices, iid and switching models;
- 6 windows x 120 daily bars, plus 30 warm-up bars;
- both sides x both directions = 8 rows, horizons 1-5;
- 400 simulations per cell, with A8.5.1a's own 2,000 resamples per simulation
  (the same number the gate already used for method A);
- **pass:** no answer in at most 5% of simulations, and the share of
  p < 0.05 within [0.025, 0.075] at every horizon, in all 8 rows.

**One signal per gate run.** run_065 trades two signals:
- `DonchianBreakoutComponent(period=20)`: variants `base` and
  `donchian_solusdt_crossasset`;
- `DonchianBreakoutComponent(period=14)`: variant `donchian_period_14_reactive`.

The tool's lock (D-064) lets a verdict through only for the signal a gate was
run on. So the identical gate is run once for period 20 and once for period
14. This is not a change to the gate; it is the same gate applied to each
signal that traded.

## 4. Decision rule: one bounded try

- **If the gate passes for a signal:** write its calibration file and grade the
  run_065 variants that trade that signal. Use the pre-registered spec as
  fixed:
  - the tests `upper_breakout` and `lower_breakout`;
  - the claim is supported only if both are supported;
  - the floor is 100 events and 4 windows;
  - the window-sign rule is the same sign in at least 4 of 6 windows (here,
    the per-window IC among the events);
  - refuted only when the wrong-way effect is itself significant;
  - across variants, refuted dominates.
- **If the gate fails for a signal:** that signal's variants are not graded.
  No other method is tried. The tool keeps reporting effect sizes only.
- **Either way, after this try the method search stops** (operator).

**N tests run** counts each of the 2 tests on each variant actually graded.

**What a verdict would mean.** A verdict under this method is about the pooled
rank IC between the forecast and the forward return **among breakout days**
("does a stronger breakout give a larger follow-through?"). It is not about the
spec's mean difference against other days. The report must say this next to
every verdict (amendment 3, section 4A).
