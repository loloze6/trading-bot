# Stop 05b: The orchestrator core, part b: the loop, the routes, the handoffs, the file checks

## Speech (verbatim)

**Stop 05 of 29, part b: the loop, the routes, the handoffs and the file checks.** Open on the side: `run_phase1_research.py`, `workflow_artifacts/templates/handoffs/`, `workflow_artifacts/schemas/`, run_102's `pipeline_state.yaml`, `artifacts/run_context.yaml`, `protocols/run_102_generated.json`.

**In one sentence.**
The loop is the run's itinerary: it does the stage the run is waiting on, picks the next stage, writes that down, and repeats until the run reaches an ending.

**Why it exists.**
A run must be able to stop at any point (a crash, a pause for a person, a budget limit) and resume exactly where it was, without redoing paid work.
So after every stage the loop writes the next stage into the run's state file before doing anything else. The state file, not memory, says where the run is.
It also stops a run that spends too much, so one runaway step cannot drain the budget.

**What comes in, what goes out.**
- In: the run folder prepared at launch (brief, pre-registration (the criteria and test settings fixed before any result), state file, copied handoffs (the per-stage instruction files)).
- Out: the run's test protocol (the list of test windows), every stage's files, and the state file updated after each stage, ending at one of the endings.
- Next: the launcher reads the ending (stops 23-24).

Example: run_102's protocol holds BTC on hourly bars, Kraken perp priced on Kraken spot with funding not charged, and 6 windows: fold B (a fixed set of six 4-month test blocks across 2018-2021).

**What happens here, step by step.**
1. At the start, the loop turns the pre-registration's test settings into the run's protocol file, and notes the fold in a small run-context file. It never rebuilds an existing one.
2. It re-checks the switches the run depends on. A problem marks the run "failed" before any spend.
3. It reads the stage the run is waiting on. An ending ("completed", "rejected", a pause for a person, a failed validation) stops the loop.
4. Budget check: it adds up the weighted tokens of every AI call so far. Above 1.8 million the run ends "rejected, budget exceeded", except at the record-keeping stage, which makes no AI call.
5. It counts one more attempt for this stage and marks the run "running".
6. It does the stage: an AI call (stop 05a), a Python tool, the analyst, or the record-keeping.
7. It picks the next stage. It starts from the stage's usual successor, then the switches override it. Under today's switches the chain is: hypothesis (1a) → base config (1b, with its checks) → variants (step 2, with its checks) → variant building (5a) → data check → backtests → analyst → record-keeping → then three checks in order: did any variant pass the profit bars (a pause for the operator), is a holdout decision waiting, and finally the route from the pass/fail grid, which ends the run as "completed" with the grid's verdict: validated, refuted or inconclusive.
8. Right after the backtests, three more things run before moving on: the profit-bars check of every variant, the measurement of the idea's claim, and its confirmation on the run's fold.
9. A step that cannot go on either pauses for a person, or parks the run while a missing component or missing data is provided (stop 23).
10. It writes the finished stage into the completed list and the next stage as pending, then loops.
11. Any error stops the run as "failed", with the error saved in the state file.

The handoffs. At launch, 9 instruction templates are copied into the run. Five more are written by the loop during the run, the first time their stage starts: one each for variant building, the data check and the backtests in this config-first flow, one for the analyst, one for the record-keeping. The AI stages read theirs from the run folder (stop 05a).

The file checks. A file the code writes is compared with its schema (its expected shape) as it is written. A file the AI writes is saved as raw text and compared only when the code reads it back. A mismatch is logged, never blocked.

**What it costs and how long it takes.**
The loop itself costs nothing; its stages cost what stop 05a listed.
run_102: 10 stage entries (8 stages, with the analyst and the record-keeping done twice), `stage_attempts` in `runs/run_102/pipeline_state.yaml`.
Token budget per run: 1,800,000 weighted units (`campaign_config.yaml:92`).

**What is switched off or not used here.**
- The usual successors written in the stage list follow the old order (step 2 → validation, backtests → verdict interpreter); today the switches override them at every step.
- Validation, the verdict interpreter and the old routes after them are not reached; the verdict-interpreter branch stays in the loop.
- A run state left at the deleted "specialist readers" stage is resumed into the analyst or the route.
- The handoff schema matches no run handoff by file name, so no handoff is checked.
- Of the 9 copied templates, 4 serve stages a run does not reach today (validation, the old backtest and verdict hand-offs), 2 are reached only by the review cadence or a holdout unlock, and 3 are used (1a, 1b, step 2). The data-check template name in the stage list is not among the 9.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| The loop | `run_phase1_research.py:19626-20713` | `run_loop(run_id, after_1a=None)` |
| Protocol from pre-registration | `run_phase1_research.py:19648-19670` → `:10649-10729` | Generated protocol and `run_context.yaml`; pinned protocol `_ensure_protocol_ref_pinned` |
| Run start re-check | `run_phase1_research.py:19672-19766` | Stop 03a |
| Ending check | `run_phase1_research.py:19768-19774` | `completed`, `rejected`, `human_pause`, `failed_validation` |
| Deleted stage resume | `run_phase1_research.py:19776-19800`; `:5376` | `specialist_readers` resumes into analyst / regroup / route |
| Budget breaker | `run_phase1_research.py:19804-19820`; `:956`; `:983-998` | Weighted units vs `token_budget_per_run_weighted_units` |
| Stage-specific entry branches | `run_phase1_research.py:19832-19945` | Analyst, regroup, holdout, campaign review |
| Attempt count | `run_phase1_research.py:19947-19964` | `stage_attempts`, status `running` |
| Doing the stage | `run_phase1_research.py:19966-20150` | Analyst `:20070`, regroup `:20074`, 1b/2 composition and exact paths `:20079-20086`, AI stages via the retry wrapper `:20087-20135` |
| Routing chain | `run_phase1_research.py:20153-20675` | `default_next` (`:20153`), 1a→1b (`:20160-20161`), brief exhausted / no new idea (`:20163-20166`), backtests→analyst (`:20177-20184`), analyst→regroup (`:20185-20187`), validation (`:20189`), 1b route (`:20205-20218`), step 2 route (`:20225-20244`), 5a route (`:20246-20256`), legacy 5a (`:20257-20327`), data gate with variant loop (`:20329-20397`), legacy gate (`:20399-20451`), backtests with variant loop (`:20453-20520`), legacy backtests (`:20522-20553`), verdict interpreter (`:20555-20574`), regroup → bars stop, holdout unlock, refold, grid route, review (`:20576-20611`), campaign review (`:20613-20624`), holdout (`:20626-20632`) |
| After the backtests | `run_phase1_research.py:20640-20653` | Profit bars on every backtest; claim measurement; fold confirmation |
| Grid route now | `run_phase1_research.py:20176`, `:20660-20675` | Entry checks, then `determine_post_specialist_readers_route` (`:5403`) |
| Record and loop | `run_phase1_research.py:20677-20701` | `completed_stages`, `pending_stage`, `after_1a` hook |
| Errors | `run_phase1_research.py:20703-20713` | Budget terminated; any other error `failed` |
| Endings | `run_phase1_research.py:5683-5684`; `:5218` | `completed_validated|refuted|inconclusive`; `completed_refold` |
| Templates | `workflow_artifacts/templates/handoffs/` | 9 files copied at launch |
| Config-direct handoffs | `run_phase1_research.py:9958-9963`, `:9975-10060` | 5a, data gate, backtests (and verdict interpreter) written once per run |
| Analyst handoff | `run_phase1_research.py:4538-4546` | `protocol_to_analyst.yaml` |
| Regroup handoff | `run_phase1_research.py:5485`, `:8834-8838` | `specialist_readers_to_regroup_record.yaml` |
| Data gate entry | `run_phase1_research.py:208-211` | Names `backtest_spec_to_data_availability_gate.yaml`, not a template |
| Handoff schema | `workflow_artifacts/schemas/handoff.schema.json` (and `.yaml`) | Stem `handoff`; no run handoff has that stem |
| Schemas | `workflow_artifacts/schemas/` | 27 `.schema.json` files read by the check (plus one `.yaml`) |
| Write-time check | `run_phase1_research.py:535-548` | Every `save_yaml` write |
| Read-time check | `run_phase1_research.py:518-532` | Every `load_yaml` read, so AI files are checked when read back |
| AI files written raw | `run_phase1_research.py:1552` | `open()`, no check at write |
| Examples | `runs/run_102/pipeline_state.yaml:5-15`, `:31-39`; `runs/run_102/artifacts/run_context.yaml`; `protocols/run_102_generated.json`; `runs/run_102/handoffs/` (14 files) | The live path, attempts, fold B, the protocol |

Remarks: send them as "stop 05b: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Speech 5b
Direct: "turns the pre-registration's test settings into the run's protocol file" here only if there is pre-registration test, right ? If the claim is to be decided, this step is skipped ? 

Direct answer: The protocol file is built from the pre-registration's test settings (coins, bar size, fold or dates), not from the claim or the criteria. Two cases:
- **Test settings present** (every brief that carries `machine_constraints`, the template's normal case): the protocol is built at run start, whether the criteria are given by the brief or left to step 1a. A brief that leaves the criteria to step 1a still gets a pre-registration at launch, with its pass rule empty and marked pending, and its test settings filled (`run_campaign.py:795-855`). The loop reads those settings (`run_phase1_research.py:19648-19670`, `_load_machine_constraints` `:10395-10400`) and builds the protocol (`:10649-10729`). So "the claim is to be decided" does not skip this step: the claim and the criteria are written later by step 1a; the test months are already fixed.
- **No test settings in the brief:** no pre-registration file is written (`run_campaign.py:795-798`), `_load_machine_constraints` returns nothing (`:10397-10398`), and no protocol is built at this point (`:10666-10668`). The protocol is then looked for later, when a stage needs it, through a run-context file or a campaign-wide fallback; with neither, it raises "[B10] No run_context.yaml override and no machine_constraints.protocol_ref ..." (`tools/protocol_resolution.py:303-322`). Every brief in the tour carries test settings.

Once the switchboard cleaned (my remark on speech around switchboard) i would prefer expect that there is no "wrong" combination anymore 

On the steps, i would expect that each and every control around an objective (eg: data check) is located at the step, or reusing the step logic - no duplicate. 

I would challenge the check around holdout decision waiting, that i am discovering.

Direct: Can you confirm that step7 "three checks part" check 1 around profit bars , check 3 arounf route from the grid are the same than step 8 point 1 and point 2. I do not get difference between 8.2 and 8.3

Direct answer: They are not the same; each pair is two halves of one job, done at two moments.
- **7.1 and 8.1, the profit bars.** 8.1 is the grading: right after the backtests, every variant is graded against the campaign's profit bars and the result is written to `profit_bars_evaluation.yaml`; it never pauses (`run_phase1_research.py:20640-20642` → `_evaluate_profit_bars_every_backtest` `:15413-15419`: "Never pauses: the profit_bars_reached stop is raised later"). 7.1 is the decision on that grade: after the record-keeping step, if a variant passed every bar, the run pauses for the operator (`_profit_bars_stop_route`, `:15570-15580`, called at `:20584-20585`). Same evaluation, written once, read once.
- **7.3 is not 8.2.** 7.3, the route from the grid, reads `idea_status.yaml` (validated, refuted, inconclusive), which the grid wrote during the backtest step (`:2439-2499`), and ends the run with that status (`:20600`). 8.2 is the claim measurement: it measures the effect sizes of the run's own claim tests on each graded variant's bars, "measured, not proven", information only (`_measure_claim_tests_after_backtests`, `:18437`, called at `:20648`). It does not touch the status.
- **8.2 versus 8.3.** Both measure a claim, but not the same one and not for the same purpose:
  - 8.2 measures **this run's own claim** (the one on its hypothesis card) on **every graded variant**, and writes effect sizes only, with no verdict (`claim_measurement.yaml`, per-variant `claim_test.yaml`).
  - 8.3, fold confirmation, takes **the claim of the earlier run this run was built from** (a decide-next child), measures it on **this run's fold** (test months the claim was not found on), and grades it with a rule: confirmed, not confirmed or not measurable (`_confirm_on_fold_after_backtests`, `:18591-18600`; it does nothing unless the folds switch is on and the run was built from a side finding). It writes `fold_confirmation.yaml` and one row in `campaign_record/confirmations.yaml`.
  - For run_102 the two happen to measure the same claim text, because its claim was pre-filled from run_101's: 8.2 wrote "measured" on 4 variants; 8.3 wrote `not_confirmed` on fold B.
- **7.2, the holdout decision**, is only reached when 7.1 raised its stop on an earlier pass: without that stop, any `holdout_decision.yaml` is ignored and the route goes on (`_holdout_unlock_route`, `:7515-7535`).

And again some legacy. 

--- 
Consider these remarks and direct ones and i will go to comment step 6 after.

5b. So i get that 8.1 measures, 7,1 -located at the very end- stop the run loop in case 7.1 measurements are passing the profit bars. Let me know otherwise. Do not get why these steps are not one still. 

I get also that 8.1 is basically branch 1 around claim's verification on pass/fail. 
8.2 is concerning because i do not get the business objective of it . 

8.3 as well, because the previous claim already had a pass/fail decision. Here it means we are reopening the claim to test it on a new fold. I do not get why. 

Stop 6 review will be next

Guide's answer (the remark asks "let me know otherwise"; facts from the files):
- **8.1 then 7.1.** Correct: 8.1 grades every variant against the profit bars, 7.1 pauses the run if any variant passed every bar. 7.1 is not at the very end: it runs after the record-keeping step and before the grid's route, which ends the run. The code says why it waits until then: "after regroup_record (so the memory already holds the per-variant results)" (`run_phase1_research.py:15571-15573`).
- **8.1 is branch 3, not branch 1.** 8.1 grades profit (the campaign-wide profit bars), not the claim. Branch 1, the pass/fail on the idea, is the grid on the pre-registered criteria: computed during the backtest step (`:2439-2499`) and read at 7.3.
- **The claim never gets a pass/fail in its own run.** The run's pass/fail comes from the criteria (the grid), not from the claim. The claim measurement (8.2) is information only: "effect sizes only, no p-value: the number is shown, the claim is not graded; information only, it never changes idea_status" (`tools/claim_measure.py:55-58`); the claim verdict path is parked (D-077, `tools/claim_tests.py:15-26`).
- **8.3 is therefore the first grade the claim receives,** on test months it was not found on: "an idea is never confirmed on the bars where it was observed" (`config/folds.yaml:3-7`); the confirmation row is "measured on the run built from the claim, on a fold its source run was not on; not proven" (`runs/run_102/artifacts/fold_confirmation.yaml`, `rule.text`).

## Inspector notes

### (1) Design and mechanism

1. The resume promise holds: after every stage the loop writes `completed_stages`, `current_stage`, `pending_stage` and `status` in one atomic state write (`RP:20684-20690`, `save_yaml :535-548`), and a crash anywhere in the stage body lands in `failed` with `last_error` (`:20710-20713`). The state file, not memory, is the itinerary (`:19768-19774`). This is the part of the orchestrator that lets the campaign run unattended across crashes; it is sound. Its one soft spot is noted by the code itself: an empty-but-present state file crashes `update_state` (`:609-625`) and leaves the queue line `in_progress`.
2. The live route is written as overrides on a flag-off chain, and the chain is read in two passes. Pass one (`:20153-20187`) sets `next_stage` from `default_next` and the 1a/backtests/analyst overrides; pass two (`:20189-20631`) is a 440-line `if/elif` keyed on the stage, in which the live run takes six branches (`:20205`, `:20225`, `:20246`, `:20329`, `:20453`, `:20576`) and skips eight (`validation :20189`, legacy 5a `:20257-20327`, legacy gate `:20399-20451`, legacy backtests `:20522-20553`, `verdict_interpreter :20555-20574`, the two `campaign_review` branches, `holdout_evaluation :20626`). For `protocol_execution` the two passes both fire (`:20177` sets `analyst`, `:20453` may override to `human_pause`). The run_102 order (1a → 1b → 2 → 5a → gate → backtests → analyst → regroup → `completed_refuted`) exists nowhere as a list; it is the residue of flags over a diagram no run takes. The consequence for autonomy: a change to the route is a change in a 1,090-line function whose tests pin both shapes; stop 28 should say what folding the flags would delete here.
3. The regroup branch is the real end-of-run decision and its order is right for the goal: profit-bars stop (a pass on every bar pauses for the operator) → holdout unlock (only if the operator answered) → refold terminal → grid route to `completed_<idea_status>` → review cadence (`:20583-20611`). Under `verdict_routing_retired`, `inconclusive` no longer pauses (`_route_retired_idea_status :6649-6666`), so a run with an undecidable grid ends `completed_inconclusive` and decide-next treats it like any other result. Whether decide-next discounts an inconclusive parent is stop 24's question; here the fact is that the loop makes no distinction between "refuted" and "could not tell".
4. Three run endings are second-class. `completed_brief_exhausted` and `completed_no_new_hypothesis` (`:8588`, `:8590`, set at `:20163-20166`) and the data gate's `completed_rejected` (`:20451`, legacy branch only) are not in `RETIRED_ROUTING_TERMINALS` (`:5683-5684`), so the state write at `:20685-20686` leaves `status: active` for the first two (`rejected` for the third) with a `completed_*` pending stage. The launcher must know these shapes separately (stop 23). A run ending at 1a (no new idea) records no memory entry and no grid: a correct refusal to spend, but invisible to `campaign_memory.yaml` (stop 22), so decide-next cannot learn that the brief is exhausted from memory, only from the queue (stop 02 note 1.6).
5. The budget breaker (`:19804-19820`) is checked at the top of each stage, with `regroup_record` exempt; on the live path it can only ever stop a run before `analyst` (stop 05a note 1.3), and after a hand `retry-analyst` the run's audit log already holds two analyst passes (run_102: 1.53 M of 1.8 M). A third pass would push the sum over budget; what the retry command does with that is stop 21b's question (the itinerary names `RC:2692` as an enforcement site).
6. Protocol generation (`:19648-19670` → `_ensure_protocol_from_constraints :10649-10729`) runs before any flag pre-flight and before 1a, and is idempotent on two files existing together (`:10675-10676`): the protocol in the shared `SR/protocols/` directory and `run_context.yaml` in the run. The run's test windows therefore live outside the run folder; a run folder backed up alone (SR/CLAUDE.md `:118`) loses its protocol. The validation guard (`:10709` → `:10641-10646` → `:10583-10604`) and the holdout guard (`:10637`, `:10569`) both run here, before the first paid call: the "no window touches a forbidden period" promise of stop 04 is kept at this line, not in the launcher's pre-flight (stop 04 note 3.1).
7. Run-start re-check (`:19672-19766`): seven readers, each failing the run `failed` before spend if a dependency is unmet. Sound, and the one place a run records (by not failing) that its flags were consistent. The parked-marker check (`:19758-19766`) is the only guard against a hand restart of a parked run; it depends on `_vrr_flag`.
8. The handoffs on the live path are five of nine copied templates unused (speech section 6) plus five loop-written files. The loop-written ones are rebuilt from the flags at every entry (`_config_direct_handoff_path(..., rebuild=True) :19830`, `:10057-10059`), so the on-disk handoff for 5a/gate/backtests is a flag snapshot, while the three AI handoffs keep the copied template plus `run_id` and `injected_context` (`:19980-19997`). Two shapes of "handoff" under one folder; the AI ones are prompts, the tool ones are records.
9. The schema story (speech "The file checks") is right in mechanism and weak in effect: write-time checks cover the code-written files whose stems have a schema (grid, idea_status, protocol_result, memory, registry, decision_record...), read-time checks cover the AI files when `load_yaml` reads them back (`:518-533`), and both only warn to stderr (05a note 1.5). `pipeline_state.yaml` has no schema; `variants/index.yaml` (stem `index`) has none; the handoffs have one that matches no stem (note 2.1). So the file the loop depends on most is unchecked.

### (2) Legacy or simplifiable (leads)

1. `handoff.schema.json` (and its `.yaml` twin): applied to nothing by stem, and would reject every handoff if it were: `assigned_engine` enum is `claude|gemini` (`:57-60`) while six templates and all loop-written handoffs use `tool`/`tool_only`; `additionalProperties: false` (`:62`) forbids `handoff_version`, `notes_for_orchestrator`, `stop_conditions`, `config_direct_authoring`, `per_variant_outputs`, all present (1b template `:1`, `:41-47`; `_config_direct_handoff_doc :9992-9993`, `:10023`); `primary_input_artifact` is required (`:10`) and the loop-written handoffs have none. Grep: `primary_input_artifact` appears in `RP` once (`:7841`, campaign review) and in no reader. Delete both files.
2. Templates copied for stages the run never reaches (`innovation_expansion_to_validation`, `validation_to_backtest_specification`, `backtest_spec_to_protocol_execution`, `protocol_to_verdict_interpreter`; `campaign_review` and `holdout_evaluation` reachable only by cadence/unlock): copied into every run by `setup_run.py:115-118`. The registry entry for the data gate names `backtest_spec_to_data_availability_gate.yaml` (`:209`), a file that exists nowhere (the loop writes `config_direct_data_availability_gate.yaml` instead); harmless because `_config_direct_handoff_path` overrides it (`:19830`), but a flag-off run would crash at `load_yaml` on that path. Not checked whether a test covers the flag-off gate.
3. `_resume_stage_after_readers_deleted` and `LEGACY_READERS_STAGE` (`:5376`, `:5389-5400`, `:19776-19802`): a resume path for state files written before D-198, and also the sentinel used for a route-only resume at `:20673-20674`. The second use keeps it alive even once no pre-D-198 run remains; a named sentinel (`route_only`) would free the deleted stage's name.
4. The `verdict_interpreter` entry branch (`:19972-19977`, `:20013-20049`) and route (`:20555-20574`), the `validation` route (`:20189-20197`), legacy 5a (`:20257-20327`, with the inline `validate_config.py` subprocess and `_create_remaining_handoffs`), legacy gate (`:20399-20451`), legacy backtests conformance (`:20522-20553`), `campaign_review` flag-off branch (`:20623-20624`), `holdout_evaluation` loop branch (`:20626-20631`), the campaign-review YAML re-check (`:20140-20150`), `_skip_agent` (`:20001-20022`): all unreached under the live flags. Stop 28 names the stages; this is the loop-side list.
5. `after_1a` (`:19626`, `:20697-20698`): `extra_cards_at_1a` off; the only caller passing non-None is the flag's path in `RC`. Not checked.
6. `injected_context.refinement_attempt` and `human_data_paths_injected` (`:19989-19994`): the first names an unreached loop's counter, the second a human-context merge whose writer (`injected_human_context`) was not located; both are dumped into every AI prompt (05a note 1.6).
7. `_config_direct_handoff_doc`'s `verdict_interpreter` branch (`:9980-9987`) and `_CONFIG_DIRECT_HANDOFFS["verdict_interpreter"]` (`:9962`): a config-direct handoff for a stage the config-direct flag set never reaches.
8. The main-guard CLI (`:20715-20724`, `run_loop`/`resume_pipeline` by run id): a second entry point beside `run_campaign.py`, which the K3/A4 comment (`:19652-19656`) says bypasses the launcher's lints. Whether the RUNBOOK still names it was not checked.

### (3) Disagreements between the speech and the element

1. Step 7 says "under today's switches the chain is: hypothesis (1a) → base config (1b, with its checks) → variants (step 2, with its checks) → variant building (5a) → data check → backtests → analyst → record-keeping → then three checks in order". Correct against `:20160-20161`, `:20205-20218`, `:20225-20244`, `:20246-20255`, `:20329-20397`, `:20453-20520`, `:20177-20179`, `:20186`, `:20583-20611`. The speech omits that `protocol_execution` passes through two branches (pass one `:20177`, pass two `:20453`), and that the refold terminal sits between the holdout check and the grid route (`:20593-20595`); the reading map does name it.
2. Step 3 lists the endings as "completed, rejected, a pause for a person, a failed validation": these are the prefixes at `:19771`; the speech does not say that `completed_brief_exhausted` and `completed_no_new_hypothesis` end with `status: active` (note 1.4). Omission.
3. Step 4: "Above 1.8 million the run ends rejected, budget exceeded, except at the record-keeping stage": correct (`:19813-19819`); the fallback budget when the config is missing is 300,000 (`:993`), not stated; fine.
4. "The handoffs ... Five more are written by the loop during the run, the first time their stage starts": for the analyst and regroup handoffs, once (`:4542-4547`, `:8834-8838`, `if not exists`); for 5a, the gate and the backtests, rewritten at every stage entry (`:19830`, `rebuild=True`, `:10057`). "The first time" is wrong for three of the five.
5. Section 6: "The data-check template name in the stage list is not among the 9": confirmed (`:209`; 9 template names listed). "A run state left at the deleted stage is resumed into the analyst or the route": also into `regroup_record` (`:5398-5399`); the reading map says so.
6. Reading map "Endings `:5683-5684`; `:5218`": correct (`REFOLD_TERMINAL = "completed_refold"`). "Schemas: 27 `.schema.json` ... plus one `.yaml`": 28 files counted, correct.
7. Example sentence ("run_102's protocol holds BTC on hourly bars, Kraken perp priced on Kraken spot with funding not charged, and 6 windows: fold B"): fold B confirmed by `run_context.yaml:3`; the protocol file itself was not opened by the inspector (it carries dates); the venue keys are written by `_generated_protocol_venue_keys` (`:10695`), stop 18.
8. Verified as stated: `RP:19626-20713`, `:19648-19670`, `:10649-10729`, `:19672-19766`, `:19768-19774`, `:19776-19800`, `:5376`, `:19804-19820`, `:956`, `:983-998`, `:19832-19945`, `:19947-19964`, `:19966-20150` (`:20070`, `:20074`, `:20079-20086`, `:20087-20135`), `:20153-20675` (every sub-range in the reading map), `:20640-20653`, `:20176`, `:20660-20675`, `:20677-20701`, `:20703-20713`, `:5683-5684`, `:5218`, `:9958-9963`, `:9975-10060`, `:4538-4546`, `:5485` not opened (`:8834-8838` read), `:208-211`, `:535-548`, `:518-532`, `:1552`; `run_102/pipeline_state.yaml:5-15`, `:31-39`; `run_context.yaml`; 14 files in `runs/run_102/handoffs/`.
