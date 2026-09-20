# E-056 S2 (owns delivery_plan_v26.md Slice 3) — characterization findings (2026-09-21)

Read-only. No code, config, or backtest runs executed. `local_data/holdout_sealed/` was
not opened. All file:line references below were re-grepped fresh on this worktree's own
HEAD, not copied from the delivery plan or from the E-056/E-046b S1 docs.

## 0. Base-commit / worktree state

Worktree HEAD and `origin/master` are both `f01afc28` (merge PR #180) — **not stale**,
unlike the E-056 S1 and E-046b S1 worktrees, which were 1-2 commits behind and had to read
several files via `git show`. Everything below was read directly from the working tree.

Confirmed via `git log`: **E-046b S2 (the grid) has already landed on master**, in two
commits not mentioned by name in `delivery_plan_v26.md` itself (written before they merged):
`38269fe9` ("feat(E-046b S2): the grid — evaluate_grid() beside evaluate_pass_rule_criteria")
and `fec92e58` ("fix(E-046b grid): isolate grid-eval exceptions from trial recording,
exclude era gaps from sign check"). `strategy-research/config/criterion_menu.yaml` **exists
for real** (109 lines) — read directly, not from the S1 proposal. It currently has exactly
**two live entries** (`realized_edge_to_cost_ratio`, `sign_consistent_by_era`) plus two
explicitly commented-out placeholders (`residual_ic`, `gated_beats_ungated`, both blocked on
slice 7 composition work per the file's own comment). This matters for Slice 3's own
criterion-menu dependency: the menu Slice 3 would reference already exists and already
validates against `evaluate_grid()`, so 1a's criteria-from-menu requirement (delivery plan
line 234-236) has a real, non-empty menu to point at — but it is a 2-entry menu, not the
richer one E-046b S1 sketched. Confirmed nothing under `strategy_config_authoring`,
`config_direct_authoring`, `strategy-config-authoring`, or `variant_patches` exists anywhere
in the repo yet (`grep -rn` across `.py`/`.yaml`/`.md`, zero hits outside the planning docs
themselves) — Slice 3 is entirely unbuilt, confirming the dispatch's own framing.

## 1. What the three skills instruct the LLM to produce TODAY

Read in full (not excerpted): `strategy-research/workflow_artifacts/skills/hypothesis-design/SKILL.md`
(341 lines — matches E-056 S1's count exactly, unchanged since `6123edfd`),
`strategy-research/workflow_artifacts/skills/innovation-expansion/SKILL.md` (254 lines — **drifted
from 195 to 254** since E-056 S1 measured it; real content, not measurement error, confirmed
by reading the file), `strategy-research/workflow_artifacts/skills/backtest-engineering/SKILL.md`
(255 lines — **drifted from 228 to 255**). Paths are exactly as the delivery plan and E-056 S1
named them; no path staleness, only line-count staleness (both S1 docs were correct as of
their own measurement date; both files gained content since — `5f6b7b03` "record which
backtest_spec variant was chosen" and `6123edfd` "asset-generalizability" additions to
innovation-expansion; `63052a1f`/`6123edfd` additions to backtest-engineering).

**`hypothesis-design/SKILL.md` (1a today):** produces `hypothesis_card.yaml` with, in
required order, `hypothesis_id, thesis, rationale, edge_source, signal_concept,
target_market, timeframe, assumptions, expected_failure_modes` (lines 20-29), plus
`library_lookup` (Improvement 04) and `power_parameters.plausible_ic_upper` picked from a
fixed anchor table (A8.6, lines 275-301) rather than free-handed. **Zero mention of
`pass_rule`, `criteria`, `config`, `class`, `weight`, or `transforms` anywhere in the file** —
confirmed by re-reading end to end, matching E-056 S1's finding exactly. This is the file
Slice 3 rewrites to add: criteria drawn from `config/criterion_menu.yaml` (now real, 2
entries), the pass-through rule, and the two "mechanism purity"/"daily-feed timing" checks
that live in `quant-validation/SKILL.md` today (see §2) but the delivery plan wants moved
here as rules rather than a second LLM pass.

**`innovation-expansion/SKILL.md` (Step 2 today):** produces `expanded_hypothesis_card.yaml`
with `expanded_variants` (prose fields: `library_category`, `data_requirements`,
`diversity_axis` — lines 92-99) and `regime_specific_variants` (routed to
`detector_wishlist`, never the run queue, per the standing A2.3 no-regime-gating policy —
lines 55-68), plus `innovation_notes.yaml` carrying `diversity_audit` and
`asset_diversity_audit` (Improvement 06, lines 152-159: ≥2 candidate symbols from a
DIFFERENT `coin_universe.yaml` category than the base instrument, or an explicit
single-asset opt-out). **No variant field is a config-field patch** — `diversity_axis` is a
free-text description of what makes a variant different, not a JSON-pointer diff. This
confirms card K's framing exactly: Slice 3's `variant_patches.yaml` (base + design patch +
asset patch, each `{variant_id, patch: [{path, value}], rationale}`) is new structured
output this skill does not produce today in any form, prose or otherwise.

**`backtest-engineering/SKILL.md` (Step 5-ish today, "5a" in the plan's numbering):**
produces `backtest_spec.yaml` (`status: spec_ready|component_gap`, `config`,
`config_rationale`, `selected_variant_id` (Improvement 01, lines 59-86 — a closed-set pick
against the `expanded_variants` menu, already machine-checked downstream by
`_record_variant_selection`, see §6) and `decision.yaml`. **This is already, functionally,
1b** — it is the one stage today that actually authors the `regime_detector`/`strategies`
object, cites `STRATEGY_CONFIG_REFERENCE.md` as required reading, and hand-encodes in prose
exactly the two checks Slice 3 wants to move into code: the ungated-pattern rule (lines
151-220, "THE canonical pattern", with the `default_regime="unknown"` one-bar-warmup-defect
explanation) and the V9 default_regime bypass rule (Forbidden section, lines 232-251).
Confirms E-056 S1's finding verbatim: `strategy-config-authoring/SKILL.md` is substantially
this file relocated from post-validation to pre-validation (1b instead of ~5), not a new
invention. One thing this file does NOT do today that the design guide (§5 below) has no
seed for: emit an instrument-set/manifest block — confirmed absent from both the "Required
outputs" and "Output requirements" sections.

## 2. `quant-validation/SKILL.md` — the stage the plan wants removed under the flag

Read in full (202 lines, unchanged since before this session's baseline — no recent commits
touch it per `git log -3` on the file). Produces `validation_protocol.yaml`
(`falsifiable_statement, null_expectation, required_evidence, bias_risks, failure_modes,
sample_split_design, decision_rules, cost_feasibility`) and `validation_decision.yaml`
(`status: approve|conditional_approve|refine|reject`), and — since E-039 S4 folded
`refinement_planner` into this same call — `refinement_notes.yaml` when its own verdict is
`refine`. Two checks live here that the delivery plan (line 236) wants relocated to 1a as
rules rather than re-run as a second LLM stage:
- **Cost-feasibility / "mechanism purity" gate** (Improvement 09, lines 143-176): populates
  `cost_feasibility.plausibility` from `config/cost_model.yaml`'s round-trip cost, with a hard
  rule that `implausible` forbids `approve`/`conditional_approve`. This is NOT literally
  "mechanism purity" in the A1.3 anti-confabulation sense (that check already lives in
  `hypothesis-design/SKILL.md` itself, §1's Improvement 01/A1.3) — it is a cost-survival
  plausibility check. The dispatch's phrase "mechanism purity" most likely refers to A1.3,
  which is already in 1a, not here; flagged under "Not determined" below since the dispatch
  text doesn't disambiguate and I could not find a "mechanism purity" label anywhere in
  `quant-validation/SKILL.md` itself.
- **Daily-feed timing** — this exact phrase and check ("A1.3 Spirit check... Caught
  confabulation 2... Daily feed forward-filled to 1h without signal timing constraint") is
  **already in `hypothesis-design/SKILL.md`** (lines 130-137), not in `quant-validation`. So
  at least this half of the delivery plan's "two design-guide checks that used to live in the
  validation stage" claim is **not accurate as stated** — the daily-feed timing check already
  lives in 1a today, not in validation. This needs a correction relayed to whoever owns the
  delivery plan text before S2 build: only the cost-feasibility check is a genuine
  validation-stage-only rule; the daily-feed-timing check requires no relocation, it is
  already where Slice 3 wants it.

## 3. Real orchestrator wiring, current line numbers (re-grepped, not from the plan)

`STAGE_CONFIGS` (`strategy-research/workflow/run_phase1_research.py:126-189`) — **9 real
entries** (matches `strategy-research/CLAUDE.md`'s own corrected count):
`hypothesis_generation` (:127), `innovation_expansion` (:133), `validation` (:142, skill
`quant-validation`), `backtest_specification` (:155, skill `backtest-engineering`),
`data_availability_gate` (:166, **no `"skill"` key — the existing tool-stage precedent**),
`protocol_execution` (:170, no skill key), `verdict_interpreter` (:174),
`campaign_review` (:179), `holdout_evaluation` (:185, no skill key).

`determine_post_validation_route` (`:2492-2540ish`, def at `:2492`) — **exactly one real
caller**, `run_loop`'s `current_stage == "validation"` branch at `:6434-6442`; the other 3
hits (`test_run_phase1_research_cp1252.py`, `test_validation_route_family_status.py` ×3) are
tests. Routes `approve → backtest_specification` (the stage graph's own `default_next`),
`refine → determine_post_refinement_route` (loops to `innovation_expansion` or pauses),
`reject → completed_rejected`.

`backtest_specification`'s current shape (`:6453-6522`) — **confirmed LLM-authored today,
not tool-only**, directly contradicting nothing in the plan (the plan's assumption is
correct, now verified by execution-path reading, not inference): `_invoke_agent_with_yaml_retry`
runs the Claude worker per `async_invoke_agent`'s `engine == "claude"` branch (`:2468-2470`),
producing `backtest_spec.yaml` with an embedded `config` object. Immediately after
(`:6473-6520`), deterministic code extracts `config_obj`, force-injects
`significance_methodology` from `machine_constraints` if present (F4d fix), writes
`artifacts/candidate_strategy_config.json`, and subprocess-calls
`trading-bot/tools/validate_config.py` against it (`:6486-6491`) — non-zero exit writes
`spec_validation_report.txt` and routes to `failed_validation`; zero exit calls
`_create_remaining_handoffs` and, if `_data_availability_gate_enabled()`, routes to
`data_availability_gate` instead of straight to `protocol_execution`.

`determine_post_spec_route` (`:6190-6211`) — the smaller routing function actually invoked
just before the block above (not named in the delivery plan's seam table at all — an
omission, not an error, since it's a thin `spec_ready→protocol_execution` /
`component_gap→human_pause` dispatcher the LLM's own `decision.yaml.status` drives). This
function is unaffected by Slice 3's flag either way; it reads the same `decision.yaml.status`
field a tool-authored `backtest_specification` would also need to write.

**The load-bearing seam for "backtest_specification becomes a `tool:` stage":**
`async_invoke_agent` (`:2439-2473`) has a hardcoded
`tool_stages = {"protocol_execution", "data_availability_gate"}` set literal at `:2440`. If
`stage_name in tool_stages`, it calls `run_tool_worker(stage_name, run_id)` (`:2442`) and
returns — no handoff load, no LLM call. **This is the exact, already-proven mechanism Slice 3
needs**: under the flag, `backtest_specification` must join this set (conditionally — flag
off must still route it through the `engine == "claude"` LLM path, since retiring
`backtest-engineering` as an LLM stage is itself the declared behaviour change). `run_tool_worker`
(`:1122-…`, an `if stage_name == "data_availability_gate": ... elif stage_name ==
"protocol_execution": ...` dispatch, each branch a `subprocess.run` against a `tools/*.py`
script whose output YAML is copied into `artifacts/`) is the direct template for a new
`elif stage_name == "backtest_specification":` branch that applies patches, runs
`validate_config.py`, and performs the new component-existence check — the same
subprocess-and-copy shape as the two existing branches, not a new invocation pattern.

`validation` stage removal: only one real registry entry to delete
(`STAGE_CONFIGS["validation"]` at `:142-154`) and one real routing call site to guard
(`:6434-6442`, the `current_stage == "validation"` block) — both are conditional on the new
flag, per the plan's own "keep the code path only for flag-off runs" instruction. No other
code path branches on the literal string `"validation"` as a stage name outside these two
sites and the three test files already named in §5.

## 4. `trading-bot/tools/validate_config.py` — what it actually checks today

Read in full (306 lines). **Confirms V1-V11** (11 checks; `strategy-research`'s own
`CLAUDE.md` at the repo root already carries the corrected "V1-V10... has V11 too" note from
E-056 S1). What it does: V1 top-level structure; V2 every veto/rule/score-component `id`
cross-references a declared `regime_detector.components[].id`; V3 every transform op exists
in `TRANSFORM_OPS_REGISTRY`; V4 every op has a `TRANSFORM_MIN_PERIODS` entry; V5
history-ops-before-scalar-ops ordering; V6 explicit `lookback` ≥ transform min-periods; V7
every regime name used anywhere is one of the 4 valid `MarketRegime` values; V8 numeric
per-component weight, per-regime total > 0; V9 `default_regime` may not alias a real regime
while `rules` is non-empty (the gate-bypass bug); V10 a fully-ungated detector may not point
`default_regime` at a null `strategies.regimes` entry (the "dead config" bug); V11
`strategies.min_allocation_change` non-negative if present.

**What it does NOT check, confirmed by reading every line: it never verifies that a
component's `class` dotted path actually resolves to a real, importable class.** V2 only
cross-references `id` values against each other (are veto/rule ids declared in
`regime_detector.components`) — it never imports or introspects
`strategies.strategy_components` at all. This is exactly the gap the delivery plan's "checks
every `class` in `strategies.regimes.*.components[]` and `regime_detector.components[]`
exists (import `strategies.strategy_components` and check attribute presence)" item targets
— confirmed as genuinely new logic, not a relocation of an existing check. The failure mode
today (an invented class name) currently surfaces only at actual engine startup
(`_load_class`, `ValueError`, per E-056 S1's own table), never at `validate_config.py` time —
so a bad class name passes today's validator and would only be caught much later, at
`protocol_execution`, wasting a real backtest run. This is the concrete cost-of-the-gap the
new check buys back.

## 5. Component catalog — mechanical count

`grep -c "^class.*SubStrategyComponent" trading-bot/strategies/strategy_components.py`
(Git Bash, this session) → **24**, matching `CLAUDE.fork.md`'s corrected figure and E-056
S1's independent count exactly. File is 1444 lines, unchanged in recent history relevant to
this slice (no commits touching it appear in the last 10 `git log` entries for the repo).
Full class list re-verified by name (24 distinct `class NameComponent(SubStrategyComponent):`
lines) — not reproduced here in full since `STRATEGY_CONFIG_REFERENCE.md` §4 already
tabulates all 24 with params, and E-056 S1 already cross-checked every one against
`self.parameters.get(...)` calls.

`trading-bot/strategies/registry.py::TRANSFORM_OPS_REGISTRY` — not re-counted this session
(E-056 S1's count of 15 stands; `validate_config.py:11` imports it directly by name,
confirming it's the single source of truth both the engine and the validator already share).

## 6. Design guide vs. `STRATEGY_CONFIG_REFERENCE.md` rewrite — real scope estimate

Read `trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md` in full (283 lines) this session,
independently of E-056 S1's read. Confirms S1's "~99% accurate, already the real seed"
verdict with more precision: sections 1-6 (top-level shape, `regime_detector`, `strategies`,
transform ops, component catalog with all 24 classes + worked variant patterns, a full worked
example, an edit checklist) are comprehensive and current — cross-checked spot-fields (e.g.
`WhaleLargeTradeImbalanceComponent`'s NaN-abstention behavior, §4a's `aux_feeds` deny-by-default
behavior) against the file's own prose, no contradictions found. **One field the delivery
plan's task list (line 168, "params typos are silently ignored... design guide needs a
positive required/optional param list") claims is a *gap* is actually already explicit
documentation, not a gap**: line 108 of the reference file already states, verbatim, "WARNING:
keys are NOT validated — a typo'd key is silently ignored and the default is used.
Double-check spelling against the catalog" — and §4's table IS the positive param list. This
is a second correction to the delivery-plan text (after §2's mechanism-purity mislocation
above): the "params typo" design-guide gap is already closed in the existing reference doc;
Slice 3 does not need to add this, only preserve it in whatever new/rewritten file it produces.

**Real new content the design guide needs, confirmed genuinely absent from
`STRATEGY_CONFIG_REFERENCE.md`:**
1. **Instrument-set / symbol / timeframe field** — confirmed absent from the reference file's
   entire top-level shape section (§0, lines 5-13: only `regime_detector`, `strategies`,
   `aux_feeds`). This is real new schema surface, not documentation — it needs a
   `validate_config.py` addition (a V12) if it is to be enforced at all, and a decision on
   where in the config object it lives. E-056 S1 already flagged this as the single largest
   gap; this session's independent read confirms it and finds no counter-evidence.
2. **The manifest contract** (`block_manifest.yaml`: `{block: {kind: forecast|regime,
   config_paths: [...]}, scaffolding: [...], rationale}`) — has zero precedent anywhere in
   the current reference file or any skill file; this is 100% new content, not reorganized.
3. **Comparator-vocabulary divergence note** — `regime_detector.rules`' `gte/gt/lte/lt/between`
   (reference file line 87) vs. `verdict_criteria_evaluator.py`'s `>=/>/<=/</==`
   (`_VALID_COMPARATORS`) is real and already independently confirmed by both this session
   and E-056/E-046b S1 — needs one explicit callout paragraph, not a rewrite.

**Estimate:** of a new `STRATEGY_DESIGN_GUIDE.md`, roughly **85-90% would be the existing
283-line reference file carried over near-verbatim** (§§1-6 as-is, since none of it is wrong
or design-guide-incompatible), plus a genuinely new ~30-60 line block covering the three
items above and a "1b workflow" framing paragraph (how an LLM should read a hypothesis card
and choose components — the reference file has no authoring guidance today, only a lookup
reference; `backtest-engineering/SKILL.md`'s own Checklist/Forbidden sections, lines 126-251,
already supply most of this authoring guidance and would fold in largely as-is). **This is a
targeted rewrite/merge, not a from-scratch document** — consistent with E-056 S1's verdict,
now with a concrete estimate attached (roughly 300-350 total lines in the merged result, not
an order-of-magnitude larger new artifact).

## 7. `_record_variant_selection` / `variants_not_pursued.yaml` — current real behavior

Read `_record_variant_selection` (`run_phase1_research.py:2063-2169`) in full. Flag-gated by
`_variant_selection_record_enabled()` (off by default — returns immediately, no read, no
write, when off). When on: reads `backtest_spec.yaml.selected_variant_id` (RAISES if absent —
the actual enforcement Improvement 01's schema field alone cannot provide), matches it against
`expanded_hypothesis_card.yaml`'s `expanded_variants` menu via `_derive_variant_id` (RAISES on
no match — refuses to record a hallucinated ID), then writes
`artifacts/variant_selection.yaml` (chosen variant + resolved instrument/timeframe +
rationale) and `artifacts/variants_not_pursued.yaml` (every OTHER menu entry, verbatim, none
dropped/duplicated). Called from exactly one site, `run_loop`'s `backtest_specification`
branch (`:6462`), immediately after a successful `spec_ready` validation — i.e. it is
downstream of, and depends on, exactly the LLM-authored single-config-per-run model Slice 3
retires (config-direct authoring produces one config PER VARIANT, all pursued, so there is no
"selected vs. not pursued" distinction left to record under the flag). Confirmed **real
current call sites, no others**: `run_phase1_research.py:2063` (def), `:6462` (call);
consumers/testers are `tests/test_variant_selection_record.py` (480 lines) and
`tests/test_variant_anti_adjacency_gate.py` (678 lines, tests the E-034 S3 gate that reads
`variant_selection.yaml` right after it's written, `_route_post_variant_selection`, called
at `:6469`). The delivery plan's "become legacy" framing is accurate: under the flag, this
whole function's precondition (a single-selected-variant model) no longer exists, so it is
naturally unreachable rather than needing active retirement — but it must **remain reachable
and its existing tests must keep passing when the flag is off**, since `_variant_selection_record_enabled()`
is itself an independent, pre-existing flag this slice does not touch.

## 8. Consumers/tests enumerated (dispatch task 7)

**Tests asserting today's `backtest_specification` is LLM-driven or the `validation` stage's
current routing** (grepped across `strategy-research/tests/`, `-rln` on
`backtest_specification|backtest-engineering|determine_post_spec_route|validate_config`):
`test_anti_adjacency_retry_policy.py`, `test_e054_stage_wiring.py`,
`test_halt_quarantine_policy.py`, `test_k3_protocol_pinning.py`,
`test_prereg_conformance_gate.py`, `test_profit_bars_stop.py`, `test_run_id_allocation.py`,
`test_trial_accounting_characterization.py`, `test_variant_anti_adjacency_gate.py`,
`test_variant_selection_record.py`. None of these assert "backtest_specification always calls
an LLM" as a literal proposition to break — they exercise flag-gated behavior (E-054 gate
wiring, anti-adjacency retry, variant selection/gate) that sits AFTER a spec-ready
`backtest_spec.yaml` already exists, so they are agnostic to WHO produced it, matching E-056
S1's finding for `build_exclusion_digest.py`/`anti_adjacency_gate.py` (shape-dependent, not
authorship-dependent). **`test_e054_stage_wiring.py` is the closest thing to a stage-graph
identity test today** (`assert "data_availability_gate" in rpr.STAGE_CONFIGS`,
`rpr.STAGE_CONFIGS["data_availability_gate"]["handoff"] == ...`) — this is the literal
pattern Slice 3's own flag-off stage-graph-identity test should follow, now confirmed to
exist and be readable, not just referenced secondhand.

`determine_post_validation_route`'s only test-file dependents
(`test_run_phase1_research_cp1252.py`, `test_validation_route_family_status.py`) exercise the
function directly, not the stage graph — they call `rpr.determine_post_validation_route(d)`
on a synthetic run dir. These continue to pass unmodified whether or not `"validation"` stays
in `STAGE_CONFIGS`, since the function itself isn't touched by Slice 3 (only its ONE caller,
gated by the new flag, stops reaching it).

**No test in the repo currently asserts `STAGE_CONFIGS` has exactly 9 entries or enumerates
its full key set** (only `test_e054_stage_wiring.py` asserts membership of one specific key) —
so Slice 3 adding `strategy_config_authoring` and (flag-on) removing `validation` cannot break
an existing "stage count" assertion; the flag-off byte-identity test still needs to be new
code, not a modification of a test that doesn't exist yet.

## 9. S2 build-list proposal (per dispatch item 8 — proposal only, not executed)

In dependency order:

1. **`docs/STRATEGY_DESIGN_GUIDE.md`** — a rewrite/merge of `STRATEGY_CONFIG_REFERENCE.md`
   (§6 above: ~85-90% carried over) plus the 3 genuinely-new sections (instrument-set field,
   manifest contract, comparator-vocabulary note) plus authoring guidance folded from
   `backtest-engineering/SKILL.md`'s Checklist/Forbidden sections. A test verifying the
   component list stays in sync with `strategy_components.py` (`grep -c` pattern, §5) —
   `tests/test_design_guide_in_sync.py` per the delivery plan.
2. **`validate_config.py` V12: component-existence check** — import
   `strategies.strategy_components`, check `getattr(module, comp["class"].rsplit(".", 1)[-1])`
   (or equivalent) exists for every `class` value in both engines' `components[]` lists. This
   can ship independently of everything else in this slice (it strictly adds a check; no flag
   needed if scoped as a pure addition to `validate` — though the delivery plan frames it as
   living inside the NEW tool-stage's own logic, not `validate_config.py` itself, since the
   plan's own text says "no new registry needed unless 1.1 finds one" and treats it as part of
   `backtest_specification`'s new tool-branch, not the shared validator both flag states call).
   **This is the first sub-slice boundary candidate** (see §10).
3. **`strategy-config-authoring/SKILL.md`** — adapted from `backtest-engineering/SKILL.md`'s
   existing content (§1 above: this file already does ~80% of the target job). Pre-registered
   success signal per E-056 S1: byte-diff the retired skill's rule content against the new
   skill's rule content, confirm no rule silently dropped (the "Ungated hypotheses" and
   "Forbidden" sections in particular, §1/§4 above, must carry over intact).
4. **`hypothesis-design/SKILL.md` rewrite** — add criteria-from-`config/criterion_menu.yaml`
   (now real, 2 entries — confirmed §0), the pass-through rule, and (per §2's correction) only
   the cost-feasibility check genuinely needs relocating from `quant-validation`; the
   daily-feed-timing check is already here and needs no change.
5. **`innovation-expansion/SKILL.md` rewrite** — Step 2 becomes patch-writing
   (`variant_patches.yaml`: base + design patch + asset patch) instead of prose
   `expanded_variants`. This is the largest content change of the three skill rewrites (§1:
   currently zero structured-patch output of any kind exists here).
6. **Orchestrator wiring** (`run_phase1_research.py`):
   - `STAGE_CONFIGS` gains `strategy_config_authoring` (Claude, between
     `hypothesis_generation` and `innovation_expansion`) — a pure dict addition, safe under
     the flag-off/on split since it's simply not routed to when the flag is off.
   - `backtest_specification` becomes conditionally tool-only: `async_invoke_agent`'s
     `tool_stages` set (`:2440`) gains `"backtest_specification"` **only when
     `orchestrator.config_direct_authoring.enabled` is true** (the set-literal itself would
     need to become a function call or an `if` guard, not a bare literal, to support the
     conditional membership — a genuinely new code shape at this exact line, not a copy-paste
     of the existing two-tool-stage set).
   - `run_tool_worker` gains an `elif stage_name == "backtest_specification":` branch (§3's
     confirmed template shape) doing: apply each variant's patch (JSON pointer set) to the
     base config, call `validate_config.py` per variant, call the new component-existence
     check per variant, check manifest paths resolve, write
     `artifacts/variants/<variant_id>/strategy_config.json` per variant, and on any failure
     write `campaign_record/component_requests.yaml` + mark that variant `not_tested` in
     `artifacts/variants/index.yaml`.
   - `STAGE_CONFIGS["validation"]` entry and the `current_stage == "validation"` routing
     block (`:6434-6442`) both become flag-conditional removals — code stays for flag-off,
     is simply unreached when the flag is on (deletion from the live stage graph, not from
     the file).
7. **Flag registration**: `orchestrator.config_direct_authoring.enabled` in
   `config/campaign_config.yaml` (off by default) + `config/feature_flag_register.yaml` entry,
   following the exact documented pattern of `grid_evaluation`/`data_availability_gate`
   (§0 confirmed both exist and are readable as templates).
8. **Tests**: patch-application unit tests; component-existence check (positive/negative
   fixtures); manifest-path check; flag-off stage-graph identity
   (`test_e054_stage_wiring.py`-pattern, confirmed real and readable, §8); a new
   `tests/test_design_guide_in_sync.py`.
9. **Docs**: `strategy-research/docs/USER_GUIDE.md` §2.1 diagram, `strategy-research/CLAUDE.md`
   stage list (currently states "9 stages" — would need updating to 10 under the flag's own
   documentation convention, mirroring how the `data_availability_gate` addition was
   documented there), `DOC_INDEX.md`.

## 10. Sub-slice recommendation

**Recommend splitting into two S2 builds, not one.** Reasoning:

- **Sub-slice 3a — "Guide + validator hardening" (low risk, no orchestrator change):** item 1
  (design guide) + item 2 (component-existence check). Both are additive: the design guide is
  a doc, and the component-existence check is a pure addition to a validation path that
  already runs today (either inside `validate_config.py` as a V12, or as a new, independently
  flaggable check called wherever `backtest_specification`'s existing subprocess call already
  runs). **This sub-slice can ship and be tested in isolation, with its own before/after
  diff, before any skill or orchestrator code changes** — and it de-risks the harder work,
  since the design guide is exactly what the new skill (item 3) will be built against, and a
  wrong/incomplete guide would force a rewrite of the skill built on it.
- **Sub-slice 3b — "Skills + orchestrator + patches" (the actual declared behaviour
  change):** items 3-9. This is where the real risk concentrates — three skill rewrites, a
  new stage in `STAGE_CONFIGS`, a genuinely new conditional-membership code shape in
  `async_invoke_agent`'s `tool_stages` set (§9 item 6, confirmed not a copy-paste of existing
  code), a new `run_tool_worker` branch, and the `validation` stage's conditional removal —
  five independently-failing surfaces in one flag. Splitting this further (e.g. "stage
  registration + tool-worker branch" separate from "the three skill rewrites") is possible
  but not clearly worth it: the skill rewrites and the code that consumes their output
  (patches, manifest) are tightly coupled — a skill rewrite without the code to apply its
  output can't be tested end-to-end, and vice versa. Recommend 3b stays as one dispatch but
  budgets for its size (five files touched, all interdependent) rather than being treated as
  routine.

This split is justified by evidence gathered this session, not just slice size: item 2 (the
component-existence check) is the one piece of Slice 3 that closes a REAL, currently-exploitable
gap in production code today (§4 — a bad class name currently wastes a full backtest before
failing) independent of whether config-direct authoring ever ships. Shipping it standalone
gets that fix live sooner and de-risks it from the much larger, declared-behaviour-change
bundle.

## Not determined

- **Whether the dispatch's "mechanism purity" phrase (item 2 of the delivery plan's own
  Slice 3 bullet) refers to A1.3 (already in `hypothesis-design/SKILL.md` today, confirmed
  §2) or to something in `quant-validation/SKILL.md` under a different name** — no text
  literally labeled "mechanism purity" exists in `quant-validation/SKILL.md`; only the
  cost-feasibility/Improvement-09 check lives there. Flagging this as a real discrepancy for
  the operator to resolve before S2 build, not guessing which the plan author meant.
- **Where exactly a symbol/timeframe/instrument-set field would live in the config object**
  (top-level sibling of `regime_detector`/`strategies`/`aux_feeds`, or inside a new
  `block_manifest.yaml` only) — E-056 S1 flagged this gap; this session confirms the gap is
  real but does not resolve the placement question, since it depends on the composition
  (Slice 7) design that isn't built yet either.
- **Exact conditional-membership code shape for `tool_stages` in `async_invoke_agent`**
  (`:2440`) — confirmed this needs to change from a bare set literal to something
  flag-aware, but the precise implementation (a function call, an `if`/union, a
  config-read-per-call) was not designed here, only identified as a required, non-trivial
  code change at a specific line.
- **Full enumeration of every place `STAGE_CONFIGS["validation"]` or the literal string
  `"validation"` as a stage name is referenced beyond the two sites in §3 and the tests in
  §8** — a targeted grep for the two known real sites was done; a repo-wide grep for the bare
  string `"validation"` (which also matches unrelated things like schema validation, JSON
  Schema `"validation"` keys, etc.) was not exhaustively triaged line-by-line.
- **Whether `config/criterion_menu.yaml`'s current 2-entry state (vs. the richer menu E-046b
  S1 sketched) is sufficient for Slice 3's 1a criteria requirement, or whether Slice 3 is
  effectively blocked on more menu entries first** — not assessed against what a realistic
  hypothesis's `pass_rule` would need; flagged for the operator, not resolved here.

---

## Paste-ready Linear comment

**E-056 S2 (Slice 3: config written at 1b, patches, mechanical 5a) — characterization
complete (2026-09-21).** Read-only, worktree at `origin/master` tip `f01afc28`, not stale.
Full findings: `strategy-research/engineering/roadmap/E-056/S2_FINDINGS.md`.

Headline findings:
- **E-046b S2 (the grid) already merged** (`38269fe9`, `fec92e58`) — `config/criterion_menu.yaml`
  is real today, 2 live entries (`realized_edge_to_cost_ratio`, `sign_consistent_by_era`), 2
  commented-out pending slice 7. Nothing for Slice 3 itself exists yet anywhere in the repo
  (grepped clean).
- **The exact code seam for "backtest_specification becomes tool-only" is confirmed and
  concrete**: `run_phase1_research.py:2440`'s `tool_stages = {"protocol_execution",
  "data_availability_gate"}` set literal in `async_invoke_agent`, and `run_tool_worker`
  (`:1122`)'s `if/elif` subprocess-dispatch pattern — both already have a live 2-stage
  precedent to extend, not a pattern to invent.
- **Two corrections to the delivery-plan text itself**: (1) the "daily-feed timing" check the
  plan says needs relocating from `quant-validation` to `hypothesis-design` is **already in
  `hypothesis-design/SKILL.md`** (lines 130-137) — only the cost-feasibility check genuinely
  needs to move; (2) the "params typos are silently ignored" design-guide gap the plan lists
  as missing is **already explicit** in `STRATEGY_CONFIG_REFERENCE.md:108` — not a gap to close,
  only content to preserve.
- **`validate_config.py` (306 lines, V1-V11) confirmed to never check that a component
  `class` dotted path resolves to a real class** — today this only fails at engine startup,
  after a wasted backtest. The new component-existence check is a real, valuable, and
  independently-shippable fix.
- **Component count**: 24 (`grep -c`, matches CLAUDE.fork.md). Design guide estimate: ~85-90%
  of `STRATEGY_CONFIG_REFERENCE.md`'s existing 283 lines carry over near-verbatim; genuinely
  new content is the instrument-set field, the manifest contract, and one comparator-vocabulary
  callout — roughly 300-350 total lines in the merged result, not an order-of-magnitude
  larger new document.
- **`_record_variant_selection`/`variants_not_pursued.yaml`** (`:2063-2169`) traced fully:
  flag-gated, single real call site (`:6462`), naturally unreachable (not actively broken)
  once config-direct authoring makes every variant pursued — but its own flag and tests
  (`test_variant_selection_record.py`, `test_variant_anti_adjacency_gate.py`) must keep
  passing flag-off.
- **Recommendation: split into two S2 dispatches**, not one — 3a (design guide + the
  component-existence check, additive, independently valuable and shippable first) and 3b
  (the three skill rewrites + orchestrator wiring + the new tool-stage branch, the actual
  declared-behaviour-change bundle, five interdependent files). Do not split 3b further;
  its pieces are too tightly coupled to test in isolation.

Not determined (see file for full list): the "mechanism purity" phrase's real referent;
symbol/timeframe field placement; exact `tool_stages` conditional-membership code shape;
full `"validation"`-string reference audit; whether the 2-entry criterion menu is sufficient
for Slice 3's own 1a requirement.
