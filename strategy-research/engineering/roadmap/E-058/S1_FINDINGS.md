# E-058 S1 — Regroup and record (delivery_plan_v26.md slice 6a): characterize-and-stop

Read-only characterization at `902ca05f` (origin/master). No code, config or backtest
changed. Line numbers are from that commit; function names are the stable reference.
Target design: roadmap v26/v27 cards A, G, H, I, M; `delivery_plan_v26.md` §2 slice 6a
(L332-343), row "9 · regroup + record" (L66), cross-cutting table (L467), E-058 row (L500).

---

## Guesses for the operator (read this first)

Each item is a real choice the target does not already make. The recommendation is what
S2 will build if you say nothing.

1. **Where the block's config piece comes from.** The registry stores "the block's piece of
   bot config" (card A). The only thing that says which part of a config is the block is
   `block_manifest.yaml`, and **nothing writes it today**: the design guide marks it
   "PROPOSED, NOT BUILT" (`docs/STRATEGY_DESIGN_GUIDE.md` §7c) and the config-authoring
   skill says not to write one (`strategy-config-authoring/SKILL.md:126`). So a validated
   idea has no block boundary on disk.
   *Recommendation:* 6a registers a block only when the manifest exists. A validated run
   without one gets a memory note `registry: skipped_no_manifest` and a loud log line, not
   a failure. Separately, as its own small ticket, teach the 1b skill to write the manifest
   (the path checker `_check_manifest_paths` already exists, L7934). Until that ships the
   registry stays empty. The alternative (register the whole base config as the "block")
   would put scaffolding into slice 7's composites, so I advise against it.
2. **Parallel KB write under the flag.** The plan says to "keep `_write_kb_findings_entry`
   writing the legacy KB in parallel". Under the readers flag, that writer **never runs and
   cannot run** (§1.1): it needs `verdict_interpretation.yaml`, and it is called only on
   refine/pivot/escalate routes, which are retired. Reusing it with a fake input would record
   `refuted` as `inconclusive` (its outcome map has no grid words).
   *Recommendation:* add a small new writer, called from `regroup_record`, that adds one KB
   entry per run: `outcome: <idea_status>`, `legacy_schema: false`, and
   `pass_rule_evaluation_ref: runs/<id>/artifacts/idea_status.yaml`. The existing provenance
   check already accepts that file, because it carries `result: PASS|FAIL` (§1.1). The entry
   never merges into, or closes, a legacy entry with the same `hypothesis_id` (so the F09
   reactivation machinery is never touched). This needs one line in the closed KB schema
   (`legacy_schema: FLAG` in `tools/record_schema.py`).
   *Alternative:* skip the KB entirely under the flag and let the memory file replace it.
   The catch is that hypothesis-design still reads the KB, so new results would not reach it.
3. **Old runs in the memory file.** Target: old verdicts are tagged legacy, never cause a
   refusal, and still count as trials. Trials are already counted in
   `campaign_state.trial_sharpes`, and the memory file has nothing to do with that.
   *Recommendation:* no backfill. The memory file holds only runs that pass through
   `regroup_record`. Its header says legacy history lives in `campaign_knowledge_base.yaml`,
   where every entry without `legacy_schema: false` counts as legacy when read (plan §3 row
   "add the marker on read where the file is closed-schema"). *Alternative:* backfill the 60
   old runs as `legacy: true` stubs.
4. **Profit bars (branch 3) in the memory.** Card H says to record after branches 1–3. Today
   the profit-bars check runs only on promote, and only after the route
   (`_dispatch_verdict_route` L7414; `_evaluate_profit_bars` needs `promotion_audit.yaml`,
   L6917). *Recommendation:* 6a records `profit_bars: null` with the reason
   "not evaluated before regroup". Making branch 3 run on every backtest belongs to the
   0.2 follow-up, not 6a.
5. **Near-miss scoreboard.** `build_scoreboard` reads only `verdict_interpretation.yaml`
   and ranks by the retired refine/pivot/escalate words, so every new run would show up as an
   empty row. Its output is a tracked file under `engineering/roadmap/E-018/artifacts/`,
   placed there on purpose so decision code can never pick it up.
   *Recommendation:* (a) teach `build_row` to read `grid_evaluation.yaml` when it is present
   (closest failing cell, from value, threshold and comparator; tier `grid`; old rows tagged
   `legacy`); (b) keep the output location, and by-hand review of the firewall stays as card H
   says. Accept that each run then changes a tracked file.
   *Alternative:* write to `campaign_record/`. That breaks the module's own firewall note.
6. **Component-error runs.** When `protocol_result.yaml` has component errors, the readers
   are skipped and the route pauses. *Recommendation:* `regroup_record` still records the run,
   with `engineering_fault: component_execution_error`, but writes no registry entry and no KB
   entry, then the route pauses as today.
7. **Re-runs of an already-recorded run.** *Recommendation:* the memory entry is keyed by
   `run_id` and replaced on re-run. The registry is append-only. If a re-run would change a
   run that already registered a block, it stops loudly and a person decides; it never edits
   the registry silently.

Already answered by the target, so not asked: the idea's identity is its `hypothesis_id`; a
test on another coin is a variant of the same idea; a validated block is usable on any coin;
the idea's status comes only from the grid; proposal scores only rank candidates (6b); old
verdicts never populate the registry; `correlation_to_composite` is slice 7.

---

## 1. The four writers today

The plan's slice-9 row (L66) names them: `_write_kb_findings_entry`,
`_auto_generate_findings_carryover`, `_record_backtest_trial`, and
`tools/near_miss_scoreboard.py`. The `campaign_state` writers are characterized alongside
because the trial writer shares their file.

### 1.1 `_write_kb_findings_entry` (`run_phase1_research.py:5997`)
- **Writes:** `campaign_record/campaign_knowledge_base.yaml` (`_KB_PATH`, L5893). It updates
  or creates an entry keyed by `hypothesis_id`, closes an open reactivation by the F09 rule
  (L6069-6101), validates *every* finding with `validate_verdict_provenance` (L6139-6144),
  then recomputes `coverage_matrix` / `exhausted_mechanisms`.
- **Input:** the `interp` dict (verdict_interpretation.yaml). Outcome comes from
  `_VERDICT_TO_OUTCOME` (L5895), which has no `validated`/`refuted` key, so either word would
  default to `"inconclusive"`. Provenance comes from `_verdict_provenance_stamp` (L5908). It
  cites `pass_rule_evaluation.yaml`, which on a menu-shaped rule returns `legacy_not_evaluable`
  when `outcomes` is missing (`_resolve_pass_rule`, `verdict_criteria_evaluator.py:911`), so
  the entry would be stamped `ungated`.
- **Called from:** only `determine_post_verdict_route` L7581, after the
  promote/terminate short-circuit (L7574). Flag off, it fires only on refine/pivot/escalate.
  **Under `specialist_readers` it is never reached** (`S2_5B_II_B_CALLERS.md` row 10, Q2).
- **Readers:** `hypothesis-design/SKILL.md:443` plus the `research_brief_to_hypothesis.yaml`
  handoff (the only reader still reached under the flag); `campaign_review` (not reached under
  the flag); `run_campaign._regenerate_summary` (count only, L1601);
  `evaluate_wishlist_predicate` (L732); `anti_adjacency_gate` layer 1 (flag off).
- **Retired dependencies:** F09 reactivation closure, `_check_kb_reactivation_conformance`
  (callers `_route_refine`/`_route_pivot`/campaign-review, all retired or unreached).
- **Checked:** the live KB (19 findings) passes `validate_verdict_provenance` with 0 errors;
  `outcome_is_verdict_bearing("validated"/"refuted") == True`, `("inconclusive") == False`.
  `resolve_evaluation_ref` (`verdict_criteria_evaluator.py:636`) checks that the file exists,
  that it sits under the entry's own run, and that `result ∈ {PASS, FAIL}`. It does not check
  the file name. `idea_status.yaml` carries exactly `result: PASS|FAIL` for
  validated/refuted (`_GRID_IDEA_STATUS_ROUTING` L2282), so it can be cited as-is.
  `KB_FINDING_SCHEMA` (`record_schema.py:164`) is closed and has no `legacy_schema` field, so
  a write carrying it raises until the field is added.

### 1.2 `_auto_generate_findings_carryover` (`:6150`)
- **Writes:** `runs/<id>/artifacts/findings_carryover.yaml` (`what_failed`, `what_not_to_try`,
  `next_altitude`), only for lineage_routing ∈ {refine, pivot, escalate} (L6173). It parses
  `altitude_justification` prose with a regex.
- **Called from:** L7578 and the run_loop `verdict_interpreter` branch L8559. Both are
  unreached under the flag.
- **Readers:** `_verify_verdict_outputs` (pivot/refine/escalate checks) and the next run's
  hypothesis_generation (as lineage memory).
- **Verdict:** **entirely retired machinery** (altitude, family, lineage). 6a must not
  call or rebuild it. Its target replacement is memory + proposals.

### 1.3 Trial accounting: `_record_backtest_trial` (`:5712`) / `_record_failed_backtest_trial` (`:5814`)
- **Writes:** `campaign_record/campaign_state.yaml → trial_sharpes` (`CAMPAIGN_STATE_PATH`,
  L88). The idempotency guard keys on `(trial_id, source)` (L5739, L5871).
- **Called from:** `run_tool_worker` protocol_execution only:
  - variant loop (`orchestrator.variant_loop.enabled`): one row per tested variant,
    `trial_id=f"{run_id}:{variant_id}"` (L1422, L1510). A failed variant gets a
    `backtest_failed` row (L1435/1466/1479/1499/1513). A variant not tested (data gate or
    component gap) gets no row, which matches card D.
  - flag-off single branch: one row, `trial_id=run_id` (L1852), plus failure rows
    (L1669/1680/1826/1855).
- **Readers:** `_write_promotion_audit` → `_dedupe_trials` (L6409/6447), `deflate_sharpe.py`,
  `run_campaign._regenerate_summary`.
- **Not dependent** on retired machinery or on verdict_interpretation.
- `research/TRIALS.csv` (repo root) is the fork's hand-kept research ledger. No pipeline code
  writes it (`killed_run_gate.py:21` and `dual_writer_demo.py:17` state that they never append
  to it), so it is out of scope for 6a.

### 1.4 `tools/near_miss_scoreboard.py::build_scoreboard` (`:605`)
- Pure: `build_scoreboard(runs_dir)` returns ranked rows. `main()` (L614) writes
  `engineering/roadmap/E-018/artifacts/near_miss_scoreboard.{yaml,md}` (both tracked).
  `main` prints "NOT yet wired" (L646).
- `build_row` (L406) reads only `verdict_interpretation.yaml` (plus the
  `pipeline_state.yaml` fallback). Ranking tier 1 uses `_VERDICT_PRIORITY` on `status`
  (refine/escalate/pivot/kill, L506), which is the retired vocabulary. Under the flag every
  new run lands in tier 2 `thin_no_verdict_file`.
- **Only pipeline reader:** the `verdict_interpreter` handoff's optional input (L4012),
  unreached under the flag. **Under the flag nothing reads it.** Card I/E-035 say its future
  consumer is idea generation.
- Firewall doctrine (module docstring L9-39): no decision code may read it. The static test
  was removed on 2026-09-13; review now enforces it (card H: "must preserve by hand").
- `STRATEGY_RESEARCH_ROOT` comes from `__file__` (L97), **not** from the orchestrator's `ROOT`,
  so the test sandbox's `ROOT` patch (`tests/conftest.py:291-299`) does not cover it. A test
  that runs the wired hook without passing `--out-dir` would overwrite the tracked E-018 file.

### 1.5 `campaign_state` writers (context)
- `update_campaign_state_after_run` (L242) writes `runs`, `altitude_history`,
  `recent_parameter_dimensions_by_family`, `diagnostics_log`. All its callers are
  `_route_refine/_pivot/_escalate/_kill` (legacy) and campaign-review reframe. **Retired.**
- `record_pivot` (L271, `failed_families`) and `record_escalation` (L281): **retired.**
- Under the flag, `_route_kill` (L5615-5627) appends only `runs` + `diagnostics_log`. Promote
  and pause do not append to `runs`, so **`campaign_state.runs` is incomplete under the
  flag**. The memory file must be the complete per-run list and must not rely on it.

## 2. Where the stage goes

Current flag-on flow: `protocol_execution → specialist_readers → (route)`, where the route is
`determine_post_specialist_readers_route` (L3033) in the run_loop branch at L8575-8584.

Proposed flow (only when `orchestrator.regroup_record.enabled`):
`protocol_execution → specialist_readers → regroup_record → determine_post_specialist_readers_route`.
This follows card H's "memory before decision" and 6c's wording "returns
`completed_<idea_status>` after `regroup_record`".

- `STAGE_CONFIGS` gains `"regroup_record": {"handoff": "specialist_readers_to_regroup_record.yaml",
  "default_next": "dynamic_routing"}`. It is registered unconditionally with no `skill` key,
  the same convention as `specialist_readers` (L191-203).
- Handoff created lazily at stage entry, like `_ensure_specialist_readers_handoff`
  (L2721, called at L8121). Required inputs: `artifacts/idea_status.yaml`,
  `artifacts/grid_evaluation.yaml`, `artifacts/hypothesis_card.yaml`.
- Stage body: an explicit `elif current_stage == "regroup_record": _run_regroup_record_stage(...)`
  before `elif not _skip_agent` (L8237-8242). No LLM call and no `_invoke_agent_with_yaml_retry`.
  Also not in `async_invoke_agent`'s `tool_stages` (L3801), matching `specialist_readers`.
- Routing: in the `specialist_readers` branch (L8575), when the regroup flag is on set
  `next_stage = "regroup_record"` instead of calling the route. A new
  `elif current_stage == "regroup_record"` branch calls
  `determine_post_specialist_readers_route` unchanged, with the same `human_pause` break.
- Flag resolved once in run_loop next to `_sr_flag` (L8086). A run whose `pending_stage` is
  `regroup_record` while the flag is off fails loudly, mirroring the verdict_interpreter guard
  at L8157.
- **Flag off** (the default, or readers off): stage graph and every artifact byte-identical.
  **Flag on:** one more tool stage; the route is unchanged in value, only later in time.
- **Dependency:** `regroup_record` requires `specialist_readers.enabled` (which already
  requires grid + reports). If it is on without that, it raises, the same pattern as
  `_specialist_readers_enabled` L2609-2621. It does not require `variant_loop`: the memory
  handles both grid column shapes (`run_id` column flag-off, `variant_id` columns under the
  loop).
- `_clear_specialist_readers_artifacts` (L2634) clears only run-local files. The
  campaign_record writes are outside the run, which is why guess 7 is needed.
- `campaign_review` is not reachable under the flag (`S2_5B_II_B_CALLERS.md` L8). Its trigger
  `_should_trigger_campaign_review` (L6341) keys on `failed_families` (retired). Making it
  reachable again belongs to 6c.

## 3. `campaign_record/campaign_memory.yaml` — proposed schema

Sourced only from files that exist under the flag. One entry per `run_id`, replaced on re-run.

```yaml
schema_version: 1
legacy_note: >-            # guess 3
  Runs before regroup_record are not listed; their history is campaign_knowledge_base.yaml
  (legacy unless legacy_schema: false). Trial counts live in campaign_state.trial_sharpes.
runs:
  run_061:
    run_id: run_061
    hypothesis_id: FOO_BAR            # hypothesis_card.yaml (_idea_hypothesis_id, L2819)
    legacy: false
    recorded_at: <utc>
    idea_status: validated|refuted|inconclusive   # idea_status.yaml
    idea_status_reason: <str>                      # idea_status.yaml.reason
    idea_status_ref: runs/run_061/artifacts/idea_status.yaml
    engineering_fault: null | component_execution_error   # _protocol_component_errors (L2749)
    grid:
      ref: runs/run_061/artifacts/grid_evaluation.yaml
      criteria: [ic_median, ...]                  # grid_evaluation.criteria
      variants: [base, design, asset]             # grid_evaluation.variants
      cells:                                      # compact copy of grid.<crit>.<variant>
        ic_median: {base: {result: PASS, value: 0.031, threshold: 0.02, n_windows: 8, n_trades: 412}}
      counts: {PASS: 8, FAIL: 1, INCONCLUSIVE: 0}
    variants:                                     # artifacts/variants/index.yaml (+ protocol_result)
      base: {status: tested|not_tested|failed, reason: null, config_ref: ..., config_sha256: ...,
             symbols: [BTCUSDT], n_windows: 8, trial_id: "run_061:base"}
    trial_ids: ["run_061:base", ...]              # READ-ONLY cross-link to trial_sharpes
    protocol_ref: <resolved window-set path>      # for 6b cost estimate + slice 8 hash
    timeframe: 1h                                  # hypothesis_card / config
    proposals:                                    # artifacts/proposals/<category>.yaml
      - {category: profitability, ref: runs/run_061/artifacts/proposals/profitability.yaml,
         proposal_ids: [profitability-run_061-1], count: 1}
    registry: {block_ids: [...]} | {skipped: no_manifest|not_validated|engineering_fault}
    profit_bars: null                              # guess 4
    kb_entry_id: <id> | null                       # guess 2
```

Deliberately absent: `hypothesis_family`, `altitude`, lineage/continuation fields, proposal
scores (6b reads them from the proposals files by ref; copying them here would invite a
second reader to route on them), and any verdict-routing pair.

What 6b's `decide_next` needs (plan L346-357), and where it comes from: memory (status, grid,
proposal refs), `block_registry.yaml` (R1 "changed since last composition": give it a
top-level `revision` counter plus `updated_at`), the queue, the proposals files, and open
briefs. Cost estimate by protocol class = window count × variant count, so `n_windows` per
variant and `protocol_ref` are included. The feasibility gate reads
`campaign_record/component_requests.yaml` (L2014) and `data_requests.yaml` (L1316) directly;
memory stores only counts, as a pointer.

## 4. `campaign_record/block_registry.yaml`

A block is registered only when `idea_status == validated`, there is no engineering fault,
and the run is not legacy (card A). Per field:

| Field | Source today | 6a fills? |
|---|---|---|
| `block_id` | deterministic `f"{hypothesis_id}:{run_id}"` (idempotent) | yes |
| `kind` | `block_manifest.yaml → block.kind` (forecast\|regime) | only if manifest (guess 1) |
| `config_fragment` | JSON-pointer values of `block.config_paths` in the **base** variant's `artifacts/variants/base/strategy_config.json` (pointer helpers exist: `_json_pointer_exists`) | only if manifest |
| `regime_assignment` | derived from the pointer path (`/strategies/regimes/<name>/…` → `<name>`); for a regime block, the detector rule path | only if manifest |
| `criteria_passed` | `grid_evaluation.criteria` (all PASS when validated) | yes |
| `variants_passed` | `grid_evaluation.variants` | yes |
| `numbers` | grid cells `{value, threshold, n_windows, n_trades}` per criterion × variant | yes |
| `correlation_to_composite` | residual IC vs composite (slice 7.1) | **null** — slice 7 |
| `validated_by_run` | run_id | yes |
| `registered_at` | utc | yes |

Two additions: `hypothesis_id`, and `source_config_sha256` (canonical JSON, same method as
`_compute_forecast_hash` L5684) so slice 8's exact-match hash can be cross-checked. Any-coin
eligibility is decided (card F), so no symbol restriction is stored; `symbols_tested` is
informational only. Registry is append-only with a top-level `revision` counter.

## 5. Trial rows: already handled, 6a must not write them

Proof from the code (§1.3): every data-touching look already writes exactly one row in
`protocol_execution`, per variant under the loop (`run:variant`) and per run otherwise.
Failures write a `backtest_failed` row. Untested variants correctly write none. The plan's
"appends the trial rows if slice 4 did not" therefore reduces to **nothing to append**. S2
ships a test that `campaign_state.trial_sharpes` is byte-identical before and after
`regroup_record` in both grid-column shapes; memory only *reads* `trial_ids`. Live ledger now:
15 rows, sources `{backtest, prescreen, prescreen_backfill}`.

## 6. Readers of the new files

- `campaign-review/SKILL.md` "Required inputs" (L16-17) lists only `campaign_state.yaml`. The
  handoff template (`templates/handoffs/campaign_review.yaml`) requires `campaign_state.yaml`,
  `research_brief.yaml`, and the KB (under stale `../../` paths, which
  `stale_input_path_fix` repoints). **Do not add the memory file to the template's
  `required_inputs` unconditionally**: flag-off runs have no memory file, and `ensure_files`
  (run_loop L8131) would fail them. Add it through an `_apply_regroup_record_context` helper
  only under the flag (the `_apply_config_direct_authoring_context` pattern, L3078), with the
  correct path `../../campaign_record/campaign_memory.yaml`. The SKILL.md gains a section
  naming the fields it must cite (`idea_status`, `grid.counts`, `registry`, `proposals`).
  Campaign-review is unreachable under the flag until 6c, so this is wiring for 6c, and a test
  proves the prompt is byte-identical when the flag is off.
- `decide_next` (6b): see §3.
- Scoreboard: see guess 5. Its row builder would read `grid_evaluation.yaml` + `pre_registration`
  (comparator) + menu.

## 7. Proposed S2 build list (split in two)

**S2a — the stage and the memory (no KB, no registry):**
1. `_regroup_record_enabled()` (strict bool, requires `specialist_readers`) plus a
   `campaign_config.yaml` entry and a `feature_flag_register.yaml` entry (`off_incomplete`).
2. `STAGE_CONFIGS["regroup_record"]`, lazy handoff, run_loop dispatch and routing (§2), and
   the pending-stage guard.
3. A new module `tools/campaign_memory.py` (importable without the orchestrator, like
   `reader_proposals.py`): `build_memory_entry(run_dir, run_id)` (pure) and
   `upsert_memory(path, entry)` (atomic `save_yaml`). Paths resolved from the orchestrator's
   `ROOT` at call time, so the conftest sandbox covers them.
4. Docs: USER_GUIDE §2.1/§2.2 stage block (required by `test_guide_covers_the_code.py`),
   CLAUDE.md stage count (12 registry entries), DOC_INDEX, `workflow_artifacts/schemas/campaign_memory.schema.json`.

**S2b — registry, KB mirror, scoreboard, campaign-review input:**
5. `tools/block_registry.py`: `register_block(...)` (manifest-gated, append-only, revision).
6. KB mirror writer per guess 2, plus `legacy_schema: FLAG` in `KB_FINDING_SCHEMA`.
7. Scoreboard: grid-aware `build_row` plus a `write_scoreboard(rows, out_dir)` helper that
   `regroup_record` calls with an explicit `out_dir`.
8. Campaign-review: `_apply_regroup_record_context` plus the SKILL.md section.

## 8. Tests (all runnable here with system `python` 3.13.2; no API key, no backtest)

Checked: `python -m pytest tests/test_e046a_slice5b_ii_b_readers_stage.py
tests/test_e046a_slice5b_ii_b_review_fixes.py tests/test_near_miss_scoreboard.py
tests/test_guide_covers_the_code.py` → 98 passed. Fixtures follow the readers-stage tests
(synthetic run dir with idea_status/grid/proposals, mocked LLM not needed since no LLM call).

- Flag: false when absent; non-bool raises; on without `specialist_readers` raises.
- Flag off: stage graph identity (`specialist_readers → route` unchanged), no campaign_record
  file created, campaign-review prompt byte-identical.
- Flag on: `specialist_readers → regroup_record → route`; the route value equals the flag-off
  route for validated/refuted/inconclusive; memory is written *before* the route (order
  asserted).
- Memory: both grid-column shapes; re-run replaces rather than duplicates; engineering-fault
  run recorded with no registry/KB write; `trial_sharpes` byte-identical (§5); schema has no
  retired fields (a test fails if `hypothesis_family`, `altitude` or `lineage_routing`
  appears).
- Registry: validated + manifest → one entry with the §4 fields and
  `correlation_to_composite: null`; no manifest → skipped with reason; refuted/inconclusive →
  none; re-register a different outcome → raises.
- KB: new entry passes `validate_verdict_provenance` citing `idea_status.yaml`; a legacy entry
  with the same `hypothesis_id` is untouched; inconclusive needs no ref.
- Scoreboard: the grid row gets tier `grid`; the hook writes only to the passed `out_dir`
  (guards the tracked E-018 file).

Run budget stays 0 as the plan says, but note: **no run on disk has `idea_status.yaml` or
`grid_evaluation.yaml`** (checked all 60 `runs/` dirs). The plan's "verified on slices 4–5's
runs" therefore waits on those slices' own real runs, which have not happened yet (no API
budget). Until then verification is fixture-only.

---

## Decision (operator, 2026-09-23)

All 7 "Guesses for the operator" accepted as recommended: register blocks only
when `block_manifest.yaml` exists (teaching 1b to write it is a separate small
ticket, consistent with the target's "1b writes config + manifest + rationale");
new grid-based KB writer (`legacy_schema: false`); no backfill of old runs;
`profit_bars: null` for now; scoreboard learns `grid_evaluation.yaml`, output
location unchanged; component-error runs recorded as an engineering fault with
no registry/KB entry; memory entry replaced on re-run, registry append-only and
stops loudly on conflict. Build split S2a (flag + stage + memory writer) then
S2b (registry + KB writer + scoreboard).
