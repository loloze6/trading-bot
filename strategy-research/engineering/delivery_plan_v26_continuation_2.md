# Delivery plan v26, continuation 2: what E-068 delivered (record)

**Status:** record of delivered work, written 2026-10-06 for the operator. It follows
`delivery_plan_v26_continuation.md` (closed by PR #313). Unlike that file, this one is not a
plan: it explains, in plain words, what was built after the closure, why, and what is still
open. Source of truth for the details: `roadmap/E-068/DESIGN_PROPOSAL.md`,
`roadmap/E-068/VALIDATION_RUN.md`, `roadmap/E-068/REGRADE_run065.md`, and `DECISION_LOG.md`
rows D-062..D-076.

## The goal in one sentence

Every run should **test its own idea, keep what it learned, and propose a sensible next
test**, instead of only asking "did the strategy make money?".

Why: run_065's idea was "after a breakout, the price keeps going for 1-5 days". The grid
tested a generic correlation over all days and said "refuted". Nobody ever looked at the
days after a breakout. The readers then proposed changes to settings that do not exist.

The rest of this file follows one run through the pipeline.

---

## 1. Step 1a writes the idea, now with a claim card

Step 1a still writes the idea. It now also fills in a form that says how to test the
claim, built from four slots:

```yaml
claim:
  statement: "The signal's rank predicts the next 1-4 hours' returns."
  kind: direction_forecast
  tests:
    - selector:  all bars          # which bars
      outcome:   fwd_return 1-4h   # what happens next
      baseline:  other bars        # compared with what
      statistic: rank_ic           # measured how
```

- **Code checks the form before anything is spent.** If it is malformed, 1a gets one
  retry. (PR #319)
- **When the idea is a strategy block, at least one test must measure that block's own
  output signal** (the `forecast` column, or `regime` for a regime block). A test that reads
  only the price is "blind": run_070 selected "bars where the close is in the top 10% of the
  last 100 closes", which depends on the market, not on the strategy, so the base
  (period 1) and its variant (period 250) gave identical numbers. A blind claim gets one
  revision. A claim that only points at the standard criteria is not enough either.
  (PRs #327, #334)
- **Two warnings, never stops:** not enough separate events for the horizon ("at most 40
  possible, your floor is 100"); 1a's test does not match the block 1b built.
- **"This can't be tested" is allowed.** 1a writes `tests: none` and names the missing piece.
  It must never approximate. The missing piece is recorded as a request (section 7).
- **A new building block, `past_return`,** so "after a big 1-hour move" can be expressed.
  It reads past bars only.

## 2. Step 1b builds the strategy, and parks less

- **Nearest build (PR #333, flag `nearest_build`).** Before, 1b parked whenever one
  ingredient was missing. Now it builds the closest version it can and lists every
  difference. Example (run_071): candle body became the 1-bar move; "close near the bar's
  high" became position in the last 20 bars' range; "hold for 4 bars" was not expressible.
  The run continues, and the finding and the readers see "this run tested an approximation:
  ..." first. 1b parks only if the core of the idea cannot be built, and must say why.
- **It must show what it tried (PR #324).** If 1b declares a component missing, it must list
  the combinations it tried, transforms included, or it gets one retry. (It once parked over
  "ATR versus standard deviation", when the catalogue's z-score form would do.)
- **Patch ideas (PR #332).** A reader can propose changing one setting of the strategy it
  read, e.g. "change `shock_reversal`'s `period` from 1 to 2". Decide-next turns that into
  the next run: the same strategy with only that setting changed (run_073). Step 1b only
  copies the config, and code now writes that run's manifest itself; the AI's rewording of
  one phrase used to trip a word-for-word guard and kill the run (run_072).

## 3. After the backtest: the claim is measured (a number, not a verdict)

- **The number, automatically (PR #320).** Code runs the claim's tests on the bars the
  backtest saved. Example (run_074): rank correlation +0.054, positive in 6 of 6 windows.
  Labelled **"measured, not proven"**. It never stops a run and never changes the idea's
  status.
- **A number is not a verdict.** A verdict would say "this is real, not luck". That needs
  to know how often pure luck produces such a number, estimated by running the test on fake
  prices with no edge (the "calibration gate"). It worked for one signal on daily data only;
  the other methods flattered or refused, mostly because there was too little independent
  data. run_065's claim came out "inconclusive" (`REGRADE_run065.md`).
- **Decision (operator, 2026-10-06): the running pipeline has no verdict.** It shows the
  number only. The verdict engine in `tools/claim_tests.py` and its gate are kept as code but
  **parked** (Linear CUL-394), and no run, reader or document of the running pipeline speaks
  of a verdict. The real pass/fail is unchanged: profit bars, the count of all attempts, and
  the holdout.

## 4. The result is stored as a finding (PR #328)

- Each run's memory entry holds its claim, its tests, the numbers per variant, whether the
  tests could see the block, and any approximation 1b made.
- A short **"what we measured so far"** list is given to the readers: earlier runs' claims
  and their numbers. Example rows:
  - run_070: "after a big 1h move, price reverses", measured on BTC as the opposite
    (+18 bp continuation);
  - run_074: "the signal's rank predicts the next 1-4h", +0.054, 6 of 6 windows.
- Why: readers build on what is known and do not re-propose a test already done.
- **It never bans an idea (D-055):** a past result never forbids trying a similar idea; at
  most a warning says "this exact test was already measured in run_070".

## 5. The readers explain and propose (PRs #309, #310, #329, #330, #334)

- **Before:** they were fed another run's file, never saw the real settings, and invented
  names like `stop_loss_pct` on components that do not have it.
- **Now they see:** the idea, the real config, the component catalogue, each variant's exact
  changes, and the claim's measured numbers.
- **They write:** an explanation of the result; 0-2 **side findings**, each a full claim with
  its own test (one became run_074); an optional **patch**, written precisely as
  `{component_id: shock_reversal, field: params.period, before: 1, after: 2}` and checked by
  code when written (the component exists, the setting exists, its current value really is
  1); otherwise refused. They never judge the claim.
- **Skip rules save money.** The regime reader is skipped when the regime detector is
  "ungated": it has no rules and no components and `default_regime: unknown`, so every bar
  is labelled `unknown` and the signal applies all the time (the manifest marks
  `/regime_detector` as scaffolding). That reader then has nothing to analyse; on runs 065,
  066 and 070 it kept proposing "fix the detector". Verified on run_073, where the skip and
  its rule are recorded. The component reader is skipped when there is one component.
  Reader cost fell from $0.72 to $0.39 per run.

## 6. Running campaigns safely

- **Approval mode (PR #326).** Every next idea the system picks waits for the operator
  (`run_campaign.py --approve <id>`).
- **Retries keep the answer (PR #323).** A "fix the format" retry gets the AI's own first
  answer back with "change only the layout". Before, a retry turned two good ideas into
  "exhausted".
- **A brief closes only after two "exhausted" answers in a row (PR #324).** One answer is
  unreliable: 4 of 6 calls on the same inputs still had ideas.
- **Smaller:** the cost log keeps every retry; operator holds really hold; at most 3
  component quarantines per brief; token budget 1.8M; `--relaunch <id>` restarts a failed
  entry fresh; tests run on 4 workers locally and CI runs the fast suite.

## 7. Where requests are recorded

Missing pieces are written to to-do files. Nothing waits on them: when several ideas ask for
the same piece, someone builds it and later ideas can use it.

| File | What lands there | Written by |
|---|---|---|
| `campaign_record/component_requests.yaml` | missing strategy components (e.g. run_071's candle shape, CUL-407), and the differences 1b recorded when it built an approximation | step 1b |
| `campaign_record/test_requests.yaml` | missing test building blocks (`tests: none` + what is missing) | step 1a, readers' side findings |
| `campaign_record/data_requests.yaml` | data a reader said an idea needs | readers (`requires_feed`) |
| `campaign_record/feed_wishlist.yaml` | named data feeds wanted but not built | campaign review, by hand |
| `config/detector_wishlist.yaml` | regime-detector ideas | campaign review, by hand |

## 8. What the real runs showed

| Run | What it proved |
|---|---|
| run_070 | the whole chain works end to end, but the test could not see the block |
| run_071 | 1b builds an approximation instead of parking |
| run_073 | readers v3 work: two skips, valid side findings |
| run_074 | a reader's idea becomes a full run. First steady signal (+0.054, 6/6 windows), but the trade still lost money: real-looking, too small to trade alone at these costs |

## 9. Decided next (operator, 2026-10-06), to implement

1. **No verdict in the running pipeline** (section 3). Remove verdict wording from the
   pipeline's documents and reader instructions; mark the offline verdict tool as parked
   (CUL-394); rename the run file `claim_status.yaml` to `claim_measurement.yaml`, since it
   only says whether the claim was measured.
2. **One kind of reader proposal.** A patch is a claim plus a config change: "period 1 → 2"
   only makes sense with a reason ("a 2-bar move is less noisy, so the signal's rank should
   line up better with the next 1-4 hours"), and that reason is a claim with a test. A
   patch-only proposal produces no finding (run_073), duplicates what step 2's variants
   already test, and invites tuning without a reason. So: readers propose side findings
   only, each a claim with a test, optionally carrying a config change to test it with; the
   stand-alone patch is removed.
3. **CUL-412:** a reader's side finding carries the source run's config, and 1b starts from
   it (any change recorded as a difference). On run_074, 1b built a different signal from
   the one the claim was about.
4. **CUL-413:** label every correlation in the reader digest ("Pearson, all bars" vs "rank
   IC, the claim test").
5. **`--relaunch` follow-ups:** refuse an entry whose old run already queued extra cards, and
   a legacy split child; write the "orphaned" note only after the queue save succeeds.
6. **Requests in one place:** move `config/detector_wishlist.yaml` into `campaign_record/`,
   and add a "Requests" section to `campaign_summary.md` (open rows per file, newest few).

## 10. Parked

- CUL-394: automatic verdicts (calibration store, hourly gate, more recomputable signals).
- CUL-397: an AI review of test-versus-claim (it failed its own offline test).
- CUL-387: run_066's Keltner signal cannot be rebuilt exactly.
- CUL-391: a significance method for regime claims.
- E-069: one model per AI step.
- E-071: combining validated blocks into one strategy (run_074's "real but too small"
  result points there).
- E-066: more coins and longer periods.

## PRs, for reference

| PR | What |
|---|---|
| #314 | review fixes: reader instructions, test rule |
| #315, #316, #318 | claim test engine and calibration gate; run_065 re-graded offline (inconclusive) |
| #317, #311 | E-068 design proposal and its update |
| #319 | slice 2: step 1a writes the claim card |
| #320 | slice 3: the claim is measured after the backtests |
| #321, #323 | retry bugs; parser, retries keep the answer, cost log, holds |
| #322, #325, #331 | validation reports |
| #324 | two "exhausted" answers to close a brief; 1b must show what it tried |
| #326 | approval mode, quarantine cap, reader name warnings, 1.8M budget |
| #327 | claims must be able to see the block; `past_return` |
| #328 | slice 4: findings |
| #329 | slice 5: readers v3, skip rules |
| #330 | readers continue when an input file cannot be written |
| #332 | patch ideas: code writes the manifest; their claims are checked |
| #333 | nearest build |
| #334 | block claims need a block test; readers see variant patches; `--relaunch` |
