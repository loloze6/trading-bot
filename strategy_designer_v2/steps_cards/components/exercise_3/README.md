# components, exercise 3: the second pass (2026-11-17, written before the run)

**Purpose.** The card's validation, second pass: the step answers the open wishes left after exercises 1 and 2
(36 open wishes: night_run, night_013_run, volume_run), with the rules ruled on since (rule 1: the same quantity against another
base, and a mirror, are one measure; rule 2: a new setting must change the output on real data, checked on real data).

**Call.** `build_component.py --runs <all runs> --python VENV` (only open wishes are asked).

**Pre-registered outcomes.**
- **A.** Quality: every built component passes every check and the proof.
- **B.** Standardization: no two classes for one measure once the call ends (read the catalogue); variants of an
  existing measure come back as exists or as a setting on it (a mean of several bars' volume, the median of the bars
  before t: settings on `VolumeRatioComponent`); a past high or its break, one or two new measures.
- **C.** Rule 2 refuses a setting that changes nothing (if one is proposed), and the model then answers exists.
- **D.** Few cannot build, each naming what is missing.
- **E.** A defect of the step: fixed if general, written here.
- Unblocking: counted after the call (the ideas whose wishes are all answered built or exists); rerunning them waits
  for the ranking discussion (topic 3).

## Reading (15:50 to 16:45 UTC; 36 wishes, 37 calls with the one asked again, 4.44 USD, 53 minutes of calls)

**Answers: 13 built, 23 exists, 0 cannot build.** No wish is open in the 11 runs. Every build passed every check and
the proof (the new rule-2 check included).

| Built | What | Kind |
|---|---|---|
| `VolumeRatioComponent` + `short_period`, `centred`, `log`, `statistic` | a mean of several bars' volume; minus 1; its log; the median | settings (rule 1) |
| `DistanceFromHighComponent` + `source`, `exclude_current` | the high of the bars' highs; the high of the bars before t (a break of a past high) | settings |
| `CloseLocationInRangeComponent` + `reference` | the close's place from the high (1 minus it: a mirror no config step gives) | setting (rule 1, mirror) |
| `VolatilityScaledReturnComponent` + `lag` | the move of an earlier bar (a move held over the next bars) | setting |
| `HighProximityMomentumComponent` (+ `proximity`) | the month's rise weighted by nearness to the high | new (a product) |
| `VolumeWeightedScaledReturnComponent` | the move in usual moves times its volume ratio | new (a product) |
| `FallCloseLocationComponent` | a fall's size times how near its low it closed | new (a product) |
| `HighProximityVolatilityRatioComponent` | nearness to the high over the volatility's level | new |
| `VolatilityRankedFallComponent` | a fall ranked against the coin's volatility | new |
| `StallUnderHighCountComponent` | bars of the last 60 within 10 % under the 365-bar high | new |

**Against the outcomes.** A: met (every build passes every check). B: met (the variants came back as settings or exists:
the mean of several bars, the median, the break of a past high; the products as one class each). C: not met by
the model (it proposed no setting that changes nothing). D: no cannot build. E: one defect, fixed (below).

**Unblocking:** 46 of the 49 ideas refused for missing components in the 11 runs are unblocked now (night_013_run 14,
night_run 10, volume_run 8, night_rsi_run 7, night_012_run 4, night_006_run 2, night_005_run 1). Still blocked: the
bearish divergence (cannot build: on/off), and two whose refusal was written with today's catalogue. Rerunning them
waits for the ranking decision (topic 3).

**Defect of the step, fixed:** the harness's synthetic data was 400 bars; a component with a 425-bar warm-up could not
be ready in it (`StallUnderHighCountComponent` failed three times). The data now follows the warm-up (a test); the
wish was asked again and built.

**Findings for the operator (standardization):**
- `ConvexHighProximityComponent` (built in exercise 1, before rule 1 was ruled) is the distance below the high in
  another form ((1 / (1 + D))^power, D the distance): by rule 1, a setting on `DistanceFromHighComponent`. A merge to
  propose, as for the lower wick.
- `VolumeRatioComponent` has 6 settings now; `centred` (ratio minus 1) and `log` (its log) both centre it near 0. Each
  passed rule 2 (it changes the output), but two settings for one purpose is not simple. A rule to consider: one setting
  per purpose.

**Ruled and done (operator):** the merge (`ConvexHighProximityComponent` is now `DistanceFromHighComponent` with `form`
"proximity" and `power`) and the rule "one setting per purpose" (`VolumeRatioComponent`'s `centred` and `log` are now
`form`: "ratio", "centred" or "log"; in the card's rule 2 and the prompt). Proof: every standard check passes on both
classes; 336,271 values on 19 coins compared with the old classes, for every old setting: 0 differ; no plan used the old
names. The index lines keep the names and settings as they were answered (the record).

**The card's validation** (quality, standardization, unblocking, twice): exercises 1 and 3 on the fixed inputs (the
night runs' wishes): every build passes every check (quality, met twice); standardization met with two findings above;
unblocking: 46 of 49 ideas unblocked, of which one rerun so far (010-01, planned with its new component). Status:
met on quality and unblocking; standardization pending the two findings.
