# E-034 S1 — Characterize the selection gap, and STOP

**Story:** S1 (characterize and STOP — no production code).
**Scope:** where does N variants become 1, what must a selection record
contain, who should write it, and does it actually close E-032's and E-031's
downstream needs. No code changes in this story.

All counts below are MEASURED by
`strategy-research/engineering/roadmap/E-034/artifacts/s1_measure_variants.py`
(read-only, re-run any time from `strategy-research/` with
`../venv/Scripts/python engineering/roadmap/E-034/artifacts/s1_measure_variants.py`).
Denominators are stated with every count. `local_data/holdout_sealed/` was
never read, listed, or globbed.

## Conclusion first

The narrowing happens **inside the `backtest_specification` LLM stage's own
reasoning, with no routing decision anywhere in the code.** Both routing
functions near this boundary — `determine_post_validation_route` and
`determine_post_spec_route` — read a single `status` string (approve/refine/
reject; spec_ready/component_gap) and never touch variant identity at all.
The stage reads a menu (`expanded_hypothesis_card.yaml.expanded_variants`,
schema-required, up to 8 items, 138 across 43 runs) and its own contract
(`backtest-engineering/SKILL.md`: *"Do not emit more than one config"*)
forces it down to one `backtest_spec.yaml`. Neither `backtest_spec.yaml` nor
`decision.yaml` has a schema field for which variant was picked. In practice
the chosen variant's identifier sometimes leaks into `decision.yaml`'s free
prose `rationale` field (confirmed on run_019, see Task 1) — but this is
incidental, inconsistent across the corpus, and in several runs names
*multiple* variant IDs with no way to tell which one was actually chosen. **No
code seam currently exists.** The cheapest fix is not a new routing branch —
it's a required field on the artifact the stage already emits, joined against
the menu by new deterministic code that runs right after the stage completes.

## Task 1 — locate the narrowing, precisely

### Where I looked and what each source is

| Claim | Source | Confirms |
|---|---|---|
| Which stages exist / stage order | `STAGE_CONFIGS`, `workflow/run_phase1_research.py:87-137` | `backtest_specification`'s handoff is `validation_to_backtest_specification.yaml`; `default_next` after it is `"dynamic_routing"` (i.e. `determine_post_spec_route`) |
| What `backtest_specification` receives | `workflow_artifacts/templates/handoffs/validation_to_backtest_specification.yaml` | `primary_input_artifact: expanded_hypothesis_card.yaml`; `required_inputs` also includes it, described as "the validated hypothesis **and variants** to implement" |
| How the stage is briefed to reason | `workflow_artifacts/skills/backtest-engineering/SKILL.md` | "Mission: ... one valid strategy config"; Forbidden list: **"Do not emit more than one config."** No instruction anywhere to record which of the menu's entries was used, or why the others weren't. |
| Routing after validation | `determine_post_validation_route`, `run_phase1_research.py:1730-1798` (read in full) | Reads only `decision.get("status") or decision.get("family_status")` from `validation_decision.yaml`. Branches are `approve/conditional_approve → backtest_specification`, `refine → refinement_planner`, `reject → completed_rejected`. **No variant is read, named, or chosen here** — `approve` can and does approve a whole family of variants at once (see run_019 below: `variants_to_test` lists 4 IDs). |
| Routing after spec | `determine_post_spec_route`, `run_phase1_research.py:5380-5397` (read in full) | Reads only `decision.get("status")` from `decision.yaml` (`spec_ready`/`component_gap`/unknown → `human_pause`). **No variant field is read here either.** |
| The other routing decision near this boundary | `_route_post_innovation_expansion`, `run_phase1_research.py:1472-1584` (read in full) | This is the anti-adjacency gate call E-032 built. It reads `run_dir/artifacts/hypothesis_card.yaml` — the **parent**, pre-expansion card — as `candidate_path`. It runs *before* `validation`, i.e. before variants even exist in expanded form for this pass. It cannot be the variant-selection point; it structurally predates variant existence, and this is exactly E-032's logged defect (see below). |
| Schemas for the two candidate artifacts | `workflow_artifacts/schemas/backtest_spec.schema.json`, `.../decision.schema.json` (read in full) | Neither has a field for a chosen variant. `backtest_spec.schema.json` requires `hypothesis_id, status, config, config_rationale`; `config_rationale` is prose (`hypothesis_claim`/`config_choice` strings), not a variant pointer. `decision.schema.json` requires `hypothesis_id, stage, status, rationale`; `rationale` is a free string. |
| Schema for the menu itself | `workflow_artifacts/schemas/expanded_hypothesis_card.schema.json` (read in full) | Declares `expanded_variants` as `items: {type: string}` — bare strings only. **The real corpus violates this schema for the majority of runs** (see Task 2) — the schema is stale/aspirational, not what the pipeline actually produces. |
| Validation stage's own briefing | `workflow_artifacts/skills/quant-validation/SKILL.md` (grepped for "variant": zero hits); `workflow_artifacts/schemas/validation_decision.schema.json` (read in full, `additionalProperties: false`, only `hypothesis_id/status/rationale/blocking_issues`) | Confirms validation doesn't narrow either, by skill instruction or by schema. Real `validation_decision.yaml` files (e.g. run_019) add an undeclared `variants_to_test` list — again, real artifacts deviate from the schema, this time in the direction of naming *multiple* surviving variants, not one. |

### Concrete answer

At what point does N become 1: **inside `backtest_specification`'s LLM
reasoning**, between reading `expanded_hypothesis_card.yaml` (N variants) and
writing `backtest_spec.yaml` (1 config). This is LLM judgement, not
deterministic code — there is no `if`/routing branch in
`run_phase1_research.py` that selects a variant; the only instruction is the
SKILL.md's "do not emit more than one config."

Is the chosen variant identifiable from artifacts alone: **not mechanically,
and not reliably even by prose grep.** Measured pattern across the 18
multi-variant runs that also produced a `backtest_spec.yaml`
(`run_005, 017, 018, 019, 020, 021, 022, 023, 024, 025, 027, 028, 029, 030,
031, 034, 035, 039, 053` — denominator: runs with `expanded_variants` count
>1 and an existing `artifacts/backtest_spec.yaml`):

- `backtest_spec.yaml` itself: grepping the literal word "variant" returns
  0-2 hits per run, always inside free-text `config_rationale` strings, never
  a structured pointer.
- `decision.yaml`'s `rationale` field: sometimes names one variant ID
  cleanly (run_018: `V2-PIVOT-A-CONSERVATIVE`; run_020:
  `V2-PIVOT-A-THRESHOLD-REFINED`), sometimes names several with no
  disambiguation of which was actually used (run_031: `V1, V1_Conservative,
  V2, V6`; run_039: `V1, V1_RSI_CONSERVATIVE, V2, V2_STOCHASTIC_CROSSOVER,
  V3`), and sometimes names none (run_023, run_024, run_025, run_034,
  run_035, run_053: 0 "variant"-adjacent tokens in `decision.yaml`).
- Spot check on run_019 (the case named in the dispatch): `expanded_variants`
  has 3 real threshold variants (`V2-THRESHOLD-17p5/20p0/22p5`, plus a 4th,
  `V2-THRESHOLD-20p0-BTC-ONLY`, inside `validation_decision.yaml`'s
  undeclared `variants_to_test` list — 4 total survived validation, not 3).
  `backtest_spec.yaml` contains **no** `V2-THRESHOLD-*` token anywhere and no
  `variant_id`/`variant` key. `decision.yaml`'s `rationale` string does say
  *"V2-THRESHOLD-20p0 config is valid, complete, and ready..."* — this
  happens to disambiguate correctly in this one run, but it is unstructured
  prose in an optional-content field, not a contract, and 6 of the other 18
  multi-variant runs have zero such mentions. **A mechanical reader (a
  script, a gate) cannot depend on this.**

## Task 2 — what a selection record must contain

### Corpus shape, measured

- 46 `expanded_hypothesis_card.yaml` files under `runs/*/artifacts/`
  (denominator: 59 run dirs), plus 2 more under superseded
  `attempt_*_blocked/` dirs (run_043, run_044 — not double-counted).
- Of the 46: 1 fails to parse (`run_006`, YAML syntax error at line 64 —
  pre-existing corpus damage, unrelated to this story), 2 have no
  `expanded_variants` key at all (`run_011`, `run_016`). **43 runs
  successfully yield the EPIC's stated 138 variants, max 8 in one run
  (run_007)** — this reproduces the EPIC's numbers exactly.
- `variants_not_pursued` appears in exactly **1** file across all of `runs/`
  (denominator: every `.yaml/.yml/.json/.md` under `runs/`) —
  `run_0001/artifacts/innovation_notes.yaml`. This reproduces the EPIC's "1
  file out of 59" claim exactly (the file is `innovation_notes.yaml`, an
  optional narrative artifact from `innovation_expansion`, not a structured,
  schema-governed record).

### Variant item shape — inconsistent, confirmed against the real corpus, not the schema

Across the 138 variants: **74 are dicts, 64 are bare strings**
(`expanded_hypothesis_card.schema.json` declares them as bare-string-only —
the majority-dict reality is a corpus/schema mismatch, not a corpus
anomaly). 15 of the 46 runs mix bare strings into the same
`expanded_variants` list that also holds dicts. Field presence among the 74
dict-shaped variants (denominator 74, from
`s1_measure_variants.py`'s companion field-presence pass):

| Field | Presence |
|---|---|
| `variant_id` | 68/74 (92%) |
| `id` | 6/74 (8%) |
| `name` | 20/74 (27%) |
| `label` | 21/74 (28%) |
| `rationale` | 31/74 (42%) |
| `description` | 16/74 (22%) |
| `target_market` + `target_markets` combined | 11/74 (~15%) |
| `timeframe` + `timeframe_expanded` + `timeframe_original` combined | 18/74 (~24%) |
| `parameters` + `params` + `config_params` combined | 22/74 (~30%) |

Every one of the 74 dict variants has *some* id-like key
(`variant_id`/`id`/`name`/`variant_name`/`label`) — 0 have none — but no
single key is universal, and 92% is the best any one key does.

**Consequence for design**: instrument and timeframe — which E-032's gate
needs — are usually **not** on the variant itself (only ~15%/~24%
respectively). They live reliably on the *parent* `hypothesis_card.yaml`
instead: its schema (`hypothesis_card.schema.json`) makes both
`target_market` and `timeframe` **required** top-level fields, confirmed
present on run_019's `hypothesis_card.yaml`. Confirmed separately: the
strategy `config` object inside `backtest_spec.yaml` (run_019 spot check)
carries neither `target_market` nor `timeframe`/`symbol` — the engine config
itself is not a source for this either. **A selection record cannot get
instrument/timeframe by reading only the chosen variant; it must resolve
them as "variant's own override if present, else the parent card's value,"
and record the resolved values explicitly** — this mirrors exactly what
`anti_adjacency_gate.evaluate_candidate()`'s docstring already says about its
own `instrument`/`timeframe` override parameters (*"required when a caller
is evaluating one variant of a multi-symbol card individually"*) — the gate
was already built expecting this resolution to happen upstream of it; E-034
is that upstream.

### Minimum content

**To let a later stage mechanically identify the tested variant** (what
E-032's gate needs):
1. `hypothesis_id` (the base hypothesis this run is testing).
2. A **stable variant identifier** — `variant_id` when present (92% of dict
   variants); for the 8% dict remainder and all 64 bare-string variants,
   there is no author-supplied stable ID, so the record-writer must derive
   one deterministically (e.g. positional index within `expanded_variants`,
   or a content hash of the string/dict for bare strings) — see "handling
   inconsistent shape" below.
3. Resolved `instrument`/`target_market` and `timeframe` (variant override
   if present, else inherited from `hypothesis_card.yaml` — see above).
4. A pointer back to the source artifact + line/index (so a human or a
   future gate can go re-read the original variant text without the record
   duplicating everything).

**To make a discarded variant reconsiderable months later** (what E-034's
own Done-when #2 asks for):
1. The variant's **full original definition, copied verbatim** — not
   re-summarized by an LLM. Given field presence is inconsistent (item 2
   above), "verbatim" is the only safe move; anything else invites silent
   loss of whatever context that particular variant happened to carry
   (`parameters`, `rationale`, `expected_outcome`, etc. — the union of keys
   actually used across the corpus is large and non-standardized, see the
   script's key-presence output).
2. **Why it lost** — one sentence minimum, distinguishing "not chosen this
   round" (still viable) from "actively contraindicated by
   validation/screening" (should sink, not resurface). This distinction
   does not exist anywhere in the current corpus and must be a required
   field on the new record, not inferred after the fact.
3. `run_id` + `hypothesis_id` it was discarded from, and the timestamp, so a
   future dedup/anti-adjacency pass (E-032) can tell how old and how many
   times a given idea has already been proposed-and-passed-over.

### Is `variants_not_pursued` (used once) a usable foundation?

**No — supersede it.** It exists in exactly one file
(`run_0001/artifacts/innovation_notes.yaml`), it is not schema-governed
(`innovation_notes.yaml` has no schema in `workflow_artifacts/schemas/`), it
was never repeated in 58 subsequent runs, and — most importantly — it lives
inside `innovation_notes.yaml`, which is `innovation_expansion`'s own
narrative output, written *before* `validation` and *before*
`backtest_specification` ever narrows anything. It documents variants that
existed at generation time, not the ones actually discarded at selection
time (those are different moments — validation can itself drop variants
between `expanded_hypothesis_card.yaml` and `validation_decision.yaml`'s
`variants_to_test`, as run_019 shows: 3 threshold variants generated, plus a
BTC-only variant that only appears at the validation stage, 4 total reaching
`variants_to_test`). One prior, unrepeated, unschemad, wrong-stage field is
not a foundation to extend — S2 should introduce a new, schema-governed
artifact instead.

## Task 3 — where the record should be written, and by whom

**Deterministic code, joining a small structured LLM output against the menu
it already has on disk — not the LLM self-reporting freeform after the
fact.**

The LLM inside `backtest_specification` is the only actor that knows *why*
it picked what it picked (that reasoning is not recoverable by code after
the fact — it's genuine judgement: cost/power tradeoffs, which threshold
best matches the validated hypothesis, etc., as seen in run_019's real
`config_rationale`). So the LLM must still be the source of the *choice and
reasons*. But it should not be trusted to also correctly copy every other
variant's full definition into a discard pool, or to compute the
instrument/timeframe resolution — that's exactly the class of
self-reporting-drift this project has been burned by before (per the
dispatch brief). Split the responsibility:

1. **LLM's job (schema change, S2):** add one new required field to
   `backtest_spec.yaml`'s schema — e.g. `selected_variant_id: string` — and
   require it to be copied verbatim from whichever `expanded_variants` entry
   was used (for bare-string variants, verbatim = the string itself, or the
   `variant_id`/`id`/`name`/`label` key if it's a dict). `SKILL.md` gets one
   new instruction: name the exact variant used, from the closed set present
   in `expanded_hypothesis_card.yaml`; fail loud (existing `component_gap`-
   style stop condition) if none of the variants fit rather than silently
   inventing a hybrid. This is a closed-set pick, structurally the same kind
   of constrained output the stage already produces for `status`
   (`spec_ready`/`component_gap`) — not open-ended self-report.
2. **Deterministic code's job (new function, S2):** immediately after
   `backtest_specification`'s output passes schema validation (same place
   `_apply_b7_mandatory_inputs`/friends already hook into the stage
   lifecycle in `run_phase1_research.py`), add a function — e.g.
   `_record_variant_selection(run_dir)` — that:
   - Loads `expanded_hypothesis_card.yaml.expanded_variants` and
     `hypothesis_card.yaml` (for instrument/timeframe fallback).
   - Loads `backtest_spec.yaml.selected_variant_id`.
   - Matches it against the menu using variant_id (or the derived fallback
     ID for unlabeled/bare-string variants — same derivation rule for both
     record-writing and later matching, so it's stable). **Fail loud** (raise,
     halt the run) if the LLM named something not in the menu — this is
     exactly the "fail loud on degenerate inputs" standing rule, and it
     catches a hallucinated or malformed `selected_variant_id` before it
     becomes an unreadable record.
   - Writes `variant_selection.yaml`: `run_id`, `hypothesis_id`,
     `selected_variant_id`, the full matched variant definition (copied
     verbatim by code, not retyped by the LLM), resolved `instrument` +
     `timeframe`, and `chosen_rationale` (lifted verbatim from
     `backtest_spec.yaml.config_rationale` / `decision.yaml.rationale` —
     already LLM-authored, just relocated to a place a machine can find it).
   - Writes `variants_not_pursued.yaml`: every other entry in
     `expanded_variants`, verbatim, each tagged with its derived/native ID,
     `run_id`, `hypothesis_id`, and (best-effort, optional) a "why it lost"
     string if the LLM chose to say more than the bare selection (SKILL.md
     can invite this without requiring it, to avoid forcing fabricated
     reasons for variants the stage genuinely didn't consider deeply).

This is the cheapest seam: it adds one required string field to an existing
LLM output (closed-set, schema-checkable, same shape as `status` today) and
one new deterministic post-processing function invoked at a lifecycle point
that already exists for exactly this kind of stage-output enrichment. It
does not move a stage boundary, does not change `determine_post_spec_route`,
and needs no second LLM call.

### Handling the inconsistent variant shape (bare string vs dict)

S2 must not assume dict shape. Recommended derivation, to be applied
identically wherever a variant needs an ID (record-writing and any future
matching/gate code):
- Dict with `variant_id` (92% of dicts): use it verbatim.
- Dict without `variant_id` but with `id`/`name`/`variant_name`/`label`: use
  the first of those present, in that priority order (all 74 dicts have at
  least one).
- Bare string (64/138, all string-shaped): use a short deterministic hash of
  the string content, prefixed with the positional index (e.g.
  `str_{index}_{hash8}`) — stable across re-reads of the same file, distinct
  even if two bare-string variants happen to share text.
This is a derivation rule for S2 to implement, not something this story
invents a library for — flagging it here so S2 doesn't have to re-discover
the 92/8/bare-string split from scratch.

### Itemized build list for S2 (dispatch-ready)

1. `backtest_spec.schema.json`: add required `selected_variant_id: string`.
2. `backtest-engineering/SKILL.md`: instruct the stage to populate it from
   the closed set of `expanded_variants` IDs (using the derivation rule
   above when the menu has no native ID); fail (`component_gap`-style stop)
   if it cannot map its choice back onto one menu entry.
3. New schema: `variant_selection.schema.json` (fields per Task 2's minimum
   list) and `variants_not_pursued.schema.json` (array of the same
   shape, plus `lost_to_run_id`/`lost_reason` optional fields).
4. New function `_record_variant_selection(run_dir)` in
   `workflow/run_phase1_research.py`, called right after
   `backtest_specification`'s outputs are validated (same lifecycle point
   `_apply_*` helpers already hook into) — writes
   `artifacts/variant_selection.yaml` and
   `artifacts/variants_not_pursued.yaml`.
5. Flag-gate the new function per the standing off-by-default rule (E-034
   Done-when #4): absent flag/config → function is not called at all (same
   "the code path is entirely unreached" proof shape used by
   `_anti_adjacency_retry_enabled()` and friends), so existing runs'
   assembled prompts and outputs stay byte-identical.
6. Bit-identity test: flag off → no new files, no change to
   `backtest_spec.yaml`'s existing keys' values, no change to any prompt
   assembled for any stage.
7. Fixture-driven unit tests for the derivation rule (dict-with-variant_id,
   dict-without-variant_id-with-label, bare-string) and for the fail-loud
   path (an out-of-menu `selected_variant_id`).

S3 (separate story, not built here) then repoints
`_route_post_innovation_expansion`'s `candidate_path` construction — or
rather, since that gate call happens *before* `validation`/`backtest_spec`
in the pipeline order, S3's actual repoint target is a **new** gate
invocation point, right after `variant_selection.yaml` exists, that builds
its `candidate` dict from `variant_selection.yaml` (merging base-card fields
for anything the variant doesn't override) and passes the resolved
`instrument`/`timeframe` through `evaluate_candidate()`'s existing override
parameters — no change needed inside `anti_adjacency_gate.py` itself; it
already accepts exactly this shape.

## Task 4 — downstream consumers

### E-032's gate

**What it would read**: `artifacts/variant_selection.yaml`'s
`selected_variant_id` (as `hypothesis_id` for logging/KB-check purposes, or
paired with the base `hypothesis_id`), plus its resolved `instrument` and
`timeframe`, passed explicitly to `evaluate_candidate(candidate,
instrument=..., timeframe=...)` — the exact override mechanism the function
already exposes and currently has zero real callers for (grep-confirmed:
`_route_post_innovation_expansion` calls `evaluate_candidate(candidate, ...)`
with no `instrument=`/`timeframe=` kwargs at all).

**Does this fully close the wrong-artifact defect logged 2026-08-24?** It
closes the *data availability* half — for the first time there is a
concrete, single, schema-governed artifact naming the actual variant under
test, with instrument/timeframe resolved. It does **not**, by itself, close
the defect end-to-end: E-032's EPIC log is explicit that
`_route_post_innovation_expansion` runs *before* `validation`, i.e. before
`variant_selection.yaml` can possibly exist yet (that artifact is a
`backtest_specification`-stage output, several stages later). So S3 cannot
simply "point the existing call at the new file" — it needs a **second,
later gate check** (or a moved/duplicated call site) positioned after
`backtest_specification`, which is a real, non-trivial routing change beyond
"read a different path." This story flags that gap for S3 rather than
papering over it; E-034's EPIC.md already scopes S3 as coordinating with
E-032, which is the right shape for this.

### E-031's refill

Read `engineering/roadmap/E-031/artifacts/s1_refill_sources.md` in full
(cited above). E-031 S1 ranked five source classes and found exactly one
open, unblocked candidate today (the funding-rate 4h reactivation branch,
source class #1: **KB reactivation clauses with a pre-existing evidentiary
bar** — an `exhausted: false` disposition and an explicit
`reactivation_condition` someone already judged worth re-checking).

**Would a persisted E-034 variant pool qualify, and under what routing
tier?** It is a legitimate source, but it does not enter at E-031's
strongest tier — it sits closer to E-031's *weakest* named tier
(refinement_planner's deferred branches, which E-031 explicitly declined to
build machinery for: "too sparse... not indexed"), except better, because
E-034 S2 makes it dense (138 variants, not 1-in-59) and indexed (a real
schema-governed file per run, not buried per-run prose). What it structurally
lacks relative to E-031's tier-1 KB clauses is the **evidentiary bar**: a KB
`reactivation_condition` exists because a human/LLM already judged the
mechanism sound and pinned a specific, checkable condition for when it's
safe to retry. An E-034 discarded variant only carries "not chosen this
round, here's roughly why" — it was never itself run, screened, or
falsified; it's supply, not a vetted disposition.

**Extra qualification required, per E-031's own recommended policy**
(Task 3 of that document, points (a)-(e)): any E-034-sourced candidate must
still pass through the same admission gates E-031 lays out for every
machine-minted source — critically, **it must clear E-032's anti-adjacency
gate first** (once S3 wires the gate to read `variant_selection.yaml`-shaped
candidates, the same gate can run against pool entries), plus the
exclusion-context checks (`failed_families`,
`recent_parameter_dimensions_by_family`), and it must land as
`status: "paused:pending_operator_ratification"`, never auto-`ready`,
exactly like every other source E-031 examined. **A persisted E-034 pool is
not a legitimate refill source on its own — it becomes one only after
E-032's gate (which itself depends on E-034 S2 existing) has filtered it.**
This is a real sequencing dependency worth naming for whoever scopes E-031
S2/S3: E-034 S2 → E-032 S3 (gate reads variant_selection-shaped candidates)
→ only then is an E-034 discard pool an admissible E-031 refill input.

## Deliverables produced by this story

- `engineering/roadmap/E-034/artifacts/s1_selection_record.md` (this file).
- `engineering/roadmap/E-034/artifacts/s1_measure_variants.py` (the
  measurement script; re-run any time, read-only, does not touch
  `local_data/holdout_sealed/`).

## Files read (source-of-truth per finding, no archived `stages.yaml` used)

- `strategy-research/workflow/run_phase1_research.py` — `STAGE_CONFIGS`
  (87-137), `_route_post_innovation_expansion` (1458-1584),
  `determine_post_validation_route` (1730-1798),
  `determine_post_spec_route` (5380-5397).
- `strategy-research/workflow_artifacts/templates/handoffs/validation_to_backtest_specification.yaml`
- `strategy-research/workflow_artifacts/skills/backtest-engineering/SKILL.md`
- `strategy-research/workflow_artifacts/skills/quant-validation/SKILL.md`
- `strategy-research/workflow_artifacts/schemas/{backtest_spec,decision,
  expanded_hypothesis_card,hypothesis_card,validation_decision}.schema.json`
- `strategy-research/tools/anti_adjacency_gate.py` (`evaluate_candidate`,
  402-422)
- `strategy-research/runs/run_019/artifacts/{expanded_hypothesis_card,
  validation_decision,backtest_spec,decision,hypothesis_card}.yaml`
- `strategy-research/runs/run_{005,007,017,018,020-025,027-031,034,035,039,
  053}/artifacts/{expanded_hypothesis_card,decision,backtest_spec}.yaml`
  (spot checks, script-assisted)
- `strategy-research/engineering/roadmap/E-032/EPIC.md` (2026-08-24 OPEN
  DEFECT log entry, in full)
- `strategy-research/engineering/roadmap/E-031/artifacts/s1_refill_sources.md`
  (in full)
- `strategy-research/engineering/roadmap/E-034/EPIC.md` (in full)
