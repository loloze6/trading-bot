# Stop 04: Launch (`run_campaign.py --once`)

## Speech (verbatim)

**Stop 04 of 29: Launch.** Open on the side: `run_campaign.py`, `setup_run.py`, `campaign_lock.py`, `RUNBOOK.md`, and run_102's `artifacts/` and `handoffs/` folders.

**In one sentence.**
The launcher takes the next brief off the to-do list, opens a fresh run folder for it, writes the run's first files, checks the test period, and hands the run to the orchestrator.

**Why it exists.**
A run must start from exactly what the brief says, and nothing else.
Without a fixed start, a run could test the wrong coin, reuse another run's test windows, or quietly test on the period kept back for validation.
The launcher also refuses before spending: every check here runs before the first AI call.
And it keeps one campaign at a time, so two processes never write the same records.

**What comes in, what goes out.**
- In: the queue (stop 02), the switchboard (stop 03), and the chosen brief.
- Out: a run folder with its state file, the step instructions, the brief as a data file, the pre-registration (criteria and test settings fixed before any result is seen), and for an "open" brief, the list of ideas it already produced.
- Next: the orchestrator (stop 05) runs the stages in the same process.

Example: run_102 came from the line `trade_efficiency-run_101-1`. Its pre-registration fixed one criterion (the forecast's rank correlation with the next 24 hours' return, median above 0.02 over at least 5 windows), BTC on hourly bars, fold B. Its venue check said Kraken perp is tradable.

**What happens here, step by step.**
1. The operator starts the launcher from the research folder: one step, or a loop until nothing is left.
2. It takes the campaign lock (a small file next to the campaign state). If another campaign holds it, it refuses. A lock whose process is gone, or older than 6 hours, is cleared.
3. Each step, it lists run folders that no record refers to, and logs them. It changes nothing.
4. It reads and checks the switchboard (stop 03), and refreshes the queue health file.
5. It picks a line: one already in progress first, else the ready line with the smallest number. None: it logs "queue exhausted", names lines waiting for approval or parked, and stops.
6. It decides the action: a new launch, a saved extra idea, or continuing a run already started.
7. For a new launch, it re-reads the brief and takes the next free run number. It creates the run folder, a fresh state file, and copies of the 9 step instruction templates (the handoffs).
8. It writes the brief as a data file, adding whether the operator may legally trade that exchange and product.
9. It writes the pre-registration, after checking the criteria against the criterion menu (stop 08) and the test settings.
10. If the brief may still yield more ideas, it writes the ideas already produced from it, so step 1a does not repeat one.
11. It marks the line "in progress" and logs the launch.
12. Before any AI call, it checks the test windows the run will use: no two windows share a day, none touches the validation period (except fold D's exact blocks), and once data has been spent on a run its windows are never rebuilt.
13. It hands over to the orchestrator.
14. Any error on the way pauses the line with a named reason. A half-made run folder is kept as a record.

After the run, the same step reads how it ended (stops 23 and 24).

A dry run exists: it walks the same wiring on a throwaway run folder, spends nothing, and deletes it.

**What it costs and how long it takes.**
No AI call; the launch itself takes seconds.
9 handoff templates copied at setup; run_102's `handoffs/` holds 14 files at its end, the other 5 written by later stages (`workflow_artifacts/templates/handoffs/`, `runs/run_102/handoffs/`, listed).

**What is switched off or not used here.**
- The operator-written "refinement brief" path is refused under retired verdict routing: the launcher pauses instead of creating a child run.
- Quarantine is off, so any pause stops the whole campaign.
- Queueing step 1a's extra ideas as soon as 1a ends is off.
- The refold launch (a re-run on another fold, profit bars only) is a separate path, used only by the refold command.
- The state file's template fields (limits, counters, flags) are written at setup; stop 00 named what reads them.
- The setup writes a "TODO" brief file that the launch overwrites at once.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Command line and folder guard | `run_campaign.py:5931-5981` | `--once`, `--dry-run` and the other commands; must run inside `strategy-research/` |
| Lock | `run_campaign.py:6014-6028` | Acquire, `run_forever`, release |
| Lock file | `tools/campaign_lock.py:48`, `:68-70` | `.campaign.lock` next to `campaign_record/campaign_state.yaml` (`run_phase1_research.py:93`) |
| Staleness | `tools/campaign_lock.py:52-54`, `:127-150` | Dead pid on this host, or older than 6 h |
| Acquire / release | `tools/campaign_lock.py:171-218` | Exclusive create, clear a stale lock once, refuse otherwise |
| Loop | `run_campaign.py:5787-5791` | `process_once` until it returns False, or once |
| One step | `run_campaign.py:4497-4880` | The whole step |
| Orphan scan | `run_campaign.py:3669-3697` | Read-only; one log line |
| Flag pre-flight | `run_campaign.py:4508-4525` | Stop 03a |
| Queue health | `run_campaign.py:3605`, `:4516-4518` | Schedulability file every step |
| Pick and exhaust | `run_campaign.py:4527-4542`, `:223-235` | Select; "Queue exhausted"; flag refusal pauses |
| Action | `run_campaign.py:238-260`, `:4544` | refinement brief / fresh launch / queued card / continue |
| Refinement brief refused | `run_campaign.py:4546-4556` | Halt under retired routing |
| Queued card check | `run_campaign.py:4592-4610` | Missing card file pauses before any run dir |
| Launch | `run_campaign.py:4611-4620`, `:4392-4440` | Fresh launch at `:4410-4427`; exception pauses (`:4243`) |
| Run number | `run_campaign.py:736-757` | Next free number from `runs/` and `campaign_state.yaml` |
| Run folder | `workflow/setup_run.py:96-128` | Folders, state file, 9 templates copied, TODO brief |
| State file | `workflow/setup_run.py:47-94` | Refuses to overwrite a run with progress |
| Brief and pre-registration | `run_campaign.py:777-935` | Stop 01 part 4; venue check `:787-792`; `research_brief.yaml` `:793`; lints `:862-933`; `pre_registration.yaml` `:935` |
| Retired promotion dropped | `run_campaign.py:760-774` | Drops `protocol.promotion` before pre-registration |
| Ideas already produced | `run_campaign.py:5455-5475` | `brief_hypotheses_context.yaml`, only for a brief with an owner |
| Continue path | `run_campaign.py:4621-4640` | Legacy continuation halt; finish a park |
| Pre-flight and hand-over | `run_campaign.py:4642-4655`, `:4443-4494` | Protocol pre-flight, regeneration, `orch.run_loop(run_id)` at `:4463` |
| Protocol pre-flight | `run_campaign.py:4095-4174` | Pinned, generated or resolved protocol |
| Generated protocol plan | `run_campaign.py:3994-4092` | Spend evidence first; never rebuild after spend |
| Window checks | `run_campaign.py:3958-3991` | Shared day; validation period under folds |
| After run_loop | `run_campaign.py:4656-4880` | Children, park, pause, DONE (stops 23-24) |
| Dry run | `run_campaign.py:5837-5926` | Sandbox run, no spend |
| Runbook pre-flight | `RUNBOOK.md:65-127` (§0b) | Four gates, open PRs, brief check, dry-run warnings, closed-book check |
| Runbook dry run | `RUNBOOK.md:130-143` (§1a) | Command and expected last line |
| Runbook new pipeline | `RUNBOOK.md:269-469` (§1e) | Flag set, register, bars file signed, dry run, first-run checks |
| Runbook test period | `RUNBOOK.md:470-509` (§1f) | End day rule, window lengths, draft limits |
| Example files | `runs/run_102/artifacts/research_brief.yaml`, `pre_registration.yaml`, `brief_hypotheses_context.yaml`; `runs/run_102/pipeline_state.yaml`; `runs/run_102/handoffs/` | What the launch wrote for run_102 |

Remarks? Mark a remark "direct" for an answer before the next stop; say "next" to continue.

## Operator remarks (verbatim, with the guide's direct answers)

Direct: Not sure i get :
Step 6 actions
step 9
Step10

Direct answer:

**Step 6: the four actions.** Once a queue line is picked, the launcher asks one question: what does this line need now? The answer comes from `_next_action_for_entry` (`run_campaign.py:238-260`) and depends only on what the line already holds.
- **New launch** ("fresh_launch", `:253-259`): the line has no run yet. A new run is created from its brief (`:4410-4427`). run_102 was this case.
- **Saved extra idea** ("queued_card", `:257-258`): the line has no run yet but points to a hypothesis card saved earlier. When step 1a writes several ideas from one brief, the first runs at once; the others are saved under `campaign_record/queued_cards/` and each gets its own queue line, status `queued`, with a link to its card (`:5525-5541`). Launching such a line creates a run that skips step 1a: the saved card is copied in as the run's card, the run starts at step 1b, and the criteria are written from that card (`:5478-5500`, `:4428-4440`). 3 lines in today's queue carry a card link; none is waiting.
- **Continue** ("continue", `:260`): the line already has a run. The launcher does not create anything; it takes the last run (`:4621-4622`) and lets the orchestrator carry on from the stage that run was waiting on, for example after `--resume`.
- **Refinement brief** ("refinement_brief", `:250-252`): an old path where the operator attached a follow-up brief to a line. With verdict routing retired it is refused: the line pauses and the operator is told to register the brief as a new line instead (`:4546-4556`).

**Step 9: the checks before the pre-registration is written.** The pre-registration is the file that fixes, before any result exists, how the idea will be judged and on which test period. It is written only when the brief carries test settings (`run_campaign.py:795-798`), and only if every check passes; any failure stops the launch with the reason (`:851-933`).
1. Who writes the criteria: a brief that says "step 1a will choose the criteria" must not also carry criteria. Both at once is refused (`:843-855`).
2. Criteria taken from the menu may carry nothing but the list of menu ids (`:862-869`).
3. Two older checks, for criteria written by hand in the pre-menu format: every outcome must name what happens next (`:871-885`), and every criterion must be well formed (`:887-897`). Both are skipped when the criteria are menu ids.
4. The menu check (`:899-917`, `tools/verdict_criteria_evaluator.py:1964`): each id must exist in the criterion menu; a brief may change only what the menu lets it change; a threshold the menu locks cannot be moved; a minimum sample cannot be lowered; an entry the menu has retired cannot be newly chosen.
5. The menu ids are then expanded into full criteria (`:918-920`). run_102's brief said only `forecast_ic_median` at horizon 24; its pre-registration holds the full criterion: metric, window by window, median, above 0.02, at least 5 windows (`runs/run_102/artifacts/pre_registration.yaml`).
6. The test-period selection: a brief must either describe its test windows or point to one existing protocol file, never both; a pointer must be a file name under `protocols/` (`:925-933`, `run_phase1_research.py:10908-10935`).

**Step 10: the list of ideas already produced.** It only matters for a brief that can yield several ideas over time (an "open" brief, stop 02).
- When it is written: at launch, for a line whose brief has an owner line (the line registered with "open"), either that owner itself or a later "more ideas" request on the same brief (`run_campaign.py:5455-5475`, `tools/decide_next.py:729-745`). A line created by decide-next from an analyst proposal gets nothing.
- What it holds: the queue line, the owner line, the brief path, whether this is the first launch or a request for more, and the ids of every idea already produced from this brief file, taken from each earlier run's card and each saved card not yet run (`tools/decide_next.py:819-835`).
- What reads it: step 1a. When the file exists, the AI receives it with an extra instruction sheet, `BRIEF_HYPOTHESES.md`: do not repeat these ideas; you may write several ideas; or say the brief has nothing new left (`run_phase1_research.py:8566-8584`, `:8615-8635`).
- One exception: a run launched from a decide-next brief does not get it, even when the file is written (`run_phase1_research.py:8623-8624`, `:8144-8172`). run_102 is that case: its file says `request: first_launch`, `already_produced: []`, and its brief is a decide-next brief carrying its source's criteria, so by this code step 1a did not receive the file.

Direct : 
Do not get why we differenciate a new launch from a "saved extra idea"

Direct answer:

The difference is one question: has step 1a already written the idea?
- **New launch:** the line has a brief but no idea yet. The run starts at step 1a, where the AI turns the brief into a hypothesis card (`run_campaign.py:4410-4427`; the state file starts at `hypothesis_generation`, `workflow/setup_run.py:68`).
- **Saved extra idea:** step 1a already wrote this idea, in an earlier run on the same brief. It wrote several cards at once; the first was run, the others were saved, each on its own queue line, because one run tests one idea (`run_campaign.py:5525-5541`; `campaign_config.yaml:688-691`). When such a line is launched, running step 1a again would cost a second AI call and would not give back the same idea. So the launcher copies the saved card in and starts the run at step 1b (`run_campaign.py:5478-5500`). The code's own comment: "launched past 1a with that card ... (no second 1a call, no card drift)" (`:4593-4595`).

Everything else is the same for both: the same brief file, a new run number, the same brief and pre-registration files (`:4429-4433` calls the same `_materialize_run` as `:4416`), and the same checks after. The saved-idea path adds one step that step 1a would otherwise have done: it writes the criteria from the saved card into the pre-registration (`:5494-5500`).

A saved idea's line is created with status `queued`, which the launcher never picks on its own (`run_campaign.py:223-235`); decide-next ranks these lines by the scores step 1a gave them and releases one when it is picked (`campaign_config.yaml:688-691`, stop 24).

Direct: I still do not get Step 9: the checks before the pre-registration sorry.

Direct answer (simpler, with run_102 walked through):

**What the pre-registration is.** The rules of the game, written down before the game is played: which test decides pass or fail, with which threshold, on which test months. It is written once, at launch (`run_campaign.py:935`), and the pass/fail grid reads it at the end (stop 19). Writing it first is what stops us from choosing the rule after seeing the result.

**Where the rules come from.** Two ways: the brief names them, or the brief says "step 1a will choose them". Either way they are picked from the criterion menu (`config/criterion_menu.yaml`, stop 08): a fixed list of approved tests, each with its threshold and its minimum sample.

**What the checks are for.** To make sure the rules are valid and not loosened, before any money is spent. If one check fails, no pre-registration is written and the launch stops with the reason.

**run_102, check by check.** Its brief named one test: `forecast_ic_median` (the forecast's rank correlation with the coming return, its median over the windows), at a 24-hour horizon.
1. "Not both": a brief may not say "step 1a chooses" and also give rules (`run_campaign.py:843-855`). run_102's brief only gave rules: pass.
2. "Names only": when the brief names menu tests, it gives the names and nothing else that would be silently ignored (`:862-869`). run_102 gave one name: pass.
3. "Old format": two checks for rules written by hand the old way (`:871-897`). run_102 used menu names, so both were skipped.
4. "Not loosened": the named test exists in the menu, and the brief changes only what the menu allows: no locked threshold moved, no smaller minimum sample (`:899-917`). `forecast_ic_median` exists; 24 hours is one of the allowed horizons (1, 6, 24, 72, 168; `campaign_config.yaml:1097-1098`); nothing else changed: pass.
5. "Spelled out": the short name is replaced by the full rule from the menu (`:918-920`). run_102's file now reads: median of the windows' values, above 0.02, at least 5 windows, 24-hour horizon (`runs/run_102/artifacts/pre_registration.yaml`).
6. "One test period": the brief describes its test months one way only, either written out (here: fold B) or as a pointer to one protocol file, never both (`:925-933`). Pass.

All passed, so the file was written.

Remark:
Ok so i think i understand that we are testing the validity of the criterias associated to a claim, the ones that will decided pass/fail. ONLY  when claims are given in brief and not decided step 1a. 

So to summarize the stop here: it does:
- check that there is no parrallel run (lock) 
-clear run folder unused
-ensure which flag and setup the run with that
-decide what to launch based on queue line
- initiate the folders and elements for the run
- in case of claim given, check the claim is valid 
- in case of brief that already generated claims, link brief and claim, before proceedibg to next steps
- log the in progress 
- in case of windows given, check time consistency

Challenge: 
The part about "in case of claim given, check validity" as well as "in case of windows, check time". For me this is not the place. The writer should be responsible to ensure that both are valid. Happy to be challenged, or even to move the control in another place. But this step should be mechanics around run preparation and orchestration of calls around that. 
Of course legacy should be cleaned as well. 
Next

## Inspector notes

### (1) Design and mechanism

1. The launcher's purpose for the goal is the one the speech gives: freeze the rules (criteria, windows) before any result exists, so a pass cannot be chosen after the fact. The frozen copy is `pre_registration.yaml` (`RC:935`; run_102's holds the resolved criterion `:7-19`, fold B `:20-28`). That part is sound and is read back by the grid (stop 19). Everything else in the step is routing around it.
2. On the operator's challenge (the criteria and window checks "are not the place"): the code half-agrees. Of the six pre-registration checks (`RC:843-933`), under the live flags only two do work for a menu brief: the menu lint (`:905-917`) and the id-to-criterion resolution (`:918-920`). The "not both" check (`:843-855`) guards a shape only a hand brief can produce; B11 and CUL-267 (`:871-897`) are skipped for menu ids; the K3 protocol-selection lint (`:925-933`) guards `protocol_ref`, which only three legacy briefs use (`briefs/FUNDING_MR_4H_RETEST.md`, `FUNDING_MR_DAILY_RETEST.md`, `H-041-C-v2.md`; grep) and no live entry. The one check that must stay at launch, whoever writes the brief, is the resolution (`:918-920`): it is what turns a name into the frozen rule, and it reads the menu as it is on launch day, which is the "rules fixed before the result" guarantee. The lints could move to the writers (register for a hand brief, decide-next for a candidate) with the resolution kept here.
3. The venue check at launch (`RC:787-792`, speech step 8) has no effect on the research loop. `research_only` is read only by `_research_only_hold` (`RP:15626-15648`), called at the holdout unlock (`RP:7614`, `:7655`), which the live path never reaches without an operator unlock (stop 27). A brief on a non-tradable venue would be researched to its end, spent on, and recorded; the hold would fire only at a spend. For the goal "a strategy the operator can trade" this is a late gate, not a door; a fact to carry to stop 27.
4. The protocol pre-flight (`RC:4095-4174`, `:3994-4092`) is almost entirely for shapes the live path does not produce: pinned protocols (`:4133-4146`), `run_context`/`last_escalation` resolution (`:4147-4173`), promotion-block ratification and regeneration (`:4052-4092`), post-spend protection (`:4025-4043`). For the live case (a fresh launch with a fold in `machine_constraints.protocol`, no generated file yet) the branch taken is `:4044-4061`: build the expected protocol (`_expected_generated_protocol`, `:3881-3909`, which runs the windows helper and so the holdout guard, `RP:10637`) and return no refusal (`promotion_is_generic(None)` is False, `protocol_resolution.py:62-64`). The shared-day check (`_windows_overlap_in`, `:3958-3967`) and the validation-period check (`_validation_overlap_in`, `:3970-3991`) both need an existing protocol file and are not reached on that branch (`:4059` returns before them); the windows are generated inside `run_loop` (`RP:10649-10729`) with its own validation guard (`RP:10641-10646`). Whether `_expected_generated_protocol` also applies the validation guard beyond `:3909` was not read. So for the live case the pre-flight's real content is: the fold's windows can be generated and clear the holdout.
5. Two identities for one run: `pre_registration.hypothesis_id` is the placeholder `run_102-initial` (`RC:811`, run_102 `:2`), while the brief's candidate id is `SMA_PULLBACK..._trade_efficiency-run_101-1` and the card's id must equal the candidate's (`RP:8406-8410`). No reader of `pre_registration.hypothesis_id` was found (grep over `workflow/` and `tools/` for `pre_reg...hypothesis_id`: none). A field written at every launch, never reconciled, never read: lead.
6. `brief_hypotheses_context.yaml` was written for run_102 (`request: first_launch`, `already_produced: []`) and, as the guide's direct answer says, not read by 1a because the run is a decide-next candidate (`RP:8623`). The cause is a double identity: the entry `trade_efficiency-run_101-1` was operator-registered through `register`, so it carries `brief_status: open` (`campaign_queue.yaml:1349`) and counts as a brief owner (`decide_next.py:729-745`), while its brief is a candidate brief. An R2 request ("more hypotheses on this open brief", stop 24) can therefore be raised on a brief whose `research_goal` is a code-built finding with a pre-filled claim. Whether R2 excludes candidate briefs was not checked; lead for stop 24.
7. `sample_split_design.holdout_range` copies the sealed dates in clear into every run's `pre_registration.yaml` (`RC:829-835`; run_102 `:29-32`), whose own comment says nothing reads it back (`:826-828`). The repository's rule is to refer to those dates only through the policy file; this writer puts them in every run folder, which the run viewer and the AI stages (the file is a context input of 1b, `RC:764-765`) then see. Not a leak of data, but a copy of the one value the rule says not to copy.
8. Orphan scan (`RC:3669-3697`) is read-only and logs one line; it clears nothing. The operator's summary ("clear run folder unused") misreads the speech's step 3; worth a correction so no one expects cleanup.
9. The lock (`campaign_lock.py:171-211`) is sound for one host (exclusive create, PID liveness on this host, 6 h age fallback); `register` bypasses it (stop 02 note 1.4). The dry run (`RC:5837-5926`) exercises the flag-off wiring: `_materialize_run` without `promotion_retired` (`:5875`), the legacy terminal `completed_rejected` and the `no_signal_artifact` pause (`:5897-5912`), and by its own comment never the "continue" branch (`:5856-5860`). It proves the queue-to-folder wiring, not the live path.

### (2) Legacy or simplifiable (leads)

1. Launch actions: `refinement_brief` (`RC:4398-4409`, `:4546-4591`) is refused under retired routing before it can run; with the flag folded in, the action, `_materialize_refinement_run`, `_parse_refinement_brief_yaml`, `_existing_continuation_child` and the `refinement_brief_*` queue fields go together.
2. Protocol pre-flight: the pinned (`protocol_ref`), `run_context`/`last_escalation` and promotion branches (`RC:4025-4043`, `:4052-4092`, `:4133-4173`) serve three legacy briefs and the retired routing. `_GENERATED_PROTOCOL_FIELDS`, `_regenerate_protocol`, `assert_promotion_ratified`, `promotion_is_generic` are their helpers. Not checked: whether `tools/protocol_resolution.py` has any other live caller.
3. Handoff templates: 9 copied at setup (`setup_run.py:115-118`); on run_102 the stages used `research_brief_to_hypothesis`, `hypothesis_to_strategy_config_authoring`, `hypothesis_to_innovation_expansion` from the copies and five files written by `run_loop` (`config_direct_backtest_specification`, `config_direct_data_availability_gate`, `config_direct_protocol_execution`, `protocol_to_analyst`, `specialist_readers_to_regroup_record`; `ls runs/run_102/handoffs/`). Six of the nine copies (`innovation_expansion_to_validation`, `validation_to_backtest_specification`, `backtest_spec_to_protocol_execution`, `protocol_to_verdict_interpreter`, `campaign_review`, `holdout_evaluation`) are copied into every run for stages it will not reach. The name `specialist_readers_to_regroup_record` is a deleted stage's. Stop 05b.
4. `setup_run.py:121-126` writes a `# TODO` `research_brief.yaml` that `_materialize_run` overwrites seconds later (`RC:793`); the console messages (`:94`, `:104`, `:119`, `:126`, `:128`) address a human filling the file by hand. The script predates the campaign runner.
5. `pre_registration.yaml`'s `reactivation_context` sentence (`RC:813-818`), `sample_split_design` (`:829-835`, note 1.7) and `hypothesis_id` placeholder (`:811`, note 1.5): three fields written per run with no reader found.
6. `_write_brief_hypotheses_context` runs for candidate briefs whose 1a then ignores the file (note 1.6): either skip the write when `_decide_next_candidate` is true, or make the owner test exclude candidate briefs.
7. Dry run (`RC:5837-5926`): simulates legacy states only; if kept, it should simulate the live terminal (`completed_refuted`) and `promotion_retired=True`.
8. `_PREFLIGHT_TERMINAL_PREFIXES` includes `rejected` and `failed_validation` (`RC:3849`), states of the unreached routes; `_LAUNCH_ACTIONS` (`:4389`) carries `refinement_brief`.

### (3) Disagreements between the speech and the element

1. Step 12 says the launcher checks, before any AI call, that "no two windows share a day, none touches the validation period (except fold D's exact blocks)". For the live case (fresh launch, generated protocol, no file yet) those two checks are not reached in the pre-flight (`RC:4059` returns before `:4066`; `_windows_overlap_in` and `_validation_overlap_in` need a file). What the pre-flight does check there is that the fold's windows generate and clear the holdout (inside `_expected_generated_protocol`). The shared-day and validation checks run later, in `run_loop`'s generation and `run_protocol.py`, still before the first AI call in the case of the validation guard (`RP:10641-10646` at protocol generation, which precedes 1a). The speech's claim is right in timing for the validation guard and wrong in location; for the shared-day check it was not verified where it first runs on a generated protocol (`holdout_policy.windows_overlap` inside generation was not read).
2. Step 8 "adding whether the operator may legally trade that exchange and product" is right; the speech does not say that the value has no effect until a holdout spend (note 1.3).
3. Section 6, "The state file's template fields ... stop 00 named what reads them": consistent with stop 00 (nothing live).
4. The direct answer on step 10 ("by this code step 1a did not receive the file") is confirmed (`RP:8623-8624`); the reason (the entry is both brief owner and candidate) is in note 1.6.
5. Direct answer on step 9, item 6: `RP:10908-10935` is the K3 lint; correct. The answer says "run_102's brief said only `forecast_ic_median` at horizon 24"; confirmed by the brief (`research_brief.yaml:20-24`) and the resolved rule (`pre_registration.yaml:7-19`).
6. Counts verified: 9 templates (`workflow_artifacts/templates/handoffs/`), 14 files in `runs/run_102/handoffs/`. Reading-map ranges verified: `RC:5931-5981`, `:6014-6028`, `:5787-5791`, `:4497-4660`, `:3669-3697`, `:4508-4525`, `:4527-4542`, `:223-235`, `:238-260`, `:4544-4556`, `:4592-4610`, `:4611-4620`, `:4392-4440`, `:4410-4427`, `:4243` (`_halt_launch_exception`), `:736-757`, `:777-935`, `:760-774`, `:5455-5475`, `:4621-4640`, `:4642-4655`, `:4443-4494`, `:4463`, `:4095-4174`, `:3994-4092`, `:3958-3991`, `:5837-5926`; `setup_run.py:47-94`, `:96-128`; `campaign_lock.py:48`, `:54`, `:68-70`, `:127-150`, `:171-218`; `RP:93`.
