# C5.7b — Score provenance, Phase A (characterize and STOP)

Continuation plan C5.7 second half; review finding C12 (`DELIVERY_REVIEW.md:78`; A2 H-N §"Score provenance is trust-based", `A2_cards_H-N.md:138-140`; row I.5 at `:41`; "could not verify" at `:164`).
Base: `origin/master` at 9c4b05ab. Read-only investigation: no LLM call, no backtest, no writes outside this file. All paths are under `strategy-research/`; `rpr` = `workflow/run_phase1_research.py`, `dn` = `tools/decide_next.py`, `rp` = `tools/reader_proposals.py`. Line numbers are from this checkout (the review's `rpr:5967-5970` has drifted to `rpr:6678-6683`).

Not measured (needs a paid call or a recorded transcript; none exists on disk: `runs/` has no `proposals/` dir and no reader has ever run on it, and `~/.claude/projects/` holds no stage-agent transcripts): the actual string `AssistantMessage.model` returns for `claude-haiku-4-5`, and what a reader writes in `model_id` today. Everything below that depends on either is marked *(unmeasured)*.

## 1. Where a score and its model_id / rubric_version are produced, stored, read

Search terms (all file types under `strategy-research/`, excluding `runs/`, `campaign_record/`, `engineering/`): `model_id`, `rubric_version`, `confidence_real`, `distance_to_profitable`, `mechanism_plausibility`, `"scores"`, `reader-v`, `brief-card`, `load_proposals(`, `assigned_engine`, `query(`, `genai`.

| Role | Site | What happens |
|---|---|---|
| Produce (reader) | 5 SKILL.md: `workflow_artifacts/skills/readers/<cat>-reader/SKILL.md` (`profitability:122-123`, `forecast_power:80-81`, `regime_power:111-112`, `component_attribution:110-111`, `trade_efficiency:91-92`) | Tell the LLM to write `model_id: <str>` (no value given) and a literal `rubric_version: "<cat>-reader-v2"`. Anchored score tables in each SKILL. |
| Produce (brief cards) | `workflow_artifacts/skills/hypothesis-design/BRIEF_HYPOTHESES.md:32-42` | Stage 1a writes `extra_card_scores.yaml` items `{card, scores, model_id: <your model id>, rubric_version: brief-card-v1}`; only when it wrote several cards. |
| Call (reader) | `rpr:3679-3694` `_invoke_reader_llm`; `rpr:3734-3790` `run_reader_worker` | One `query()`; returns `(text, {usage, cost_usd, num_turns})`. Body written verbatim to `artifacts/proposals/<cat>.yaml` (`rpr:3768-3775`). |
| Call (1a) | `rpr:1056-1071` `run_claude_worker`; deliverables regex-saved at `rpr:1133-1137` | Any fenced `# name.yaml` block is written as-is, including `extra_card_scores.yaml`. |
| Validate (reader) | `rp:63-65` | `model_id`, `rubric_version`: non-empty string only. Evidence: non-empty list of non-empty strings (`rp:93-96`). Scores: exactly 3 keys, int 0..3 (`rp:113-122`). Undeclared fields rejected (`rp:62`). |
| Validate (cards) | `dn:675-691` `validate_card_scores`; constant `dn:150` `BRIEF_CARD_RUBRIC = "brief-card-v1"` | `rubric_version` is already a closed value (exact match, else `DecideNextError`). `model_id`: non-empty string only. |
| Store (cards) | `rpr:6617-6660` (`_queue_extra_hypothesis_cards`), `rpr:6678-6683` `_card_scores_as_item` | Copies both fields into `artifacts/queued_hypotheses.yaml` verbatim. |
| Store (candidate) | `dn:1441-1442` (reader), `dn:1478` (card); `dn:718` (card load); `dn:863` (`load_proposals`) | Copies `p["model_id"]`, `p["rubric_version"]` into the candidate `scores`, then `decision_record.yaml` (`workflow_artifacts/schemas/decision_record.schema.json:178-190`, both `string|null`). |
| Schema | `workflow_artifacts/schemas/proposal.schema.json:108-115` | `model_id`: string ("e.g. a Claude model string"); `rubric_version`: string. |
| Read (rank) | `dn:1557` `_score_key`, `dn:1587` `rank_key` | Use only `confidence_real`, `distance_to_profitable` (+ cost, id). `mechanism_plausibility` recorded, not ranked (`dn:1584`). **`model_id`/`rubric_version` are never read by any code**; they are write-only metadata. |
| Not consumers | `tools/campaign_memory.py:366` (loads proposals for counts; header `:21` says scores never copied), `tools/near_miss_scoreboard.py`, regroup, `run_campaign.py:4561-4587` (reads queued-card record for a queue title), campaign review | grep for `model_id`/`rubric_version`/the 3 score names in these files: no hits. Campaign review's reframe emits no scores (known: review C8/A2 item 7). |
| Audit log | `rpr:3758-3765` (reader), `rpr:1097-1117` (1a) | Records engine, time, cost, `num_turns`, tokens. **No model field at all** (CUL-336 logging is cost/tokens only). |

Contradiction with the review (I.5, `:41`): it says `rpr:5967-5970` is the only place `model_id` is copied. Current code also copies it at `dn:691`, `dn:1442`, `dn:1478`, and at the card path `rpr:6683`. Same conclusion (nobody stamps it), more copy sites.

## 2. What the call actually knows

| Fact | Evidence |
|---|---|
| Both Claude stages go through one options builder, `_stage_agent_options()`, with `model=_CLAUDE_WORKER_MODEL` = `"claude-haiku-4-5"` (`rpr:949`, `rpr:1006-1013`). So the *requested* model is a code constant, already known without the SDK. | `rpr:949,1006` |
| SDK is `claude_agent_sdk` 0.2.82 (installed; the version `_stage_agent_options`'s docstring cites). `AssistantMessage.model: str` is a required field, populated from `data["message"]["model"]`. | `site-packages/claude_agent_sdk/types.py:1025-1030`; `_internal/message_parser.py:174` |
| `ResultMessage.model_usage: dict | None` (parsed from `modelUsage`), plus `usage`, `total_cost_usd`, `num_turns`. | `types.py:1145-1159`; `message_parser.py:261` |
| Both call sites already iterate the stream and see every `AssistantMessage`, but read only `.content` and (from the result) `usage/total_cost_usd/num_turns`. They discard `.model` and `model_usage`. | `rpr:1056-1071`, `rpr:3685-3693` |
| So the real model id is available at the call site, **before** the artifact is written (reader: text is validated then written at `rpr:3768-3775`, same function that holds `meta`; 1a: `rpr:1056` precedes the write at `rpr:1133-1137`). | same lines |
| Gemini: `run_gemini_worker` (`rpr:1154`) hard-codes `gemini-2.5-flash-lite` (`rpr:1206`) and is reached only when a handoff sets `assigned_engine: gemini` (`rpr:7622-7629`). Every in-repo handoff builder sets `claude` or `tool` (`rpr:3531,3620,5980,7781`; templates). Readers never reach it (they call `_invoke_reader_llm` directly). It writes only fixed filenames per stage and cannot produce `extra_card_scores.yaml`. So Gemini is not a live score path. | `rpr:1273-1276` |
| Unmeasured: whether `AssistantMessage.model` is the dated id (e.g. a `-2025...` suffix) or the alias we requested; whether it can differ across messages in one session (tools=[] makes one turn by construction, `rpr:1002-1004`, so expected one message). | *(unmeasured)* |

Test-harness facts that matter for design: the e2e stub yields `AssistantMessage(..., model="stub-claude")` (`tests/test_e061_end_to_end_wiring.py:531`) while its stub readers self-report `"stub-reader"` (`:665`); the CUL-336 `_Capture` stub yields a bare object with no `.model` (`tests/test_cul336_closed_book_stages.py:120-126`). So code must tolerate "no observed model".

## 3. Proposal: model_id from the call

Design (all behind one new flag, default off):

1. **Capture** in `_invoke_reader_llm` and `run_claude_worker`: collect `{m.model for AssistantMessage}` and `ResultMessage.model_usage` keys; return as additive `meta["models"]` (reader). Flag-off: nothing recorded or written.
2. **Stamp** at write time (the only place both the observed value and the artifact are in hand): in `run_reader_worker` after validation succeeds, parse the body, set every proposal's `model_id` to the observed id, re-dump (`yaml.safe_dump(sort_keys=False)`), write via the existing temp-file + `os.replace`. Same for `extra_card_scores.yaml` in `run_claude_worker`'s save loop (`rpr:1133-1137`). Downstream (`dn:1442`, `dn:691`, decision record, schema) then carries the observed value with no change.
3. **Record both, never crash**: add a `provenance` block to the existing audit-log entry (`rpr:3758` / `rpr:1097`): `{requested, observed_models, self_reported: {<proposal_id or card>: <str>}, mismatch: bool, self_report_differs: bool}`. No raise, no retry, no stop, on any mismatch.
4. **What "mismatch" should mean** (my recommendation): `mismatch = observed does not start with the requested constant, or more than one distinct observed model`. That is the real trust question ("did the CLI run the model we asked for?"). A self-report that differs from the observed id is recorded as `self_report_differs` (informational), because the SKILL never tells the LLM its id (`model_id: <str>`), so a differing self-report is expected on essentially every run *(unmeasured hypothesis)* and a flag on it would fire always and mean nothing.
5. **No observed model** (stub, empty stream): leave the field as written, record `observed_models: []`, `mismatch: null`. Never fabricate.
6. **Schema**: no field added (`additionalProperties: false`, `rp:62` rejects extras); `model_id` keeps its type and only its meaning tightens (edit the `description` string at `proposal.schema.json:108-111`). A sidecar file in `proposals/` is impossible: `load_proposals` raises on any unexpected `*.yaml` there (`rp:135-140`).
7. **Flag**: `orchestrator.score_provenance.enabled` (new) in `config/campaign_config.yaml`, reader `_score_provenance_enabled()` following the `_specialist_readers_enabled` shape (`rpr:3387`: non-bool raises; hard dependency on `specialist_readers`), plus an entry in `config/feature_flag_register.yaml` (enforced by `tests/test_feature_flag_register.py`).
8. **Flag-off byte identity**: reader body is written verbatim as today (`rpr:3768-3775`); audit-log entry has no new key; `meta` gains a key nobody reads. Test: run `run_reader_worker` and the 1a save with a stub stream flag-off, assert output files and audit-log entries equal the pre-change bytes.

Rejected alternative: stamping in `decide_next` from the audit log. It must pick the right stage attempt/retry entry per proposal file; write-time stamping avoids that join.

## 4. rubric_version: closed set from the SKILL files

Facts: each reader SKILL carries exactly one literal, all `-v2` (C2 S2e). The rubric for a proposal is fully determined by its category, which `_check_proposal` already receives (`rp:57`, `cat`). Cards are already closed (`dn:687`).

Proposal:
- `rp.READER_RUBRIC_VERSIONS = {cat: f"{cat}-reader-v2"}` constant, and in `_check_proposal` require `p["rubric_version"] == READER_RUBRIC_VERSIONS[cat]` when a `strict_provenance` kwarg is on. Failure raises `ProposalError`, which `_validate_reader_output` (`rpr:3713-3731`) already turns into one retry with the error appended, then a stop. That is the existing contract for any malformed reader output.
- "Derived from the SKILL files" is enforced by a **pin test** that reads the five SKILL.md files, extracts the `rubric_version` literal, and asserts equality with the constant (the pattern `rp`'s docstring already uses for the schema). No SKILL parsing at runtime.
- Kwarg plumbed through `load_proposals` (callers: `rpr:3726,3809,3814,3818`; `dn:863`; `campaign_memory.py:366`; 13 test call sites). Default False keeps every caller and every `-v1` fixture unchanged.
- Alternative (less strict, listed for the operator): code stamps `rubric_version` too, as it does `model_id`, since code knows which SKILL it sent. Removes the retry/stop failure mode but hides SKILL drift. Recommend reject-unknown for `rubric_version` (it is a copy-a-literal task) and stamp for `model_id` (the LLM cannot know it).
- Bumping a SKILL to `-v3` then requires bumping the constant; the pin test fails otherwise (intended).
- Unknown value on a stale on-disk file re-validated at `rpr:3809`: raises. Under the flag, an old `-v1` proposals dir from a pre-flag attempt would stop; `protocol_execution` already clears `proposals/` each attempt (`rpr:3430,3444`, `_SPECIALIST_READERS_RUN_SCOPED_DIRS`), so this only bites a mid-run flag flip. State it in the flag's register entry.

## 5. Citation per score

What exists: `evidence` is a per-proposal list, non-empty strings only (`rp:93-96`). The SKILLs require each item to "cite a specific field path from `<cat>.yaml`'s own `slices`" (e.g. `profitability-reader/SKILL.md:160-174`, `:264`), including `variants.base.slices.per_symbol.BTCUSDT[*].core.cost_drag_pct` style with `[*]`, `[]` and trailing `=value`, plus one item citing a `registry_summary.yaml` field for `distance_to_profitable` (`:256-257`). Nothing in code checks any of it, and nothing links an evidence item to a particular score.

What the reader received (so what a check may use): `artifacts/reports/<cat>.yaml` (`{category, variants: {<vid>: {slices: {overall, per_window[], per_regime{}, per_symbol{}}}}}` for schema_version 2; `tools/build_reports.py:8-31,153-162`), `grid_evaluation.yaml`, `registry_summary.yaml` (`rpr:3620-3630`). Code has all three on disk.

| Option | What it checks | Cost | Benefit | Risk |
|---|---|---|---|---|
| A. Evidence-path existence, record-only | Extract `variants.…` / `this_run.…` tokens from each evidence string, normalise `[*]`, `[]`, `[n]`, `=value`; walk them in the received files; record `{resolved, unresolved}` per proposal in the audit-log `provenance` block. No reject. | SMALL: one pure function + tests; no SKILL, schema or prompt change | Turns "cites a field" from convention into a measured rate; tells us the false-unresolved rate on real output before anything is gated | Does not link to a specific score; a real path can be quoted around a wrong claim |
| A+. Same, but reject-with-retry when any evidence item has zero resolvable path or any cited path is unresolvable | Same walker | SMALL code; BIG in false-reject risk: the tokens are LLM-formatted prose, and no real reader output exists on disk to calibrate against *(unmeasured)* | Hard guarantee that the cited fields exist | A false reject costs a retry (a paid call) then stops the run |
| B. Per-score citation field | New `score_basis: {confidence_real: [evidence indices], ...}`; check indices valid and each score has at least one resolvable citation | BIG: schema, `_PROPOSAL_KEYS`, decision_record, 5 SKILLs (prompt change means behavior change, needs a paid re-test of all five readers) | The only option that actually answers "what does this score rest on" | Changes model output shape; new failure mode; does not prove the score follows from the cited value (anchor semantics stay LLM judgment) |
| C. A + value check (`=142.82` equals report value within rounding) | Compares literals | MEDIUM; brittle on formatting, rounding, `n=` vs `mean=` | Catches quoted-but-wrong numbers | Highest false-reject rate |
| D. Do nothing on citations | — | none | none | C12's third clause stays open |

Brief cards have no report to check against (they score a card before any backtest; rubric text says "cite it" but there is no field), so no mechanical citation check exists for them under any option.

**Recommendation (operator call):** A first (record-only, ships with the model/rubric slices), then decide A+ from the measured unresolved rate after the first real reader run. B only if the operator wants per-score attribution enough to pay for prompt and schema change. Decision needed: A only, A then A+, or B.

## 6. Slices

| # | Slice | Contents | Tests (new unless stated) | Declared test changes |
|---|---|---|---|---|
| S0 | Flag + capture | New flag `orchestrator.score_provenance.enabled`, reader fn, register entry, `config/campaign_config.yaml` comment; `meta["models"]` capture in `_invoke_reader_llm` and `run_claude_worker`; audit-log `provenance.requested/observed_models` only under flag | flag parse (non-bool raises, dep on specialist_readers raises); capture from a stub stream with two `AssistantMessage`s; no-model stub; flag-off audit-log entry equals baseline | none. `tests/test_feature_flag_register.py` passes by the added entry, not by editing the test. CUL-336 `_Capture` stub has no `.model`, so the no-observation path is required behavior |
| S1 | Reader model_id stamp | Stamp in `run_reader_worker`; `provenance` self_reported/mismatch/self_report_differs; schema description edit | stamp overwrites; mismatch recorded and run continues; unobserved leaves field; flag-off reader file byte-identical; downstream `dn:1442` carries stamped value | none (e2e stubs run flag-off) |
| S2 | Reader rubric closed set | `READER_RUBRIC_VERSIONS`, `strict_provenance` kwarg through `load_proposals`, call sites under flag; SKILL pin test | unknown/other-category/`-v1` rejected under flag; accepted flag-off; pin test vs 5 SKILL files; retry message reaches the reader | none while default False. Existing `-v1` fixtures (`tests/test_e046a_slice5b_i_reader_skills.py:217-288`, `test_e059_s2a_decide_next.py:88,98`, etc.) stay valid because the kwarg defaults off |
| S3 | Card model_id stamp | Stamp `extra_card_scores.yaml` in `run_claude_worker`'s save loop; provenance for 1a stage | card stamp; `brief-card-v1` still enforced at `dn:687`; flag-off bytes | none |
| S4 | Citation option A (after operator call) | Pure `resolve_evidence_paths(report, evidence)`; record in provenance | table-driven cases from the SKILL GOOD/BAD examples; `[*]`/`[]` handling; unavailable-slice reports; registry_summary root | none |
| S5 (only if chosen) | A+ gate or B | per operator | — | B: schema/SKILL changes = declared, re-test five readers |

Order: S0 → S1 → S2 → S3 independent after S0; S4 after operator decision. One PR per slice; the flag stays off in the shipped config, so no default output changes and no baseline is invalidated.

## 7. Guesses table

| # | Guess | Size | Blocks build? |
|---|---|---|---|
| G1 | One new flag `orchestrator.score_provenance.enabled`, default off, hard-dep on `specialist_readers` | SMALL | No |
| G2 | Stamp at write time (not in decide_next) | SMALL | No |
| G3 | Stamped `model_id` = `AssistantMessage.model`; if several distinct, join sorted with `,` and set mismatch | SMALL | No |
| G4 | "Mismatch" = observed vs requested constant, not observed vs self-report; self-report difference is informational | SMALL | No, but operator should confirm meaning (a flag on self-report would fire always) |
| G5 | Mismatch never raises or retries; recorded in audit log only | SMALL | No |
| G6 | Rubric: reject unknown (retry then stop, existing contract) rather than stamp | SMALL | No |
| G7 | Rubric constant + SKILL pin test rather than runtime SKILL parsing | SMALL | No |
| G8 | Same rubric closed-set for cards already true (`dn:150,687`); no change | none | No |
| G9 | Citation: Option A (record-only) first | SMALL | **Yes: operator call A / A→A+ / B** |
| G10 | Real dated-id string from the SDK matches "starts with requested" | SMALL if true | No; verify on the first real reader call *(unmeasured)*; if false, normalise (strip date suffix) |
| G11 | Re-dumping the stamped YAML with `safe_dump(sort_keys=False)` is acceptable (comments/format lost, semantics same; only `load_proposals` reads the file) | SMALL | No |
| G12 | Gemini path out of scope (no live score path) | none | No |

## Decision (operator, 2026-09-29) — recorded as D-048

- G9 citations: **option A** (record-only); A+ / B decided after C4's first real reader output.
- G4 mismatch = observed vs requested model; the self-report is informational.
- Other guesses as recommended. Build in two slices (orchestrator, small-slice rule): **C5.7b-1** = S0 + S1 + S3
  (flag, capture, reader and card model_id stamp); **C5.7b-2** = S2 + S4 (rubric closed set, citation record).

### C5.7b-1 built

S0 + S1 + S3 on branch `feat/c5-7b1-model-id-stamp`, behind `orchestrator.score_provenance.enabled` (default false, strict bool, requires `specialist_readers`; pre-flighted in `run_loop` and `run_campaign._flag_preflight`; registered `off_incomplete`, blocked on C5.7b-2 and C4's first real reader output). Code: `run_phase1_research.py` (`_score_provenance_enabled`, `_note_stream_models`, `_stamp_reader_body`, `_stamp_card_scores_text`; capture in `_invoke_reader_llm` and `run_claude_worker`; stamp in `run_reader_worker` and `run_claude_worker`'s save loop); `proposal.schema.json` gets a `description` edit only. Tests: `tests/test_c5_7b1_model_id_stamp.py` (34); no existing test changed.
Guesses made: `mismatch` treats the requested id or `<requested>-<suffix>` as a match (G10; the real SDK string is still unmeasured); `ResultMessage.model_usage` keys are recorded as `result_models` (information only, never stamped); a stamped reader body is re-validated and the unstamped body kept if that fails (`stamped: false`, `stamp_error`); card provenance sits under `provenance.cards` of the 1a stage's audit entry; unchanged bodies (self-report already equal, empty list) are written verbatim.
Still open: the observed string for `claude-haiku-4-5` (measure on C4's first real reader call); S2 and S4 are C5.7b-2.
