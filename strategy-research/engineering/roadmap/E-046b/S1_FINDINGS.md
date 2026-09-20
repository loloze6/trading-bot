# E-046b S1 — Findings (characterize-and-STOP)

Read-only. No code, config, or backtest runs executed. `local_data/holdout_sealed/` was not opened.

## 0. Worktree staleness — read BEFORE trusting anything below

This worktree's HEAD is `8bfcd0b6`. The dispatch's source files
(`strategy-research/engineering/roadmap_review_2026-09-18.md`,
`engineering_roadmap.html`, `delivery_plan_v26.md`) **do not exist in this
worktree** — they do not exist at any commit reachable from HEAD
(`git log --oneline --all -- strategy-research/engineering/engineering_roadmap.html`
returns only `844e6a17`, which sits on `master`/`fix/cul-275-…`, not on this
worktree's branch; `git merge-base --is-ancestor 844e6a17 HEAD` → false).
`master` (the branch named in this session's git-status context, tip
`a20fb7ec`) does carry them; `844e6a17 IS ancestor of a20fb7ec` confirmed.

Separately and more importantly: `git diff HEAD a20fb7ec -- strategy-research/tools/run_protocol.py`
shows **57 insertions / 9 deletions** — this worktree's copy is stale on the
one file S2 will edit. The diff repoints `_pooled_ic_with_bootstrap_fallback`
/`_assemble_pooled_symbol_records` from the removed `prescreen_signal.py` to
`trading-bot/performance/signal_statistics.py`, and — load-bearing for task 3
below — **adds `_era_id_for_timestamp` and `_load_campaign_data_policy` as
local functions** (they did not exist in this worktree's copy at all).
`strategy-research/tools/verdict_criteria_evaluator.py` is byte-identical
between HEAD and `a20fb7ec` (empty diff) — that file's findings below are
read directly from the worktree. Everything else below was read via
`git show a20fb7ec:<path>` (non-destructive, no checkout performed) because
that is the only place the content exists. **Before S2 starts, whoever
provisions its worktree needs `run_protocol.py` at `a20fb7ec` or later, not
at this HEAD**, or the new `_era_id_for_timestamp` seam task 3 relies on
won't be there to reuse.

---

## 1. `verdict_criteria_evaluator.py` — current criterion shape

Read end to end (`strategy-research/tools/verdict_criteria_evaluator.py`, 926 lines).

**Criterion dict fields actually read**, all in `_evaluate_one_criterion`
(L217-276) and `_lookup_metric_value` (L188-214):

| field | read at | meaning |
|---|---|---|
| `metric` | L218, L196 | key name to resolve |
| `comparator` | L219, `_VALID_COMPARATORS` L51 `(">=", ">", "<=", "<", "==")` | applied by `_apply_comparator` L174-185 |
| `threshold` | L265 (pooled) / per-symbol dict L227 | scalar (pooled) or `{symbol: threshold}` (per-symbol) |
| `per_symbol_threshold` | L224, L227-263 | if present, evaluates once per symbol key, ANDs results (any FAIL → overall FAIL) |
| `null_handling` | L225, L233/268 | only value ever seen in the corpus is `"fails_threshold"` (L233, L268 handle it explicitly); anything else with a null value → `SPEC_ERROR` |
| `statistic` | L201, L205-206, L211-212 | sub-key into a dict-valued pooled metric (e.g. `{"mean": ..., "median": ...}`); only real usage found is a test fixture, `tests/test_k2_verdict_machinery.py:72` — **no run in the corpus uses it** |
| `id` | L221, L847 | criterion label, echoed into the result and into `branches_failed` (`FAIL-{id}`) |

**`_lookup_metric_value` (L188-214) resolution order** — this is the entire
resolvable-metric universe today, and it is flat (no per-window access):

1. If `symbol is not None` (i.e. `per_symbol_threshold` was used): reads
   `protocol_result["per_symbol_summary"][symbol][metric]` only. No fallback.
2. Else (pooled): tries `protocol_result["trade_diagnostics_summary"][metric]`
   first, then falls back to
   `protocol_result["hypothesis_verdict"]["diagnostics"][metric]`. If the
   resolved value is itself a dict and `statistic` is set, sub-keys into it;
   otherwise returns the dict/scalar as-is. Returns `None` if neither source
   has the key — the null-handling branch then decides FAIL vs SPEC_ERROR.

**It never reads `protocol_result["results"][*]["core"][metric]` (the raw
per-window rows) at all.** Every metric it resolves is something
`run_protocol.py` already pre-aggregated. This is the key gap task 3's new
`reducer` field has to fill — median/mean/fraction_above/etc. over windows is
new code, not a reuse of this lookup path.

**Every metric name resolvable today**, from the corpus measured in task 2
below (union of `per_symbol_summary`, `trade_diagnostics_summary`,
`hypothesis_verdict.diagnostics` keys) — 4 + 10 + 9 = 23 names, 3 of them
duplicated across sources (`zero_trade_slot_pct` in all three shapes;
`per_trade_expectancy_bps` in two):

`median_sharpe`, `max_abs_drawdown_pct`, `min_trade_count`,
`zero_trade_slot_pct` (per_symbol_summary, L2101-2106) · `entry_efficiency_median`,
`exit_efficiency_median`, `exit_reason_breakdown`, `holding_period_distribution`,
`mae_mfe_ratio_median`, `per_trade_expectancy_bps`, `pnl_concentration`,
`stop_loss_recovery_rate`, `win_rate_net` (trade_diagnostics_summary, measured
on run_059) · `below_floor_pct`, `median_avg_trade_duration_bars`,
`median_cost_drag_pct`, `median_forecast_return_corr`, `median_gross_pnl`,
`uninformative_regimes`, `win_rate_vs_sharpe` (hypothesis_verdict.diagnostics,
same run).

Everything else in `verdict_criteria_evaluator.py` (G1-G6 preconditions,
`resolve_evaluation_ref`, `honest_verdict_count`, the closed-schema G6 gate)
is orthogonal to the grid — it gates whether a verdict may be RECORDED at
all, not how one is computed, and none of it needs to change for `evaluate_grid`.

## 2. `run_protocol.py` — the full universe of addressable fields

Measured directly on `strategy-research/runs/run_059/artifacts/protocol_result.yaml`
(chosen: newest run in the corpus with a populated `results` list — `run_060`
was prescreen-killed with an empty `results: []`, confirmed by loading it).
This is the same run the existing roadmap review cites ("98 windows × 14 core
metrics", `roadmap_review_2026-09-18.md` Part 1 table row 4) — reproduced
independently here: **98 windows, 14 core keys per window.**

**(a) `results[i]["core"]` keys (14)** — sourced from `trading-bot`'s
`metrics.json["core"]`, assigned at `run_protocol.py:2017,2028` (master
version; this worktree lacks the file's tail, but this section of the file
is unchanged in the diff):

```
avg_trade_duration_bars, avg_trade_net_pnl, cost_drag_pct, fees_paid,
forecast_return_corr, forecast_return_corr_pvalue, gross_pnl,
max_drawdown_pct, net_pnl, net_return_pct, sharpe, sharpe_annualization,
trade_count, win_rate
```

`result_entry` (L2024-2042) also carries `symbol`, `window`, `run_id`,
`per_regime`, `regime_validity`, `data_quality` as siblings of `core` — not
metrics, but available for symbol/window/regime-keyed reducers.

**(b) `per_symbol_summary` keys (4)**, built at L2101-2106:
`median_sharpe`, `max_abs_drawdown_pct`, `min_trade_count`, `zero_trade_slot_pct`.

**(c) `trade_diagnostics_summary` keys (10)** and **`hypothesis_verdict.diagnostics`
keys (9)** — listed in full in task 1 above (measured on the same run_059 load).

Top-level `protocol_result.yaml` keys on run_059: `config_sha256`,
`hypothesis_verdict`, `per_symbol_summary`, `prescreen_backtest_cross_check`,
`protocol_file`, `protocol_run_id`, `results`, `trade_diagnostics_summary`,
`verdict`, `verdict_reason`.

## 3. Proposed criterion record shape and reducers

Record shape as specified in the dispatch is directly buildable from what
exists:

```
{id, metric, source: window|pooled, reducer: median|mean|min|max|
 fraction_above|sign_consistent_by_era, reducer_arg, comparator, threshold,
 floor: {min_windows|min_trades|min_n_eff}, scale_free: true,
 symbol_reducer: null|per_symbol_all|pooled}
```

- `source: window` + a reducer → operates on `results[*]["core"][metric]`
  (task 2a's 14 names), one list per (variant, symbol). This is the NEW
  capability `_lookup_metric_value` doesn't have.
- `source: pooled` → same three-source lookup `_lookup_metric_value` already
  does (per_symbol_summary / trade_diagnostics_summary /
  hypothesis_verdict.diagnostics) — no reducer needed, the value is already
  aggregated; `reducer` should be `None`/unset for these.

**Reducer pseudocode** (over `values = [core[metric] for w in windows]`,
optionally filtered to one symbol first per `symbol_reducer`):

```
median(values)              -> statistics.median(v for v in values if v is not None)
mean(values)                -> statistics.mean(v for v in values if v is not None)
min(values) / max(values)   -> straightforward, None-filtered
fraction_above(values, arg) -> count(v > arg for v in values if v is not None) / count(values, None-filtered)
sign_consistent_by_era(values_with_ts, eras):
    for each window, era = _era_id_for_timestamp(window.timestamp, eras)
    group values by era
    per-era sign = sign(median(era's values))   # or mean, matching the primary reducer
    PASS iff every era's sign is equal AND non-zero (an era with a zero
      median is ambiguous, not a passing sign)
```

`floor` gates the reducer's OWN input count before the comparator ever runs:
`min_windows` → `len(values)` after None-filtering; `min_trades` → sum of
`core["trade_count"]` over the same window set; `min_n_eff` → not resolvable
from anything in task 2's field list — no window or pooled key called
`n_eff` or similar exists anywhere in the corpus survey (see Not Determined).
Under-floor → cell = INCONCLUSIVE, never FAIL.

**`campaign_data_policy.yaml`'s `eras` list** (`strategy-research/config/campaign_data_policy.yaml`)
has exactly the shape `sign_consistent_by_era` needs: 6 entries, each
`{era_id, range: [lo, hi], feeds_available, note}`, e.g.
`era_2019_2023_full_feed: [2019-09-10, 2023-12-31]`. The existing pattern to
reuse, `run_protocol.py::_era_id_for_timestamp` — **this function does not
exist in this worktree's checkout of `run_protocol.py`**; it exists only at
`a20fb7ec` (task 0 above), added 2026-09-12 as a local copy of
`prescreen_signal.py`'s (now-removed) function of the same name:

```python
def _era_id_for_timestamp(ts, eras: list) -> str:
    d = pd.Timestamp(ts).strftime("%Y-%m-%d")
    for era in eras:
        lo, hi = era["range"]
        if lo <= d <= hi:
            return era["era_id"]
    return "era_unmapped"
```

**Bug found reading it, not yet triggered in the corpus:** the last era,
`era_2026_h2_forward_recorded`, has `range: [2026-07-26, null]` — an
open-ended upper bound. `lo <= d <= hi` with `hi = None` raises `TypeError`
in Python 3 (`str <= None` is unorderable) the moment a timestamp reaches
that far without matching an earlier era. No backtest window in the current
corpus can reach 2026-07-26 (holdout is frozen at 2026-06-30 and terminal on
touch), so this has not fired — but `sign_consistent_by_era`'s reducer must
either special-case a `None` upper bound or this WILL crash the first time a
composition/live-adjacent run's window set reaches past the holdout boundary.

## 4. Corpus survey (raw material for `config/criterion_menu.yaml`)

**Denominators**, both counted directly, not estimated:
- `pre_registration.yaml`: 10 files (`run_043,044,047,048,050,053,057,058,059,060`).
  Dict-shaped `pass_rule.criteria`: **3** (`run_058, 059, 060`). Nested legacy
  string (`machine_constraints.pass_rule`, a prose string): **1** (`run_057`).
  Missing entirely: **6**. Matches `roadmap_review_2026-09-18.md`'s "3
  dict-shaped pass_rule" claim — independently reproduced here.
- `verdict_interpretation.yaml`: 39 distinct run-artifact copies (42 files on
  disk, 3 are `*_SUPERSEDED*`/`attempt_2`/`superseded_*` duplicates, excluded).
  `criteria_summary` key present: **37 of 39**. Total individual criteria
  entries across those 37: **104**.

**The 3 dict-shaped `pass_rule.criteria`** use exactly 3 distinct metric
names, none of them scale-free in card B's sense (all are raw, non-IC
thresholds): `median_sharpe` (`> 0.8` per-symbol), `max_abs_drawdown_pct`
(`< 30` per-symbol), `zero_trade_slot_pct` (`<= 40` or `<= 50` per-symbol,
inconsistent between run_058/059 — same criterion, different threshold, no
stated reason found in either file).

**`verdict_interpretation.yaml`'s `criteria_summary`** is LLM-narrated prose,
not structured data — `criterion` is a free-text string
(`"criterion_b: max_abs_drawdown_pct < 30% for BOTH symbols"`), only
sometimes prefixed `criterion_<label>:` (5 of 104 entries followed that
convention cleanly enough to regex-extract a label; the rest are unlabeled
prose). Scanning snake_case tokens across all 104 entries' `criterion` text
for candidate metric names (frequency, token): `trade_count` (5),
`max_drawdown_pct` (5), `regime_frequency` (4), `min_trade_count` (3),
`forecast_return_corr`/`forecast_return_correlation` (3), `ic_all_bars` (1),
`ic_active_bars` (1), `edge_to_cost_ratio` (1), `median_sharpe_gated_bars` (1),
`per_episode_expectancy` (1), `forward_return_mean` (1),
`prescreen_ic_gate`/`prescreen_cost_gate` (1 each). This is weak evidence
(prose, not a schema) but it independently corroborates that
`edge_to_cost_ratio` and IC-based criteria are real historical vocabulary,
not an invented addition — relevant to task 4's requested seeding of
`edge_to_cost_ratio` (0.3) into the menu v1 draft.

## 5. Grid aggregation contract (pseudocode)

Reading card C (`engineering_roadmap.html`, `order mono">C<` block,
`.desc` text) again:

```
for idea in ideas:
  for criterion in idea.criteria:            # rows
    for variant in idea.variants:            # columns (≤4, task says cap 4)
      windows = variant.windows_for(criterion.source)   # symbol_reducer applied here
      n = floor_count(windows, criterion.floor)
      if n < criterion.floor.min_*:
        cell[criterion, variant] = INCONCLUSIVE
        continue
      value = apply_reducer(criterion.reducer, windows, criterion.metric, criterion.reducer_arg)
      cell[criterion, variant] = PASS if apply_comparator(criterion.comparator, value, criterion.threshold) else FAIL

  # idea-level status by UNANIMITY (card C: "the idea is validated only if
  # every criterion holds on every variant")
  all_cells = flatten(cell[*, *])
  if any(c == FAIL for c in all_cells):
      idea.status = REFUTED
  elif any(c == INCONCLUSIVE for c in all_cells) and no FAIL present:
      idea.status = INCONCLUSIVE
  else:
      idea.status = VALIDATED
```

**The tie-break the dispatch asks for explicitly** (one cell INCONCLUSIVE,
another FAIL, same idea): **FAIL dominates.** This is the only reading
consistent with card C's own text — "any failing cell with enough data
refutes the idea; any cell under its sample floor makes the idea
inconclusive" states refutation and inconclusiveness as two independently
sufficient triggers, but a real FAIL is evidence the idea is wrong while an
INCONCLUSIVE cell is only a missing measurement; treating a missing
measurement as capable of overriding a positive refutation would let an
under-sampled variant rescue an idea one of its OTHER variants already
disproved. **This is a design decision, not something the source text pins
down explicitly** — flagged for the S2 dispatch to confirm with the operator
rather than silently encode.

## 6. Consumers of `evaluate_pass_rule_criteria` / `pass_rule_evaluation.yaml`

Real (non-test, non-doc) call sites, via grep:

| Caller | file:line | Disposition |
|---|---|---|
| `workflow/run_phase1_research.py` `protocol_execution` stage | L1303 `_vce.evaluate_pass_rule_criteria(summary, _pre_reg_for_eval, _brief_for_eval)`, writes `pass_rule_evaluation.yaml` at L1306 | **Must be repointed** — this is the writer slice 2 targets; delivery plan's own text: add `evaluate_grid` beside the existing function, write `grid_evaluation.yaml`+`idea_status.yaml` when menu-shaped, route through existing `_resolve_verdict_fields` for now |
| `tools/anti_adjacency_gate.py` L225 `runs_dir/run_id/artifacts/pass_rule_evaluation.yaml`, reads `lineage_routing` | **Keep reading legacy shape** for now — delivery plan slice 2 explicitly keeps old routing (`validated→promote` etc.) through the existing binding path until slice 6c |
| `tools/lint_verdict_provenance.py` | reads for provenance-citation checking only (does it exist / resolve), not content shape | Unaffected either way — G6 provenance is orthogonal to what's inside the file |
| `workflow/run_campaign.py` | L849-850, L1058, L1075-1077 — operates on the flag name `pass_rule_evaluation_disagreement`, a human-review trigger, not the artifact's criteria content | Unaffected — doesn't parse criteria |
| `workflow_artifacts/skills/verdict-interpreter/SKILL.md` | L16, L35, L47, L76, L89 — lists `pass_rule_evaluation.yaml` as a REQUIRED LLM-stage input | **Repointed, then deleted** — delivery plan slice 2 docs note: gains `grid_evaluation.yaml` as a required input when present; slice 5b deletes this skill outright (Part 5 operator decision: "delete it. The five specialist readers are the whole explanation layer") |

## 7. S2 build-list proposal (per dispatch item 7 — proposal only, not executed)

1. `evaluate_grid(protocol_results_by_variant, pre_registration, research_brief, menu)`
   in `verdict_criteria_evaluator.py`, beside (not replacing) `evaluate_pass_rule_criteria`.
2. Reducer functions per §3 above, operating on `results[*]["core"][metric]`
   (new) and the existing pooled lookup (reused from `_lookup_metric_value`).
3. `config/criterion_menu.yaml` v1, styled on `hypothesis-design/SKILL.md`
   §A8.6's anchor table (`Signal class | Description | value | Basis`,
   read at L289-295), seeded from §4's corpus survey: `edge_to_cost_ratio`
   (0.3, per dispatch), `residual_ic`, `gated_beats_ungated`,
   `sign_consistent_by_era`, plus the 3 non-scale-free legacy criteria
   (`median_sharpe`, `max_abs_drawdown_pct`, `zero_trade_slot_pct`) explicitly
   marked NOT reusable as idea-criteria under card B (scale-free requirement)
   — they remain valid only as campaign-wide profit-bar checks, a different
   file per card B.
4. `grid_evaluation.yaml` / `idea_status.yaml` writers, wired into
   `run_phase1_research.py`'s `protocol_execution` branch per §6.
5. Pre-registered success signal: re-grade `run_054`, `run_058`, `run_059`
   (delivery plan's own named set) through `evaluate_grid` and diff against
   their recorded `verdict`/`hypothesis_verdict` — calibration only, does not
   alter history.

---

## Not determined

- **CUL-298's actual content.** The dispatch and multiple docs reference
  "CUL-298 merged into E-046b" but Linear tool access is unauthenticated in
  this session — could not read the issue to confirm what it originally
  asked for beyond the roadmap's own paraphrase ("shared-queue item").
- **`min_n_eff` floor source.** No field named `n_eff` or equivalent exists
  anywhere in the task-2 field inventory (core/per_symbol_summary/
  trade_diagnostics_summary/hypothesis_verdict.diagnostics). Either it needs
  a new computed field (e.g. from the bootstrap significance machinery in
  `run_protocol.py`'s `_pooled_ic_with_bootstrap_fallback` /
  `_a851a_episode_significance`, which does compute effective-sample-size-like
  quantities) or the menu simply never uses `min_n_eff` in v1. Not resolved here.
- **Whether the FAIL-dominates-INCONCLUSIVE tie-break (§5) is actually the
  operator's intent** — inferred from card C's text, not confirmed against
  the operator directly (no record of this specific question being asked in
  `roadmap_review_2026-09-18.md`'s Part 4 remarks list).
- **Whether `run_protocol.py`'s divergence (task 0) is the only stale file**
  in this worktree relevant to E-046b/E-056 work — only the two files named
  in the dispatch were diffed against `a20fb7ec`; a full worktree-vs-master
  diff was not run (out of scope for a read-only single-epic characterization).

---

## Paste-ready Linear comment

**E-046b S1 — characterization complete.**

Read `verdict_criteria_evaluator.py` end to end + `run_protocol.py` (from
`master`@`a20fb7ec` — **this worktree's HEAD, `8bfcd0b6`, predates the
roadmap-review commit and is missing 57/9 lines of `run_protocol.py`,
including the `_era_id_for_timestamp` function S2 needs — reprovision S2's
worktree off `master`, not this HEAD**). Measured on `run_059`: 98 windows,
14 `core` keys/window, 4 `per_symbol_summary` keys, 10
`trade_diagnostics_summary` keys, 9 `hypothesis_verdict.diagnostics` keys —
23 unique metric names resolvable today, all pre-aggregated (the evaluator
never reads per-window `core` directly — that's new code for the grid).
Corpus: 3/10 `pre_registration.yaml` are dict-shaped (3 non-scale-free
metrics: `median_sharpe`, `max_abs_drawdown_pct`, `zero_trade_slot_pct`);
37/39 `verdict_interpretation.yaml` carry prose `criteria_summary` (104
entries total) — weak but real corroboration for `edge_to_cost_ratio` and
IC-based criteria as historical vocabulary. `campaign_data_policy.yaml`'s
6-era list fits `sign_consistent_by_era` directly via the existing
`_era_id_for_timestamp` pattern, but that function has a latent `TypeError`
on the open-ended last era (`hi: null`) — unhit today, will fire the first
time a window reaches past 2026-07-26. Full findings, criterion-shape
proposal, reducer pseudocode, grid pseudocode (FAIL-dominates-INCONCLUSIVE
tie-break proposed, not operator-confirmed), consumer disposition table, and
S2 build list: `strategy-research/engineering/roadmap/E-046b/S1_FINDINGS.md`.
Not determined: CUL-298's original text (Linear unauthenticated this
session), `min_n_eff`'s data source.

## Decision (operator's session, 2026-09-20, overnight autonomous) — the FAIL/INCONCLUSIVE tie-break

**Decided: FAIL dominates.** If any criterion cell has enough data and genuinely fails on any variant, the idea's overall status is REFUTED, regardless of whether other cells are INCONCLUSIVE (under their sample floor). INCONCLUSIVE is the overall status only when no cell has failed yet but at least one lacks enough data to judge.

Reasoning: card C's unanimity rule already requires every criterion to pass on every variant for validation — a single genuine failure already breaks unanimity permanently, independent of what any other cell says. "Not enough evidence yet" on one criterion cannot un-fail a criterion that has already failed with sufficient data elsewhere; treating that as merely inconclusive would let a real negative result hide behind an unrelated data gap. This is a reasonable, low-stakes, easily-revisable interpretive call, made to unblock S2 rather than leave the grid's core logic undefined — confirm with Jeremy before this ships, but do not treat it as an open blocker for continuing S1/S2 drafting.

## Independently verified (operator's session): the `_era_id_for_timestamp` None-comparison bug is real

Confirmed directly against `strategy-research/tools/run_protocol.py:1310-1322` on real merged master: `if lo <= d <= hi` where `hi` comes from `era["range"][1]`. `campaign_data_policy.yaml`'s last era (`era_2026_h2_forward_recorded`) has `range: ["2026-07-26", null]` — YAML `null` loads as Python `None`, and `str <= None` raises `TypeError` in Python 3 (no fallback ordering exists). Not yet hit because no backtest window reaches that era. Will fire the first time a composition run or a late-dated protocol window does. Worth a small, standalone ticket before `sign_consistent_by_era` (this project's own reducer) is built on top of it — filed as a follow-up, not yet in Linear.
