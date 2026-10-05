# E-068 validation on real runs (2026-10-04)

**Goal:** one real run with `orchestrator.claim_tests.enabled` on, on top of the C4 flag set
(branch `c4/flag-set`, merged with master at `b90b4c43`, then `452ef9fd` after PR #321).
It had to show three things on real AI output:
- **(a)** step 1a writes a valid claim card;
- **(b)** the claim is measured after the backtests (`claim_test.yaml`, `claim_status.yaml`);
- **(c)** the readers, with their new inputs, stop inventing components and settings.

## Update: the final run (run_070 resumed after PR #324, 2026-10-04)

**All three goals are now shown on real output, each with a caveat.** run_070 was unparked
after PRs #323 and #324 merged (c4/flag-set at `01013c5e`), relaunched with `--once`, and
ended `completed_refuted`.
- Every call took 1 turn; `flags.holdout_reserved: false`; no sealed path in any run file.
- Spend: $1.72 logged for run_070. Since CUL-396 the log includes the retries; the total also
  covers the two earlier parked 1b calls.
- Weighted token budget: 1,212,255 of 1,500,000 used (80.8%; 19% headroom).
- Trial rows `run_070:base`, `:shock_lookback_250`, `:sol_generalization`, `:uni_defi`;
  `campaign_memory.yaml` has run_070; `decision_record.yaml` exists.

**(a) Claim card: shown** (quoted below). It was valid first time with no power warning. But
its tests read the closing price LEVEL, not the 1h move the claim states (CUL-397).
- The 1a/1b match check flagged this on its first real case: `claim_match.yaml` reads
  `status: mismatch`, "the test does not read this block's output".

**Step 1b after O-21 (PR #324): passed with no retry.**
- It built `PriceEvolutionComponent(period=1)` + `zscore` + `negate` + `scale(10)`, the form the
  operator accepted.
- It wrote a `DEVIATION:` entry, "normalised by the std of 1-bar returns (zscore), not ATR(20)".

**Step 2: two retries, both kept the content.**
1. The CUL-379 format retry. The first answer wrote only `expanded_hypothesis_card.yaml`. The
   retry got its first answer back (input 42,213 vs 39,155 cached tokens) and returned all three
   files in 39 s.
   - It was logged as `innovation_expansion_attempt_0_retry`, so the first call's cost was kept
     (CUL-396).
2. The existing variant-shape retry (`V1_base` must be `base`).

**(b) Measured after the backtests: shown.**
- `claim_status: measured`: 8 tests (2 tests x 4 variants), 0 not measured, labelled "measured,
  not proven", no p-value.
- Effect per horizon (mean forward return on selected bars minus all other bars, in basis
  points; "sign" = windows with the claimed sign / windows with a value):

| Variant (coin) | Test (claimed direction) | 1h | 2h | 4h | 6h | 12h |
|---|---|---|---|---|---|---|
| base (BTC) | top-10% close (lower) | +1.5 (0/6) | +2.6 (1/6) | +5.4 (1/6) | +8.2 (1/6) | +18.2 (2/6) |
| base (BTC) | bottom-10% close (higher) | -2.1 (0/6) | -3.9 (1/6) | -7.1 (2/6) | -10.9 (3/6) | -17.7 (3/6) |
| shock_lookback_250 (BTC) | both tests | identical to base | | | | |
| sol_generalization (SOL) | top-10% close (lower) | +4.7 (1/6) | +10.1 (2/6) | +19.9 (1/6) | +24.9 (2/6) | +40.1 (2/6) |
| sol_generalization (SOL) | bottom-10% close (higher) | -4.4 (0/6) | -6.7 (0/6) | -13.7 (0/6) | -20.5 (1/6) | -42.6 (1/6) |
| uni_defi (UNI) | top-10% close (lower) | -5.8 (5/6) | -8.6 (5/6) | -15.4 (6/6) | -21.6 (6/6) | -34.3 (5/6) |
| uni_defi (UNI) | bottom-10% close (higher) | -1.0 (3/6) | -1.7 (3/6) | -5.2 (2/6) | -6.5 (2/6) | -5.0 (3/6) |

  About 3,100-3,600 events per test.
- **Reading, measured not proven:**
  - On BTC and SOL the effect has the opposite sign to the claim: after a close near the
    100-hour high, returns are higher (continuation), not lower.
  - On UNI, highs are followed by lower returns, as claimed, but lows are too.
- **Why base and shock_lookback_250 are identical:** the tests select on the price, which no
  config change alters, so they cannot see the block. This is the CUL-397 gap made concrete.

**(c) Readers with the new inputs: partly shown.**
- **trade_efficiency:** one patch, `shock_reversal` / `params.period` 1 -> 2, `before` matches.
  The component id, the setting and the old value all exist in run_070's base config. In
  run_066 the same reader invented `keltner_breakout_entry`.
  - Decide-next ranked it first and queued it as `trade_efficiency-run_070-1` (held by hand,
    `blocked_on_e068`).
- **regime_power:** one `new_block`. Its config paths (`/regime_detector/components`,
  `/regime_detector/rules`, `/strategies/regimes`) all exist, but:
  - its rationale names `VarianceRatioRegimeComponent`, which does not exist (the real class is
    `VarianceRatioComponent`). It sits in prose, so no feasibility gate checks it;
  - it again diagnoses the deliberately ungated detector as "uninformative", the same wrong
    diagnosis O-19 recorded on run_065.
- **profitability, forecast_power, component_attribution:** no proposal.
- **Verdict:** settings and ids in structured fields are now right (1 of 1); a class name in
  free text is still invented (1 of 2 class names).

**Reader input growth, measured (cache_creation tokens per call, run_066 -> run_070):**

| Reader | run_066 | run_070 | Added |
|---|---|---|---|
| profitability | 22,667 | 50,274 | +27,607 |
| trade_efficiency | 29,958 | 60,523 | +30,565 |
| forecast_power | 11,246 | 35,479 | +24,233 |
| regime_power | 18,292 | 39,302 | +21,010 |
| component_attribution | 14,527 | 39,557 | +25,030 |

Reader cost: $0.437 -> $0.715 (+64%), against the proposal's estimate of ~$0.55.

**New findings from this run:**
1. **Claim tests that read price cannot see the block** (`base` = `shock_lookback_250`). The
   PR 3b (CUL-397) review call should flag a claim whose tests ignore the block's output.
2. **Free-text class names are not checked.** regime_power invented one. A check that every
   `*Component` name in a proposal exists in the catalogue (warning only) would catch it.
3. **The O-19 wrong diagnosis repeats:** regime_power treats ungated scaffolding as a defect.
   `block_manifest.yaml` marks the detector as scaffolding, and the reader still proposes
   rebuilding it.
4. **After `--unpark`, use `--once`, not `--resume --once`.** `--resume` finds no paused entry
   (the entry is `ready`) and does nothing (RUNBOOK §4 already says "relaunch").

## Result in one paragraph (first attempts, before PR #324)

**Only (a) was shown.** Four runs were started (run_067 to run_070). None reached a backtest.
- run_067 hit two bugs in step 1a's retry path (fixed: CUL-395, PR #321). It then ended with
  step 1a declaring its brief "exhausted".
- run_068 was launched by mistake by an unpaced `--resume` and killed during step 1a.
- run_069, the same brief re-opened, was declared exhausted again.
- run_070, a new hourly brief:
  - step 1a wrote a valid two-test claim card first time, with no retry and no power warning;
  - step 1b then parked the run twice as `component_gap`, over ATR versus standard deviation.

So (b) and (c) are **not shown**: no variant was backtested, and no reader ran. Total spend is
about **$1.62**, plus run_068's killed call (not logged, probably under $0.10). The holdout was
never touched.

## The runs

| Run | Brief / entry | What happened | Spend (console) |
|---|---|---|---|
| run_067 | `C4_vol_managed_trend_kraken_perp__more_1` (R2 "more ideas", 1h) | 1a call 1: broken YAML; F4b retry wrote `hypothesis_card_2.yaml` and was judged on the stale broken file (stop). Resume: 1a wrote a lone `hypothesis_card_2.yaml` (stop). After PR #321: 1a said `exhausted`. | $0.1929 + $0.2269 + $0.1980 + $0.1542 = **$0.77** |
| run_068 | `C4_donchian_daily_trend_kraken_perp__more_2` | Queued by decide-next despite the operator's hold (CUL-398), launched by an unpaced `--resume` (my error), killed during 1a. Status `failed`. | unknown (killed mid-call) |
| run_069 | `C4_vol_managed_trend_kraken_perp__more_2` (brief re-opened, test B of O-20) | 1a proposed two new cards; the parser missed them (blank line between file name and fence); the format retry answered `exhausted`. | $0.2144 + $0.1953 = **$0.41** |
| run_070 | `E068_hourly_shock_reversal_kraken_perp` (new brief, operator-approved) | 1a: valid claim card first time. 1b: `component_gap` (parked); unparked; 1b parked again with the same reason. | $0.2070 + $0.1350 + $0.0997 = **$0.44** |

Every call took `num_turns: 1`. `flags.holdout_reserved` is `false` on every run, and no path
under the sealed store appears in any run folder.

## (a) The claim card step 1a wrote (run_070), quoted

```yaml
statement: 'Unusually large 1-hour moves on BTC/ETH are followed by partial mean-reversion within 1-12 hours.
  After extreme-high closes (top 10%), subsequent returns are lower than baseline; after extreme-low closes
  (bottom 10%), subsequent returns are higher. Reversal is largest in first hours and fades over the 12-hour horizon.'
kind: event_behaviour
tests:
- name: high_close_shock_reversion
  selector: {kind: quantile, field: close, side: top, q: 0.1, lookback: 100}
  outcome: {kind: fwd_return, horizons: [1, 2, 4, 6, 12]}
  baseline: {kind: complement}
  statistic: decay_curve
  direction: less
  floor: {min_events: 50, min_windows: 4}
  consistency: {unit: window, min_same_sign: 3}
- name: low_close_shock_reversion
  selector: {kind: quantile, field: close, side: bottom, q: 0.1, lookback: 100}
  outcome: {kind: fwd_return, horizons: [1, 2, 4, 6, 12]}
  baseline: {kind: complement}
  statistic: decay_curve
  direction: greater
  floor: {min_events: 50, min_windows: 4}
  consistency: {unit: window, min_same_sign: 3}
```
(`pass_if`, `fail_if` and `rationale` are in `runs/run_070/artifacts/hypothesis_card.yaml`.)

- **check_claim passed first time.** `claim_check.yaml` has one attempt, with `errors: []` for
  both tests.
  - `claim_test_status.yaml`: `usable: true`, both tests `verdict_possible: true`.
  - `claim_test_coverage.yaml`: `run_070: {usable: true, power_warning: false}`.
  - The campaign summary has a "Claim tests" section: "Runs with a usable claim test: 1".
- **Power warning: none.** `claim_power.yaml`: 17,520 bars x 2 coins, longest horizon 12,
  floor 50 events, `status: ok`.
- **But the tests do not test the claim.**
  - The statement is about an unusually large 1-hour *move*.
  - The selectors pick bars whose closing *price level* is in the top or bottom 10% of the last
    100 closes, i.e. "near a 100-hour high or low".
  - The faithful selector reads the card's own forecast (`-shock`, scaled): `quantile(field:
    forecast, ...)`.
  - `check_claim` checks the form only, so this passed. This is the same gap as run_067's
    "1-10 days" claim with 1-10 bar horizons (CUL-397).
- **The other claims written today** were all checked by nobody, because each run stopped first.
  They were all short-horizon:

| Run, call | Idea | Claim horizons | Note |
|---|---|---|---|
| run_067, 1 | `SPARSE_HIGH_CONVICTION_EMA_TREND_1H` | 1, 2, 4 bars | fits the statement ("next 1-4 hours") |
| run_067, 2 | `VOL_MANAGED_MOMENTUM_BTCETH_KRAKEN_PERP` | 1, 2, 5, 10 bars | statement says "1 to 10 days": unit mismatch (CUL-397) |
| run_067, 3 | `VOLATILITY_CONTRACTION_MOMENTUM_EXTENSION` | 1, 2, 4, 12 and 1, 2, 4 bars | two tests; file held a stray `---` (two YAML documents) |
| run_069, 1 | two cards, `TIME_SERIES_MOMENTUM_UNSCALED` and `TREND_FOLLOWING_MOMENTUM_WITH_VOLATILITY_REGIME_GATING` | not checked | parser missed them (blank line before the fence) |

## (b) Measured effect sizes and statuses per variant

**Not reached.** No run got past step 1b, so no variant was backtested.
- There is no `artifacts/variants/<vid>/claim_test.yaml` and no `claim_status.yaml`.
- There are no trial rows for run_067 to run_070 in `campaign_state.yaml`, which is correct:
  nothing was graded.

## (c) What each reader proposed

**Not reached.** No reader ran.
- The baseline to compare against when one does is run_066's trade_efficiency reader. It named
  the component `keltner_breakout_entry`, which is not in its config (only `keltner_momentum`
  exists). The other four readers named no component id.
- Reader input growth and budget headroom could not be measured.
- Measured input sizes (`cache_creation` tokens per call):
  - 1a: 60,262 on run_070 (60,507 / 60,192 on run_067);
  - 1b: 33,032.
- The claim files add little: run_066's 1a was 56,891 without them, so they add about 3.4k
  tokens.

## Warning artifacts

- `runs/run_070/artifacts/claim_power.yaml`: `ok`, no warning.
- `claim_match.yaml`: not written, because 1b produced no manifest (parked). The mismatch
  above (tests read `close`, the idea is a forecast block) would have been its first real case.
- `campaign_record/test_requests.yaml`: none (no `tests: none` claim).
- 1b's `decision.yaml` on both parks failed schema validation (warn-only): `'hypothesis_id' is
  a required property`. The park still worked.
- 1b, both calls: `optional_input never resolved: artifacts/findings_carryover.yaml`.
- Runs 067/069 (exhausted, no card) leave no row in `claim_test_coverage.yaml`. The coverage
  count does not see runs that wrote no card.

## What broke, and tickets

| # | What | Status |
|---|---|---|
| 1 | Step 1a: a single card named `hypothesis_card_2.yaml` stops the run | **fixed**, CUL-395, PR #321 (merged) |
| 2 | F4b YAML retry judged on the first attempt's stale broken file | **fixed**, CUL-395, PR #321 (merged) |
| 3 | Every retry inside `_invoke_agent_with_yaml_retry` overwrites the first call's cost in `audit_log` (logged spend $0.41 lower than real across run_067/069) | open, CUL-396 |
| 4 | The claim check cannot catch a claim whose test does not measure its statement: units (days vs bars, run_067) and field (price level vs move, run_070) | open, CUL-397 |
| 5 | An operator hold (`blocked_on_*`) on an R2 request does not hold its brief. Decide-next queued 6 unapproved `ready` entries today, and one was launched (run_068). | open, CUL-398 (held by hand each time) |
| 6 | The CUL-379 parser accepts a file name only directly above the fence; one blank line loses the answer (run_069) | open, proposed fix (a) |
| 7 | The format and YAML retries do not give the model its own first answer, so a "format only" retry re-draws the content (run_069: two cards -> `exhausted`) | open, proposed fix (c); O-20 |
| 8 | A brief is closed for good by one step-1a "exhausted" answer. 4 of 6 calls on the same inputs proposed new ideas. | open, O-20 (design decision) |
| 9 | Step 1b parks over ATR vs standard-deviation normalisation, although `PriceEvolutionComponent(period=1)` + `zscore`/`negate`/`scale`/`clip` expresses the move in units of its usual size (both documented in `COMPONENT_CATALOG.md`) | open, O-21 |
| 10 | My error: `--resume` without `--once` ran the next queue entry (run_068) | lesson recorded (`tasks/lessons.md`) |

## What a next validation run needs

1. Fix 6 (parser) and 7 (retry design). Otherwise 1a's answers keep being lost or re-drawn.
2. CUL-398, or keep holding new R2 entries by hand and launch only with `--once`.
3. Get one idea through 1b. Either:
   - accept standard deviation for ATR on run_070 (operator call, O-21), or
   - add a small ATR-normalised one-bar-move component.
4. Then (b) and (c) can be checked on the same run.

## Decisions (operator, 2026-10-04)

1. **Robustness PR (one PR):**
   - the parser accepts blank lines before the fence;
   - CUL-396: one audit key per retry;
   - retries receive their own first answer with "change only the layout, keep the content",
     and the "Missing: hypothesis_card.yaml" message follows the multi-card rule;
   - CUL-398: a `blocked_on_*` R2 request counts as outstanding, and R2 never queues
     `ready` entries past an operator hold.
2. **Decisions PR (phase A first):**
   - O-20: a brief closes only after two consecutive independent "exhausted" answers.
   - O-21: accept the zscore form. 1b must show that no combination of components and
     transforms expresses the idea before a `component_gap`. No ATR component.
   - CUL-397: check whether the slots can express "a large 1h move". If not, add a bar-t
     past-return selector field (past bars only, with a lookahead test). CLAIM_TESTS.md tells
     1a to write `tests: none` + `missing_block` instead of approximating. Add the
     test-vs-claim review call (proposal section 4) as a warning: 1a gets the comment once,
     and the run continues either way.
3. **After both PRs, with the operator's go:** `--unpark E068_hourly_shock_reversal_kraken_perp`,
   then `--resume --once`, to finish (b) and (c); this file is then updated. Held entries stay
   held; slices 4 and 5 wait for (b) and (c).

## Final run (2026-10-05): readers v3 switched on, but no run reached the readers

**In short:** two launches, both stopped before any backtest, so no reader ran. Readers v3 is
therefore still unmeasured on a real run. Spend: $0.832 of the operator's $3 cap. The
holdout was not touched: `holdout_reserved: false` on both runs, and no sealed path in either
run folder. Every call took 1 turn. Two new blockers were found (CUL-405, CUL-406).

**Setup**
- `c4/flag-set` at `54356e88`: master including PR #330, the fix so that a reader input that
  cannot be written never stops the readers.
- Flags: the C4 set plus `claim_tests`, `reader_findings` and `operator_approval`, all on and
  read back through the code's own flag readers. Weighted token budget: 1,800,000 per run.
- Queue: all 8 `blocked_on_e068` entries converted to `blocked_on_operator_approval`, each with
  a note; `P4_ts_trend` left as it was. The dry run passed with the real entry ready.

| Run | Entry | Released by | What happened | Spend |
|---|---|---|---|---|
| run_071 | `E068_hourly_shock_reversal_kraken_perp__more_1` (R2: more ideas for the hourly brief) | `--approve`, then `--once` | 1a wrote a new idea. 1b parked it as `component_gap`. No backtest. | $0.305 |
| run_072 | `trade_efficiency-run_070-1` (reader patch, `shock_reversal.params.period` 1 -> 2) | the operator's pre-approved fallback: `--approve`, then `--once` | 1a, 1b and step 2 ran. `backtest_specification` refused the run with "pass-through mismatch". Status `failed`. | $0.527 |

After this, the operator's limit of two launches is reached. No other entry was approved or
launched.

### (a) The claim card

**run_071, written by 1a: `HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH`.** It is a new idea:
continuation, the opposite of run_070's reversal.

```yaml
statement: 'After high-conviction directional 1h candles (body_fraction > 70%, close in top or bottom
  10% of intrabar range), price continues in the same direction over 1-4 hours, indicating
  herding-driven momentum rather than mean-reversion.'
kind: conditional_behaviour
tests:
- name: continuation_by_conviction
  selector: {kind: event, field: forecast, op: '>=', value: 12}
  outcome: {kind: fwd_return, horizons: [1, 2, 3, 4]}
  baseline: {kind: complement}
  statistic: mean_diff
  direction: greater
  floor: {min_events: 40, min_windows: 3}
  consistency: {unit: window, min_same_sign: 3}
```

- **Valid first time:** `claim_check.yaml` has one attempt with `errors: []`;
  `claim_test_status.yaml` is `usable: true`; `claim_power.yaml` is `ok` (17,520 bars x 2 coins,
  no warning).
- **Did the test read the block's signal? Yes.** It selects on the block's own `forecast`.
  run_070's tests read the price level, so this is the improvement PR #327 aimed for.
- **But only half the claim is tested.** The statement covers both directions; the test selects
  only `forecast >= 12`, the up side. Added to CUL-397.
- **The visibility check and the revision were not triggered.** Both run after 1b, and 1b parked
  the run. run_071 has no `claim_match.yaml` and no `claim_revision.yaml`.

**run_072, the reader patch:** a "pass-through" card (config, manifest and criteria come from
upstream). It carries a sensible claim: a `direction_forecast` whose test is the rank IC of
`forecast != 0` at horizons 1-3, so it reads the block. But every claim step marked it exempt:
- `claim_check.yaml` and `claim_test_status.yaml` (`usable: false`);
- `claim_match.yaml` (`exempt`, visibility `not_applicable`);
- `claim_revision.yaml` (`not_applicable`).

So a reader patch never has its claim measured (CUL-406).

### (b) The claim measurement and the finding in campaign memory

**Not reached.** Neither run backtested anything. There is no `claim_test.yaml`, no
`claim_status.yaml`, no trial row in `campaign_state.yaml` and no run_071/run_072 entry in
`campaign_memory.yaml`. That is correct, since nothing was graded. On run_072 the measurement
would have found no usable test anyway, because the card was exempt (CUL-406).

### (c) The readers

**Not reached in either run.** So none of slice 5's machinery has run on real output yet:
- the skip rules;
- the claim digest and the earlier-findings summary;
- side findings, checked patches and invented-name checks;
- PR #330's missing-input path.

The one reader-related signal: decide-next, after run_071, warned again about run_070's old
regime_power proposal ("unknown component class `VarianceRatioRegimeComponent`, nearest real
class `VarianceRatioComponent`"). That is the PR #326 warning working, but on a v2 proposal,
and it repeats at every decide-next.

### (d) What decide-next created

**Nothing.**
- **After run_071:** it stopped with `no_eligible_candidate`.
  - The 5 candidates were older reader proposals (regime_power from runs 065/066/070,
    trade_efficiency from runs 065/066); their gates ruled all 5 out.
  - R2 found no open brief: 3 exhausted, 5 legacy, and 2 held by an operator hold.
  - It listed the 7 entries awaiting approval.
- **After run_072:** decide-next did not run (the run halted with `unhandled_exception`).

No entry became `ready` without the operator. The queue now holds:
- 6 entries `blocked_on_operator_approval`;
- `E068_..._more_1` as `paused:waiting_for_component`;
- `trade_efficiency-run_070-1` as `paused:unhandled_exception`;
- `P4_ts_trend` unchanged.

### (e) Cost and weighted tokens per stage

| Stage | run_070 | run_071 | run_072 |
|---|---|---|---|
| 1a hypothesis_generation | $0.207 / 146,348 | $0.200 / 138,296 | $0.228 / 166,242 |
| 1b strategy_config_authoring | $0.373 / 272,571 (3 calls) | $0.105 / 71,666 | $0.124 / 90,290 |
| 2 innovation_expansion | $0.427 / 304,922 (3 calls) | not reached | $0.175 / 134,754 |
| readers | $0.715 / 488,414 | not reached | not reached |
| **Run total** | **$1.723 / 1,212,255** | **$0.305 / 209,962 (11.7% of 1.8M)** | **$0.527 / 391,286 (21.7%)** |

- **Readers:** no comparison with run_070's $0.715 and 488k is possible yet.
- **Single calls cost the same as run_070:** a 1b call cost $0.105-0.124 (run_070: about $0.124
  per call), and a step-2 call cost $0.175 (run_070: about $0.142 per call).
- **Budget headroom:** both runs were far under 1.8M. A run_072 that reached the readers would
  have had about 1.41M weighted tokens left for them, roughly 2.9 times run_070's whole reader
  stage.

### (f) Warning artifacts

- **run_071:**
  - `claim_power.yaml` is `ok`.
  - `decision.yaml` is a `component_gap` with a `tried:` list of 3 configurations: Donchian(20),
    Donchian + PriceEvolution(1), and PriceEvolution(1) + zscore + scale. 1b showed what it
    tried, as O-21 requires.
  - **The park is only partly justified (corrected after the operator's review).**
    - On a 24/7 market, a bar's open is the previous bar's close, or very nearly; this is not yet
      checked on the cache. So the body (close-open) is about the 1-bar move,
      `PriceEvolutionComponent(period=1)`.
    - Normalised by its usual size (zscore), that is exactly the form the operator accepted in
      O-21 for run_070. 1b's own `tried:` list rejected it as "a different yardstick", which
      contradicts that decision.
    - What really cannot be built exactly is the rest: dividing by the current bar's own range
      (high-low), and "close near the bar's high or low". No component reads the current bar's
      high and low, except inside ATR smoothing (ADX, Keltner).
    - A row was added to `component_requests.yaml`.
    - Finding: 1b's park reason ignores O-21's accepted approximation.
  - 1a wrote a single `hypothesis_card_2.yaml`; it was used as the card (the PR #321 path).
  - Schema warning: `hypothesis_card.yaml` has `edge_source.requires_new_feed: false`, but the
    schema wants a string (CUL-404).
  - `optional_input never resolved: artifacts/findings_carryover.yaml` (1b).
- **run_072:**
  - "run_072 has no usable claim test (exempt: pass_through card)" (CUL-406).
  - Schema warnings: `hypothesis_card.yaml` has an extra field `nearest_library_analog`;
    `backtest_spec.yaml` is missing `hypothesis_id` (CUL-404).
  - `optional_input never resolved`: `findings_carryover.yaml` (1b) and `refinement_notes.yaml`
    (step 2).
- **No `reader_input_gaps.yaml`:** the readers were never reached.

### (g) What broke, and tickets

| # | What | Ticket |
|---|---|---|
| 1 | **A reader patch cannot reach its backtest.** 1b copied the config exactly but changed one sentence of `block_manifest.yaml`'s free-text `rationale` ("1-bar" became "2-bar"). The pass-through check hashes the whole manifest, prose included, so it refused the run. The diff between the two manifests is that one field. Every patch that changes a number the rationale mentions will fail the same way. | CUL-405 (high; operator decision: hash structure only, or let code write the manifest) |
| 2 | **Reader-patch cards are exempt from claim tests**, so patch runs, decide-next's most common follow-up, would never produce a claim measurement or a finding. | CUL-406 (high; operator decision) |
| 3 | run_071's test covers only the up side of a two-sided statement. | CUL-397 (comment added) |
| 4 | Warn-only schema mismatches on real cards. | CUL-404 (low) |
| 5 | The `VarianceRatioRegimeComponent` warning repeats at every decide-next for an old proposal. | noted here, no ticket |

### What a next validation run needs

To see the readers, a run must reach a backtest. Either:
- decide CUL-405 (and ideally CUL-406), then `--unpark` `trade_efficiency-run_070-1` and run
  `--once`; or
- approve a 1a idea that the catalogue can build.

run_071 would need a body-fraction component first (OHLC: open, high, low). That is a component
decision for the operator. The optional "approve a reader side finding" run still needs readers
v3 to have produced one.
