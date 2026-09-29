# E-062 S2b-2 — One scoring mechanism (D-041): characterization (read-only)

Base: `origin/master` `a5d3abf5`. Every `file:line` below is at that commit (S1_FINDINGS'
line numbers were at `9900dee3` and have moved: its "9017-9052" is now
`run_phase1_research.py:9770-9876`, its "9887-9918" is now `:10719-10750`).

Method: code read + grep (search terms listed in Q1). Read-only Python over tracked run
artifacts and the committed ledger, using the S2a functions themselves
(`tools/portfolio_daily.load_windows`, `tools/portfolio_whole_test.chain_windows` /
`whole_test_sharpe`) and `tools/deflate_sharpe`'s own ledger functions. No backtest, no
LLM call, nothing written except this file. Nothing under the sealed store was opened.
Dates are written only when before the holdout start.

---

## Contradictions and surprises (read first)

| # | Finding | Evidence | Consequence |
|---|---|---|---|
| X1 | **Today's "DSR" is not the Bailey & López de Prado DSR.** It computes z = (SR − E_max) ÷ σ_cross, where σ_cross is the spread of the trial Sharpes. It does not use T (number of observations), skew or kurtosis. It also adds the trial mean: E_max = μ_cross + σ_cross·Z(N). | `run_phase1_research.py:10812-10816`; `deflate_sharpe.py:541-545` | Q3 as briefed (per-period SR, T, skew and kurtosis) is a **formula change as well as a basis change**. D-039 "kept" the 0.95 threshold under the current formula, so 0.95 would mean something else. D-041 does not mention this. **Operator must confirm (G3).** |
| X2 | **The two bases are not a rescaling of each other: 2 of the 3 legacy backtests change sign.** | measured, table in Q4 | run_054: ledger −1.66 (median of per-window medians) vs whole-test daily +0.979 annualised. run_057: −0.686 vs +0.407. run_059: −0.6375 vs −0.535. Any DSR that mixes the two bases is meaningless, not just biased. |
| X3 | The current E_max adds μ_cross. The ledger's trial Sharpes are negative, so this **lowers** the bar compared with the published SR0 = σ·Z(N), in the flattering direction. | `:10812`, `deflate_sharpe.py:542` | G3 proposes max(μ, 0) + σ·Z. |
| X4 | "Recompute legacy rows where possible" covers **3 rows**. The committed ledger has 15 rows. 12 of them are prescreen rows: no backtest was ever run, so there is no Sharpe to recompute. | ledger inventory, Q4 | D-041's recompute is small. It gives K = 3 same-basis values, below any sensible variance floor (G4). |
| X5 | **CLAUDE.fork.md is stale.** It says `run_campaign.py:1119-1122` "counts N". At `a5d3abf5` those lines materialise a brief. run_campaign never reads a trial Sharpe (it counts rows only, `:2501-2552`). N is computed in `_promotion_dsr_context` (`run_phase1_research.py:10590-10660`) and `deflate_sharpe.compute_promotion_audit` (`:562-610`). | grep of `run_campaign.py` for `sharpe` | Doc fix only. |
| X6 | **D-041 says "one mechanism".** Under C4's flags, the legacy promote path (`_write_promotion_audit`, the `holdout_evaluation` DSR gate `:12216`) and the `deflate_sharpe.py` CLI stay unreached but keep the sparse branch until D-043's clean-up. | Q6 | Literally, two mechanisms remain in the code until D-043 (G9). |
| X7 | 28 pre-ledger runs (run_011–run_039) have saved results but **no ledger row, so they are not in N**. All 28 also read NOT_EVALUABLE under the S2a chain rules: head data 4–8 days late in window `2024-01`, more than `warmup_days=2`. The main checkout also holds untracked full-backtest re-runs of 7 prescreen-killed runs (`runs/run_0{43,44,47,48,50,53,60}/e039_s1_rerun*`). Those are on one machine only and have no ledger rows. | Q4 | An existing N gap, not introduced by D-041. Parked (G13). |
| X8 | Comparator drift. The v2 DSR bar row uses `>=` 0.95 (`_COMPARATOR_V2`, `:11569-11573`). The promotion audit uses `>` (`:10818`, `deflate_sharpe.py:689`). | — | Keep `>=` on the bar. Noted only. |
| X9 | Dead config. `campaign_config.yaml:114 below_floor_pct_threshold: 50.0` and `:782 trade_floor_per_window: 5` are read by no code (grep empty). The 50.0 is hard-coded at `:9845`, `:10696` and `deflate_sharpe.py:825`. The 5 is `run_protocol.py:55`. | grep | Remove with the sparse path, or leave for D-043. |

---

## Q1 — Every producer and consumer of trial Sharpe

Searched (non-test `.py` under `strategy-research/workflow` and `tools`, then read each hit):
`trial_sharpes`, `statistic_valid`, `below_floor_pct`, `is_sparse|expectancy_t_stat|expectancy_promotion`,
`deflated_sharpe|passes_deflated`, `dsr_basis|_promotion_dsr_context`,
`_record_backtest_trial|_record_failed_backtest_trial`. Non-code hits (docs, the verdict-interpreter
SKILL, schemas) are listed at the end and are not consumers of the value.

**Count: 3 producers, 16 consumers (7 read the Sharpe value, 9 read only the row set or the counts).**

| # | Site | P/C | What it does with the trial Sharpe | Under D-041 |
|---|---|---|---|---|
| P1 | `run_phase1_research._record_backtest_trial` `:9770-9876` (called `:1779` variant loop, `:2244` single) | producer | `sharpe` = median of per-coin `median_sharpe` (`:9820-9823`); `statistic_valid` = `expectancy` if `below_floor_pct > 50`, else `sharpe`/`neither` (`:9845-9850`) | adds the whole-test block (G1) |
| P2 | `_record_failed_backtest_trial` `:9879-9957` | producer | `sharpe: None`, `statistic_valid: failed` | unchanged (counts in N, never in K) |
| P3 | `_mark_trial_invalidated` `:9161-9200` (called by run_campaign `:2041-2083`) | producer (in-place edit) | adds `invalidated_artifact`/`invalidation_reason` | unchanged (row leaves N, per F8b) |
| C1 | `_promotion_dsr_context` / `_dsr_candidate` `:10558-10836` | consumer, **value** | N = deduped valid rows (`:10643`); Sharpe sample = `statistic_valid=="sharpe"` rows (`:10628-10649`); sparse branch `:10719-10750`; DSR `:10779-10824` | v2 branch: whole-test sample, no sparse branch |
| C2 | `_grade_profit_bars_protocol_result` `:11894-11930` (branch 3 + grid) | consumer, value | DSR row from C1; v2 note says "per-window basis unchanged until S2b-2" (`:11911-11916`) | uses the v2 DSR |
| C3 | `_grade_profit_bars_v2` `:11844-11892` | consumer | DSR row; not-evaluable text "sparse-trading or insufficient-trials" (`:11856-11859`) | text + basis string change |
| C4 | `_evaluate_profit_bars_every_backtest` `:11982-12065` | consumer, counts | writes `dsr_basis {n_dsr_total, n_trials}` (`:12047`) | adds same-basis fields (G7) |
| C5 | `_profit_bars_grid_grader` `:4530-4570` | consumer | calls C1/C2 | follows C2 |
| C6 | `_dsr_on_current_ledger` `:5400-5427` (holdout spend) | consumer, value | recomputes the DSR on the current ledger via `ctx["dsr_candidate"](pr)`, which takes only `pr` | needs `run_dir` for the whole-test SR, plus a basis check (G7) |
| C7 | `_write_promotion_audit` `:10838-11040` (legacy promote path) | consumer, value | per-variant DSR/sparse, `_evidence_strength` falls back to the t-stat (`:10944-10954`) | legacy, kept (G9) |
| C8 | `_evaluate_profit_bars` `:11150+` (legacy promote) | consumer | reads `promotion_audit.yaml`'s DSR | legacy, kept |
| C9 | `holdout_evaluation` DSR gate `:12216-12220` (via `_holdout_hypothesis_id` `:4881`) | consumer | `passes_deflated_threshold` | legacy, kept |
| C10 | `tools/deflate_sharpe.py` `load_sharpe_trials :381`, `compute_dsr :431`, `compute_promotion_audit :562`, CLI `main :735` | consumer, value | the lockstep twin of C1 | new pure function lives here (S2b-2a); legacy functions kept |
| C11 | `tools/decide_next.py` `_dsr_computable :1057-1059`, `_classify_block_set :1095-1106` | consumer, counts | composition re-fire when `n_dsr_total>=2 and n_trials>=2` | must read the same-basis count and the floor (G4) |
| C12 | `run_campaign._ledger_dsr_basis :4379-4385` (→ decide_next, `:4206`) | consumer, counts | passes C1's counts | passes the new fields |
| C13 | `run_campaign._run_has_trial_row :2032-2038`, `_regenerate_summary :2500-2552`, `:3027`, `:3221` | consumer, rows | presence / row count only | unchanged |
| C14 | `tools/campaign_memory._trial_rows :202-219`, `_tested_trial :222-232` | consumer, rows | `forecast_hash` only | unchanged |
| C15 | `tools/replay_repeat_gate.py :182-200, :269-270, :342-352` | consumer, rows | via C14 | unchanged |
| C16 | `tools/killed_run_gate.py :168, :290, :333`; `tools/dual_writer_demo.py :186, :259` | consumer (verification tools) | C10 on fixtures | unchanged (legacy basis) |

Not consumers: `run_campaign.py:2397-2399` (a `median_sharpe` read from `protocol_result.yaml` for
the queue summary, not from the ledger); `run_protocol.py:1741-1755, 2450-2451` (produce
`below_floor_pct` and the per-window Sharpe that is nulled below 5 trades); `composite_cache.py:49-50`
(writes no trial row). Docs: `docs/USER_GUIDE.md`, `docs/RUNBOOK.md:679`,
`workflow_artifacts/skills/verdict-interpreter/SKILL.md:675-705`,
`workflow_artifacts/schemas/promotion_audit.schema.json`.

---

## Q2 — Ledger schema today; carrying the basis

**Today** (`campaign_record/campaign_state.yaml → trial_sharpes`, a list; the only in-place edit is P3):

| source | keys written | Sharpe meaning |
|---|---|---|
| `backtest` (P1) | `trial_id, source, sharpe, expectancy_bps, n_trades, statistic_valid, below_floor_pct, forecast_hash, [symbols], [reproduces_trial]` | median over coins of the median per-window Sharpe (trade-exit P&L, nulled below 5 trades) |
| `backtest_failed` (P2) | `trial_id, source, sharpe:null, expectancy_bps:null, n_trades:0, statistic_valid:failed, forecast_hash, error, [symbols]` | none |
| `prescreen`, `prescreen_backfill` (legacy writer, removed) | `+ route, ic_pooled, cost_pass, hypothesis_id, note…` | none (`neither`) |

Identity: `(trial_id, source)`, enforced by `check_no_duplicate_trial_ids` (`deflate_sharpe.py:213`)
and the union merge (`:327-378`). Dedup for N: `(forecast_hash, sorted symbols, source)` plus
`reproduces_trial` (`:10500-10555`, `deflate_sharpe.py:125`).

**Committed ledger, measured:** 15 rows = 3 `backtest` (054/057/059) + 10 `prescreen` (3 of them
invalidated) + 2 `prescreen_backfill`. Today N (`n_dsr_total`) = **12**. Sharpe sample
(`n_trials`) = **1** (run_059 only; 054/057 are `expectancy`). So the DSR is not computable today.
One oddity: `run_057` has rows but is missing from `campaign_state.runs`.

**Proposal (G1).** Legacy fields are frozen: they keep feeding only the legacy readers
C7–C10/C16. Flag-on rows gain one nested block:

```yaml
whole_test:                    # absent when the flag is off -> row byte-identical
  basis: whole_test_daily_equal_weight_v1
  status: ok | not_evaluable | error
  reason: null | "<text>"
  sr_daily: <float>            # mean / stdev(ddof 1) of the chained daily returns, NOT annualised
  n_daily_returns: <int>       # T
  skew: <float>                # population m3 / m2^1.5
  kurtosis: <float>            # population m4 / m2^2, raw (normal = 3)
```

The v2 DSR reader admits a value into its sample **only** when `basis` equals the exact string
and `status == ok` (native block, or the recompute overlay, Q4). A legacy row without a
block contributes to N and never to the variance. So no single distribution can mix
per-window-median and whole-test-daily values, and the legacy readers never see the new value.
The union merge compares nested dicts canonically (`deflate_sharpe.py:287-308`), so the block
is merge-safe as written.

---

## Q3 — DSR on the new basis, exactly

| symbol | definition | source |
|---|---|---|
| ŜR | candidate `sr_daily` = `whole_test_sharpe(chain) / √365`. It must equal, bit for bit, the value its own ledger row carries (lockstep assert; a mismatch raises). | `portfolio_whole_test.py:719-735` |
| T | `n_daily_returns` of the candidate's chain (≥ 30, else the Sharpe is already NOT_EVALUABLE). The chain's multi-day steps count as one observation each. | same |
| γ3, γ4 | skew and raw kurtosis of the candidate's chained daily returns | new pure fn |
| N | **unchanged rule**: `len(deduped valid rows)`, i.e. every `backtest`, `backtest_failed`, `prescreen*` row, minus `invalidated_artifact` rows (F8b, existing). It is computed from `trial_sharpes` only, so it cannot depend on whether a row was recomputed. **N never shrinks.** Test: N is identical with the flag on and off, and with and without the overlay. | `:10590-10660` |
| {SR_k} | same-basis sample: deduped valid rows whose `whole_test` (native or overlay) is `ok`, basis-matched; K = its size. The candidate's own row is in it. | new |
| V | sample variance of {SR_k}, ddof 1 (G5) | new |
| SR0 | max(mean{SR_k}, 0) + √V · [(1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(eN))], γ = 0.5772156649 (G3) | BLP 2014 A.6, mean floored |
| **DSR** | Φ( (ŜR − SR0) · √(T−1) / √(1 − γ3·ŜR + ((γ4−1)/4)·ŜR²) ) | BLP 2014 eq. 9 |

**NOT_EVALUABLE (fail loud, never a default):** N < 2; **K < `dsr_min_same_basis_trials`** (G4,
reason names K, N and the floor); V == 0; the candidate's own block is not `ok`; the
denominator's argument is ≤ 0 (it is ≥ (1 − γ3·ŜR/2)² ≥ 0 because γ4 ≥ 1 + γ3², so this only
fires at exactly 0); N < K raises (caller bug, as `deflate_sharpe.py:479-486`).

**Too few same-basis rows.** A σ estimated from 2–3 values can come out tiny. A tiny σ lowers
SR0, which is the flattering direction. So below the floor the DSR reads NOT_EVALUABLE and
the bar blocks. There is no σ floor and no prior: any such number would be invented. The
re-fire rule in decide_next (C11) must use K and the floor, not `n_trials >= 2`, or it will
re-fire a composition that cannot become evaluable.

Scale check from the 3 legacy values (sr_daily 0.0512, 0.0213, −0.0280): σ_cross ≈ 0.040.
The estimator standard error at T = 2695 is ≈ 1/√2694 ≈ 0.019. The two are the same order of
magnitude but they are different quantities. This is why X1 matters.

---

## Q4 — Legacy recompute: inventory and mechanism

Inventory: all 41 `protocol_result.yaml` under the worktree's `runs/`, each run through
`load_windows` → `load_protocol_window_bounds` → `chain_windows` → `whole_test_sharpe`:

| group | rows / files | whole-test curve rebuildable? | why |
|---|---|---|---|
| ledger `backtest` rows run_054, run_057, run_059 | 3 | **3 EVALUABLE** | tracked `portfolio_states.csv` (60/30/191 files), protocol files present. See the table below. |
| ledger `prescreen*` rows (041-044, 047, 048, 050, 053, 054, 057, 059, 060) | 12 | not applicable | no backtest; `protocol_result.results` is empty; there never was a Sharpe |
| superseded artifact dirs (054 `artifacts_SUPERSEDED_…`, 059 `superseded_…tz_bug`, 044 `attempt_2_invalidated…`) | 3 | NOT_EVALUABLE | equity files not kept. Not ledger rows. |
| pre-ledger runs 011–039 | 28 | NOT_EVALUABLE | head data 4–8 days after the nominal start in window `2024-01` (> `warmup_days=2`). Not ledger rows (X7). |

| run | protocol | nominal span | T | sr_daily | ×√365 | skew | kurt (raw) | ledger `sharpe` (basis) |
|---|---|---|---|---|---|---|---|---|
| run_054 | ts_trend_daily_v1 | 2018-04-01..2025-10-01 | 2695 | 0.0512 | 0.979 | −0.39 | 11.63 | −1.66 (`expectancy`) |
| run_057 | ts_trend_daily_v1 | 2018-04-01..2025-10-01 | 2695 | 0.0213 | 0.407 | −1.51 | 31.42 | −0.686 (`expectancy`) |
| run_059 | funding_mr_daily_retest_v1 | 2019-12-01..2024-01-01 | 1394 | −0.0280 | −0.535 | 0.78 | 15.65 | −0.6375 (`sharpe`) |

These are measured characterisations, not graded results. Raw trade counts (both coins,
including forced closes): 117 / 42 / 699.

**Recomputable: 3 of 3 backtest rows. Not recomputable: 0 backtest rows; 12 prescreen rows have
nothing to recompute.** After recompute: N = 12 (unchanged), K = 3.

**Mechanism (G8)** — `tools/recompute_trial_sharpe_basis.py`:
- Output: a **separate append-only file** `campaign_record/trial_sharpe_basis_recompute.yaml`,
  never an edit of `trial_sharpes`. An in-place edit would break the union merge's equal-row
  rule (`deflate_sharpe.py:365-371`). New rows in `trial_sharpes` would enter N through the
  dedup key's `source` and inflate it.
- One entry per `backtest` row: `{trial_id, source, basis, status, reason, sr_daily,
  n_daily_returns, skew, kurtosis, inputs_sha256: {protocol_result, protocol_file,
  portfolio_states: {path: sha}}, code_sha256: {portfolio_whole_test.py, portfolio_daily.py}}`.
  The entry has **no timestamp**, so the same inputs give the same bytes on both writers'
  machines and the union merge keeps it once. `not_evaluable` entries are written too, so
  the accounting is explicit.
- `--dry-run` is the default: it prints the table and the would-be diff. `--write` appends
  only missing keys. An existing key with different content **refuses** (as the union merge
  does). Re-running is a no-op (idempotent).
- The DSR reader's precedence: a native `whole_test` block beats an overlay entry; both present
  and different → raise.
- Non-recomputable rows: counted in N as today, excluded from K. There is no imputed value.

---

## Q5 — Flag gating and byte identity

- **Same flag** `orchestrator.profit_bars_v2.enabled` (G6). D-041 supersedes G4, which was part
  of the v2 definition. The flag is default-off and no real run has used it
  (`campaign_config.yaml:417-418`). C4.2's target set already includes it.
- **Flag off, byte-identical:** ledger rows (no `whole_test` key; P1 untouched on that path),
  `profit_bars_evaluation.yaml` (no new `dsr_basis` keys), `promotion_audit.yaml`, the golden
  fixtures (`tests/fixtures/profit_bars_golden/`, pinned to fixture bars files). **Declared
  change:** the committed `profitability_bars.yaml` gains `dsr_min_same_basis_trials`
  (required only under v2, like the three S2b-1 keys, `:2972-2990`). Its sha256 changes, so any
  evaluation graded under the old sha is unspendable (`bars_changed`, `:5391-5395`). This is by
  design: the file is unsigned and the operator signs it before C4 anyway.
- **Spend:** `_evaluation_under_current_bars` (`:5363-5397`) is unchanged. `_dsr_on_current_ledger`
  under v2 recomputes on the v2 basis (needs `run_dir`). It refuses `dsr_fails_current_ledger` when
  the evaluation's `dsr_basis.sharpe_basis` is absent or different (this catches any evaluation
  graded by S2b-1 code with the flag on), or when K is now below the floor. `bars_definitions`
  stays `v2`; no label bump is needed because the basis check covers it.

---

## Q6 — The sparse path

| Under the flag | Disappears | Stays |
|---|---|---|
| branch 3 + grid (C1–C5), spend (C6) | `is_sparse` branch and expectancy t-stat (`:10695-10750`); the "sparse-trading" not-evaluable text (`:11856-11859`, `:11911-11916`) | D-035 `trade_count_min` 100 per coin without forced closes (S2b-1 row); `cost_edge_ratio_min` 100-trade floor |
| ledger (P1) | nothing is removed: `statistic_valid`/`expectancy_bps`/`below_floor_pct` are still written for the legacy readers | new `whole_test` block |

Other callers of the sparse statistic, all legacy, unreached under C4's flags (G9): C7
`_write_promotion_audit` (including the `_evidence_strength` t-stat fallback), C9 holdout gate,
C10 `deflate_sharpe.compute_promotion_audit` and its CLI (`:825-831`), C16 fixtures, the
verdict-interpreter SKILL text (`SKILL.md:675-705`, legacy stage). Removal belongs to D-043.

---

## Q7 — Proposed split (small, sequential)

| slice | content | tests | depends |
|---|---|---|---|
| **S2b-2a** pure | `portfolio_whole_test.whole_test_sharpe_stats(daily_returns)` → {sr_daily, T, skew, kurtosis}, where sr_daily·√365 == `whole_test_sharpe` exactly. `deflate_sharpe.compute_dsr_whole_test(candidate, same_basis_srs, n_total, min_same_basis)`: **one** implementation, which the pipeline will import; no third lockstep copy. The overlay loader/validator. Same-basis sample selection. Nothing calls it. | a hand-computed BLP example; K below the floor → NOT_EVALUABLE; N<2; V=0; N<K raises; mean floored at 0 (a negative mean does not lower SR0); moments on a known series; mixed legacy/whole-test sample never mixes; overlay precedence and conflict raise | — |
| **S2b-2b** wiring (flag) | P1 `whole_test` block (flag-on only; `not_evaluable`/`error` caught into the block, G10); C1 v2 context; C2/C3 DSR row (new basis string `deflated_sharpe_whole_test_daily_on_campaign_trial_ledger`); C4 `dsr_basis` + `sharpe_basis`, `n_same_basis`, `min_same_basis`; C6 spend; C11/C12 decide_next re-fire on K; loader key `dsr_min_same_basis_trials`; register + config text | flag-off: ledger row, evaluation and golden fixtures byte-identical; flag-on: a sparse candidate (below_floor > 50) gets a real DSR; N equal flag on/off; ledger SR == bar SR; spend refuses a basis mismatch; the re-fire waits for K | S2b-2a |
| **S2b-2c** recompute | the tool (dry-run default) + fixture tests (idempotent, refuses a conflict, the hash covers every input) | tool tests only | S2b-2b |
| operator step | `--write` on the real ledger → one commit touching `campaign_record/` (dual-writer: the other writer merges it) | — | S2b-2c, operator nod |

**Existing tests that must change (declared):** `tests/test_e062_s2b1_profit_bars_v2.py` (the
DSR row's expected basis `:62`; `_seed_dsr_ledger` needs same-basis rows for the flag-on
DSR). Only if the `dsr_basis` shape changes flag-on: `tests/test_e060_s3b_composition_wiring.py`
(additive keys keep it green). No flag-off test changes. The lockstep tests
(`test_dedup_predicate_lockstep`, `test_expectancy_promotion_lockstep`,
`test_non_finite_sharpe_exclusion`, etc.) stay on the legacy functions.

---

## Q8 — Guesses for the operator

| # | Question | Recommendation | Size | Blocks build? |
|---|---|---|---|---|
| G1 | Where does the whole-test SR live on a row? | A nested `whole_test` block (Q2). The legacy `sharpe`/`statistic_valid` stay frozen for the legacy readers. | SMALL | yes (2b) |
| G2 | Basis tag | `whole_test_daily_equal_weight_v1`, matched as an exact string | SMALL | yes (2a) |
| G3 | DSR formula | **Exact BLP 2014** with per-period SR, T, skew and raw kurtosis. SR0 = max(μ_K, 0) + σ_K·Z(N), never below either the published form or today's. **This redefines what the ratified 0.95 means (X1).** | **BIG** | yes (2a) |
| G4 | Minimum same-basis values for the variance | `dsr_min_same_basis_trials: 10` in `profitability_bars.yaml`, required under v2; below it NOT_EVALUABLE. K is 3 after the recompute, so branch 3 cannot pass until ~7 new trials exist. With per-coin variants (D-016) that is ~2 runs. | **BIG** (a new signed value) | no (the key is required; the value is signed) |
| G5 | Variance estimator on the new basis | sample, ddof 1 (larger, so conservative; no lockstep twin exists on this basis). The legacy path keeps population (#56). | SMALL | yes (2a) |
| G6 | Flag | reuse `profit_bars_v2`; no new flag | SMALL | yes |
| G7 | Spend and evaluation | `dsr_basis` gains `sharpe_basis`, `n_same_basis`, `min_same_basis`; the spend recomputes on the v2 basis and refuses `dsr_fails_current_ledger` on a basis mismatch | SMALL | yes (2b) |
| G8 | Recompute storage | a separate append-only overlay file, deterministic entries (no timestamp), input and code sha256, dry-run default, refuse on conflict (Q4). The `--write` is an operator step. | **BIG** (writes the shared trial record; the dual-writer must merge) | no (the tool builds; the write waits) |
| G9 | Legacy promote path + `deflate_sharpe` CLI | leave them on the per-window/sparse basis, unreached under C4 flags; remove in D-043. Literally "two mechanisms" until then (X6). | SMALL | no |
| G10 | Whole-test computation fails at ledger-write time | NOT_EVALUABLE → `status: not_evaluable`; any other error → `status: error` + reason. The row is still written (N counts it, K does not). Grading recomputes and fails loud. | SMALL | yes (2b) |
| G11 | Which rows enter K | the deduped valid rows (the same dedup as N) with a basis-matched `ok` block; the candidate's own row included | SMALL | yes (2a) |
| G12 | Comparator of the DSR bar | keep `>=` (X8) | SMALL | no |
| G13 | Pre-ledger runs 011–039 and the untracked e039 re-runs are outside N | parked; not introduced by D-041 (X7) | **BIG — parked** | no |

## Decision (operator, 2026-09-29) — recorded as D-046

- **G3:** exact BLP 2014 formula (Q3) with SR0 = max(mu_K, 0) + sigma * Z(N). Threshold 0.95 kept, re-signed with the bars file.
- **G4 (revised after the operator's challenge):** the proposed "NOT_EVALUABLE below 10 same-basis values" is **rejected**. It
  would fail branch 3 closed and force a rerun of the same variant later (nothing re-grades). Instead, with K the number of
  same-basis trial Sharpes: K < `dsr_min_same_basis_trials` (10, signed key) gives SR0 = sigma_null * Z(N);
  K >= 10 gives SR0 = max(mu_K, 0) + max(sigma_K, sigma_null) * Z(N). sigma_null = 1/sqrt(T-1) (null SR = 0, where the
  skew/kurtosis terms vanish), T = the candidate's daily observations. N = every counted trial, as today. NOT_EVALUABLE stays
  only for the S2a whole-test rules (under 30 daily returns, zero stdev, missing curve), never for a small K.
  Measured hurdle (normal returns, DSR > 0.95, N = 12): annualised Sharpe 1.22 at T = 2695, 1.69 at T = 1394.
- **G8:** build the recompute tool (dry-run default); the real `--write` waits for the operator's nod.
- **Split approved:** S2b-2a (pure functions, Opus) -> S2b-2b (flag wiring, Opus) -> S2b-2c (recompute tool, Sonnet), each
  reviewed and merged before the next. Flag `profit_bars_v2` (G6). SMALL guesses as recommended. G13 parked.

### S2b-2a built

Pure functions, not wired (`aef6574f`): `portfolio_whole_test.whole_test_sharpe_stats` (shares one computation with `whole_test_sharpe`; `WHOLE_TEST_BASIS`), and in `tools/deflate_sharpe.py` `compute_dsr_whole_test` (D-046: sigma_null below the floor, max(mean_K, 0) + max(sigma_K, sigma_null) at or above it), `select_same_basis_sample` and `validate_basis_overlay` / `load_basis_overlay`. Legacy DSR functions untouched.
Tests: `tests/test_e062_s2b2a_dsr_whole_test.py` 44 passed; the existing tests of both modules (18 files) 335 passed; 15 of 15 hand mutations killed.
Measured with the new function (normal returns, N = 12, K below the floor, DSR = 0.95): annualised hurdle 1.219 at T = 2695, 1.696 at T = 1394 (D-046 records 1.69).
Guesses (conservative, for review): overlay file shape `{entries: [...]}` keyed (trial_id, source, basis) with an exact key set; an overlay entry for a row absent from the ledger raises (ledger not merged); a native block must carry exactly the Q2 keys; candidate T is checked >= 2 only (the S2a 30-return rule applies where the stats are produced); candidate-in-sample membership is not asserted here (S2b-2b's lockstep assert).
Round-1 review fixes: the candidate's T and every `ok` same-basis block (native or overlay) must reach `SHARPE_MIN_DAILY_RETURNS` (imported from S2a; candidate below it is NOT_EVALUABLE with a reason, an `ok` block below it raises); an unknown candidate status string raises; candidate moments with raw kurtosis < 1 + skew^2 raise. Tests: 52 passed in the S2b-2a file; 387 passed across it, the S2a tests and every test importing `deflate_sharpe`.

### S2b-2b built

Flag wiring under `orchestrator.profit_bars_v2` (`run_phase1_research.py`): P1 writes the `whole_test` block (`_whole_test_ledger_block`, never raises: not_evaluable / error are recorded in the block and the row still counts in N); the bar rows, the ledger block and the DSR build their chain in one place (`_whole_test_chain`); the DSR row (basis `deflated_sharpe_whole_test_daily_on_campaign_trial_ledger`) calls S2b-2a's `compute_dsr_whole_test` / `select_same_basis_sample` for branch 3, the grid and the spend. The legacy evaluator and its sparse branch are no longer called on those paths. `dsr_basis` gains `sharpe_basis`, `n_same_basis`, `min_same_basis`, `basis_overlay {present, sha256}`. The spend refuses a `sharpe_basis` mismatch. `dsr_min_same_basis_trials: 10` is added to the bars file (unsigned). The file's LF blob sha256 changed from `357cab76...` to `4a75ed66...`.
Review items: (a) the overlay is read only through `TRIAL_SHARPE_BASIS_OVERLAY_PATH`, hashed from the bytes it parses, absent recorded as absent. (b) Lockstep: the candidate's own row must carry a block equal to the recomputed stats (status and all four values), and it must sit in the same-basis sample; a dedup collapse raises. The sample N must equal the pipeline's n_dsr_total. (c) decide_next is not changed: under D-046 the v2 DSR is NOT_EVALUABLE only when N < 2, or when the candidate's own chain fails, in which case sharpe_min is NOT_EVALUABLE too and R1 already reads `fired_before`. Nothing waits on K.
Tests: `tests/test_e062_s2b2b_dsr_wiring.py` 35 passed; 8 of 8 hand mutations killed. Declared changes: `test_e062_s2b1_profit_bars_v2.py` (DSR basis, v2 key, block on seeded rows) and `tests/conftest.py` (sandbox the overlay constant).
Guesses: a collapse raises even onto an earlier row that has an ok block. A retried protocol_execution whose results differ from the first attempt's row raises at grading. An `error` block fails grading loud (G10).
Round-1 review fixes (supersede the Guesses line above): a condition a normal run can hit never raises out of grading, it makes THAT variant's DSR row NOT_EVALUABLE with a specific reason and touches no other variant nor K. (1) dedup collapse (onto an ok-block or a block-less earlier row) -> reason `dedup_collapse: <earlier trial>`; (2) an `error` block on the candidate row -> the block's own reason; (3) recomputed stats or status differ from the frozen ledger row -> `ledger_stats_mismatch` naming the fields (malformed rows / blocks / basis still raise); (4) decide_next `_classify_block_set` returns `fired_before` whenever `dsr_basis` carries `sharpe_basis`, ahead of the legacy n_trials rule; (5) the spend path also turns `yaml.YAMLError` (overlay) into the classified refusal, the "three v2 keys" docstring is the four keys it is, and a two-variant test shows one variant NOT_EVALUABLE while the other is graded normally.
