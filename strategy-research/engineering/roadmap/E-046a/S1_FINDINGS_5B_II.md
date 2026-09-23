# E-046a Slice 5b-ii (verdict-synthesis + orchestrator loop + 16-caller re-point) — deep S1 characterization (2026-09-22)

Read-only. No code, config, or backtest runs executed. `local_data/holdout_sealed/`
was not opened. Worktree base and `origin/master` are both `ccde0329` at dispatch
time (verified, not stale). Every file:line reference below was re-grepped fresh on
this worktree this session — none copied from `S1_FINDINGS.md` (the 5b-wide
document) or `SLICE_5B_SCOPE_PREVIEW.md` without independent verification. All of
`S1_FINDINGS.md`'s own line numbers for `run_phase1_research.py` were re-checked and
found byte-identical (same commit, no drift) — cited directly below without
re-deriving, except where noted as corrected.

This document goes deep on 5b-ii specifically, now that 5b-i (the 5 reader skills +
`proposal.schema.json`, commits `7ac22dba`/`bfe15b66`, merged `ccde0329`) is real and
readable. It assumes `S1_FINDINGS.md` §1 (16-caller enumeration), §2
(campaign-review/SKILL.md resolved false), §4 (verdict-interpreter's real shape),
§6 (reports), §7 (proposal schema origin) as background and does not re-derive them
except where this pass found something S1 missed or got wrong.

## 1. Correction to S1_FINDINGS.md §8 item 5 — the `STAGE_CONFIGS` removal claim

**S1's own citation is wrong, and the delivery plan's "removed from STAGE_CONFIGS"
framing has no existing code precedent — it would be new territory, not a mirror of
the `validation` stage's removal.**

- `S1_FINDINGS.md` §8 item 5 says: "`STAGE_CONFIGS["verdict_interpreter"]` removal
  ... mirroring the `validation` stage's own real precedent from Slice 3b:
  `STAGE_CONFIGS.py:186-189` entry". **`:186-189` is `verdict_interpreter`'s OWN
  dict entry** (`run_phase1_research.py:186-190`, confirmed by direct read: `{
  "handoff": "protocol_to_verdict_interpreter.yaml", "default_next":
  "dynamic_routing", "skill": "verdict-interpreter" }`), not `validation`'s (which
  is `:154-166`). S1 cited the wrong stage's own entry as if it were the
  precedent being mirrored.
- More importantly: **the real `validation`-stage precedent does not delete
  anything from `STAGE_CONFIGS`.** Confirmed by direct read of
  `run_phase1_research.py:7631-7646` (the `innovation_expansion` routing branch)
  and its own comment at `:7639-7641`: *"under config-direct authoring, the
  validation stage becomes naturally unreached (not deleted) -- redirect its ADMIT
  target straight to the tool-only backtest_specification stage instead."* The
  `validation` STAGE_CONFIGS entry (`:154-166`) stays in the dict, byte-identical,
  flag-on or flag-off; only the ROUTING (`next_stage` assignment at
  `run_loop:7645-7646`) is conditional. `strategy_config_authoring` (E-056 Slice 3b)
  follows the identical pattern: registered unconditionally (`:140-144`, `_SKILL_MAP`
  `:757`), routed to only when `orchestrator.config_direct_authoring.enabled` is on
  (`run_loop:7610-7611`).
- **No existing code anywhere in this file literally removes a key from the
  `STAGE_CONFIGS` dict at runtime, conditionally or otherwise.** The delivery plan's
  own text (`delivery_plan_v26.md:315-316`, re-confirmed this session: "the
  `verdict_interpreter` stage is removed from `STAGE_CONFIGS` under this slice's
  flag, not kept as a narrator") asks for something stronger than any precedent in
  this codebase. This is buildable (Python dict deletion, or a flag-gated
  dict-comprehension filter at module load, or simply never adding it back once
  `specialist_readers` exists and this repo decides to hard-cut the old stage) but
  it is **new pattern, not a mirror** — S2 should not cite Slice 3b as prior art for
  the deletion mechanic itself, only for the general idea of "flag-gated stage
  behavior change."
- **Recommendation for 5b-ii's actual design, consistent with every other flag in
  this file:** follow the `validation`/`strategy_config_authoring` pattern instead
  of literal deletion — keep `STAGE_CONFIGS["verdict_interpreter"]` in the dict
  unconditionally (cheapest, most consistent with this file's own established
  convention, zero risk of a `KeyError` from any code that still does
  `STAGE_CONFIGS["verdict_interpreter"]` a stale reference), and make it
  **unreached** by changing `STAGE_CONFIGS["protocol_execution"]["default_next"]`
  (`:184`, currently `"verdict_interpreter"`) to `"specialist_readers"` when the
  flag is on, mirroring exactly how `innovation_expansion`'s routing branch
  redirects around `validation`. This also sidesteps the literal-deletion question
  entirely — a real, provable disagreement with the delivery plan's exact wording
  that should go back to the operator, not be resolved unilaterally here.

## 2. The `run_claude_worker` deliverable-write path — a real, previously-uncharacterized blocker for `artifacts/proposals/<category>.yaml`

**Not found by `S1_FINDINGS.md` (which characterized the stage-dispatch layer,
`_SKILL_MAP`/`STAGE_CONFIGS`, but not how a stage's LLM output actually becomes a
file on disk).** Traced this session, full read of `run_claude_worker`
(`run_phase1_research.py:862-966`):

```python
# :949
pattern = r"```yaml\s*#\s*([a-zA-Z0-9_.]+\.yaml)\s*(.*?)```"
matches = re.findall(pattern, agent_output, re.DOTALL)
...
# :961
dest_path = path / "artifacts" / filename.strip()
with open(dest_path, "w", encoding="utf-8") as f:
    f.write(yaml_content.strip())
```

The model is expected to emit a fenced block headed by a comment naming the
filename (e.g. ` ```yaml\n# verdict_interpretation.yaml\n...` `, per
`_build_stage_prompt`'s own prompt template, `:841-846`: *"# filename.yaml"*). The
filename capture group **`[a-zA-Z0-9_.]+` explicitly excludes `/`** — it cannot
match `proposals/profitability.yaml`. `dest_path` is always
`path / "artifacts" / filename` with **no `.parent.mkdir()` call anywhere in this
function** — even if the regex were widened to allow `/`, writing to a
not-yet-existing `artifacts/proposals/` subdirectory would raise
`FileNotFoundError` on the `open(..., "w")` call, since `Path.open("w")` does not
create parent directories.

Grepped `"proposals"` across the entire file: **zero hits.** The orchestrator has no
knowledge of the `proposals/` subdirectory at all today — every one of Slice 5a's
`reports/*.yaml` files is written by `tools/build_reports.py` directly (real Python
I/O, not through this LLM-output-parsing path, so reports never hit this
limitation), but `proposals/*.yaml` per the 5 reader `SKILL.md` files' own "Required
outputs" sections (all 5 read: `artifacts/proposals/<category>.yaml`, e.g.
`profitability-reader/SKILL.md:58`) **are** meant to be written by an LLM-invoked
skill, which today can only go through `run_claude_worker`'s regex-and-flat-write
path (or the parallel `run_gemini_worker` path, `:1096-1097`, which has the
identical flat-filename limitation: `re.sub(r'^[a-zA-Z0-9_\-.]+\.yaml\s*\n', ...)` at
`:1096` plus a hardcoded `stage_outputs` dict at `:1101-1111` with no
`specialist_readers`/reader-category entry).

**This is a concrete, previously-undiscovered implementation blocker for the
orchestrator loop (task 3), not a design nicety.** Whatever new lower-level worker
function `specialist_readers`'s loop calls (§3 below) must either: (a) pass an
explicit destination path per category (bypassing the general-purpose
filename-from-model-output convention entirely — the new function decides the
output path itself, e.g. `RUN_DIR / "artifacts" / "proposals" / f"{category}.yaml"`,
and just extracts the YAML body from whatever fenced block the model returns,
ignoring its self-declared filename), or (b) widen the regex to accept `/` AND add
`dest_path.parent.mkdir(parents=True, exist_ok=True)` before the `open()` call —
touching `run_claude_worker` itself (used by every other stage), which is a real,
if narrow, edit to shared code, not purely additive. **(a) is lower-risk**: it keeps
`run_claude_worker` itself untouched (bit-identity for every existing stage
preserved trivially) and matches the "new function accepting an explicit
skill-directory override" shape S1 §5 already flagged as necessary for the
`_SKILL_MAP` problem — the same new function can also own the explicit output path,
solving both problems in one seam.

## 3. Orchestrator loop — concrete design, building on S1 §5's two shapes

S1 §5 (re-confirmed, `async_invoke_agent:3202-3211`, `_SKILL_MAP:755-763`,
`_build_stage_prompt:766-859`) already established that `_SKILL_MAP` is strict 1:1
and that the actual skill-resolution choke point is `_build_stage_prompt`'s own
`skill_file_name = _SKILL_MAP.get(stage_name)` at **`:775`** (not `_SKILL_MAP` in
isolation — `_build_stage_prompt`, extracted E-032 S2a per its own docstring
`:768-774`, is a pure function `run_claude_worker` calls at `:867`, and is the single
real seam).

**Recommendation: shape (a) from S1 §5** — a new internal loop inside `run_loop`'s
`current_stage == "specialist_readers"` handling, calling a new lower-level worker.
Concretely, grounded in what actually surrounds the existing `verdict_interpreter`
branch (`run_loop:7539-7589`, full read this session):

- The existing `elif current_stage == "verdict_interpreter":` skip-check
  (`:7539-7548`), regime-context injection (`:7550-7565`), and single
  `_invoke_agent_with_yaml_retry(current_stage, run_id, RUN_DIR, expected_outputs,
  state)` call (`:7586`, inside the shared `if not _skip_agent: ... else:` block at
  `:7578-7589`) are all **linear, single-stage-scoped code**, not a generic
  dispatch table — there is no existing "loop N times" shape anywhere in this
  region to reuse. A `specialist_readers` branch replacing this needs its own
  `for category in REPORT_CATEGORIES:` loop (reusing `build_reports.py`'s own
  `REPORT_CATEGORIES` list, `S1_FINDINGS.md §6`, so the 5-category list has exactly
  one source of truth across Slice 5a and 5b).
- Per category, the loop needs: (1) a synthetic handoff dict built in-memory —
  `required_inputs: [{"path": f"artifacts/reports/{category}.yaml"}]` plus the
  optional `grid_evaluation.yaml` (matching every reader `SKILL.md`'s own "Required
  inputs" section, e.g. `profitability-reader/SKILL.md:20-27`) — since there is no
  `STAGE_CONFIGS["specialist_readers"]["handoff"]` file on disk to `load_yaml()` the
  way every other stage does at `async_invoke_agent:3219`; (2) a new
  `run_claude_worker`-adjacent function, e.g.
  `run_reader_worker(category: str, skill_dir: str, handoff: dict, path: Path)`,
  built from `_build_stage_prompt`'s existing logic but with `skill_file_name` taken
  directly from a `category -> skill_dir` map (`{"profitability":
  "readers/profitability-reader", ...}` — the 5 real directory names, confirmed
  this session via `Glob`:
  `workflow_artifacts/skills/readers/{profitability,trade_efficiency,forecast_power,
  regime_power,component_attribution}-reader/SKILL.md`) instead of
  `_SKILL_MAP.get(stage_name)`; (3) an explicit output path
  `RUN_DIR / "artifacts" / "proposals" / f"{category}.yaml"` per §2 above,
  sidestepping the filename-regex limitation entirely rather than widening the
  shared regex.
- The regime-power reader is the one category needing the retune-firewall guard —
  see §4.
- **Not a 5-hidden-sub-stage-identifier design (S1 §5's shape (b))**: shape (b)
  would need each hidden identifier to still resolve through `STAGE_CONFIGS`/
  `_SKILL_MAP` to get a handoff path and skill, which reintroduces the exact 1:1
  problem being solved and gains nothing over shape (a) — S1 itself only offered
  (b) as an alternative without evaluating it this deeply; this pass's recommendation
  is (a), unambiguously, once `_build_stage_prompt`'s real internals are visible.

## 4. `_validate_retune_firewall` re-point — concrete call-site relocation

Confirmed unchanged from `S1_FINDINGS.md` §3: `_validate_retune_firewall`
(`:3481-3494`) validates `regime_audit_decision.yaml.recommended_action`, independent
of which downstream skill consumes the result — zero logic change needed, this is
purely a call-site move.

**Concrete new location, per §3's loop design above:** inside the per-category loop,
immediately before invoking `run_reader_worker` for `category == "regime_power"`
specifically — i.e. the guard-and-inject pair that today runs once
(`run_loop:7555-7565`, gated on `current_stage == "verdict_interpreter"`) moves to
run once, inside the loop body, gated on `category == "regime_power"`:

```python
for category in REPORT_CATEGORIES:
    if category == "regime_power":
        _regime_aud = load_yaml(RUN_DIR / "artifacts" / "regime_audit_decision.yaml") \
            if (RUN_DIR / "artifacts" / "regime_audit_decision.yaml").exists() else None
        if _regime_aud:
            _fw_violations = _validate_retune_firewall(_regime_aud)
            if _fw_violations:
                raise RuntimeError(...)
    # build handoff, call run_reader_worker(category, ...)
```

**`_inject_regime_context_into_handoff` does NOT move the same way.** Re-read this
session (`:3497-3544`): it injects `regime_detector_confidence`/
`ungated_escape_eligible` into `protocol_to_verdict_interpreter.yaml` (the OLD
stage's handoff file, which under 5b-ii no longer exists as a real handoff since
`specialist_readers` builds its handoffs in-memory per §3, not from a
`STAGE_CONFIGS`-declared file on disk). Its call needs to be re-targeted at whatever
in-memory handoff dict the loop builds for `category == "regime_power"` specifically
— i.e. inject those two fields directly into that iteration's synthetic handoff
dict, not into a file path. **This is a real code change to the function's own
call site's argument shape** (from `(handoff_path: Path, ...)` to something that
either still takes a path (the loop could still materialize the per-category handoff
to disk before calling the worker, which would let this function's existing
file-based signature work completely unchanged) or takes a dict directly (cheaper,
but changes the function's contract). **Recommendation: materialize the synthetic
handoff to disk** (e.g.
`RUN_DIR / "handoffs" / "specialist_readers_regime_power.yaml"`) before calling
`_inject_regime_context_into_handoff` on it — this reuses `_inject_regime_context_
into_handoff`'s existing file-path signature completely unchanged (true zero-logic-
change re-point, matching the firewall's own zero-change status), at the cost of one
new handoff file on disk per run (cheap, consistent with every other stage's
existing handoff-file convention, and auditable the same way).

## 5. The mechanical verdict-synthesis function — concrete design

### 5.1 What `determine_post_verdict_route` actually needs, traced field-by-field

Full read this session, `determine_post_verdict_route` (`:6815-6986`) plus its two
real helpers `_resolve_verdict_fields` (`:6622-6686`) and `_apply_circuit_breaker`
(`:6558-6593`). The routing decision is **not one monolithic LLM judgment today** —
it already splits into two clearly separated cases:

**Case A — `pass_rule_evaluation.yaml` is BINDING** (`pre_eval.get("result") in
("PASS","FAIL")` AND `pre_eval.get("discretion") != "stage"`,
`_resolve_verdict_fields:6658`). `hypothesis_verdict`/`lineage_routing` come
**directly from `pass_rule_evaluation.yaml`'s own mechanical fields** (`:6659-6668`)
— written today by `tools/verdict_criteria_evaluator.py::evaluate_pass_rule_criteria`
(confirmed real, `:816` in that file; `discretion: "stage"` set at `:994-997` when
the matched pre-registered outcome branch explicitly declares "use stage
judgment"), **already 100% mechanical, zero LLM/reader involvement required by
5b-ii at all.** This is the common case E-018 was designed to make common
(`_resolve_verdict_fields`'s own docstring, `:6628-6638`: "for any run with a
registered, binding pass rule, the stage no longer holds the pen on the actual
promote/kill decision"). **5b-ii's synthesis function should reuse this exact
mechanism verbatim** — read `pass_rule_evaluation.yaml`, and if binding, the
route is already decided; the 5 readers' proposals are irrelevant to the
promote/kill/refine/pivot/escalate DECISION in this case, only to the qualitative
explanation layer (findings_carryover/root_cause narrative — see §5.3).

**Case B — NOT binding** (`pass_rule_evaluation.yaml` absent, or
`discretion: "stage"`). Today this falls through to `interp.get("hypothesis_verdict")`/
`interp.get("lineage_routing")` (`:6670-6681`) — i.e. verdict-interpreter's OWN LLM
judgment is the real decision authority, not copy-through. **This is the one case
5b-ii's synthesis function needs genuinely new design**, since no existing
mechanical evaluator produces a routing decision here. See §5.2.

**Two additional safety-critical checks, independent of both cases above, read
directly from `interp.get("root_cause")` (`:6843-6853`, `:6863-6872`):**
`mechanism_failure == "component_execution_error"` and
`mechanism_failure == "regime_misattribution"` each force an unconditional
`human_pause`, **before** the circuit breaker even runs (`_apply_circuit_breaker`'s
own docstring, `:6569-6572`, states callers MUST check this first — the breaker
must never touch an engineering-failure diagnosis). **Neither check is implemented
as deterministic code anywhere today** — grepped `component_error_count` across
`run_phase1_research.py`: zero hits; the ONLY thing that currently notices
`component_error_count`/`detector_confidence` is the LLM, per
`verdict-interpreter/SKILL.md`'s own enum table (`:296-305`, full read this
session): `component_execution_error` fires when `active_n_bars=0` combined with a
nonzero `component_error_count`/`component_error_sample` in `protocol_result.yaml`;
`regime_misattribution` fires when a `regime_uninformative` rule match combines
with low/medium `detector_confidence` from `regime_detector_report.yaml`. **Both
triggers are simple, non-narrative field comparisons against files already on
disk** (`protocol_result.yaml`, `regime_detector_report.yaml`) — genuinely new
deterministic logic to write (no existing mechanical precedent to reuse, unlike
Case A), but low-risk to write correctly since the trigger conditions are already
fully specified in `verdict-interpreter/SKILL.md`'s own table, and they do NOT
require the 5 readers' proposals at all — the synthesis function should check these
two conditions **directly against `protocol_result.yaml`/`regime_detector_report.yaml`,
independent of and prior to consulting any reader's proposals**, mirroring exactly
how today's code structure checks `root_cause` before circuit-breaker/routing logic
runs.

### 5.2 The proposed rule for Case B (discretion: stage) — grounded in the real `scores` fields

**Proposed rule:** when `pass_rule_evaluation.yaml` is absent or
`discretion == "stage"`, and neither safety-critical mechanism_failure check (§5.1)
fired, compute for each of the 5 proposal files a **per-file best-proposal score**
`S = confidence_real + distance_to_profitable + mechanism_plausibility` (max 9,
min 0) over that category's proposals (an empty `[]` file contributes no score at
all, not a zero — see §6). Let `S_max` be the highest single-proposal score across
all 5 files, and `R` the reader category that produced it.

- **If no reader produced any proposal at all** (all 5 `proposals/*.yaml` are `[]`):
  route to **`kill`/`terminate`** — every reader, reading only its own report,
  found nothing evidence-worthy in this run's own data on which to base even a
  speculative config change. This mirrors `_LEGACY_STATUS_TO_VERDICT_ROUTING`'s own
  `"kill": ("kill", "terminate")` pair (`:6604-6609`) and needs no new pair invented.
- **If `S_max >= 6`** (i.e. at least one proposal scores 2+ on ALL THREE
  dimensions, or a lopsided-but-strong combination like 3+3+0): route to
  **`refine`**, with `proposed_change_dimension` taken directly from that winning
  proposal's `patch`/`block` field path (§5.3) and `hypothesis_family` copied
  forward from `hypothesis_card.yaml` unchanged (verdict-interpreter never
  re-derives this field independently either — it is upstream metadata, not a
  reader's own output).
- **If `0 < S_max < 6`**: route to **`refine`** as well, but flag
  `confidence: low` in the synthesized `root_cause` block (§5.3) — a weak-but-
  nonzero proposal is still the best evidence-grounded next step available; this
  project's own "parameter plateau" and "never soften a kill" instincts argue
  against manufacturing false confidence, not against attempting a cheap refine
  when SOME evidence exists.
- **Why this rule over alternatives:**
  - *N-of-5-readers-must-agree* was considered and rejected: the 5 readers are
    deliberately scoped to non-overlapping, mutually exclusive report categories
    (each reader's own "Scope boundary"/"Forbidden" sections, e.g.
    `profitability-reader/SKILL.md:157-162`, explicitly forbid reading another
    category's report) — a real profitability problem and a real regime-detector
    problem are not expected to show up as corroborating evidence in two different
    readers' proposals; requiring agreement would systematically favor
    "everything's fine" (no single dominant failure mode) over "one clear,
    well-evidenced failure mode," which is backwards for a diagnostic system whose
    whole purpose is root-causing ONE dominant failure.
  - *Highest-confidence-alone (`confidence_real` only)* was considered and
    rejected: `confidence_real` measures whether the EVIDENCE is real (not noise),
    not whether the proposed FIX is any good — a high-confidence proposal with
    `distance_to_profitable=0` (this proposal would not close the gap even fully
    realized, per every reader's own 0-anchor text, e.g.
    `profitability-reader/SKILL.md:141`) is confidently-observed but not actionable.
    Summing all three dimensions is the only combination that rewards a proposal
    that is simultaneously real, closes a meaningful gap, and has a plausible
    mechanism — exactly the three questions `S1_FINDINGS.md §7`'s own schema
    grounding intended these three scores to jointly answer.
  - The `S_max >= 6` threshold is a genuine, undesigned-before-now number — chosen
    because it requires an AVERAGE of 2/3 ("evidence spans 2+ windows... plausibly
    supports a specific patch," per every reader's own anchor-2 row, e.g.
    `profitability-reader/SKILL.md:143`) across all three dimensions, which is this
    project's own stated bar for "not a lone spike" (the parameter-plateau
    principle, `CLAUDE.fork.md`'s own bars list: "neighbours (±25-50%) remain
    profitable. A lone spike = curve fit, kill it" — anchor-3's own text for
    `mechanism_plausibility` cites exactly this ±25-50% precedent,
    `profitability-reader/SKILL.md:144`). **This threshold is a first proposal, not
    a validated one** — it has never been run against a real proposal corpus (no
    `ANTHROPIC_API_KEY` in this environment, §8 below); S2 should treat `6` as a
    starting constant to tune once real reader output exists, not a fixed rule.

### 5.3 Reconstructing `root_cause`, `findings_carryover.yaml`-equivalent content

`root_cause.mechanism_failure`'s FULL 11-value enum (`verdict-interpreter/SKILL.md`
:294-305, full table read this session) requires real narrative judgment for most
values — e.g. distinguishing `already_priced_in` vs `no_informational_content_this_
venue` vs `edge_arbitraged_away` needs `hypothesis_card.yaml`'s own
`edge_source.category` field, which **none of the 5 readers receive** (every
reader's own "Scope boundary" explicitly excludes `hypothesis_card.yaml`/`research_
brief.yaml` — e.g. `profitability-reader/SKILL.md:29-35`). **This is a real,
unresolved gap between what the 5 readers can produce and what the legacy
`root_cause` schema expects — flagged in "Not determined" below, not solved here.**
Two narrower things ARE resolvable now, though:

- The two safety-critical values (`component_execution_error`,
  `regime_misattribution`) are handled entirely OUTSIDE the reader-proposal path,
  per §5.1 — they never need this narrative disambiguation.
- For the `refine` case (§5.2), `_auto_generate_findings_carryover` (`:5532-5614`,
  full read this session) needs `altitude_justification` (free text it REGEX-PARSES
  for `corr=`/`cost_drag=`/`gross_pnl=` numbers, `:5563-5574`), `criteria_summary`
  (list of `{criterion, result}` dicts), `proposed_change_dimension`, and
  `hypothesis_family`. **A mechanical synthesis function can populate these MORE
  reliably than today's regex-scraping of LLM prose**: `corr`/`cost_drag`/
  `gross_pnl` are already real numbers in the winning proposal's own cited
  `evidence` category report (`profitability.yaml`/`forecast_power.yaml`'s
  `slices.overall.diagnostics`, S1 §6), `criteria_summary` can be built directly
  from `pass_rule_evaluation.yaml`'s own per-criterion PASS/FAIL list (already
  structured, not needing extraction from anything), `proposed_change_dimension`
  is literally the winning proposal's `patch`'s target field path (e.g.
  `threshold_filter.min_abs`, matching `profitability-reader/SKILL.md`'s own
  Rule-1 patch example, `:113`), and `hypothesis_family` is a straight copy from
  `hypothesis_card.yaml`. **`_auto_generate_findings_carryover` itself needs ZERO
  code changes** — it already only requires an `interp`-shaped dict with these
  field names, regardless of producer (confirmed by reading its full body: no
  file-format assumption beyond dict-key access).

## 6. Task 6 — component_attribution zero-proposals, and graceful degradation

**Confirmed directly from the skill file** (`component_attribution-reader/SKILL.md`,
full read this session): "Required outputs" (`:63-68`) states explicitly: *"An empty
list (`[]`) is a valid, honest output — this report is raw per-bar data with no
pre-aggregation, so a run with many components but no distinguishable pattern
should produce few or zero proposals rather than a forced one per component."*
`profitability-reader/SKILL.md` (`:57-61`) carries the identical guarantee for its
own category. **All 5 readers share this contract** (`proposal.schema.json`'s own
`$comment`/`description` at `:3-5` frames the whole list as "0 or more"). So: yes,
genuinely confirmed, not just plausible — any subset of the 5 `proposals/*.yaml`
files, including all 5, can legitimately be `[]`.

**Graceful degradation for the synthesis function (§5.2):** the proposed rule
already handles this correctly by construction — `S_max` is computed only over
proposals that exist; an empty or entirely-absent proposal file simply contributes
nothing to the `max()` across categories, never a synthetic zero-scored entry that
would need special-casing. The "all 5 empty → kill" branch in §5.2 is exactly the
all-absent degenerate case, handled by the same `max()`-over-nothing logic (empty
input to `max()` needs an explicit guard — `max([], default=0)` — that guard IS the
"kill" branch's trigger condition, not a separate code path).

## 7. Task 2 — 16-caller re-enumeration against the concrete synthesis design

Re-checked against §5's concrete design (not just abstractly, as S1's own Tier A/B
split did). **S1's Tier A/B classification holds up; no reclassification found.**
Refined per-function verdict:

| Function | S1 tier | Needs under 5b-ii's concrete design |
|---|---|---|
| `_verify_verdict_outputs` (`:5617`) | A | Re-point path: reads whatever the synthesis function's own output path is. **No change if the synthesis function writes to the SAME path** (`artifacts/verdict_interpretation.yaml`) it always has — see recommendation below. |
| `_write_promotion_audit` (`:5829`) | A | Same — fallback-only read (`:5872`), unaffected either way. |
| `_route_holdout_evaluation` (`:6374`) | A | Same fallback pattern (`:6396`). |
| `determine_post_verdict_route` (`:6815`) | A | **Central.** Its own internal logic (§5.1) is exactly what 5b-ii's synthesis function reimplements/reuses — see recommendation below: this function's OWN body barely changes if the artifact it reads is written by new code but has the old shape. |
| `determine_post_campaign_review_route` (`:6986`) | A | Same read pattern, two load sites (`:7035`, `:7125`). |
| `run_loop` (`:7410`, loads at `:7540`/`:7886`) | A | The `elif current_stage == "verdict_interpreter":` branch (`:7885-7901`) becomes `elif current_stage == "specialist_readers":`, calling the synthesis function then `determine_post_verdict_route` exactly as today (`:7888`) — **structurally the smallest possible change to this call site**, per the recommendation below. |
| `_extract_run_numbers` (`run_campaign.py:1459`) | A | Cosmetic only, unaffected either way (S1's own assessment stands). |
| `tools/near_miss_scoreboard.py` (`:408`) | — | Unaffected if synthesis writes to the same path/shape; needs re-pointing only under the alternative (new-schema) design. |
| `_route_pivot`, `_auto_generate_findings_carryover`, `_write_kb_findings_entry`, `_resolve_verdict_fields`, `_check_pass_rule_evaluation_conformance`, `_check_kb_reactivation_conformance` (Tier B, dict-in) | B | **Confirmed: genuinely zero code change**, for either design option, as long as the dict handed to them carries the same field names they already read (traced field-by-field for `_auto_generate_findings_carryover` in §5.3; the other five were traced by S1 and not independently re-derived here beyond confirming their signatures are unchanged this session). |
| `_inject_regime_context_into_handoff`, `_create_remaining_handoffs` (handoff-side) | — | Re-pointed per §4 (regime-power reader's dispatch branch); `_create_remaining_handoffs`'s `:3417` listing (bookkeeping only, per S1) needs its `verdict_interpreter` deliverables list updated to `specialist_readers`'s 5 proposal files — a one-line-per-entry edit, not a logic change. |

**The decisive design fork, not previously posed this concretely:** should the
synthesis function (a) write its output to `artifacts/verdict_interpretation.yaml`,
in the SAME shape (`status`/`hypothesis_verdict`/`lineage_routing`/`root_cause`/
`altitude_justification`/`criteria_summary`/`hypothesis_id`/`hypothesis_family`/
`proposed_change_dimension`) the 16 callers already expect — making **14 of the 16
real callers need ZERO code changes**, only their PRODUCER changes (mechanical
function instead of an LLM invocation writing the same file) — or (b) write to a
new path/shape and re-point every caller individually? **Recommendation: (a).**
This was not explicit in `S1_FINDINGS.md` (which posed "who synthesizes" as the
open question but didn't examine whether the synthesized output could reuse the
EXACT legacy artifact shape). Reusing the legacy shape turns "re-point 16 callers"
into "re-point ~2 callers whose CALL SITE changes" (`run_loop`'s
`verdict_interpreter`-branch invocation, and possibly `_verify_verdict_outputs` if
its own conformance rules reference `verdict_interpreter`-stage-specific deliverable
names that no longer apply) **plus writing the synthesis function itself** — a much
smaller, much lower-risk surface than the delivery plan's framing implies. The
schema-purity argument for a NEW artifact shape (cleaner separation from a
retired LLM stage's naming) is real but should be an explicit operator trade-off
(migration cost vs. naming cleanliness), not assumed.

## 8. S2 build-list and split recommendation

Building on `S1_FINDINGS.md` §8's original items 2-5, refined with this pass's
concrete designs:

1. **Synthesis function** (`_synthesize_verdict_interpretation` or similar), split
   internally into: (1a) the two safety-critical mechanism_failure checks (§5.1,
   reads `protocol_result.yaml`/`regime_detector_report.yaml` directly, no reader
   dependency); (1b) Case A pass-through (§5.1, reuses
   `pass_rule_evaluation.yaml`'s existing binding fields verbatim — near-zero new
   logic); (1c) Case B scoring rule (§5.2, the one genuinely new numeric rule,
   `S_max >= 6` threshold flagged as untuned); (1d) `findings_carryover.yaml`-
   equivalent field reconstruction (§5.3). Writes to the LEGACY artifact path/shape
   per §7's recommendation (a).
2. **Orchestrator loop** — `run_reader_worker` (§3), the `specialist_readers`
   per-category loop inside `run_loop`, the explicit `artifacts/proposals/<category>.
   yaml` output path (§2, sidestepping the filename-regex limitation), synthetic
   in-memory-then-materialized-to-disk handoffs (§4).
3. **`STAGE_CONFIGS`/routing change** — per §1's correction, NOT a literal dict
   deletion; change `STAGE_CONFIGS["protocol_execution"]["default_next"]` (`:184`)
   to `"specialist_readers"` under the flag, following the `validation`/
   `strategy_config_authoring` unreached-not-deleted pattern exactly.
4. **Call-site changes** — per §7's table: `run_loop`'s `verdict_interpreter`
   branch (`:7539-7589` skip-check/injection, `:7885-7901` routing) becomes a
   `specialist_readers` branch calling the loop (item 2) then the synthesis
   function (item 1) then `determine_post_verdict_route` unchanged; verify
   `_verify_verdict_outputs`/`_create_remaining_handoffs` need no deeper change
   than their `deliverables`-list bookkeeping.
5. **Tests**: synthesis-function unit tests on synthetic proposal fixtures (all-5
   empty → kill; single high-scoring proposal → refine with correct
   `proposed_change_dimension`; `pass_rule_evaluation.yaml` binding → verbatim
   pass-through, several `discretion` values); orchestrator-loop test proving 5
   categories dispatch to 5 distinct skill directories with 5 distinct output
   paths (mockable without an LLM — see §9); flag-off byte-identity for the
   existing `verdict_interpreter` path untouched; firewall re-point test (regime
   category only, other 4 never see `regime_audit_decision.yaml`).

**Recommendation: 5b-ii should split into two S2 dispatches, not stay one — larger
than the plan's own text implies once this depth of design exists.**

- **5b-ii-A — Synthesis function alone** (item 1 + its own unit tests): pure,
  deterministic, fully testable with synthetic YAML fixtures, ZERO dependency on
  the orchestrator loop existing yet, zero LLM/API budget needed at all. Can ship
  and be validated completely independently — closer in risk profile to 5b-i than
  to 5b-ii-B.
- **5b-ii-B — Orchestrator loop + `STAGE_CONFIGS` routing change + 16-caller
  re-point** (items 2-4 + their tests): genuinely new orchestration code at an
  identified seam (§3), the filename-regex blocker (§2) needing a real fix, and the
  actual behavior-change call-site edit in `run_loop`. This is the piece that
  cannot be fully proven without either a mocked-LLM test harness (§9) or real API
  budget, and is where a regression would be most consequential (it touches the
  shared `run_loop` dispatch every other stage also goes through).

This is a **finer split than `S1_FINDINGS.md` §8's own two-way 5b-i/5b-ii
recommendation** — that split was made before 5b-i existed and before this session's
concrete tracing of `run_claude_worker`'s filename-regex limitation and
`determine_post_verdict_route`'s two-case (binding/discretion) structure. Both new
halves (A and B) depend on 5b-i's real schema (already satisfied) but 5b-ii-A does
NOT depend on 5b-ii-B — synthesis-function unit tests can be written and pass against
hand-authored fixture `proposals/*.yaml` files without the orchestrator loop existing
at all. Recommend dispatching 5b-ii-A first.

## 9. Task 8 — test feasibility, confirmed precisely

`ANTHROPIC_API_KEY` confirmed **not set** in this environment (checked directly,
value not echoed) — same as `S1_FINDINGS.md` §9's finding, unchanged.

- **Synthesis function (item 1)**: entirely unit-testable with synthetic YAML
  fixtures — zero LLM dependency of any kind. It reads `pass_rule_evaluation.yaml`,
  `protocol_result.yaml`, `regime_detector_report.yaml`, and `proposals/*.yaml`, all
  plain files a test can author directly. **Fully testable in this environment,
  today.**
- **Orchestrator loop (item 2)**: the loop-control logic (iterate 5 categories,
  build 5 handoffs, call 5 workers, write 5 output paths) is deterministic and
  testable by mocking `run_reader_worker` itself (asserting it was called 5 times
  with the right `skill_dir`/`category`/output-path arguments) — this doesn't need
  a real LLM either, following `test_e056_config_direct_authoring.py`'s own
  precedent for mocking `run_claude_worker`-adjacent calls (cited by
  `S1_FINDINGS.md` §9 as the pattern to follow; **its exact mechanics were not read
  this session either** — still genuinely deferred, see Not determined).
- **What genuinely cannot be tested without a real LLM call**: whether the 5 reader
  `SKILL.md` prompts, when actually sent to a real model, produce YAML the parser
  can handle, obey the `evidence`/scoring rules, and stay within their scope
  boundaries. This is identical in kind to 5b-i's own untested surface (the skill
  files themselves) — 5b-ii adds no NEW real-LLM-required surface beyond what 5b-i
  already carries; it is the deterministic glue code (synthesis + loop) that is
  100% unit-testable, and the prompt-quality question that isn't, exactly as `state:
  off_incomplete` already models in `feature_flag_register.yaml` (S1 §9's finding,
  not re-verified line-by-line this session but not contradicted by anything found
  here).

## Not determined

- **The full `root_cause.mechanism_failure` narrative taxonomy (9 of 11 enum
  values, excluding the 2 safety-critical ones handled in §5.1)** — genuinely
  undesigned. `already_priced_in`/`no_informational_content_this_venue`/
  `edge_arbitraged_away`/`entry_exit_execution_gap`/`indicator_incompatible_with_
  asset_flow`/`lag_mismatch_to_regime_persistence`/`insufficient_sample_
  inconclusive` all require distinguishing context (`edge_source.category` from
  `hypothesis_card.yaml`, trade-level MAE/MFE from `trade_diagnostics.json`) that
  the 5 readers, by design, do not receive. Whether `findings_carryover.yaml`'s
  consumers actually need this level of taxonomy fidelity from a mechanical
  synthesis function, or whether a coarser mechanical mapping (e.g. always
  `insufficient_sample_inconclusive` unless a safety-critical check fired) is
  acceptable, is a real operator-level trade-off, not resolved here.
- **The `S_max >= 6` threshold (§5.2)** — a first, reasoned proposal, explicitly
  not validated against any real proposal corpus (none exists yet — no API budget).
  Needs tuning once 5b-i's readers have produced real output on real runs.
- **Whether the synthesis function should write to the legacy
  `verdict_interpretation.yaml` path/shape (§7 recommendation) or a new path** —
  this pass has a strong recommendation (reuse the legacy shape, minimize caller
  re-pointing) but it is a real design choice with a real alternative (schema
  cleanliness), and should be confirmed with the operator before S2 build, not
  assumed from this document alone.
- **Whether literal `STAGE_CONFIGS` key deletion (delivery plan's stated wording)
  or the unreached-not-deleted pattern (§1's recommendation, matching every other
  precedent in this file) is what the operator actually wants** — a real
  disagreement between the delivery plan's exact text and this session's tracing
  of the only precedents that exist; flagged, not resolved unilaterally.
- **`test_e056_config_direct_authoring.py`'s exact mocking mechanics** — still not
  read directly this session either (S1 §9 also deferred this); S2 should read it
  before designing the orchestrator-loop test.
- **Whether `tools/lint_verdict_provenance.py`, `tools/record_schema.py`, and
  `tools/verdict_criteria_evaluator.py`'s comment-only references are genuinely
  comment-only** — carried forward from `S1_FINDINGS.md`, still not independently
  re-verified this session (out of this dispatch's scope; `verdict_criteria_
  evaluator.py` WAS read this session for its `discretion`/pass-rule mechanics,
  §5.1, but not re-grepped specifically for `verdict_interpretation.yaml`
  references beyond that).
- **Exact new function signatures** for `run_reader_worker` (§3) and the synthesis
  function (§5) — shapes proposed, parameter names and return types not finalized;
  real S2 design work, not characterization.

---

## Paste-ready Linear comment

**E-046a Slice 5b-ii (verdict-synthesis + orchestrator loop + 16-caller re-point) —
deep S1 characterization complete (2026-09-22).** Read-only, worktree base
`ccde0329` (matches `origin/master`, not stale). Full findings:
`strategy-research/engineering/roadmap/E-046a/S1_FINDINGS_5B_II.md`.

Headline findings:
- **Correction to `S1_FINDINGS.md` §8**: its `STAGE_CONFIGS` removal citation
  (`:186-189`) actually points at `verdict_interpreter`'s own entry, not
  `validation`'s. More importantly, **no existing code precedent literally deletes
  a `STAGE_CONFIGS` key** — the real `validation`/`strategy_config_authoring`
  pattern is "registered unconditionally, made unreached via routing"
  (`run_loop:7639-7646`). Recommend the same pattern for `verdict_interpreter`
  (redirect `STAGE_CONFIGS["protocol_execution"]["default_next"]`, `:184`) rather
  than the delivery plan's literal "removed from STAGE_CONFIGS" wording — flagged
  for operator confirmation, not resolved unilaterally.
- **New, previously-uncharacterized blocker**: `run_claude_worker`'s deliverable-
  write regex (`:949`) excludes `/` from filenames and never `mkdir`s a parent dir
  (`:961`) — `artifacts/proposals/<category>.yaml` cannot be written through the
  existing path as-is. Recommend the new per-category worker function own its
  output path explicitly rather than widening the shared regex.
- **Synthesis-function design (§5), grounded in real code**:
  `determine_post_verdict_route` already splits into a BINDING case (`pass_rule_
  evaluation.yaml` mechanical, zero reader involvement needed — reuse verbatim) and
  a `discretion: stage` case (genuinely undesigned before now). Proposed rule for
  the latter: sum each proposal's 3 scores (`confidence_real +
  distance_to_profitable + mechanism_plausibility`, max 9), take the max across all
  5 categories; `0` proposals anywhere → kill; `S_max >= 6` → refine (chosen because
  it requires a 2/3 average across all three dimensions, matching this project's own
  parameter-plateau bar cited verbatim in each reader's own scoring table). Two
  safety-critical `root_cause.mechanism_failure` values (`component_execution_error`,
  `regime_misattribution`) are handled OUTSIDE the reader-proposal path entirely —
  simple field checks against `protocol_result.yaml`/`regime_detector_report.yaml`,
  genuinely new deterministic logic (no existing mechanical precedent) but low-risk.
- **Biggest scope-reducing finding**: if the synthesis function writes to the SAME
  legacy path/shape (`artifacts/verdict_interpretation.yaml`) the 16 callers already
  expect, **14 of 16 need zero code changes** — only the producer changes. This
  turns "re-point 16 callers" into "write one new producer function + touch ~2 call
  sites," a much smaller surface than the delivery plan's framing implies. Flagged
  as a real design choice needing operator confirmation, not assumed.
- **Recommendation: split 5b-ii further, into 5b-ii-A (synthesis function alone,
  fully unit-testable today, zero orchestrator dependency) and 5b-ii-B
  (orchestrator loop + STAGE_CONFIGS routing change + call-site edits, needs the
  filename-regex fix and touches shared `run_loop` code)** — finer than
  `S1_FINDINGS.md`'s original 5b-i/5b-ii two-way split, made before this session's
  concrete tracing existed. 5b-ii-A has no dependency on 5b-ii-B and should be
  dispatched first.

Not determined (full list in file): the 9 narrative `mechanism_failure` enum values'
mechanical reconstruction (needs `hypothesis_card.yaml` context none of the 5
readers receive); the `S_max >= 6` threshold, unvalidated against any real proposal
corpus; legacy-shape-reuse vs. new-schema for the synthesized artifact (operator
call); literal STAGE_CONFIGS deletion vs. unreached-pattern (operator call);
`test_e056_config_direct_authoring.py`'s exact mock mechanics (still unread); the 3
tools' comment-only status (still unverified); exact new function signatures for
`run_reader_worker`/the synthesis function.

---

## Decision (operator, 2026-09-23)

The three items flagged above as operator calls are resolved:

1. **Synthesized artifact shape — NEW clean file/schema, not the legacy
   `verdict_interpretation.yaml` path/shape.** Overrides this document's §7
   recommendation (a). The operator judged the extra re-pointing effort worth a
   clean target. Consequence: the 16 existing readers of the legacy file must be
   re-pointed individually; that re-pointing belongs to 5b-ii-B. 5b-ii-A designs
   the new filename/schema.
2. **`STAGE_CONFIGS["verdict_interpreter"]` — bypass, not delete.** Accepts §1's
   recommendation: keep the entry registered, make it unreached by redirecting
   `STAGE_CONFIGS["protocol_execution"]["default_next"]` under the flag (the
   `validation`/`strategy_config_authoring` precedent). Applies to 5b-ii-B.
3. **Refine/kill threshold — static `S_max >= 6` as the first setup.** Accepts §5.2
   as a starting constant, explicitly untuned. Clarified for the record: this is a
   per-hypothesis refine-vs-kill decision for the non-binding (`discretion: stage`)
   case, not a ranking of an ideas backlog; the refine/kill routing outcomes remain
   live.

Build order: 5b-ii-A (synthesis function + tests) first; 5b-ii-B after.

## Decision (operator, 2026-09-23, second round -- for 5b-ii-B)

Raised by the 5b-ii-A build (PR #196, CUL-313):

4. **`hypothesis_family` source -- set once at idea creation, inherited on refine.**
   The hypothesis-generation stage writes a `family` field into
   `hypothesis_card.yaml`; every refine child inherits it unchanged. Not derived
   mechanically from components (rejected as brittle for multi-component ideas).
   Rationale: the circuit breaker counts refines/failures per family by exact
   string, so a label re-invented each run (the legacy behaviour) silently
   defeats it.
5. **Legacy fields with no new-schema home -- rebuild the useful ones
   mechanically, drop the rest.** `primary_failure_mode` and
   `reactivation_trigger` are rebuilt deterministically from reader output
   (e.g. failure mode = winning proposal's category + its lead evidence line);
   `config_to_failure_map`, `power_disposition`, `trade_attribution`,
   `prescreen_*` are dropped (`trade_attribution` has no reader at all). No LLM
   step is reintroduced for narrative fields.

---

## REALIGNMENT (operator, 2026-09-23) -- supersedes §5, §7-§8 and both Decision sections above

The design in this document re-created the verdict routing the target
retires. Per the target (roadmap v26/v27 cards G/I; delivery_plan_v26.md
slices 2, 6b, 6c):

- An idea's status is the **grid** (`idea_status.yaml`: validated / refuted /
  inconclusive, slice 2, already built). Readers never decide it.
- Reader proposal scores only **rank the next candidate** in the decide-next
  step (slice 6b), by confidence_real desc, distance_to_profitable desc, cost
  asc. There is no refine/kill threshold (`S_max`).
- refine / pivot / escalate / kill, the per-family circuit breaker and
  continuation children are **retired** in slice 6c. Repeats are caught by the
  exact-match check (slice 8). An idea's identity is its `hypothesis_id`; a
  same idea on another coin is a variant of that idea, not a new family.

What was undone (branch `fix/e046a-realign-retire-verdict-synthesis`):
- 5b-ii-B1 (PR #198, family-at-creation) reverted in full.
- 5b-ii-A's `_synthesize_verdict`, `verdict_synthesis.schema.json` and their
  tests removed; `run_phase1_research.py` is back to its pre-5b-ii-A content.
- Kept: the proposal loader/validator, moved to `tools/reader_proposals.py`
  for slice 6b, and the stricter patch-item contract in `proposal.schema.json`
  plus the reader SKILL.md wording.

**Redefined 5b-ii-B (next):** the `specialist_readers` stage loop (§2-§3 of
this document still hold: explicit per-category output path, no shared-regex
change) and the removal of `verdict_interpreter` behind a flag, with the
interim route taken from the grid as delivery_plan_v26.md slice 2 already
specifies (validated -> promote, refuted -> kill/terminate, inconclusive ->
human_pause), plus a component-error pause (an engineering failure makes the
grid meaningless). Every `verdict_interpretation.yaml` reader is then
re-pointed or marked for retirement in 6c; reader scores play no part in the
route.
