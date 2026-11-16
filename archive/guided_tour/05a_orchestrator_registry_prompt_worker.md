# Stop 05a: The orchestrator core, part a: the stage list, the prompt, the AI call

## Speech (verbatim)

**Stop 05 of 29: The orchestrator core.** Two parts: 05a, how one stage is prepared and called (this speech); 05b, the loop that chains the stages, the routes between them, the handoffs and the file checks (next). Open on the side: `run_phase1_research.py`, `workflow_artifact_validation.py`, run_102's `pipeline_state.yaml`.

**In one sentence.**
The orchestrator is the conductor of a run: it knows every step, prepares what each AI step must read, calls the AI, and files its answer.

**Why it exists.**
The AI steps must see exactly the inputs the process intends, and nothing more. An AI that could browse the repository might read a result it should not know yet, or another run's notes.
So the conductor builds each prompt itself, from fixed files, and the AI answers from that prompt alone.
It also records what every call cost, so the campaign's spending is known run by run.

**What comes in, what goes out.**
- In: the run folder (brief, pre-registration, earlier stages' files), the stage's instruction template (a handoff), the stage's role sheet (a skill), and the switchboard.
- Out: the AI's answer, cut into files in the run's artifacts folder; one cost line per call in the run's state file.
- Next: the loop (05b) reads those files and decides the next stage.

**What happens here, step by step.**
1. The conductor knows 12 stages. For each: its handoff, the stage that normally follows, and for an AI stage its skill.
2. Three stages are plain Python tools under the current switches: building the variants, the data check, the backtests. They skip the AI path. The analyst and the record-keeping stage have paths of their own (stops 21, 22).
3. For an AI stage, it loads the stage's handoff from the run folder. Then it adds inputs that depend on the switches and on the run: the files the skill says to read, the list of tried ideas, the claim-test menu, the start config, a retry message, and so on. These additions exist only in memory; the handoff file on disk stays the copied template.
4. It builds the prompt: the skill (the AI's role and rules), the handoff, the full text of every input file, and fixed answer rules: reply only with YAML blocks (a plain-text data format), each headed by its file name. A missing required input stops the stage before the call.
5. It picks the model: Sonnet 5.5 for steps 1a and 1b, Haiku 5.5 for the other stages of this path.
6. It calls the AI "closed book": no tools, no settings files, no memory, from an empty temporary folder. The prompt is all it sees.
7. It writes the call's cost, time, tokens and requested model into the run's audit log.
8. It cuts the answer into files and writes each one into the artifacts folder, as written.
9. If the answer cannot be read, or holds no file, or misses a file, the stage is retried once, with the error and the previous answer added. A second failure stops the run. One known glitch of the AI library is retried once with the prompt unchanged.
10. Every data file the conductor writes, or reads back, is compared with a schema (a description of the file's expected shape) of the same name when one exists. A mismatch is logged, not blocked.

Example: run_102's step 1a was one call and one turn; it wrote the hypothesis card that stop 07 reads.

**What it costs and how long it takes.**
run_102: 10 AI calls, 8.25 USD, 548 seconds of AI time (`runs/run_102/pipeline_state.yaml`, audit_log, summed with a read-only script).
Step 1a: 0.41 USD, 65 s (Sonnet). Step 1b: 0.45 USD, 32 s (Sonnet). Step 2: 0.88 USD, 89 s (Haiku).
Analyst: 7 calls, 6.50 USD, over two readings (the first was rejected by hand and rerun).
Tool stages, including the backtests, write no line in the audit log: their time is not recorded there.

**What is switched off or not used here.**
- A second AI engine (Gemini) has a worker, but no handoff names it.
- Skills are mapped for four stages not reached under the current switches: validation, backtest engineering, verdict interpreter; and campaign review, reached only by its cadence.
- A context-size check and the per-stage "required outputs" lists are commented out.
- The model actually observed is recorded as empty on run_102's three stage calls.
- The analyst's audit lines are still named after the deleted "specialist readers" stage.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Stage list | `run_phase1_research.py:155-256` | `STAGE_CONFIGS`, 12 entries: handoff, `default_next`, `skill` |
| Skill map | `run_phase1_research.py:1017-1027` | 7 stage → skill folder pairs |
| Prompt builder | `run_phase1_research.py:1030-1132` | Skill + handoff + inputs (`:1056-1081`) + answer rules (`:1088-1120`) + retry text (`:1122-1130`) |
| Input text filter | `run_phase1_research.py:4386-4392` | Only the criterion menu is filtered |
| B7 mandatory inputs | `run_phase1_research.py:3092-3116` | Stages that get a fixed input set and a deference sentence |
| Closed-book inputs | `run_phase1_research.py:3255` | Files the skills say to read |
| Default model | `run_phase1_research.py:1135-1140` | `claude-haiku-5-5` |
| Stage model | `run_phase1_research.py:1143-1167` | `orchestrator.stage_models`, else default |
| Closed-book options | `run_phase1_research.py:1170-1255` | No tools, no settings, no MCP, no auto-memory, neutral cwd |
| Token record | `run_phase1_research.py:1257` | Tokens and weighted units |
| AI worker | `run_phase1_research.py:1425-1560` | Call (`:1454-1469`), audit line (`:1493-1524`), deliverables written with `open()` (`:1527-1560`) |
| Deliverable parser | `run_phase1_research.py:1410-1422` | YAML blocks headed by file names |
| Retry wrapper | `run_phase1_research.py:862-929` | SDK glitch retry; one YAML retry; one missing-deliverable retry |
| Engine choice and inputs | `run_phase1_research.py:9671-9747` | Tool stages (`:9672-9680`); handoff load; 18 in-memory input and clean-up steps (`:9693-9737`); `assigned_engine` (`:9740-9747`) |
| Gemini worker | `run_phase1_research.py:1576` | No template sets `assigned_engine: gemini` |
| Tool worker | `run_phase1_research.py:1813` | Stops 16-18 |
| Read and write | `run_phase1_research.py:518-548` | `load_yaml` (repair, read-side check), `save_yaml` (write-side check, atomic) |
| Schema check | `tools/workflow_artifact_validation.py:102-130` | By file stem; warn, raise only under `WORKFLOW_ARTIFACT_VALIDATION=raise`; 28 schema files |
| Engines in templates | `workflow_artifacts/templates/handoffs/*.yaml` | `claude`, `tool`, `tool_only` |
| Cost example | `runs/run_102/pipeline_state.yaml` (`audit_log`) | 10 entries; keys per stage attempt, `_retry` suffix |

Remarks? Mark a remark "direct" for an answer before the next stop; say "next" to continue.

## Operator remarks (verbatim, with the guide's direct answers)

Speech 5a. Is the closed book option the good approach ? Wouln't it be better (if feasible) to grant it only access read to relevant files ? 

Also Again legacy code not used is there. 

## Inspector notes

### (1) Design and mechanism

1. The closed-book call is the one part of this element that directly serves "without fooling ourselves": `_stage_agent_options` (`RP:1237-1244`) removes every tool, settings file, MCP server and auto-memory, and runs from a neutral temp cwd, so an AI stage can read only what the prompt pastes (`RP:1059-1067`). Verified against the options dict, not the docstring. For the goal, this is sound: a stage cannot peek at a backtest result, the holdout, or another run. The price is that everything a stage needs must be a pasted file, which is why `async_invoke_agent` carries 18 input-mutation helpers (`RP:9693-9737`) and why the register at stop 03 has so many flags: each helper is a flag or a stage-specific patch on the prompt. The mechanism is right; its growth pattern (one helper per incident) is what makes it hard to read.
2. The registry is not the run's itinerary. `STAGE_CONFIGS` (`RP:156-256`) gives three stages a `default_next` the live run never takes (`innovation_expansion → validation :181`, `protocol_execution → verdict_interpreter :214`, `hypothesis_generation → innovation_expansion :160`); `async_invoke_agent` decides tool-vs-AI from a flag, not from the registry (`RP:9672-9680`); `_SKILL_MAP` (`:1019-1027`) is a second copy of the registry's `skill` keys (every value equal; the docstring at `:1041-1045` justifies it by a stage D-198 deleted). A new joiner reading the registry learns the flag-off pipeline (stop 00 note 1.3, stop 03a note 1.1). Not a defect in what runs; a defect in what the code says it runs.
3. The budget breaker measures the wrong thing for the live run. Weighted units (`_weighted_token_units`, `RP:947-953`: output 5, cache write 1.25, cache read 0.1) approximate dollars, fine. But run_102's `audit_log` sums to about 1.53 M of the 1.8 M budget (`pipeline_state.yaml:40-282`, summed by hand from the ten `weighted` values), of which 1.20 M is the analyst's seven calls and only 0.33 M the three stage calls. The breaker is checked at loop top before each stage (`RP:19804-19820`), never inside the analyst stage's lens calls, and `regroup_record` is exempt (`:19813`). So on the live path it can only ever fire before `analyst` (after 1a/1b/2, ~0.33 M, never) or never: a run cannot exceed its budget on the stages the breaker guards, and the stage that spends 79% of the money (stop 00 note 1.6) is guarded by its own caps (`RP:4699`, stop 21). The 1.8 M number is tuned to the analyst's cost, not to a runaway stage. A fact for stop 21b, and a lead: the breaker and the analyst caps are two budgets for one run.
4. The audit record is complete for AI calls and absent for everything else (speech section 5 says so): the three tool stages, the claim-measurement, the profit bars and the fold confirmation leave no cost or time line. The `tools/` side of a run (backtests of 4 variants over 6 windows) is the slowest step and has no figure in the run's own record. Lead for stop 18: where, if anywhere, the backtest's wall time is written.
5. The schema check cannot stop a run and leaves no trace in it. `validate_workflow_artifact` (`workflow_artifact_validation.py:102-134`) logs through `logger.warning`; no `logging.basicConfig`/`getLogger` exists in `workflow/` (grep: none), so the warning goes to Python's last-resort stderr handler, not into `pipeline_state.yaml` or any run file. A file that violates its schema is written, used by the next stage, and the only evidence is a console line. Under `WORKFLOW_ARTIFACT_VALIDATION=raise` (`:36-37`) it would block, but no runner sets it (grep over `RC`: none). So "a schema is a checked contract" (`SR/CLAUDE.md:30-31`) means "a contract whose breach is printed once". For the goal this is acceptable only because the readers that matter re-check their own inputs in code (stop 19's `validate_verdict_provenance`, stop 10's manifest check).
6. The prompt is the handoff file dumped whole (`RP:1094`): every `reason` string, `constraints`, `notes_for_orchestrator`, `stop_conditions` (1b template `:41-47`) and `injected_context` are model-visible text. The code comment at `RP:19986-19988` says nothing reads `injected_context.refinement_attempt` and `human_data_paths_injected`; the model reads them as text on every call, and `refinement_attempt` names a counter of the unreached refine loop (stop 00 note 1.5). Harmless, but the handoff is doing two jobs (orchestrator contract and prompt) and the second has no editor.
7. The retry wrapper (`RP:862-929`) is bounded and sound: one SDK-glitch retry with the prompt unchanged, one YAML retry with the error appended, one missing-deliverable retry; each retry is a second paid call under its own audit key (`:1503`, `_retry`). A second failure stops the run `failed`. For 1a, a missing card is also the multi-card/exhausted-brief signal (`:908-916`), so that stage's retry is narrower. The manual-recovery skip (`_skip_agent`, `RP:20001-20022`) exists only for `campaign_review` and `verdict_interpreter`: a 1a/1b/2 run resumed after a hand-fixed file still pays the call again. Minor for cost (0.4-0.9 USD), but the skip is on the two stages the live path does not reach.
8. Deliverables land only in `artifacts/` (`_DELIVERABLE_BLOCK_RE :1392-1393` and `:1401-1407` accept a bare name or the one `artifacts/` prefix, no other path), written with plain `open()` (`:1552`), not the atomic write `save_yaml` uses. A crash between two deliverables of one answer leaves a partial set; the next entry's `ensure_files` catches a missing file, not a truncated one. Low probability; noted because the loop's resume promise (05b) rests on the state file being atomic, which it is (`:535-548`).
9. Model choice per stage (`_stage_model :1143-1167`, config `:878-893`) is read from the YAML on every call, and the provenance block records requested vs observed (`:1521-1523`, run_102 `:54-60`). Sound. `result_models` lists `claude-haiku-4-5-20251001` beside the requested model on every call (`:59`, `:79`, `:99`): the CLI's helper model, informational (`:1281-1284`). Fine, but a reader of the audit log sees two models per call and no key says which did the work; the `observed_models` list is the one that does.

### (2) Legacy or simplifiable (leads)

1. `run_gemini_worker` (`RP:1576`) and the module-level `from google import genai` / `from google.genai import types` (`RP:62-63`): no template or loop-written handoff sets `assigned_engine: gemini` (grep over `templates/handoffs/`: values `claude`, `tool`, `tool_only`; `_config_direct_handoff_doc :9992` writes `tool`). The orchestrator imports a second vendor SDK for a path nothing takes. Not checked: whether a test pins the Gemini worker.
2. `_SKILL_MAP` (`:1019-1027`) duplicates `STAGE_CONFIGS[*]["skill"]` entry for entry; `_build_stage_prompt`'s `skill_file_name` parameter (`:1032`, `:1041-1047`) exists for the deleted readers stage and has no live caller passing it (the only call site is `run_claude_worker :1436`). Not checked: tests calling `_build_stage_prompt` with the kwarg.
3. `check_context_limits` (`:1005-1015`, commented) and `estimate_tokens` (`:1001-1003`): the latter's only consumer is the "manual estimator path" key `total_estimated_tokens` (`:977`), which no live writer produces (grep in `RP`: the one read). `required_outputs` commented out in three registry entries (`:159`, `:177-180`, `:186-189`). Dead text in the registry.
4. The B7 mandatory inputs (`_B7_MANDATORY_INPUT_PATHS :3088-3091`): `artifacts/user_brief_verbatim.yaml` is written by `RC:1163` on the refinement-brief path only (`:1065-1113`), refused under retired routing (stop 04); run_102 has no such file (artifacts listing). Four of the five B7 stages (`:3092-3108`) are unreached; the live member is `strategy_config_authoring`, which receives `pre_registration.yaml` and the deference sentence (`:3109-3113`) naming a file that never exists on this path.
5. `_CLOSED_BOOK_STAGE_INPUTS` (`:3167-3214`): entries for `validation`, `backtest_specification` (an AI stage only with config-direct off), `verdict_interpreter` and `campaign_review`; the live entries are `innovation_expansion` (coin universe) and `strategy_config_authoring` (quant fundamentals). `_write_trade_diagnostics_summary` (`:3234-3252`, `:3263-3264`) serves the verdict interpreter only.
6. Of the 27 `.schema.json` files (`workflow_artifacts/schemas/`), by name at least 13 describe files of unreached paths or no path: `handoff` (plus a duplicate `.yaml`), `holdout_result`, `human_resolution`, `refinement_notes`, `regime_detector_report`, `validation_decision`, `validation_protocol`, `promotion_audit`, `verdict_interpretation`, `regime_audit_decision`, `variants_not_pursued`, `variant_selection`, `indicator_library` (a config, not an artifact). Which have a live writer is the post-tour search; stop 05b note 2.1 for the handoff one.
7. `_stage_model` and the flag readers re-parse `campaign_config.yaml` on every call (`_orchestrator_config`, stop 03a note 1.3); one parse per run would do.
8. The audit key for the analyst is built elsewhere with the prefix `specialist_readers_` (run_102 `:101`); stop 00 lead 2.10, confirmed as a key-builder leftover, builder not yet located (stop 21).

### (3) Disagreements between the speech and the element

1. Section 6: "The model actually observed is recorded as empty on run_102's three stage calls." The file disagrees: each of the three stage entries carries `provenance.observed_models` with the requested model (`pipeline_state.yaml:56-57`, `:76-77`, `:96-97`); what is absent is the analyst entries' `provenance` block (they carry `models:` instead, `:125-126`). The statement is wrong as written.
2. Step 3: "These additions exist only in memory; the handoff file on disk stays the copied template." Half right: the 18 helpers in `async_invoke_agent` (`:9693-9737`) are in memory, but `run_loop` writes `run_id` and `injected_context` into the on-disk handoff before every stage (`RP:19980-19997`); run_102's `handoffs/research_brief_to_hypothesis.yaml:1`, `:28-31` show both. The template's `run_id: "template"` is overwritten.
3. Step 10: "compared with a schema ... when one exists. A mismatch is logged, not blocked." Right, with the omission in note 1.5: logged to stderr only, no run-file trace, and no runner sets the raise mode.
4. Reading map "Skill map ... 7 stage → skill folder pairs": correct count; the speech does not say the map equals the registry's own `skill` keys (note 2.2).
5. Reading map "Default model `run_phase1_research.py:1135-1140`": the constant is at `:1140`; range fine. "Stage model `:1143-1167`": correct.
6. Section 5 figures: 10 audit entries, 8.25 USD (sum of the ten `cost_usd` values: 0.41+0.45+0.88+1.08+0.78+1.05+0.95+0.72+1.15+0.77 = 8.24, rounding), 1a 0.41/65 s, 1b 0.45/32 s, step 2 0.88/89 s: match the file. "Analyst: 7 calls, 6.50 USD": 1.08+0.78+1.05+0.95+0.72+1.15+0.77 = 6.50. Correct.
7. Section 6 "Skills are mapped for four stages not reached": `validation`, `backtest_specification`, `verdict_interpreter`, `campaign_review` (`:1023-1026`); correct under the live flags (5a is a tool stage, `:9676-9677`).
8. Step 9 "One known glitch of the AI library is retried once with the prompt unchanged": `RP:882-886`, correct. Step 9 omits that the missing-deliverable retry is skipped for 1a when some deliverables were saved (`:915-916`), by design.
9. Verified as stated: `RP:155-256`, `:1017-1027`, `:1030-1132` (`:1056-1081`, `:1088-1120`, `:1122-1130`), `:4386-4392`, `:3092-3116`, `:3255`, `:1170-1255`, `:1257`, `:1425-1560` (`:1454-1469`, `:1493-1524`, `:1527-1560`), `:1410-1422`, `:862-929`, `:9671-9747` (`:9672-9680`, `:9693-9737`, `:9740-9747`), `:1576`, `:518-548`; `workflow_artifact_validation.py:102-130`; 9 templates; `assigned_engine` values; 27 `.schema.json` plus `handoff.schema.yaml` (28 files).
