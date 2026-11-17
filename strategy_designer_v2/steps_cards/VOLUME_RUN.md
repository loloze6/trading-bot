# Run brief: volume_run (2026-11-17, written before the run)

**Purpose.** 19 ideas were refused by step 3 overnight because no component measured a bar's volume against its own
recent average. `VolumeRatioComponent` now does (operator's go, 2026-11-17). Does it unblock them, and what do they
show once tested?

**Scope.**
- Run `volume_run`: each of the 19 ideas once through `run_idea` (steps 3 to 7), one after the other. No loop: the
  ideas the step 7 lines propose are written, not tested.
- The ideas, unchanged, from their night runs (16 need only a volume measure; 3, from brief 012, also need a wick or
  range component):
  - `02_ideation/night_012_run/ideas/012-01_liquidation-flush-rebound.md`
  - `02_ideation/night_012_run/ideas/012-02_volume-burst-fall-reversal.md`
  - `02_ideation/night_012_run/ideas/012-03_lower-wick-flush-recovery.md`
  - `02_ideation/night_012_run/ideas/012-04_flush-depth-retracement-size.md`
  - `02_ideation/night_013_run/ideas/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains.md`
  - `02_ideation/night_013_run/ideas/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.md`
  - `02_ideation/night_013_run/ideas/013-04_heavy-volume-below-high-breakout.md`
  - `02_ideation/night_013_run/ideas/013-06_breakout-volume-drives-continuation.md`
  - `02_ideation/night_013_run/ideas/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.md`
  - `02_ideation/night_013_run/ideas/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through.md`
  - `02_ideation/night_013_run/ideas/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains.md`
  - `02_ideation/night_run/ideas/003-01_thin-volume-rise-reverses.md`
  - `02_ideation/night_run/ideas/003-02_thin-volume-drop-rebounds.md`
  - `02_ideation/night_run/ideas/003-03_heavy-volume-rise-continues.md`
  - `02_ideation/night_run/ideas/003-04_heavy-volume-drop-continues.md`
  - `02_ideation/night_run/ideas/011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse.md`
  - `02_ideation/night_run/ideas/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds.md`
  - `02_ideation/night_run/ideas/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.md`
  - `02_ideation/night_run/ideas/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse.md`
- Default data (six coins, folds A to D, daily bars) unless an idea names other data. About 1 USD and 5 minutes an
  idea: about 19 USD, 1.5 hours. Nothing in a step changes during the run.

**Pre-registered outcomes.**
- **A.** Step 3 plans the 16 volume-only ideas with the new component: it unblocks them.
- **B.** Step 3 still refuses some of the 16: the component does not express what they need (the reading says what).
- **C.** The 3 brief-012 ideas stay missing-components (wick, range): expected.
- **D.** Among the tested ideas: how many confirmed, how many with a profitable book (none expected to pay, after
  briefs 003 and 011's short reversals).
- **E.** A chain defect: fixed if general and proven, or parked.

## Reading
(written after the run)

**volume_run (11:35 to 12:24 UTC; 19 ideas, 12.64 USD, 65 minutes of step time in all; no failure, no restart).**

| Outcome | Count | Ideas |
|---|---|---|
| **A.** planned with `VolumeRatioComponent` | 11 of the 16 volume-only ideas | 012-02, 013-06, 003-01, 003-02, 003-04 and six of the lines' ideas |
| **B.** still refused | 5 of 16 | a mean of several bars against a longer mean (2: `…g2_rising-volume-precedes-gains`, 013-04); the day's scaled move times its volume ratio, a product (2: 003-03, `…g1_high-volume-weekend-moves-reverse`); the volume against the median of the bars before it (1: `…g2_heavy-volume-fall-rebounds`) |
| **C.** the 3 brief-012 ideas still refused | 3 of 3 | they now ask only for a wick or range component: the volume part is covered |
| **D.** the 11 tested | 3 confirmed, 6 inconclusive, 1 mismatch, 1 not observable | **1 confirmed and profitable** |

- **Confirmed:** `…g2_heavy-volume-falls-reverse` (t +4.95; Sharpe 0.92, +0.37 over holding, Calmar 0.81; fails only the
  mean daily return, 0.042 % against 0.05 %); `…g1_short-high-break-on-volume` (t +4.17; fails the mean daily return and
  Calmar); `…e1_heavy-volume-rising-follow-through` (t +2.75), **profitable**: "while a coin's 30-day return is positive,
  the higher its daily volume against its 20-day average, the higher its return over the next 3 days"; Sharpe 0.91, +0.36
  over holding, 0.064 % a day, lowest Sharpe with one window left out 0.77, Calmar 0.80 (bar 0.75: a thin margin). The
  trend-following finding of night_013_run (rising month, long), with volume. In-sample, as the others.
- **Brief 003's own theory** (volume separates a reversal from a continuation), tested at last: 003-01 inconclusive
  (t -0.50), 003-02 not observable (5 events), 003-04 inconclusive (t -1.51), 003-03 still refused. Nothing shows.
- **E.** No chain defect. One more step 5 mismatch (`…g1_heavy-volume-precedes-gains`), as parked.
- **For the component card:** the 5 refusals are three kinds of wish: a parameter the component lacks (a mean of several
  bars), a combination the config cannot express (a product of two components), and a near variant (median, bars
  before t). They are its fixed inputs, with the components still wanted.
