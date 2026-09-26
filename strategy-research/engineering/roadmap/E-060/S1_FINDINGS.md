# E-060 S1 — Characterize composition (delivery_plan_v26.md slice 7)

**Status:** characterize-and-STOP. Read-only: no code, no config, no backtest was run.
Measured on `master` at `aa71afa7` (2026-09-26), Git Bash `grep -n` / `sed -n` on this
Windows checkout. Line numbers are from that commit; re-grep before editing.
The holdout store was not opened.

Target: roadmap v27 cards A and F, `delivery_plan_v26.md` slice 7 (L401-445) with its
2026-09-19/20 corrections (own epic E-060, not E-044; no E-048 gate; any validated block is
usable on any coin; the standardisation op is applied when combining), and the E-060 row of
the artifact table (L499).

---

## Guesses for the operator

Each is a design choice the target and the plan do not settle. I checked cards A/F, the plan,
the roadmap review of 2026-09-18 and the E-056/E-058/E-059 findings first; where they answer,
the answer is used, not asked.

1. **There is no single "standardisation op".** `zscore` and `ratio_to_mean` both throw away
   whatever the block's own pipeline did before them, so putting one in front of a validated
   block changes the block. Proposal: leave each block's pipeline as validated and add one
   `scale` step at its end, with a factor computed by code from the block's own validated
   bars so that, on bars where it speaks, its average size is 10 (the design guide's §5
   convention). Existing op, no engine change, no E-048. — **blocks the build**
2. **The three weighting formulas are not written anywhere.** Proposal: equal = 1/N;
   volatility-scaled = 1/σ of the block's stand-alone daily portfolio return in the run that
   validated it; IC-weighted = the block's residual IC from the registry. Code computes the
   numbers and puts them in the brief; 1b only places them. — **blocks the build** (S3 only)
3. **Blocks tested on different timeframes.** The registry stores no timeframe; a 500-bar
   window means different things on 1h and 1d. Proposal: one composite per timeframe, made
   only when that timeframe has at least two blocks. — **blocks the build** (S3 only)
4. **"Current composite" for residual IC.** No block yet: no composite, a block's residual
   IC is simply its IC. One block: that block's own tested config. Two or more: the
   equal-weight variant of the composition run made for the current registry; if that run
   has not happened yet, the residual-IC cell is INCONCLUSIVE ("composite is stale"). —
   default is safe to build on
5. **Where the composite forecast is measured.** On the candidate's own coins and windows,
   cached by (registry revision, composite config hash, coin, window). It never reaches the
   holdout, it is not a trial and it is not checked against the profit bars (the same config
   was already graded in its own run). — default is safe to build on
6. **Residual IC is required for every forecast-block idea**, added by code, not left to
   1a's choice (card A says a block *must* hold information). Threshold: a placeholder
   (`> 0.01`, at least 30 effective samples), marked unratified like `profitability_bars.yaml`
   was. You ratify it before switching the flag on. — default is safe to build on
7. **An exact duplicate block fails; it is not "inconclusive".** Its residual has no
   variance, so the IC is undefined; the cell records `fully_explained: true` and FAILs.
   No fake 0.0 is written. — default is safe to build on
8. **IC flavour.** Rank IC over all bars (not only bars where the block speaks), residual
   from a per-coin least-squares fit with intercept, pooled over coins, effective sample
   size = gap-aware one-day blocks summed over coins (the existing helpers). — default is
   safe to build on
9. **How "criteria = the profit bars" reaches the grid.** A new grid criterion type
   `profit_bars`, allowed only in composition runs, whose cell is the result of the same
   grading function branch 3 already runs. One computation, so the grid and branch 3 cannot
   disagree. — default is safe to build on
10. **When R1 runs.** Ahead of every agent candidate, reader proposal, extra card and R2
    request; behind a run already in progress and behind your own ready entries (6b
    decision 4). Once per registry revision; a composition run that crashes pauses for you
    instead of retrying in a loop. — default is safe to build on
11. **A composite is never a block.** It does not register (registering would change the
    registry and trigger R1 forever). The composition run writes a composition manifest, not
    a block manifest. — default is safe to build on
12. **The three composition variants are written by code**, not by the innovation-expansion
    LLM: the only difference between them is the weights, which code already computed. —
    default is safe to build on
13. **Regime blocks (7.4) as their own later story.** "Gated beats ungated" needs a grid cell
    that compares column B with column A, which the grid cannot do today, plus a definition
    of "beats" and of the label's health check. Proposal: B's portfolio Sharpe is higher
    than A's and B's worst drawdown is no worse; every label B uses is `informative` in
    `metrics.json`. Build it after the first composition run. — **blocks the build** (7.4
    only)

---

## 1. The standardisation op (item 1)

**Settled earlier?** No. Slice 3 (E-056) did not settle it. E-056 S1 recorded the gap and
stopped: "None of the 15 does cross-component forecast standardization/scaling ... `zscore`
is per-component-history-only ... the design guide ... will need to state explicitly rather
than assume" (`engineering/roadmap/E-056/S1_FINDINGS.md:71-76`). The design guide has no
composition section (`docs/STRATEGY_DESIGN_GUIDE.md` §7a-§7e; §7a L372-395 says the
instrument question "depends on composition work (Slice 7)"). The roadmap review records the
operator's intent only: "apply the existing standardisation op"
(`roadmap_review_2026-09-18.md:108-113`).

**What the engine does** (`trading-bot/strategies/strategy_engine.py:137-162`): per regime,
`ensemble = Σ (weight/Σweights) × apply_transform_pipeline(history, transforms)`, clipped to
±20. Weights are normalised **inside one regime**; blocks in different regimes never add up.

**The candidate ops** (`trading-bot/strategies/registry.py`):
- `zscore` (L56, `_safe_zscore` L26-28): (latest − mean)/std of the component's raw history.
- `ratio_to_mean` (L57, `_ratio_to_mean` L31-33): latest / mean(|history|) — Carver's forecast
  scalar; keeps sign and keeps zeros at zero. The production example uses it
  (`STRATEGY_DESIGN_GUIDE.md` §5 L292-304: `[ratio_to_mean, scale 10, threshold_filter 15]`,
  "≈ average signal = 10").
- Both are **history-based**: they "recompute from the full series `h`, ignoring `v`"
  (registry.py L40, warning L44-47: "Writing [scale, percentile] silently throws away the scale
  output"). `apply_transform_pipeline` (L90-112) runs ops in order on one value.
- The component-level `standardized_forecast` machinery
  (`strategies/strategy_base.py:95-215`) is dead code on the live path — its own docstring
  (L154-170) says the config-driven engines never call it.

**Is it sufficient?** Not as "insert the op". Consequences measured from the code:
- A block whose pipeline already starts with `percentile`/`ema`/`ratio_to_mean` would have
  that op *replaced* by an inserted `zscore` or `ratio_to_mean` (only the last history op
  counts). A `percentile` block (output 0..1, never negative) becomes a signed signal: a
  different block from the one validated.
- `zscore` de-means. A sparse block (e.g. `FundingRateMeanReversionComponent`, non-zero only
  at 8h settlement bars, design guide L213-218) turns its zeros into small non-zero values:
  an always-on signal with different turnover.
- `ratio_to_mean` over all bars inflates a sparse block by 1/activity (a 1-in-8 signal comes
  out ≈ 8× larger when active), then the ±20 ensemble clip lets it dominate.

**Proposal (guess 1):** keep each block's validated pipeline and append
`{"op": "scale", "params": {"factor": k_b}}` (a scalar op, legal after any history op).
`k_b = 10 / mean(|post_pipeline_value|)` over the block's **active** bars in its validating
run's base variant, read from `bars.csv` column
`debug_info.components.<id>.post_pipeline_value` (see §2 — the column exists). The block is
then unchanged up to a positive constant (sign, zeros and turnover preserved). Code computes
`k_b` and writes it into the brief; 1b appends it; 5a checks it. Lookahead note: `k_b` is
estimated on the block's validation windows, which may overlap the composite's windows. It
is a positive constant that changes only relative weights, never a sign; the composite's
own profit-bar grading is the check (card F). If a reader later finds the scale wrong, that
is the card-F route to E-048.

## 2. Composite forecast cache (item 2)

**What the engine writes per bar.** `bars.csv` is the flattened per-bar state
(`core/backtester.py:432-434` → `flatten_dict_columns`, `execution/portfolio_info.py:400-412`;
written at `core/backtester.py:637-639` → `reporting/run_artifact.py:190-191`). The state row
is `{**last_bar, **StrategyOutput fields, **extras}` (`execution/portfolio_info.py:467-480`),
so it carries:
- `forecast` (the final, clipped ensemble forecast) and `regime`, `timestamp`, `close`;
- per component: `debug_info.components.<id>.{last_history_value, post_pipeline_value,
  weight_normalized, weighted_contribution}` (produced by `strategy_engine.py:156-161`,
  header measured on `runs/run_011/results/20260625T223518Z_2754e184/bars.csv`).
`portfolio_states.csv` holds the same rows plus equity (the profit bars read its
`postRebalance_total_value`, `config/profitability_bars.yaml:38-42`).

So a forecast column exists, and per-block contributions exist for free inside a composite
run. `tools/build_reports.py::_parse_component_columns` (L561-573) already parses the
component columns; reuse it.

**How to read a series.** `tools/run_protocol.py::_assemble_pooled_symbol_records`
(L1321-1384) already pools one symbol's `bars.csv` across its windows (via
`protocol_result.results[*].run_id`), with `forecast`, `next_return_bps`, `active`,
`timestamp`. The residual-IC reader should reuse it (or a sibling that also returns the
timestamps as keys) rather than build a third record builder.

**Producing the composite series (guess 4, 5).** Resolver `current_composite(registry,
compositions)`:
- revision 0 → none;
- revision 1 → the single block's `source_config_ref` (`tools/block_registry.py:208`; a
  runnable, tested config);
- revision ≥ 2 → the base (equal-weight) variant config of the composition run recorded for
  that revision; none recorded → `STALE`.

Cache: `campaign_record/composite/<registry_revision>_<config_sha8>/<symbol>/<window>/bars.csv`
plus `composite.yaml {registry_revision, registry_sha256, config_ref, config_sha256,
source_run}`. A cache miss runs the composite config through the same engine
(`core/launcher.py::run_backtest`, L587) on exactly the candidate's (symbol, window). It
inherits the candidate's windows, which the data policy already admitted, so it cannot reach
2026-H1. It writes no trial row and is not a branch-3 candidate.

## 3. residual_ic (item 3)

**Reusable pieces** (`trading-bot/performance/signal_statistics.py`): `spearman_correlation`
(L68), `pearson_correlation` (L45, returns None on zero variance — the file's HARD RULE,
L1-27), `gap_aware_active_block_count` (L154-185), `block_adjusted_pvalue` (L188-211, returns
`(p, n_eff)`), `pooled_block_adjusted_significance` (L525-598). `run_artifact.py:375-404`
already computes an all-bars IC with gap-aware n_eff the same way (block size
`86400 // candle_interval_seconds`).

**Computation (guess 7, 8)** — new pure module `strategy-research/tools/residual_ic.py`:
1. per symbol, inner-join candidate and composite records on timestamp (bars missing on
   either side dropped and counted);
2. OLS `f_cand = a + b·f_comp + e` (composite with zero variance → `b = 0`, residual = the
   de-meaned candidate: well defined);
3. `residual_ic = spearman(e, next_return_bps)` pooled over symbols; `n_eff` = Σ per-symbol
   gap-aware all-bar block counts; p via `block_adjusted_pvalue`;
4. candidate zero variance → `None` (INCONCLUSIVE); residual variance ≈ 0 while candidate
   variance > 0 → `value: None, fully_explained: true` → FAIL (guess 7).
Also returns `correlation_to_composite = pearson(f_cand, f_comp)` for the registry.

**Into the grid.** The grid reads only `protocol_result` dicts: sources `window|pooled`
(`tools/verdict_criteria_evaluator.py:1055-1056`); pooled values come from
`trade_diagnostics_summary[metric]` or `hypothesis_verdict.diagnostics[metric]`
(`_lookup_metric_value`, L212-238). Proposal: under the flag, protocol_execution computes the
residual IC per variant and injects `hypothesis_verdict.diagnostics.residual_ic = {value,
n_eff, p_value, n_bars, fully_explained, composite}` into that variant's `summary` before
`evaluate_grid` (call site L1783-1797). Menu entry: `{id: residual_ic, metric: residual_ic,
statistic: value, source: pooled, comparator: ">", threshold: 0.01, floor: {min_n_eff: 30},
scale_free: true}` (placeholder, guess 6), replacing the commented block at
`config/criterion_menu.yaml:94-115`.

Two evaluator changes needed:
- `_check_floor` **raises** on `min_n_eff` today (L1211-1231). It must read the n_eff that
  comes with the metric (`diagnostics[metric]["n_eff"]`).
- a `fully_explained: true` value must map to FAIL, `composite: STALE` to INCONCLUSIVE.

**Mandatory (guess 6):** `_write_pass_rule_from_card` (`workflow/run_phase1_research.py:4719`)
appends `{id: residual_ic}` for every forecast-block idea when the flag is on (not for
composition runs, not for regime-block runs).

**First block:** no composite → step 2 is skipped, `residual_ic` = the candidate's own
all-bar rank IC, `composite: none`. Registry: `build_block` writes
`correlation_to_composite`/`residual_ic` as `None` (`tools/block_registry.py:206-207`) and the
schema types them `null` (`workflow_artifacts/schemas/block_registry.schema.json:43-44`).
S2 fills them from the base variant's cell as mappings `{value, n_eff, composite_revision}`
(so the historical basis is explicit) — the field set stays closed, no new key. The registry
file does not exist yet (`campaign_record/block_registry.yaml`: no such file), so there is
nothing to migrate.

## 4. R1 composition brief writer (item 4)

**Where R1 is.** `tools/decide_next.py:1112-1114`:
`"r1": {"registry_revision": revision, "last_composition_revision": None, "would_fire":
revision >= 2, "fired": False, "reason": "composition brief writer is slice 7"}`; docstring
L78. `load_inputs` reads only the registry revision (L651, L709). `decide()` picks, in order:
the scheduler's own entry (in_progress, else lowest-priority ready, L1047-1056), else the
top-ranked eligible candidate (L1057-1073), else R2 (L1074-1089), else stop.

**Proposal (guess 10).** Under the flag, R1 fires when the registry revision is ≥ 2 and no
composition *attempt* exists for that revision (read from a new
`campaign_record/compositions.yaml`: `{revision, timeframe, entry_id, run_id, outcome}`).
Placement: after an in_progress entry and after operator ready entries, before agent ready
entries, candidates and R2. `picked = {composition: <entry_id>, brief_path, why}`. A
composition attempt ending in an engineering fault gives a pause row (RUNBOOK §3
`composition_failed`), never an automatic re-fire.

**Inputs.** `block_registry.yaml` (all blocks, any coin — `symbols_tested` stays
informational, `block_registry.py:205`), `campaign_memory.yaml` (each block's validating run:
`timeframe`, `protocol_ref`, base variant), `config/profitability_bars.yaml`
(`target_instrument_set`, L111-116, today `[BTCUSDT, ETHUSDT]`, unratified). Grouped by
timeframe (guess 3); protocol pin = the `protocol_ref` used by most blocks of the group, tie →
most recent.

**Weighting schemes.** Named only in the target (card F: "equal, volatility-scaled,
IC-weighted"); **no formula exists anywhere** (repo-wide grep for `ic_weighted`,
`vol_scaled`, `inverse_vol`, "weighting scheme": only the roadmap and the plan). Guess 2 gives
the formulas. Blocks sharing a regime share the weights; a sub-strategy block keeps its
internal ratios and is scaled as a unit.

**Brief.** Same path as reader candidates (`candidate_brief`, L1139-1206; registered by
`run_campaign._finish_lineage_with_decision`, `workflow/run_campaign.py:3050-3077`):
`campaign_record/candidate_briefs/composition_r<rev>_<tf>.md`, queue id the same, `origin:
composition` (already in `tools/record_schema.py:133`). Frontmatter adds `composition:
{registry_revision, registry_sha256, timeframe, instrument_set, blocks: [{block_id, kind,
config_fragment, regime_assignment, source_config_ref, scale_factor}], schemes: {equal,
vol_scaled, ic_weighted: {block_id: weight}}}` and `candidate.criteria_from: profit_bars`.

## 5. 1b composition mode and the 5a checks (item 5)

**1a.** IMPROVEMENT 08 pass-through needs all four of `config, manifest, criteria, source`
(`workflow_artifacts/skills/hypothesis-design/SKILL.md:383-396`); a composition brief has no
config, so it is not an IMPROVEMENT-08 pass-through. New section (IMPROVEMENT 09): copy the
composition block through, criteria = `[{id: profit_bars}]`, write no hypothesis of its own.

**1b.** New design-guide §7f + a `strategy-config-authoring/SKILL.md` section: assemble the
listed fragments into regimes/sub-strategies, use the ungated pattern (§7e, L503-540) unless a
regime block is listed, set the equal-scheme weights, append each block's `scale` step, invent
no component. Output: the base config plus `artifacts/composition_manifest.yaml`
`{registry_revision, blocks: {block_id: [json pointers]}, scaffolding, rationale}` instead of
`block_manifest.yaml` (guess 11).

**Variants (guess 12).** Code writes `variant_patches.yaml`: `base` = equal, `vol_scaled`,
`ic_weighted`, each a patch of the weight pointers from the manifest. Per-variant trial ids
(`run_NNN:<variant>`) already exist.

**5a** (`workflow/run_phase1_research.py:1903-1954`, the tool-only `backtest_specification`
branch, which today checks `block_manifest.yaml` at L1942-1951). Under composition, instead:
every brief block id present; each block's component spec equal to its registry fragment
except `weight`, an `id` rename, and exactly one appended `scale` whose factor equals the
brief's `k_b` (relative tolerance 1e-9); per regime, normalised weights equal the scheme's
within 1e-6; no component outside blocks and scaffolding. Per variant, the same weight check
against that variant's scheme.

## 6. Regime blocks, 7.4 (item 6)

**A2.3 lives in:** `hypothesis-design/SKILL.md:160-172` (and L199, L426, checklist);
`innovation-expansion/SKILL.md:3, 32, 59-72, 315`; the ungated pattern in
`strategy-config-authoring/SKILL.md:153-155` and `backtest-engineering/SKILL.md:151-155`.
decide_next marks every regime-block proposal infeasible today:
`regime_block_needs_composition` (`tools/decide_next.py:802-805`).

**Card F:** variant A = the blocks ungated, B = the same blocks gated by the detector;
criterion "B beats A on the bars while the label passes its health checks". So a regime idea
needs at least one registered forecast block, and the lift of A2.3 applies to briefs of
origin `composition` **and** to regime-block candidates (both are composition-style runs).

**Gaps.** The grid is criteria × variants with each cell independent
(`evaluate_grid`, `verdict_criteria_evaluator.py:1455-1560`); a B-versus-A cell does not
exist, and a cell A marked INCONCLUSIVE would make the idea inconclusive (L1546-1548), so A's
cell needs a new `NOT_APPLICABLE` result excluded from the roll-up. "Health": the
`regime_power` report's detector health is a campaign-level file, not per run
(`tools/build_reports.py:479-497`); the per-run signal is `metrics.json` `regime_validity`
(`reporting/run_artifact.py:635-656`, `informative` = |mean forward return| ≥ 1e-4). Guess 13.

## 7. Grading composites (item 7)

- **Grid:** criteria = profit bars through the new `profit_bars` source (guess 9). Today a
  run with no menu-shaped criteria makes `evaluate_grid` raise (L1506-1512) and the grid is
  simply not written (L1801-1810), so this is required, not optional. Order issue: the grid
  is written inside protocol_execution (L1783-1797) and branch 3 grades "right after
  protocol_execution" using the grid's columns (`_profit_bars_backtest_candidates`,
  L9389-9427). Fix: the grid cell calls the same grading function per variant (pure given
  the variant's result files), and branch 3 keeps its own pass — same inputs, same answer;
  a test pins them equal.
- **Profit bars / branch 3:** the seam note (L9409-9413) asks for a `kind: "composite"`
  candidate. A composition run's variants *are* the composite backtests, so the seam change is
  one label: `kind: "composite"` for variants of an `origin: composition` run. The equal-weight
  portfolio across the target set and the stop rule are unchanged; a passing composite raises
  `profit_bars_reached`, and the holdout is reached only through the operator unlock (6c S2d).
- **Registry:** `block_registry.record_run` would print the loud `no_manifest` warning
  (`tools/block_registry.py:270-277`) for a validated composition run; add `skipped:
  composition` and never register (guess 11).
- **7.5 feedback:** reader proposals from a composition run go through decide_next like any
  other, but a patch proposal is INFEASIBLE today with `source_manifest_missing` because the
  source run has no `block_manifest.yaml` (`decide_next.py:773-775`). A composition source
  must be accepted with its composition manifest. Otherwise the route is already built; E-048
  starts only from such a proposal.

## 8. Test feasibility (item 8)

There is no `ANTHROPIC_API_KEY` and the registry is empty (`campaign_record/block_registry.yaml`
and `campaign_memory.yaml` do not exist on this checkout). What fixtures can prove:
- **Pure, fast:** residual IC on synthetic series (independent signal → IC close to its
  planted value; exact duplicate → `fully_explained` FAIL; duplicate + noise → near 0;
  constant candidate → INCONCLUSIVE; gaps and missing bars on one side; two symbols pooled);
  composite resolver for revisions 0/1/≥2/stale; weight formulas; scale factor from a
  synthetic `bars.csv`; R1 on a synthetic registry (fires at 2, once per revision, behind
  operator entries, ahead of candidates and R2, timeframe grouping, fault → pause); 5a
  composition check (pass; missing block; weight off by 1 %; extra component; changed params;
  wrong scale factor); grid `profit_bars` cell equals branch 3 on the same inputs; min_n_eff
  floor.
- **Slow, real engine, no LLM:** the composite cache on a hand-written two-component config
  over a short train-period window of the local `BTCUSDT_1h.csv`, proving the forecast and
  component columns are read and the cache key is stable. Not a trial; temp root.
- **Stubbed end-to-end:** canned 1a/1b outputs (card, config, composition manifest) through
  the real 5a, variant build and a real short backtest, under a temp ROOT, as the existing
  stubbed-run_loop tests do.
- **Flag-off identity:** decision_record (R1 text unchanged), pre_registration,
  grid_evaluation, idea_status, block_registry, campaign_queue — byte-identical.
- **Cannot be proven here:** what the LLM does in 1a/1b composition mode, and S4 itself. S4
  needs two blocks validated by real runs (1a, 1b, readers are LLM stages), so it waits on the
  API key and on real validated ideas. The registry must not be seeded by hand: a block's
  status comes only from the grid.

---

## Proposed split (per the E-060 row)

- **S2 · Registry + residual-IC criterion** (guesses 4-8). `tools/residual_ic.py`;
  `tools/composite_cache.py` (resolver + cache + engine call); evaluator: `min_n_eff` from the
  metric, `fully_explained`/`STALE` mapping; menu entry `residual_ic` (placeholder
  threshold); mandatory append in `_write_pass_rule_from_card`; injection before
  `evaluate_grid`; registry fills `residual_ic`/`correlation_to_composite`, schema
  `null | object`; flag, register entry, identity tests. Run budget 0.
- **S3 · Composition brief writer + 1b composition mode + 5a checks** (guesses 1-3, 9-12).
  R1 in `decide_next.py` + `compositions.yaml` + registration in `run_campaign.py`; weights
  and scale factors; 1a IMPROVEMENT 09; design guide §7f + 1b skill section; code-written
  variant patches; 5a composition-manifest check; grid `profit_bars` source; `kind:
  composite` label; registry `skipped: composition`; decide_next accepts a composition
  source (7.5); RUNBOOK `composition_failed`; USER_GUIDE/CLAUDE.md/DOC_INDEX. Run budget 0.
- **S4 · First composition run.** Run budget 1, blocked until two real blocks validate.
- **S5 (proposed, new) · Regime blocks (7.4).** A2.3 lift for composition-style briefs,
  regime candidates feasible when a forecast block exists, grid `NOT_APPLICABLE` cell and
  comparison criterion `gated_beats_ungated`, health check. After S4 (guess 13).

## Flag design

`orchestrator.composition_runs.enabled` in `config/campaign_config.yaml`, default `false`,
read by `run_phase1_research._composition_runs_enabled()` (strict boolean, same idiom as
`_profit_bars_every_backtest_enabled`, L2211-2258) and registered in
`config/feature_flag_register.yaml` (`state: off_incomplete`). Hard dependencies (raise, do
not no-op): `decide_next` (hence regroup_record, specialist_readers, grid_evaluation,
category_reports, config_direct_authoring), `variant_loop`, `profit_bars_every_backtest`
(hence profit_bars_file) and `verdict_routing_retired` — without the last, a composition run
could reach refine/pivot routing, which must never be fed. One flag covers S2 and S3; S5
takes its own (`orchestrator.regime_blocks.enabled`) because it lifts a standing skill rule.
Off: nothing new is read or written, R1 keeps its current text.

## Tests (summary)

New files, one per story: `tests/test_e060_s2_residual_ic.py`,
`tests/test_e060_s2_composite_cache.py` (one slow), `tests/test_e060_s3_composition_brief.py`,
`tests/test_e060_s3_composition_manifest.py`, `tests/test_e060_flag_off_identity.py`; plus the
existing gates `tests/test_feature_flag_register.py`, `tests/test_guide_covers_the_code.py`,
`tests/test_doc_anchors.py`, and the E-059 decide_next tests unchanged flag-off.

## Paste-ready for Linear (E-060 S1)

S1 done (characterize only). Findings: `strategy-research/engineering/roadmap/E-060/S1_FINDINGS.md`.
No single standardisation op exists (zscore / ratio_to_mean replace a block's own pipeline);
proposal: append a code-computed `scale` step per block. Weighting formulas and a timeframe
rule are undefined in the target; proposals given. Residual IC buildable from existing
helpers; the evaluator's `min_n_eff` floor raises today and must be wired. R1 is a recorded
no-op at `decide_next.py:1112-1114`. Composites never register as blocks. S4 is blocked until
two real blocks validate (registry empty, no API key). Proposed S5 for regime blocks.
