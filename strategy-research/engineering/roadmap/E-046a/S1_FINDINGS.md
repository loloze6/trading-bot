# E-046a Slice 5b (specialist readers) — S1 characterization findings (2026-09-22)

Read-only. No code, config, or backtest runs executed. `local_data/holdout_sealed/`
was not opened. Worktree HEAD and `origin/master` are both `c8a689dd` at dispatch
time (verified, not stale). Every file:line reference below was re-grepped fresh on
this worktree — none copied from the delivery plan or from
`SLICE_5B_SCOPE_PREVIEW.md`. That preview (same directory) is left untouched, as
instructed; this document supersedes it.

## 0. Headline correction to the delivery plan

`delivery_plan_v26.md` Slice 5's own text (§"5b", currently lines 307-326) names
exactly 6 callers of `verdict_interpretation.yaml` that would need re-pointing or
retiring: `_inject_regime_context_into_handoff`, `_auto_generate_findings_carryover`,
`_write_kb_findings_entry`, `_check_kb_reactivation_conformance`,
`campaign-review/SKILL.md`'s required-input list, and
`tools/near_miss_scoreboard.py`'s schema-diversity reader.

**The real count is larger, and the plan's own list contains one item that is not
actually a caller of this file at all.** Full trace below (§1). Short version:

- **3 of the plan's 6 named items are confirmed real** as stated:
  `_auto_generate_findings_carryover`, `_write_kb_findings_entry`,
  `tools/near_miss_scoreboard.py`.
- **1 of the 6 is confirmed real but mischaracterized**:
  `_inject_regime_context_into_handoff` does not read or write
  `verdict_interpretation.yaml` — it writes into the *upstream handoff that feeds
  the verdict_interpreter stage* (`protocol_to_verdict_interpreter.yaml`). Re-pointing
  it under Slice 5b means redirecting which reader's handoff gets the regime context
  injected, not touching anything downstream of the verdict artifact.
- **1 of the 6 (`_check_kb_reactivation_conformance`) is real, but is a
  content-consumer, not a file-reader** — it takes pre-extracted dict fields as
  parameters; its two real call sites are themselves inside other functions that do
  the actual `load_yaml()` call.
- **1 of the 6 (`campaign-review/SKILL.md`'s "required-input list") is confirmed
  FALSE**, not merely stale. See §2.
- **At least 7 additional real functions across 2 files directly call
  `load_yaml()` on `verdict_interpretation.yaml`'s path**, none named in the plan:
  `_verify_verdict_outputs`, `_write_promotion_audit`, `_route_holdout_evaluation`,
  `determine_post_verdict_route`, `determine_post_campaign_review_route`, `run_loop`
  (2 internal load sites), and `run_campaign.py::_extract_run_numbers`.
- **`determine_post_verdict_route`** (`strategy-research/workflow/run_phase1_research.py:6815-6816`)
  is the single most consequential omission: it is the actual routing brain that
  reads `status`/`root_cause` from the interpretation, applies the circuit breaker,
  and returns the next pipeline stage. It is not in the plan's list at all.

## 1. Full caller enumeration

All line numbers re-grepped fresh this session against
`strategy-research/workflow/run_phase1_research.py` (7900+ lines) and
`strategy-research/workflow/run_campaign.py`, via `grep -n verdict_interpretation`
narrowed with `awk` against a fresh `grep -n "^def "` function-boundary table (not
copied from any prior doc).

### Tier A — functions that directly call `load_yaml()` on `verdict_interpretation.yaml`'s path

| Function | File:line (def) | Load site(s) | What it does with the file |
|---|---|---|---|
| `_verify_verdict_outputs` | `run_phase1_research.py:5617` | `:5634` | Post-stage conformance check: verifies the right sibling deliverables exist for the declared status/lineage_routing. Not in the plan's list. |
| `_write_promotion_audit` | `run_phase1_research.py:5829` | `:5872` | Falls back to `interp["hypothesis_id"]` only when `promotion_audit.yaml` is absent (rare path — see fixture below). Not in the plan's list. |
| `_route_holdout_evaluation` | `run_phase1_research.py:6374` | `:6396` | Same fallback pattern — reads `hyp_id` only when `promotion_audit.yaml` doesn't exist yet. Not in the plan's list. |
| `determine_post_verdict_route` | `run_phase1_research.py:6815` | `:6816` | **Central routing function.** Reads `status`/`protocol_verdict`, applies E-018 mechanical-verdict override, F6 engineering-failure override, Improvement 01 `regime_misattribution` override, then `_apply_circuit_breaker(status, interp, campaign)`. Drives what the orchestrator does next. **Not in the plan's list at all.** |
| `determine_post_campaign_review_route` | `run_phase1_research.py:6986` | `:7035`, `:7125` (two separate load sites, different branches) | Reads the interpretation to resolve `next_research_question`/KB-conformance context for campaign-review follow-up routing. Not in the plan's list. |
| `run_loop` | `run_phase1_research.py:7410` (function start; the file/YAML checks are at `:7540`/`:7546` — existence+validity probe used to skip a redundant LLM call — and `:7886` — a real content load, used for the pivot check) | `:7540`, `:7886` | The orchestrator's own main loop: probes the file's existence to decide whether to re-invoke the stage, and loads it directly before calling `_route_pivot`/KB-conformance helpers. This is also where `_inject_regime_context_into_handoff` (§0) and `_validate_retune_firewall` (§3) are actually wired in — see below. |
| `_extract_run_numbers` | `run_campaign.py:1459` | `:1487` | Console-log helper only: pulls `status`/`protocol_verdict` into a `verdict_status` field for a one-line progress print (`_log_transition`, `run_campaign.py:1497`). Lowest-stakes of all the callers — purely cosmetic, easy to retire or leave orthogonal. |

That is **7 distinct functions across 2 files** that independently open the file —
already more than the plan's total of 6, before counting anything else.

### Tier B — functions that receive already-parsed `interp: dict` as a parameter (not file-readers themselves)

| Function | File:line | Real call sites | Note |
|---|---|---|---|
| `_route_pivot` | `run_phase1_research.py:4850` | called from `run_loop` | Takes `interp: dict` as a parameter (not a file path). Scans `interp`'s `primary_failure_mode`/`config_to_failure_map`/`root_cause` prose for a KB-exhausted family name before scaffolding a pivot. The docstring (`:4858`) is the only literal string match; the function itself never calls `load_yaml`. |
| `_auto_generate_findings_carryover` | `run_phase1_research.py:5532` | called from `run_loop`, after `verdict_interpreter` completes | Confirmed matches the plan's naming. Takes `interp: dict`, not a path — the docstring (`:5534`) names the file, the function body does not open it. |
| `_write_kb_findings_entry` | `run_phase1_research.py:5379` | called from `run_loop` | Confirmed matches the plan's naming. Takes `interp: dict`, not a path. |
| `_resolve_verdict_fields` | `run_phase1_research.py:6622` | called from `determine_post_verdict_route` and elsewhere | Docstring only (`:6626`) names the file; the function signature is `(interp: dict, original_status: str, breaker_status: str, pre_eval: dict | None)` — a pure dict-in/tuple-out resolver, no I/O. |
| `_check_pass_rule_evaluation_conformance` | `run_phase1_research.py:6689` | called from `determine_post_verdict_route` | **Not a file-reader at all** — takes `hypothesis_verdict`/`lineage_routing` strings as parameters (already extracted by its caller). The two grep hits (`:6718`, `:6724`) are inside f-string **violation messages** that happen to name the file for a human reading the log, not code that touches it. |
| `_check_kb_reactivation_conformance` | `run_phase1_research.py:4463` | `:4816`/`:4878` (inside `_route_pivot`), `:7004` (inside `determine_post_campaign_review_route`) | Confirmed matches the plan's naming (A5.4). Takes `next_research_question: dict` — a dict that happens to be derived from `verdict_interpretation.yaml`'s content by its callers, not the file itself. |

### Handoff-side (upstream of the artifact, not downstream)

| Function | File:line | Note |
|---|---|---|
| `_inject_regime_context_into_handoff` | `run_phase1_research.py:3497` | Called at `:7565`, inside `run_loop`'s `current_stage == "verdict_interpreter"` branch. **Writes into `RUN_DIR/handoffs/protocol_to_verdict_interpreter.yaml`** (`_vi_handoff`, `:7564`) — the handoff a stage reads on its way IN, not the artifact it produces. Confirmed via full function read (`:3497-3544`): it loads `handoff_path`, injects `regime_detector_confidence`/`ungated_escape_eligible` fields and a constraint string, and saves back to the same handoff path. **The plan's framing of this as a "caller of `verdict_interpretation.yaml`" is wrong** — it is a producer of one of the file's own *inputs*. Re-pointing it under Slice 5b means redirecting it at whichever reader replaces the regime-context consumer (almost certainly the regime-power reader), not touching the verdict artifact itself. |
| `_create_remaining_handoffs` | `run_phase1_research.py:3339` | `:3417` lists `"verdict_interpretation.yaml"` inside a `deliverables` list for the handoff the orchestrator itself expects `verdict_interpreter` to produce — bookkeeping for expected-output tracking, not a read of the artifact. |

### `tools/near_miss_scoreboard.py` — confirmed real, in scope

Full read of the relevant section: direct `load_yaml`-equivalent read at `:408`
(`verdict_path = run_dir / "artifacts" / "verdict_interpretation.yaml"`), doing
schema-diversity analysis across the run corpus (`:57-67` docstring: "21 of 59 run
dirs carry NO `verdict_interpretation.yaml` at all"), and a summary-line write at
`:536`. Matches the plan's description exactly.

### Confirmed NOT real production callers (scope-preview's spot-checks, re-verified)

- `tools/killed_run_gate.py:270` writes a **synthetic** `verdict_interpretation.yaml`
  inside `_pipeline_N` (`:263-278`), a test-fixture helper that seeds a fake run dir
  and calls the REAL `rpr._write_promotion_audit(run_dir, "run_audit")` — i.e. it
  exercises Tier A's `_write_promotion_audit`, it is not itself a production caller.
- `tools/anti_adjacency_gate.py:221` — comment only ("never
  verdict_interpretation.yaml's free-text..."), no read.
- `tools/lint_verdict_provenance.py`, `tools/record_schema.py`,
  `tools/verdict_criteria_evaluator.py` — not re-checked line-by-line this session
  (the scope preview's grep found only comment references in these three; I did not
  re-verify them independently — see Not determined).

**Total real, distinct code locations with a genuine dependency on this file's
existence/content: 7 (Tier A) + 6 (Tier B) + 2 (handoff-side) + 1
(`near_miss_scoreboard.py`) = 16**, across `run_phase1_research.py` (14),
`run_campaign.py` (1), and `tools/near_miss_scoreboard.py` (1) — roughly 2.7x the
plan's claimed 6, and the plan's own list both undercounts and misclassifies one
entry.

## 2. `campaign-review/SKILL.md` — resolved definitively

Read in full (236 lines, `strategy-research/workflow_artifacts/skills/campaign-review/SKILL.md`).

**The plan's claim is false, not stale-but-true-elsewhere.** Grep for the literal
string `verdict_interpretation` inside this file: zero hits — confirmed by full
read, not just grep. The file's own "Required inputs" section (`:16-18`) lists
exactly two files: `campaign_state.yaml` and `research_brief.yaml`. "Required
outputs" (`:20-21`) is `campaign_review.yaml` alone.

The file does reference `verdict_interpreter` **the skill/stage**, twice, but never
the artifact:
- `:125` — "`_write_kb_findings_entry`'s F09 hook" (a KB-writeback mechanism, not a
  required input).
- `:182-183` — a Forbidden-section cross-reference: fragment-pattern findings may
  never relitigate a verdict, "That is verdict_interpreter's exclusive domain... see
  `workflow_artifacts/skills/verdict-interpreter/SKILL.md`'s Forbidden section" —
  citing the *skill file*, not the artifact.

**Conclusion for Slice 5b:** there is nothing in `campaign-review/SKILL.md` to
re-point at the new readers' proposals — its own required-input list never named
`verdict_interpretation.yaml` and doesn't need to change on that account. (Slice 6a,
per the delivery plan's own text at `delivery_plan_v26.md:341`, separately plans to
give this skill `campaign_memory.yaml` as a new required input — unrelated to this
finding.)

## 3. `_validate_retune_firewall` — real definition, call site, and what re-pointing requires

Def: `run_phase1_research.py:3481-3494`. Body (verified, not paraphrased):

```python
_RETUNE_FORBIDDEN_TERMS = {
    "pnl", "sharpe", "ic", "backtest", "cost_drag",
    "forecast_return_corr", "per_trade", "expectancy",
}

def _validate_retune_firewall(regime_audit: dict) -> list:
    violations = []
    recommended = (regime_audit.get("recommended_action") or "").lower()
    for term in _RETUNE_FORBIDDEN_TERMS:
        if term in recommended:
            violations.append(...)
    return violations
```

**It validates `regime_audit_decision.yaml`, not `verdict_interpretation.yaml`.**
(The delivery plan's own text — `delivery_plan_v26.md:313-314` — already says this
correctly: "the retune firewall... re-pointed at its output" refers to the *regime
reader's* output, not the legacy verdict artifact; my read confirms the mechanism
this implies.)

Real, single call site: `run_loop`, `:7555-7563`, inside the
`current_stage == "verdict_interpreter"` branch, immediately BEFORE
`_inject_regime_context_into_handoff` (`:7565`) and gated on `_regime_aud` (loaded
from `regime_audit_decision.yaml`, `:7554`) being present:

```python
if _regime_aud:
    _fw_violations = _validate_retune_firewall(_regime_aud)
    if _fw_violations:
        raise RuntimeError("RETUNE FIREWALL VIOLATION ...")
_vi_handoff = RUN_DIR / "handoffs" / "protocol_to_verdict_interpreter.yaml"
_inject_regime_context_into_handoff(_vi_handoff, _regime_rpt, _regime_aud, run_id)
```

**What re-pointing it requires:** the firewall check itself needs zero code
changes — it already operates on `regime_audit_decision.yaml`, independent of
which downstream skill consumes the result. What moves is the *call site*: today
it runs once, guarding the single `verdict_interpreter` invocation. Under Slice 5b,
only the regime-power-category reader needs `regime_audit_decision.yaml`/
`regime_detector_report.yaml` context (the other 4 readers have no reason to see
regime-audit data at all) — so the guard-and-inject pair
(`_validate_retune_firewall` + `_inject_regime_context_into_handoff`) needs to move
from "before invoking verdict_interpreter" to "before invoking the regime-power
reader specifically," inside whatever new per-category dispatch loop
`specialist_readers` ends up being (see §5). This is a call-site relocation, not a
logic change.

## 4. Specialist-reader skills — confirmed absent; `verdict-interpreter/SKILL.md` read in full

`find strategy-research/workflow_artifacts/skills -maxdepth 2 -iname "*reader*"` and
a direct listing of the skills directory both confirm: no `readers/` directory and
no `<category>-reader` skill directories exist anywhere in the repo yet. Current
skill directories (10 total): `backtest-engineering`, `campaign-review`,
`hypothesis-design`, `innovation-expansion`, `quant-fundamentals`,
`quant-validation`, `regime-auditor`, `research-system-evolution`,
`strategy-config-authoring`, `verdict-interpreter`.

`verdict-interpreter/SKILL.md` read in full (780 lines) — the skill Slice 5b
retires. Its real shape, for whoever builds the 5 replacement skills:

- **Required inputs** (13 named items, `:13-59`): `protocol_result.yaml`,
  `pass_rule_evaluation.yaml`, `validation_protocol.yaml`, `backtest_spec.yaml`,
  `research_brief.yaml`, `campaign_state.yaml`, `trade_diagnostics.json`,
  `post_backtest_routes` (injected into the handoff, not a file),
  `config/coin_universe.yaml`, `innovation_notes.yaml`,
  `near_miss_scoreboard.yaml`, and conditionally `grid_evaluation.yaml`/
  `idea_status.yaml` — i.e. it currently reads the FULL run context, not one
  report category. Each of the 5 new readers is supposed to read only its own
  report + `grid_evaluation.yaml` (delivery plan text) — a much narrower context
  window than today's monolithic skill.
- **MACHINE-AUTHORED VERDICT** (`:61-95`): when `pass_rule_evaluation.yaml` is
  binding, `hypothesis_verdict`/`lineage_routing` are copy-through, not
  independently decided — this authority model is untouched by Slice 5b per the
  delivery plan (E-018's mechanical routing already bypasses the LLM's own
  restated verdict at `determine_post_verdict_route`, §1 above) but whichever
  reader ends up owning `verdict_interpretation.yaml`'s replacement schema
  (`proposals/<category>.yaml` — none of the 5 readers appear to own a single
  merged verdict) needs an owner for this copy-through discipline, or it needs to
  move to deterministic code. **Not resolved by this pass — see Not determined.**
- **Required outputs** (`:146-152`): `verdict_interpretation.yaml` always;
  `findings_carryover.yaml` when routing is refine/pivot/escalate; exactly one of
  `proposed_brief.yaml`/`escalation_request.yaml`/`research_decision.yaml`. None of
  these map 1:1 onto the delivery plan's `proposals/<category>.yaml` shape (§7)
  — the new schema is per-category evidence+scores, not a single routing decision.
  **This is the single largest open design question for Slice 5b**, distinct from
  the caller-re-pointing work: something still has to produce
  `hypothesis_verdict`/`lineage_routing`/`findings_carryover.yaml`/
  `proposed_brief.yaml` for the ~16 Tier A/B callers in §1 to consume, and the
  delivery plan's text names no owner for that synthesis step. **Not determined.**
- Six numbered diagnostic Rules (`:378-486`), an Asset-stability gate (`:680-720`),
  Trade Attribution (`:563-622`), Fee-reduction autopsy (`:732-770`) — all
  currently living in ONE skill's prose. These map fairly cleanly onto the 5
  report categories (Rules 1/5 → profitability, Trade Attribution/Fee-reduction →
  trade_efficiency, Rule 2/3/6 → forecast_power, Rule 4 + Regime Attribution Gate →
  regime_power) but component_attribution has no obvious existing rule-block
  analog in this file — it is new territory for whichever reader owns it.

## 5. `specialist_readers` as one looping stage — the real constraint

Confirmed exactly as the delivery plan states: `_invoke_agent_with_yaml_retry`
(`run_phase1_research.py:630-665`) makes exactly ONE call to
`async_invoke_agent(current_stage, run_id, retry_context=...)` per invocation (plus
its own bounded YAML-repair retry, unrelated to fan-out). There is no loop over
multiple skills inside it.

The deeper constraint, traced this session: `async_invoke_agent(stage_name, ...)`
(`:3202-3244`) does `config = STAGE_CONFIGS[stage_name]` (`:3215`) for its handoff
path, and `run_claude_worker` (called at `:3241`) resolves which skill to load via
the module-level `_SKILL_MAP` dict (`:755-763`):

```python
_SKILL_MAP = {
    "hypothesis_generation": "hypothesis-design",
    "strategy_config_authoring": "strategy-config-authoring",
    "innovation_expansion": "innovation-expansion",
    "validation": "quant-validation",
    "backtest_specification": "backtest-engineering",
    "verdict_interpreter": "verdict-interpreter",
    "campaign_review": "campaign-review",
}
```

**One `stage_name` string maps to exactly one skill directory and one handoff
file — there is no list-of-skills shape anywhere in this machinery.** A
`specialist_readers` stage that must invoke 5 different skills
(`readers/<category>-reader/SKILL.md`, each with its own report input and its own
`proposals/<category>.yaml` output) cannot simply call
`_invoke_agent_with_yaml_retry("specialist_readers", ...)` five times — every call
would resolve to the same single `_SKILL_MAP["specialist_readers"]` entry and the
same handoff file.

This means genuinely new orchestration code is required, of roughly the shape
`STAGE_CONFIGS["protocol_execution"]`'s existing `tool_stages` special-casing
already established as a precedent (E-056 S2's own finding, confirmed still true
at `:3203-3211`: `tool_stages` is a conditionally-extended set literal, not a
`STAGE_CONFIGS`-driven dispatch) — concretely, either:
(a) a new internal loop inside the `current_stage == "specialist_readers"` branch
of `run_loop` that calls a lower-level worker (a new `run_claude_worker`-adjacent
function accepting an explicit skill-directory override, not derived from
`_SKILL_MAP[stage_name]`) once per category, each with its own report file input
and its own handoff/deliverable path; or
(b) 5 sub-stage identifiers that never appear in the operator-visible `STAGE_CONFIGS`
stage list but are dispatched internally by the same loop.
Either way, `_SKILL_MAP` and `STAGE_CONFIGS[stage_name]["handoff"]`'s 1:1 shape is
the thing that has to change or be worked around — not something Slice 5b can
reuse unmodified. This is the same category of "genuinely new code shape at an
identified line" that E-056 S2 already flagged for `tool_stages`
(`S2_FINDINGS.md` §3/§9 item 6) — same pattern, different exact line.

## 6. `artifacts/reports/*.yaml` — Slice 5a's real, merged shape

Slice 5a is merged (`196985ee "feat(E-046a S5a): category reports"`,
`7ca4c89f`, both in `git log` for `strategy-research/tools/build_reports.py`).
`REPORT_CATEGORIES` (`build_reports.py:99-105`) is exactly:

```python
REPORT_CATEGORIES = [
    "profitability", "trade_efficiency", "forecast_power",
    "regime_power", "component_attribution",
]
```

— matching the delivery plan's 5 names exactly, byte-for-byte. Each category has
its own `build_<category>_report(sources: dict) -> dict` function
(`:230, :279, :314, :499, :594`) wrapped by a shared `_wrap(category, overall,
per_window, per_regime, per_symbol)` helper (`:128-140`) — confirming the
`category × slice` shape (`overall`/`per_window`/`per_regime`/`per_symbol`) the
delivery plan describes is real and uniform across all 5 files, not
category-specific. Wired into `run_loop` at two call sites (`:1566-1572` and
`:1731-1737`), gated by `_category_reports_enabled()` (`:2047-2060`, flag
`orchestrator.category_reports.enabled`, off by default) — both call
`build_reports.build_reports(RUN_DIR, write=True)`.

**No committed run directory under `strategy-research/runs/*/artifacts/reports/`
exists** — the flag has apparently never been run end-to-end and committed in this
repo, so there is no real example output to eyeball; the shape confirmation above
comes from reading the report-builder code directly, not from a real artifact.
Nothing in the code read would surprise a reader-skill author: field names inside
each `_wrap()` call are plain, category-specific dicts (e.g. `profitability`'s
`overall`/`per_window`/`per_regime`/`per_symbol` built directly from
`protocol_result.yaml`'s existing fields, `:230-272`), not some novel intermediate
representation.

## 7. `artifacts/proposals/<category>.yaml` schema — grounded against the design guide

`strategy-research/docs/STRATEGY_DESIGN_GUIDE.md` **already exists** (503 lines,
merged via Slice 3a: `a6b6ba53`, `70054c89`) — this was not confirmed in any prior
doc I could find and materially changes the "design-guide vocabulary" instruction
from abstract to concrete. Its §7c (`:416-437`), **"The manifest contract
(`block_manifest.yaml`) — PROPOSED, NOT BUILT"**, is the closest existing precedent
for "block sketch in design-guide vocabulary":

```yaml
block:
  kind: forecast | regime
  config_paths: [...]
scaffolding: [...]
rationale: ...
```

This is explicitly marked PROPOSED, NOT BUILT in the guide itself — i.e. the
vocabulary exists as a documented, not-yet-implemented contract, which is exactly
the shape a reader's `kind: patch | new_block` proposal should reuse: `kind:
new_block` in `proposals/<category>.yaml` should almost certainly mean "a
`block_manifest.yaml`-shaped block sketch" (kind/config_paths/rationale), while
`kind: patch` has no existing guide precedent yet and would need to reuse
`STRATEGY_DESIGN_GUIDE.md`'s "Component variant patterns" section (`:265-291`,
concrete before/after component YAML diffs) as its vocabulary instead. Grounded
proposed schema:

```yaml
proposal_id: <category>-<run_id>-<n>
kind: patch | new_block
patch:              # kind: patch — a Component variant pattern (guide §"Component
  ...                # variant patterns", :265-291): before/after component-spec diff
block:               # kind: new_block — a block_manifest.yaml sketch (guide §7c,
  kind: forecast | regime   # :416-437), even though the manifest itself is unbuilt
  config_paths: [...]
  scaffolding: [...]
evidence: [<numbers cited, each traceable to a field in this category's report.yaml>]
scores:
  confidence_real: 0-3        # anchor text TBD — not in the guide or the plan
  distance_to_profitable: 0-3
  mechanism_plausibility: 0-3
model_id: <str>
rubric_version: <str>
```

**Not resolved by this pass:** the 0-3 anchor text for each score dimension —
neither `delivery_plan_v26.md` nor `STRATEGY_DESIGN_GUIDE.md` defines it. This is
real, undesigned rubric content the S2 build needs to author, not something this
characterization pass can recover from existing files.

## 8. S2 build-list proposal and split recommendation

Proposed build order:

1. **5 skill files** `workflow_artifacts/skills/readers/<category>-reader/SKILL.md`
   — adapted from `verdict-interpreter/SKILL.md`'s relevant rule subsets (§4's
   category mapping), each scoped to read only its own `reports/<category>.yaml` +
   `grid_evaluation.yaml`, writing `proposals/<category>.yaml` (§7 schema).
2. **The verdict-synthesis owner** — §4's largest open question: something must
   still produce `hypothesis_verdict`/`lineage_routing`/`findings_carryover.yaml`/
   `proposed_brief.yaml`/`research_decision.yaml` for the 16 Tier A/B callers in §1
   to keep functioning. The delivery plan is silent on this. This has to be
   designed (not just characterized) before build, or Slice 5b cannot ship without
   breaking `determine_post_verdict_route` and everything downstream of it.
3. **Orchestrator loop** — the new `specialist_readers` dispatch mechanism (§5):
   extend or bypass `_SKILL_MAP`/`STAGE_CONFIGS[stage]["handoff"]`'s 1:1 shape to
   support 5 sequential skill invocations inside one operator-visible stage.
4. **Call-site re-pointing** — the 16 real locations from §1, individually:
   7 Tier-A direct loaders need to read from wherever item 2's synthesis lands
   instead of `verdict_interpretation.yaml`; 6 Tier-B functions likely need no
   internal change if item 2 hands them an equivalent `interp`-shaped dict; the 2
   handoff-side functions (`_inject_regime_context_into_handoff`,
   `_validate_retune_firewall`'s call site) move into the regime-power reader's
   dispatch branch per §3.
5. **`STAGE_CONFIGS["verdict_interpreter"]` removal** (flag-conditional, mirroring
   the `validation` stage's own precedent from E-056 Slice 3b:
   `STAGE_CONFIGS.py:186-189` entry + the `current_stage == "verdict_interpreter"`
   branches at `:7539` and `:7885` both become conditional).
6. **Tests**: report re-projection property test (already specified by the plan);
   proposals schema validation; firewall re-pointing; flag-off byte-identity for
   the full 16-caller surface — this last one is materially larger test surface
   than the plan's text implies, given the real caller count in §1.

**Recommendation: split into at least two S2 dispatches, not one — larger split
than E-056 S2 needed for its own Slice 3.** Reasoning:

- **5b-i — Readers + reports consumption (lower risk, additive):** items 1 and 6's
  report/proposal-schema tests. The 5 skill files and their scoped inputs/outputs
  can be built and unit-tested against Slice 5a's already-merged, already-real
  report files without touching a single existing caller — genuinely additive,
  same shape as Slice 5a itself.
- **5b-ii — Verdict-synthesis + orchestrator loop + the 16-caller re-point (the
  actual declared-behaviour change, high risk):** items 2-5. This is where Slice
  5b differs sharply from what the plan implies: item 2 (who synthesizes the
  routing decision from 5 independent proposals) is undesigned, not just
  uncharacterized, and item 3 (the orchestrator loop) requires new code at a
  precise, identified seam (§5) that doesn't exist as a reusable pattern anywhere
  in the codebase yet — `tool_stages`' conditional-set-literal precedent is the
  closest analog but is not a loop, just a conditional membership test.
  Recommend NOT bundling this with 5b-i: 5b-i can ship and be validated (mocked
  LLM, §9) independently; 5b-ii cannot be scoped further without first resolving
  item 2 as a design decision (an operator call, not something S1/S2 can decide
  unilaterally) — **this should go back to the operator as an open design
  question before an S2 dispatch is written for 5b-ii**, not be handed to a
  build lane to improvise.

This is a materially different recommendation than E-056 S2's own Slice 3 split
(3a/3b, both buildable immediately) — Slice 5b's second half is blocked on a real
design decision, not just larger in scope.

## 9. Run budget / LLM-key feasibility — confirmed infeasible in this environment, precedent found

`ANTHROPIC_API_KEY` is **not set** in this build environment (checked directly,
value not echoed). The 5 reader skills are Claude-Agent-SDK-invoked exactly like
`verdict-interpreter` today (`handoff.get("assigned_engine", "claude")` default,
`:3237-3241`) — real invocation is not testable here.

**This exact situation already has a precedent, twice, in this repo's own recent
history** (not previously documented in `S1_FINDINGS.md`/`S2_FINDINGS.md` for other
slices, but present in their commit messages):
- E-056 Slice 3b's commit (`f65182a2`): "Flag registered ... (off_incomplete: built
  and unit tested, but not proven against a real LLM pass — no API budget in this
  environment)."
- E-033.1 Slice 4a's commit (`5d51a57c`): "subprocess mocked — no resolvable
  trading-bot venv in this build environment, following
  `test_e056_config_direct_authoring.py`'s precedent."

Both precedents are captured in `config/feature_flag_register.yaml`'s `state:
off_incomplete` value (used 7+ times in that file, e.g. `:76`, `:93`, `:105`,
`:130`, `:152`, `:205`), which the register's own header comment (`:20`) defines as
built-and-unit-tested-but-not-proven-against-a-real-pass.

**Recommendation for Slice 5b's S2 build**: plan for a mocked-LLM-response test
strategy from the start, following `test_e056_config_direct_authoring.py`'s exact
precedent (not discovered here in detail — flagged for the S2 build to read
directly). Ship `orchestrator.specialist_readers.enabled` as `state:
off_incomplete` in `feature_flag_register.yaml`. The plan's stated "Run budget: 2
real runs read by all five readers" is **not achievable in this environment** and
should not be treated as an S2 acceptance criterion here — it requires a session
with real API budget, exactly as Slice 3b's own text already establishes as
acceptable practice for this codebase.

## Not determined

- **Who synthesizes `hypothesis_verdict`/`lineage_routing`/`findings_carryover.yaml`/
  `proposed_brief.yaml`/`research_decision.yaml` once 5 independent
  `proposals/<category>.yaml` files exist instead of one `verdict_interpretation.yaml`.**
  The delivery plan's text does not name an owner. This blocks scoping §8's
  5b-ii build list precisely — flagged as an operator design decision, not
  something resolved by this characterization pass.
- **The 0-3 anchor text for `confidence_real`/`distance_to_profitable`/
  `mechanism_plausibility`** (§7) — not defined anywhere in the repo today.
- **Whether `tools/lint_verdict_provenance.py`, `tools/record_schema.py`, and
  `tools/verdict_criteria_evaluator.py`'s comment-only references (per the scope
  preview) are genuinely comment-only** — not independently re-verified this
  session; taken on the scope preview's word.
- **Exact new function signature for the per-category worker override** (§5) — a
  new `run_claude_worker`-adjacent function accepting an explicit skill directory
  independent of `_SKILL_MAP[stage_name]` is clearly required, but its precise
  shape was not designed here, only identified as necessary.
- **`test_e056_config_direct_authoring.py`'s mocked-LLM-response pattern's exact
  mechanics** (§9) — confirmed to exist and be the citable precedent, but not
  read in this session; the S2 build should read it directly rather than rely on
  this document's characterization.
- **Whether component_attribution has a natural home in
  `verdict-interpreter/SKILL.md`'s existing rule prose** (§4) — confirmed it does
  NOT (no existing rule block maps to it), but what its reader's rules should
  actually say is undesigned, new content.

---

## Paste-ready Linear comment

**E-046a Slice 5b (specialist readers) — S1 characterization complete (2026-09-22).**
Read-only, worktree at `origin/master` tip `c8a689dd`, not stale. Full findings:
`strategy-research/engineering/roadmap/E-046a/S1_FINDINGS.md`.

Headline findings:
- **Real caller count for `verdict_interpretation.yaml`: 16 distinct code
  locations across `run_phase1_research.py` (14), `run_campaign.py` (1), and
  `tools/near_miss_scoreboard.py` (1)** — not the plan's claimed 6. Of the plan's
  own 6: 3 confirmed as stated, 1 confirmed but mischaracterized
  (`_inject_regime_context_into_handoff` writes the UPSTREAM handoff, not the
  artifact), 1 confirmed but is a content-consumer not a file-reader
  (`_check_kb_reactivation_conformance`), and 1 confirmed **false**
  (`campaign-review/SKILL.md` — read in full, zero references to
  `verdict_interpretation` anywhere, required inputs are only `campaign_state.yaml`/
  `research_brief.yaml`). The single biggest omission: `determine_post_verdict_route`
  (`run_phase1_research.py:6815`), the actual routing brain (reads status,
  root_cause, runs the circuit breaker) — entirely absent from the plan's list.
- **`_validate_retune_firewall` traced fully** (`:3481-3494`, real call site
  `:7555-7563`): validates `regime_audit_decision.yaml`, not the verdict artifact;
  re-pointing it under Slice 5b is a call-site relocation (into the regime-power
  reader's dispatch) with zero logic change needed.
- **The orchestrator has a real, confirmed architectural gap for "one looping
  stage":** `_SKILL_MAP` and `STAGE_CONFIGS[stage]["handoff"]` are both strict 1:1
  (one stage name → one skill → one handoff file, `:755-763`/`:3215-3216`). A
  `specialist_readers` stage invoking 5 different skills needs genuinely new
  orchestration code, not 5 calls to existing single-call machinery.
- **`STRATEGY_DESIGN_GUIDE.md` already exists** (503 lines, merged, Slice 3a) —
  its §7c `block_manifest.yaml` contract (PROPOSED, NOT BUILT) is the concrete
  vocabulary a `kind: new_block` proposal should reuse; `kind: patch` should reuse
  its "Component variant patterns" section instead.
- **Biggest open design gap, not just a characterization gap**: nothing in the
  delivery plan names who synthesizes a single routing decision
  (`hypothesis_verdict`/`lineage_routing`) once the verdict is split across 5
  independent `proposals/<category>.yaml` files. This blocks precise scoping of
  half the slice and should go back to the operator before an S2 build dispatch
  for that half is written.
- **Run budget is infeasible in this environment**: no `ANTHROPIC_API_KEY` set.
  Real precedent exists twice already (E-056 Slice 3b, E-033.1 Slice 4a commit
  messages) for shipping `state: off_incomplete` with a mocked-LLM test strategy
  instead of the plan's "2 real runs" acceptance bar.

**Recommendation: split Slice 5b into two S2 dispatches**, larger split than
Slice 3's 3a/3b — **5b-i** (5 reader skills + report/proposal-schema tests,
additive, buildable now against Slice 5a's already-merged reports) and **5b-ii**
(verdict-synthesis + orchestrator loop + the 16-caller re-point, the real
behaviour change) — but 5b-ii should not be dispatched as S2 yet: it depends on
an undesigned decision (who synthesizes the routing verdict) that needs an
operator call first, not a build-lane improvisation.

Not determined (full list in file): verdict-synthesis ownership; score-dimension
anchor text; whether 3 tools' comment-only status (lint_verdict_provenance,
record_schema, verdict_criteria_evaluator) is genuinely comment-only; exact
per-category worker function signature; `test_e056_config_direct_authoring.py`'s
mock pattern mechanics; component_attribution's reader-rule content (confirmed no
existing analog, content itself undesigned).
