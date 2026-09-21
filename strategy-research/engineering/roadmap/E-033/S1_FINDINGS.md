# E-033.1 S1 (delivery_plan_v26.md Slice 4 — "Three variants through the protocol") —
# characterization findings (2026-09-21)

Read-only. No code, config, or backtest runs executed. `local_data/holdout_sealed/` was not
opened. All file:line references below were re-grepped fresh on this worktree's own HEAD, not
copied from the delivery plan (whose own line numbers are stale for this seam per the plan's
own §1 table and per this dispatch's warning).

## 0. Base-commit / worktree state

Worktree HEAD and `origin/master` are both `b63fa3cd` (merge PR #184, "feat(E-056): config-direct
authoring") — **not stale**. Confirmed via `git log --oneline -1 origin/master` and `HEAD`
matching exactly; `git status` clean. Everything below was read directly from the working tree,
not via `git show`.

Slice 3b (config-direct authoring) is confirmed **merged and real**, matching
`strategy-research/CLAUDE.md`'s own corrected note ("STAGE_CONFIGS holds 10 entries as of E-056
Slice 3b") and `strategy-research/engineering/roadmap/E-056/S2_FINDINGS.md`'s Slice-3-level
characterization (read in full — its own analysis of Slice 3, not 3b, since it predates the 3b
merge, but its seam descriptions of `run_tool_worker`/`STAGE_CONFIGS`/`async_invoke_agent` are
still accurate scaffolding for what follows).

## 1. `artifacts/variants/index.yaml` — exact current shape (Slice 3b, real, merged)

Written by `run_tool_worker`'s `backtest_specification` branch,
`strategy-research/workflow/run_phase1_research.py:1524`:
`save_yaml(variants_dir / "index.yaml", {"variants": index})`.

Confirmed shape by reading the writer (`:1440-1524`) and the test file
(`strategy-research/tests/test_e056_config_direct_authoring.py:401-536`):

```yaml
variants:
  <variant_id>:
    status: validated | not_tested
    # when validated:
    config_path: "artifacts/variants/<variant_id>/strategy_config.json"  # RUN_DIR-relative
    # when not_tested:
    reason: "patch application failed: ..." | "manifest paths unresolved: [...]" | "validate_config.py violations"
    config_path: "..."          # present only for the validate_config.py-failure case
    report: "<validator stdout+stderr>"  # present only for the validate_config.py-failure case
```

Every `variant_id` is validated as a safe bare filesystem identifier
(`re.fullmatch(r"[A-Za-z0-9_-]+", variant_id)`, `:1468`) before use, and duplicates raise
(`:1442-1452`) rather than silently overwriting — both are Slice 3b's own code-review fixes, not
something Slice 4 needs to add.

**Critical detail for Slice 4**: only the `base` variant's validated config is additionally
copied to `artifacts/candidate_strategy_config.json` (`:1520-1522`) — the single path the
EXISTING (unmodified since before Slice 3b) `data_availability_gate` and `protocol_execution`
tool branches read. Non-base variants (e.g. `design_v2`) are validated and written to
`artifacts/variants/<variant_id>/strategy_config.json` but **nothing downstream ever reads
them today** — they sit inert in `index.yaml` with `status: validated` and are never gated,
backtested, or graded. This is the literal gap Slice 4 closes; confirmed by reading
`_route_post_config_direct_backtest_specification` next.

## 2. Current routing only ever looks at the `base` variant

`_route_post_config_direct_backtest_specification` (`:6674-6700`) is the routing function
between the tool-only `backtest_specification` stage and what comes next. Reads
`artifacts/variants/index.yaml`, but **only inspects `variants["base"]`** (`:6689`):

```python
base = variants.get("base")
if base is None or base.get("status") != "validated":
    ...pause...
if _data_availability_gate_enabled():
    return "data_availability_gate"
return "protocol_execution"
```

Non-base variants are not consulted for this decision at all today. This is the exact function
whose body Slice 4 needs to replace with the "≥3 variants remain else inconclusive" logic
(dispatch task 4) — not `run_tool_worker`'s branch, which only *produces* the index; this
function *consumes* it for routing. The delivery plan's seam table doesn't name this function
by name (it names `run_tool_worker` `protocol_execution` at "≈L1168-1260", now really
`:1177-1396`, see §3) — this is a real omission in the plan's own seam list, not a
contradiction, since the plan's intent (per-variant routing) requires touching this function
too.

## 3. The two `protocol_execution`-adjacent seams — NOT one function, contrary to the plan's framing

The delivery plan's Slice 4 bullet says "Seam: `run_tool_worker` `protocol_execution`
(≈L1168-1260) runs `tools/run_protocol.py` once... Build: iterate
`artifacts/variants/index.yaml`, run once per tested variant... Conformance:
`_check_protocol_execution_conformance` (≈L3186) runs per variant." Reading both functions in
full shows this actually spans **two separate, non-adjacent call sites**, only one of which is
`run_tool_worker`:

**3a. `run_tool_worker`'s `elif stage_name == "protocol_execution":` branch**
(`run_phase1_research.py:1177-1396`, confirmed by direct read, not `≈L1168-1260`) — runs
`tools/run_protocol.py` as a subprocess against **exactly one** config,
`ARTIFACTS / "candidate_strategy_config.json"` (`:1178`, still the base-only copy per §1), via
`_resolve_protocol_path(RUN_DIR, run_id)` (`:1182`, confirmed run-level not variant-level, see
§7). On success it: writes `ARTIFACTS / "protocol_result.yaml"` (`:1230`, **singular**, not
per-variant), runs C7's `evaluate_pass_rule_criteria` and writes `pass_rule_evaluation.yaml`
(`:1262-1266`), then — if `_grid_evaluation_enabled()` — calls
`_vce.evaluate_grid({run_id: summary}, ...)` (`:1300-1301`, **today's grid is a genuine
single-column grid keyed by `run_id`, not `variant_id`** — see §5 for why this is actually the
easy part) and writes `grid_evaluation.yaml`/`idea_status.yaml`; then (if
`_category_reports_enabled()`) calls `build_reports.build_reports(RUN_DIR, ...)`
(`:1326-1340`, Slice 5a, **also reads `artifacts/protocol_result.yaml` singular** —
`build_reports.py:38`); then calls `_record_backtest_trial(run_id, summary, config_path)`
(`:1369`, see §6). This entire branch is a single, un-looped sequence today — no per-variant
structure anywhere in it.

**3b. The conformance check's actual call site is NOT inside `run_tool_worker` at all** — it's
in `run_loop`'s own `elif current_stage == "protocol_execution":` branch,
`run_phase1_research.py:7104-7135` (confirmed by grepping the one real call to
`_check_protocol_execution_conformance(` — `:7125` is its only invocation in the whole file;
the function definition itself is at `:3741`, not `≈L3186`). This branch reads
`ARTIFACTS / "protocol_result.yaml"` (`:7112`, singular again), loads `machine_constraints`,
resolves the protocol JSON the run actually used, calls the conformance function, and on any
violation calls `_mark_trial_invalidated(run_id, "; ".join(_violations))` (`:7131`) and pauses.
**This is a materially different location than the delivery plan's text implies** ("Conformance:
`_check_protocol_execution_conformance` (≈L3186) runs per variant" reads as if it's a small
tweak inside the same `run_tool_worker` branch as the backtest loop; it is a wholly separate
function in a wholly separate top-level branch of `run_loop`, one level up in the call
hierarchy, that Slice 4 must independently restructure into a per-variant loop with its own
per-variant `_mark_trial_invalidated` calls (see §6 on why a bare `run_id` argument there is
now wrong under the new trial_id shape).**

**Net correction to the plan's seam table**: Slice 4 touches (at minimum) four distinct
functions across two files' worth of control flow — `run_tool_worker`'s `protocol_execution`
branch (the backtest loop itself), `_route_post_config_direct_backtest_specification` (routing,
§2), `run_loop`'s own `protocol_execution` elif-branch (conformance, this section), and
`run_loop`'s own `data_availability_gate` elif-branch (§4) — not one function with a per-variant
loop dropped in.

## 4. Data-availability gate — current wiring is also single-run, not per-variant

`run_tool_worker`'s `elif stage_name == "data_availability_gate":` branch (`:1141-1175`) runs
`tools/data_availability_gate.py` once against `ARTIFACTS / "candidate_strategy_config.json"`
(`:1148`, base-only copy again) and `_resolve_protocol_path(RUN_DIR, run_id)` (`:1149`, same
shared resolver as protocol_execution — confirmed independent of variant, see §7), writing a
single `RUN_DIR / "data_availability" / "data_availability_gate.yaml"` copied to
`ARTIFACTS / "data_availability_gate.yaml"`.

Its routing consumer, `run_loop`'s `elif current_stage == "data_availability_gate":` branch
(`:7071-7102`), reads that single `gate.yaml`, branches on `outcome` (`validate` →
`protocol_execution`; `refine` → `human_pause` with instructions to narrow the variant by hand;
`decline` → `completed_rejected`). **None of this loops over variants today** — it is exactly
one gate call per run, gating the base config only, with the `refine` outcome literally telling
a human to "narrow the variant" by hand, which is the single-variant-era UX Slice 4's
delivery-plan text (task 9/"3. Data per variant") replaces with an automatic
per-variant-not_tested + ≥3-remain-else-inconclusive branch. This confirms the delivery plan's
own framing ("Data gate per variant... runs once per variant config") is describing new
behavior, not a relocation of existing per-variant logic — there is no existing per-variant gate
logic anywhere to relocate.

## 5. `evaluate_grid` — confirmed it needs NO new glue code (dispatch task 5)

`strategy-research/tools/verdict_criteria_evaluator.py::evaluate_grid`
(`:1422-1423`, signature `evaluate_grid(protocol_results_by_variant: dict, pre_registration:
dict, research_brief: dict | None, menu) -> dict`) **already accepts an arbitrary
`{variant_id: protocol_result_dict}` mapping** — its own docstring states "A single-entry dict
is a valid 1-column grid... the same code later takes three" (`:1429-1433`), confirming this was
designed from the start for exactly this slice's need (matches E-046b S1's own framing, per this
function's docstring, which the dispatch asked me to check — confirmed directly by reading the
function itself, not inferred from S1 text). **Today's only call site
(`run_phase1_research.py:1300-1301`) passes `{run_id: summary}`** — i.e. it already builds a
1-column grid, just keyed by `run_id` rather than a real `variant_id`. Slice 4's change here is
purely call-site-shaped: build `{variant_id: summary_for_that_variant}` from N variants' own
`protocol_result.yaml` files instead of the single `{run_id: summary}`. **No signature change,
no new function in `verdict_criteria_evaluator.py` — confirmed.**

## 6. Trial-id shape change — every real call site enumerated (dispatch task 3, highest risk)

Today, `trial_id` is **always a bare `run_id`** (e.g. `run_042` or, per the dual-writer scheme
that is confirmed real in THIS repo — see §10 — `run_d_007`). Grepped every `trial_id` reference
in `run_phase1_research.py`:

1. **`_record_backtest_trial(run_id, summary, config_path)`** (`:4625-4716`) — idempotency guard
   `if any(t.get("trial_id") == run_id and t.get("source") == "backtest" ...)` (`:4644`) and the
   written row `"trial_id": run_id` (`:4694`). **Both must change** from `== run_id` /
   `run_id` to the new `trial_id` value (`f"{run_id}:{variant_id}"`) — this function's own
   signature must gain a `variant_id` (or `trial_id`) parameter; every one of its 3 call sites
   (`:1369` in `protocol_execution`, plus whichever new per-variant loop calls it under Slice 4)
   must pass it.
2. **`_record_failed_backtest_trial(run_id, config_path, reason)`** (`:4719-4781`) — same
   pattern: idempotency guard `== run_id` at `:4766`, written row `"trial_id": run_id` at
   `:4771`. **Same shape change required.** Called from 3 sites inside the `protocol_execution`
   branch today (`:1198`, `:1209`, `:1343`) — each of those call sites is itself inside what
   becomes Slice 4's per-variant loop, so each needs the per-variant `trial_id` threaded through.
3. **`_mark_trial_invalidated(run_id, reason)`** (`:4078-4100`) — compares `t.get("trial_id")
   == run_id` (`:4094`) and marks **every** matching row `invalidated_artifact: True`. Its
   real call site is `run_loop`'s conformance branch, `_mark_trial_invalidated(run_id, "; "
   .join(_violations))` (`:7131`, §3b). Under the new shape this is genuinely ambiguous and the
   delivery plan does not resolve it: does a conformance violation on ONE variant's protocol run
   invalidate only that variant's trial row (`trial_id == f"{run_id}:{variant_id}"`), or the
   whole run's variant family? The function's current `== run_id` exact-match would invalidate
   **zero** rows once trial_id becomes `run_id:variant_id` (a silent no-op, not a loud failure)
   unless it's changed to a prefix match or takes an explicit `trial_id`. **This is a concrete,
   previously-undiscussed risk**: an un-migrated `_mark_trial_invalidated(run_id, ...)` call
   under the new shape would silently stop invalidating anything, defeating F8b's whole purpose
   (excluding non-representative trials from the DSR basis) without any error — exactly the
   "silently wrong rather than loudly wrong" failure class this codebase's own comments
   elsewhere flag as the worst outcome. Flagged as a **Not determined / must-decide-before-S2**
   item.
4. **`_dedupe_trials`** (`:5304-5339`) — does **not** compare against `run_id` at all; keys
   purely on `(forecast_hash, source)` plus the independent `reproduces_trial` chain resolution
   (`_reproduces_collapses_inline`, `:5265-5301`, keyed on `(trial_id, source)` as an opaque
   pair, `:5318`). **No change needed here** — `trial_id` is only ever used as an opaque
   dictionary key/pair member in this function and its helper, never pattern-matched or
   parsed. Confirmed by full read.
5. **`_write_promotion_audit`** (`:5342-…`, reads through at least `:5399`) — reads
   `run_dir / "artifacts" / "verdict_interpretation.yaml"` and
   `run_dir / "artifacts" / "protocol_result.yaml"` (`:5364-5367`, **both singular, run-level
   paths**) to get `hyp_id`/`raw_median_sr`/diagnostics for ITS OWN promotion-audit
   computation — this is **not a trial_id comparison site**, but it IS a consumer of the same
   singular `protocol_result.yaml` that §3a/§3b's per-variant restructuring would leave stale or
   ambiguous (which variant's result does a single "the" `protocol_result.yaml` represent once
   there are three?). **The delivery plan's Slice 4 text does not mention
   `_write_promotion_audit` at all** — a real omission, since this function feeds directly into
   the DSR/holdout-gate decision chain and reads exactly the artifact whose cardinality this
   slice changes. Flagged below as Not determined.
6. **`tools/deflate_sharpe.py`** — grepped `trial_id` (`:101, 147-158, 193-215, 313-353,
   759-762`). `check_no_duplicate_trial_ids` (`:193-215`) keys on `(trial_id, source)` as an
   **opaque string pair with no regex/format validation** — confirmed by reading the function
   body; it does string equality only. **No shape assumption to break.** No other file in
   `strategy-research/tools/` or `strategy-research/workflow/` parses, regexes, or
   substring-splits a `trial_id` value anywhere (grepped `r"run_\d"`-style patterns and
   `trial_id.split`/`trial_id[` across both directories — zero hits outside test fixtures that
   construct literal strings).

**Summary for dispatch task 3**: 3 real production call sites need the shape change
(`_record_backtest_trial`, `_record_failed_backtest_trial`, `_mark_trial_invalidated`), one of
which (`_mark_trial_invalidated`) has a genuine, unresolved semantic question (whole-run vs.
single-variant invalidation) that the delivery plan text does not answer. `_dedupe_trials` and
`deflate_sharpe.py` need no change — trial_id is always opaque to them. `_write_promotion_audit`
needs a real design decision (not just a mechanical rename) that the plan's Slice 4 bullet never
mentions.

## 7. `_resolve_protocol_path` — confirmed variant-independent (plan's claim verified)

`_resolve_protocol_path(run_dir, run_id)` (`:3658-…`, signature confirmed, delegates to
`tools/protocol_resolution.py::resolve_protocol_path`) takes only `run_dir`/`run_id` — no
config or variant argument anywhere in its signature or body. This directly confirms the
delivery plan's own claim ("`_resolve_protocol_path` is called once (same windows for every
variant)") is correct: the protocol/window selection is a run-level decision independent of
which variant's config is being backtested, so Slice 4's loop can safely call it once and reuse
the result for every variant's `run_protocol.py` invocation, exactly as the plan states.

## 8. Per-variant data-gate + conformance + "≥3 variants remain else inconclusive" — design confirmed absent, no code to extend

Confirmed (§4, §3b) that neither the data-availability gate nor the conformance check has any
existing per-variant branching to extend — both are single-run today. The delivery plan's "≥3
variants remain, else `idea_status: inconclusive`" rule and the `campaign_record/
data_requests.yaml` file it names have **zero existing precedent** — grepped
`data_requests.yaml` and `idea_status.*inconclusive` across `strategy-research/`: the only
`idea_status` writer today is `_build_idea_status_artifact` (called from the grid-evaluation
block, `:1304`), which derives `idea_status` from `evaluate_grid`'s own
`validated|refuted|inconclusive` rollup (§5's docstring, `:1455-1466`) — a **different**
`inconclusive` concept (a criteria-grid unanimity result) than the one Slice 4 proposes (a
variant-count-floor result before any grid evaluation even runs). These must not be conflated in
the S2 build — the plan's own "idea_status: inconclusive" language for the data-gate case reuses
a field name that `_build_idea_status_artifact` already writes for an unrelated reason;
whichever code writes the gate-driven inconclusive verdict must either write to a distinct field
or very clearly union/override in a defined precedence order. **Not resolved here — flagged
below.**

## 9. Flag dependency (`orchestrator.variant_loop.enabled` requires `config_direct_authoring`) — confirmed sensible, confirmed unbuilt

Grepped `variant_loop` across the entire repo (`.py`/`.yaml`/`.md`): the **only** hit is the
delivery plan's own text (`delivery_plan_v26.md:287`) — zero code, zero config, zero tests.
Confirmed `orchestrator.config_direct_authoring.enabled` is a real, working flag today
(`_config_direct_authoring_enabled()`, `:1996-2016+`, following the exact same "false on
missing key/section/file, raise on non-bool" pattern documented in E-056 S2_FINDINGS.md and
registered in `config/feature_flag_register.yaml:200-213` /
`config/campaign_config.yaml:484-500`). The dependency makes concrete sense beyond the
dispatch's own framing: `artifacts/variants/index.yaml` (§1) is **only ever written** by the
`config_direct_authoring`-gated `backtest_specification` tool branch — with that flag off, the
file never exists, so a variant loop reading it would either find nothing (silently degrading to
zero variants processed) or need its own fallback logic duplicating the single-config path,
which the plan does not want. Recommend the new `_variant_loop_enabled()` helper follow
`_config_direct_authoring_enabled`'s exact template (`:1996-2016`) and additionally **hard-check**
`config_direct_authoring` is also on, raising or refusing (not silently no-op'ing) if
`variant_loop.enabled: true` is set while `config_direct_authoring.enabled` is false or absent —
this is a real invalid-config state, not just a redundant flag, since `index.yaml` structurally
cannot exist without the parent flag.

## 10. E-025 `run_d_NNN` note — confirmed real and relevant to THIS repo, not fork-only

The dispatch asked whether this note is even relevant here (loloze6/trading-bot master, not the
Dorian fork). **It is** — `run_d_NNN` is not a CLAUDE.fork.md-only concept. Real files exist in
this exact repo/branch: `strategy-research/engineering/roadmap/E-025/EPIC.md`,
`WRITER_CONTRACT.md`, `S4_UNION_MERGE_DESIGN.md` (dual-writer trial-ledger design, `run_NNN` for
master / `run_d_NNN` for the fork writer, disjoint by construction), and real tests exercising
the literal string (`test_dual_writer_demo.py`, `test_s4_union_merge.py`,
`test_union_merge_trial_ledgers.py`, `test_dual_writer_guards.py`) — all present and passing
their own fixtures in this worktree's `strategy-research/tests/`. So a real `trial_id` in this
codebase can already be `run_d_007`, not only `run_042`. Checked whether appending `:variant_id`
would collide with anything in the `run_d_NNN` scheme's own parsing: **no** —
`check_no_duplicate_trial_ids` and every other reader treat `trial_id` as an opaque string
(§6.6), and `WRITER_CONTRACT.md`'s own allocation rule (`master run_NNN` / `fork run_d_NNN`,
disjoint by construction) only concerns the *prefix* that guarantees cross-writer disjointness,
not the full string shape — a suffix appended after either prefix (`run_042:design_v2` or
`run_d_007:design_v2`) preserves disjointness exactly as before, since the collision-prevention
property lives entirely in the `run_`/`run_d_` numeric-allocation step, which Slice 4 does not
touch. **Confirmed applicable, confirmed non-breaking to the disjointness property, no
additional work needed beyond the trial_id shape change itself.**

## S2 build-list proposal (dispatch task 7)

In dependency order:

1. **`_variant_loop_enabled()` flag helper** — `_config_direct_authoring_enabled()`'s exact
   template (§9), registered in `feature_flag_register.yaml` + `campaign_config.yaml`, with the
   hard dependency check on `config_direct_authoring` (§9).
2. **`_route_post_config_direct_backtest_specification` restructure** (§2, `:6674-6700`) — stop
   checking only `base`; under the new flag, determine which variants are `validated` in
   `index.yaml`, decide `human_pause` (none validated), proceed if ≥1 (existing base-only
   behavior is the degenerate 1-variant case, must stay byte-identical when the flag is off).
3. **`run_tool_worker`'s `data_availability_gate` branch → per-variant loop** (§4,
   `:1141-1175`) — iterate validated variants from `index.yaml`, call
   `data_availability_gate.py` once per variant with a variant-scoped `--out-dir`, write results
   under `RUN_DIR/variants/<variant_id>/data_availability/`, and mark a `refine`/`decline`
   variant `not_tested` in `index.yaml` with an appended row in the new
   `campaign_record/data_requests.yaml` (no existing precedent, §8 — this is wholly new code).
4. **`run_loop`'s `data_availability_gate` elif-branch restructure** (§4, `:7071-7102`) — the
   ≥3-variants-remain-else-inconclusive branch; must NOT collide with
   `_build_idea_status_artifact`'s existing, differently-scoped `idea_status` field (§8 —
   needs an explicit decision, not just code).
5. **`run_tool_worker`'s `protocol_execution` branch → per-variant loop** (§3a,
   `:1177-1396`) — the core of this slice: run `run_protocol.py` once per validated,
   gate-passed variant, write `RUN_DIR/variants/<variant_id>/protocol_result.yaml` (NOT
   `artifacts/protocol_result.yaml` — needs an explicit decision on whether a "base" or
   aggregate copy still lands at the singular path for backward-compat readers, §6.5/§11).
6. **Trial-id shape change** (§6) — `_record_backtest_trial`/`_record_failed_backtest_trial`
   gain a `variant_id`/`trial_id` parameter; every call site inside the new loop (step 5) passes
   it; `_mark_trial_invalidated`'s semantics resolved (§6.3, must be decided before code, not
   during).
7. **`run_loop`'s `protocol_execution` elif-branch → per-variant conformance loop** (§3b,
   `:7104-7135`) — separate restructure from step 5, reads each variant's own
   `protocol_result.yaml`, calls `_check_protocol_execution_conformance` (itself unchanged, pure
   function, §3b) per variant, calls the now-shape-aware `_mark_trial_invalidated` per variant.
8. **Grid call-site change** (§5) — trivial relative to the above: build
   `{variant_id: protocol_result}` from step 5's N files, call the unchanged `evaluate_grid`.
9. **`_write_promotion_audit` decision + update** (§6.5) — not in the plan's own text; must be
   resolved (which variant's result feeds promotion, or a per-variant promotion-audit shape) and
   implemented.
10. **Tests**: three-variant fixture through the real loop (mocked subprocess, following
    `test_e056_config_direct_authoring.py`'s own pattern, §12); trial-id shape unit tests;
    flag-off identity test (`test_e054_stage_wiring.py`/`test_e056_config_direct_authoring.py`
    pattern); `_mark_trial_invalidated` semantics test once §6.3 is resolved.

### Split recommendation

**Recommend splitting into two S2 dispatches**, mirroring Slice 3's own 3a/3b precedent, but cut
along a different line since this slice's risk concentrates differently:

- **4a — "Loop restructure + trial accounting"**: build-list items 1, 2, 5, 6, 8 above (the
  routing change, the protocol-execution loop itself, the trial-id shape change, the grid
  call-site change). This is the slice's own stated core ("three variants through the
  protocol... three trial rows") and can be built and tested against the real engine
  end-to-end (data availability gate skipped/flag-off for this sub-slice's own test, since it's
  independently gated already) without needing steps 3/4/7/9 to exist first.
- **4b — "Data gate + conformance + grid/promotion wiring"**: build-list items 3, 4, 7, 9 — the
  genuinely new per-variant data-gate/data_requests.yaml machinery (§8, zero precedent, its own
  `≥3 remain else inconclusive` decision logic), the conformance-loop restructure (a separate
  function in a separate file location than the loop itself, §3b), and the `_write_promotion_audit`
  decision the plan never addressed (§6.5).

This split is justified by the same evidence-based reasoning E-056 S2_FINDINGS.md used: 4a is
the slice's own declared minimum viable deliverable (three variants actually backtested and
counted as three trials) and is testable/shippable in isolation; 4b bundles three independently
risky, currently-zero-precedent pieces (a brand-new file format, a brand-new inconclusive-vs-
inconclusive field collision to resolve, and an omitted-from-the-plan function) that each
deserve their own scrutiny rather than riding along with the core loop change.

## Not determined

- **`_mark_trial_invalidated` semantics under the new trial_id shape** (§6.3) — whole-run
  invalidation (all variants) vs. single-variant invalidation on a conformance violation. The
  delivery plan's text is silent; the function's current `== run_id` exact match would silently
  invalidate zero rows if left unmigrated (a real regression risk, not just an incompleteness).
- **`_write_promotion_audit`'s relationship to per-variant `protocol_result.yaml`** (§6.5, §11)
  — not mentioned anywhere in the delivery plan's Slice 4 bullet, but it reads exactly the
  artifact (`artifacts/protocol_result.yaml`, singular) whose cardinality this slice changes.
  Needs an explicit design decision before S2 build, not a mechanical carry-over.
- **Whether a singular `artifacts/protocol_result.yaml` still gets written** (as a "base variant"
  copy, an aggregate, or not at all) for the several existing readers that assume it exists as a
  single run-level file: `verdict-interpreter/SKILL.md` (grepped ~15 references, all assuming
  one file), `build_reports.py:38` (Slice 5a, merged, reads it singular), and
  `run_loop`'s own conformance branch (§3b, `:7112`). This is a real fan-out of consumers the
  delivery plan's Slice 4 bullet does not enumerate at all — flagged as the single largest
  unresolved design question this session found.
- **The exact `idea_status`-field collision between the data-gate's proposed "≥3 remain else
  inconclusive" outcome and `_build_idea_status_artifact`'s existing, differently-scoped
  criteria-grid-derived `idea_status`** (§8) — not assessed which should win, or whether they
  need distinct field names.
- **Whether a fully real, unmocked three-variant `run_protocol.py` end-to-end test is actually
  executable in an S2 build environment** — confirmed this worktree has no resolvable
  trading-bot venv (`_resolve_tbot_python()`'s two candidate paths, `venv/Scripts/python.exe`
  and `.venv/bin/python` relative to repo root, both absent — checked directly, zero results),
  and `test_e056_config_direct_authoring.py`'s own autouse fixture already stubs
  `_resolve_tbot_python`/mocks `subprocess.run` for exactly this reason (its own docstring:
  "This worktree/environment may not have a resolvable trading-bot venv"). Real BTC/ETH-family
  cached data DOES exist (`trading-bot/local_data/*.csv`, multiple symbols/timeframes/exchanges
  confirmed present), so the data half of "1 real idea, three variants, three trial rows" is
  feasible in principle — but whether the S2 build's own dev/CI environment has a working
  trading-bot venv to actually invoke `run_protocol.py` for real was not established here, only
  that THIS worktree does not. Same caveat Slice 3b's own build hit for its LLM key (E-056
  S2_FINDINGS.md's framing) — recommend the S2 dispatch confirm venv availability as its very
  first action before committing to a real-subprocess test plan, with a mocked-subprocess
  fallback (following `test_e056_config_direct_authoring.py`'s own precedent) if none exists.

---

## Decision (operator, 2026-09-22) — resolves two "Not determined" items above

**On `_mark_trial_invalidated` semantics (item 1 above):** confirmed. A conformance violation
invalidates only the specific variant's trial row, exactly as built in Slice 4a
(`_mark_trial_invalidated(trial_id, reason)`, comparison on the compound `trial_id`, not a
whole-run `run_id` match). The operator's own framing generalizes this beyond just
invalidation: **every control the target workflow defines — the data-availability gate,
conformance checking, anything else gated per-backtest — must run independently per variant,
not once for the whole run.** This is now the explicit design principle for Slice 4b's
per-variant data-availability-gate loop (build-list item 3/4): each variant gets its own gate
call, its own `refine`/`decline` outcome, its own `not_tested` marking — never a single
shared gate result applied to all three.

**On the singular `artifacts/protocol_result.yaml` question (items 2 and 3 above): resolved,
and the resolution is NOT "keep a singular bridge file forever."** Slice 4a's own singular-file
write (Decision B in its own dispatch) is confirmed as an explicitly temporary bridge, not the
target design. The real target: genuinely multiple backtest results survive per run, one per
variant, and each of the three post-backtest consumer branches is responsible for its own
N-way fan-out instead of assuming one file:

- **Branch 1 — the grid (`evaluate_grid`, Slice 2).** Already correct as built — S1 §5
  confirmed `evaluate_grid` accepts an N-column `{variant_id: protocol_result}` dict by design,
  and Slice 4a's own grid call site already passes exactly that. No further change needed here.
- **Branch 2 — the specialist reader skills (Slice 5b, not yet built).** Must receive ALL
  variants' backtest results, not a single representative one. This changes Slice 5a/5b's own
  scope from what was assumed during Slice 4a's build (category reports computed once from the
  base variant's summary only, per that build's own stated judgment call) — category reports
  and/or the readers that consume them need to become variant-aware before 5b is genuinely
  built. Flagged explicitly for whoever characterizes Slice 5b: do not carry forward the
  base-only assumption Slice 4a made for expedience.
- **Branch 3 — the profitability-bars stop (`_write_promotion_audit` / CUL-299, already
  merged).** Must check ALL variants and pass if ANY ONE clears every bar — an existential
  quantifier across variants, not a check against a single aggregate or base-only result. This
  is the concrete answer to item 2 above (`_write_promotion_audit`'s relationship to
  per-variant results): it needs to iterate every variant's `protocol_result.yaml` and each
  bar independently, with the overall profit-bars verdict PASS iff at least one variant's
  result clears every bar. This is Slice 4b's own build-list item 9, now with a real design to
  build to instead of an open question.

**Practical effect on Slice 4a's own temporary bridge file:** it stays as built for now (it is
still needed by consumers that haven't been updated yet — `run_loop`'s conformance branch,
until 4b restructures it; `verdict-interpreter/SKILL.md`), but should be understood as
scaffolding to be retired once branches 2 and 3 above are rebuilt to consume the real
per-variant fan-out directly, not extended or relied upon further.

---

## Paste-ready Linear comment

**E-033.1 S1 (Slice 4: three variants through the protocol) — characterization complete
(2026-09-21).** Read-only, worktree at `origin/master` tip `b63fa3cd`, not stale. Full findings:
`strategy-research/engineering/roadmap/E-033/S1_FINDINGS.md`.

Headline findings:
- **`artifacts/variants/index.yaml` (Slice 3b, merged) confirmed real**: `{variants:
  {variant_id: {status: validated|not_tested, config_path?, reason?, report?}}}`, written by
  `run_tool_worker:1440-1524`. Only the `base` variant's config is copied to
  `candidate_strategy_config.json` today — every non-base variant is validated and written to
  disk but **nothing downstream ever reads it**. That's the exact gap Slice 4 closes.
- **The plan's own seam table is wrong about locality**: this slice touches FOUR separate
  functions across two files' control flow, not one loop drop-in — `run_tool_worker`'s
  `protocol_execution` branch (`:1177-1396`, the backtest loop), a SEPARATE routing function
  `_route_post_config_direct_backtest_specification` (`:6674-6700`, currently checks only
  `base`), and TWO separate `run_loop` elif-branches one level up (`data_availability_gate`
  `:7071-7102` and `protocol_execution`'s conformance check `:7104-7135`, whose only real call
  to `_check_protocol_execution_conformance` is at `:7125`, not `≈L3186` as the plan states —
  that's the function's *definition* line, `:3741`).
- **`evaluate_grid` needs zero new glue code** — confirmed it already accepts an N-column
  `{variant_id: protocol_result}` dict by design (`verdict_criteria_evaluator.py:1422-1433`,
  its own docstring says so); only the call site's dict-building changes.
- **Highest-risk finding (trial_id shape, dispatch task 3)**: 3 real call sites need the
  `f"{run_id}:{variant_id}"` shape (`_record_backtest_trial`, `_record_failed_backtest_trial`,
  `_mark_trial_invalidated`) — the third has a genuine unresolved semantic question (does a
  per-variant conformance violation invalidate one trial row or the whole run's family?) that
  will silently invalidate ZERO rows if left unmigrated, since its current `==` comparison would
  simply never match the new compound id. `_dedupe_trials` and `deflate_sharpe.py` need no
  change (trial_id is always opaque there, confirmed by reading both).
- **Real, previously-unflagged gap**: `_write_promotion_audit` and multiple other readers
  (`verdict-interpreter/SKILL.md`, `build_reports.py:38`) assume a SINGULAR
  `artifacts/protocol_result.yaml` — the delivery plan's Slice 4 bullet never addresses what
  happens to this file once there are N per-variant results instead of one.
- **E-025's `run_d_NNN` note is real and relevant to this repo** (not fork-only) — confirmed
  live `WRITER_CONTRACT.md`/tests in this exact checkout — and a `:variant` suffix is confirmed
  non-breaking to the disjointness property, since every reader treats `trial_id` as opaque.
- **Recommend splitting into 4a (loop restructure + trial accounting, the slice's own stated
  minimum deliverable) and 4b (data gate + conformance + grid/promotion wiring, three
  zero-precedent pieces bundled)** — not the plan's own bullet order, cut along testability
  rather than file proximity.
- **Real end-to-end test feasibility unresolved for THIS worktree**: no trading-bot venv found
  (`venv/Scripts/python.exe` / `.venv/bin/python` both absent relative to repo root); Slice 3b's
  own tests already mock `subprocess.run` for the same reason. Cached BTC/ETH data does exist.
  S2 should confirm venv availability first, same caveat as Slice 3b's missing LLM key.

Not determined (see file for full list): `_mark_trial_invalidated` per-variant semantics;
`_write_promotion_audit`'s relationship to per-variant results; whether a singular
`protocol_result.yaml` survives in any form; the `idea_status` field collision between the
data-gate's inconclusive outcome and the existing grid-derived one; real-subprocess test
feasibility in the actual S2 build environment.
