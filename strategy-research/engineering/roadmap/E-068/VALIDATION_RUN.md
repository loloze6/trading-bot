# E-068 validation on real runs (2026-10-04)

**Goal:** one real run with `orchestrator.claim_tests.enabled` on, on top of the C4 flag set
(branch `c4/flag-set`, merged with master at `b90b4c43`, then `452ef9fd` after PR #321).
It had to show three things on real AI output:
- **(a)** step 1a writes a valid claim card;
- **(b)** the claim is measured after the backtests (`claim_test.yaml`, `claim_status.yaml`);
- **(c)** the readers, with their new inputs, stop inventing components and settings.

## Result in one paragraph

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
