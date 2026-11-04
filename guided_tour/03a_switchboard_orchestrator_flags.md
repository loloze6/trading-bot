# Stop 03a: The switchboard, part a: the orchestrator's switches

## Speech (verbatim)

**Stop 03 of 29: The switchboard (campaign config and flag register).** This stop has two parts: 03a, the orchestrator's switches (this speech); 03b, the other sections of the config and the flag register (next). Open on the side: `campaign_config.yaml`, `run_campaign.py`, `run_phase1_research.py`.

**In one sentence.**
The switchboard is the one file where the operator turns each piece of the research process on or off, and sets a few budgets and model choices.

**Why it exists.**
The process was built piece by piece. Each new piece shipped switched off, was proven harmless, then was switched on by a decision.
So one file must say which pieces are live today. Without it, nobody could tell which process a run actually followed.
It also stops a bad combination before money is spent: a piece switched on without the piece it relies on would run half-wired and give a result we cannot trust.

**What comes in, what goes out.**
- In: the operator's decisions, written by hand as yes/no switches, each with a long comment of its history.
- Out: no file. Every step of the process reads its own switch when it gets there.
- Checked by: the launcher, before every step of the campaign; and the run itself, before its first paid step.

**What happens here, step by step.**
1. Before each step, the launcher reads the whole file once.
2. It asks every switch's own reader for its value. A switch must be a plain yes or no; a quoted word or a blank is refused.
3. Each reader also checks what its switch relies on. Example: the record-keeping step needs the pass/fail grid; decide-next needs the record-keeping step and config-direct authoring.
4. Any problem pauses the queue line and names the culprit. Nothing launches, nothing is spent.
5. When the run starts, it re-checks the switches it depends on, again before any paid step.

The live switches, grouped by what they change:
- **The shape of the run:** config-direct authoring (an AI writes one base strategy config, then small variants of it); the variant loop (every variant is backtested); the data check before backtests.
- **The ideas step:** the list of tried ideas shown to the AI; corrected paths to the knowledge base; the claim test (each idea states a measurable claim); the brief's own criteria; an exact config given in the brief is built by code; the nearest buildable version when a component is missing; a size check of the forecast on invented prices; a replay check of an exact config.
- **The verdict:** the pass/fail grid; forecast quality measured at several horizons; all costs counted in the cost bar; the overlap check against proven pieces, only where one exists.
- **The profit bars:** the bars file, checked on every backtest, in version 2, with the luck correction counted among same-shaped strategies only.
- **After the backtest:** the analyst's two readings; the record into campaign memory.
- **What runs next:** decide-next; the old verdict routing retired; follow-up runs on a random fold (a fixed set of test months); combinations of proven pieces; the operator's approval for every agent-made queue line; the repeat check (same config, coins and windows already tested).
- **Bookkeeping:** the variant-selection record; the queue health file; the model provenance stamp.

The file also sets: a token budget per run; the AI model for steps 1a and 1b and for the analyst (Sonnet 5.5; Haiku 5.5 for every other AI step); and optional caps on the analyst's session, written as comments.

**What it costs and how long it takes.**
No cost: reading the file is instant.
34 switches in the orchestrator section: 30 on, 4 off (`campaign_config.yaml`, counted by hand from the file).
Token budget per run: 1,800,000 weighted units (`campaign_config.yaml:92`).

**What is switched off or not used here.**
- Off: counting zero-trade windows as "not computed" in the grid.
- Off: pausing a run when step 1b built an approximation (the deviation gate).
- Off: queueing step 1a's extra ideas as soon as 1a ends.
- Off: quarantine, which would let the campaign continue past four kinds of halt.
- Not read by any code in the workflow or tools folders (grep; only a sync test reads them): the old raw token budget, the default refinement count, the review cadence default, the failed-families trigger, the sparse-window threshold. The review cadence actually used comes from the campaign state file (stop 26).
- Three comments still say their switch is "held off" although it is on: profit bars file, config-direct authoring, variant loop. Several comments say "today's default" for a state that has since changed.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Section header | `campaign_config.yaml:84-88` | Orchestrator / pipeline governance |
| Raw token budget | `campaign_config.yaml:89-91` | Marked superseded; no reader in `workflow/` or `tools/` |
| Weighted token budget | `campaign_config.yaml:92-115` | Read by `_load_token_budget` (`run_phase1_research.py:983-998`) |
| Four old defaults | `campaign_config.yaml:116-120` | Refinements, review cadence, failed-families trigger, sparse threshold; no reader in `workflow/`/`tools/`, only `tests/test_campaign_config_sync.py` |
| Quarantine | `campaign_config.yaml:121-141` | `halt_policy.quarantine_enabled: false`; read by `run_campaign.py:1993-2007` |
| Tried ideas to 1a and 2 | `campaign_config.yaml:142-176` | `exclusion_digest_input`, on |
| Corrected input paths | `campaign_config.yaml:177-205` | `stale_input_path_fix`, on |
| Variant selection record | `campaign_config.yaml:206-246` | `variant_selection_record`, on |
| Repeat check at 5a | `campaign_config.yaml:247-278` | `variant_anti_adjacency_gate`, on |
| Queue health file | `campaign_config.yaml:279-317` | `schedulability_block`, on |
| Pass/fail grid | `campaign_config.yaml:318-348` | `grid_evaluation`, on |
| Profit bars file | `campaign_config.yaml:349-387` | `profit_bars_file`, on; comment says held off (`:384-387`) |
| Bars on every backtest | `campaign_config.yaml:388-421` | `profit_bars_every_backtest`, on |
| Bars version 2 | `campaign_config.yaml:422-462` | `profit_bars_v2`, on |
| Data check | `campaign_config.yaml:463-496` | `data_availability_gate`, on; the one switch whose code default is on |
| Config-direct authoring | `campaign_config.yaml:497-540` | `config_direct_authoring`, on; comment says held off (`:537-540`) |
| Variant loop | `campaign_config.yaml:541-579` | `variant_loop`, on; comment says off_incomplete (`:578-579`) |
| Record into memory | `campaign_config.yaml:580-612` | `regroup_record`, on; needs the grid |
| Model provenance | `campaign_config.yaml:613-648` | `score_provenance`, on |
| Decide-next | `campaign_config.yaml:649-698` | `decide_next`, on; needs regroup_record and config-direct |
| Verdict routing retired | `campaign_config.yaml:699-749` | `verdict_routing_retired`, on; needs decide_next and bars on every backtest |
| Combinations | `campaign_config.yaml:750-774` | `composition_runs`, on |
| Forecast size probe | `campaign_config.yaml:775-792` | `forecast_size_probe`, on |
| Claim test | `campaign_config.yaml:793-822` | `claim_tests`, on; needs config-direct |
| Zero-trade windows | `campaign_config.yaml:823-842` | `zero_trade_windows_not_computed`, off |
| Analyst | `campaign_config.yaml:843-877` | `analyst`, on, `model: claude-sonnet-5-5`; needs folds; caps as comments (`:874-877`, code `run_phase1_research.py:4699`) |
| Stage models | `campaign_config.yaml:878-893` | Not a switch; Sonnet for 1a and 1b; read by `_stage_model` (`run_phase1_research.py:1143-1153`) |
| Folds | `campaign_config.yaml:894-938` | `folds`, on |
| Operator approval | `campaign_config.yaml:939-959` | `operator_approval`, on |
| Nearest build | `campaign_config.yaml:960-982` | `nearest_build`, on; needs config-direct and claim tests |
| Deviation gate | `campaign_config.yaml:983-995` | `deviation_gate`, off |
| Config replay gate | `campaign_config.yaml:996-1007` | `config_replay_gate`, on |
| Exact config at 1b | `campaign_config.yaml:1008-1024` | `exact_config_1b`, on |
| Brief criteria | `campaign_config.yaml:1025-1033` | `brief_criteria`, on |
| Same-structure DSR | `campaign_config.yaml:1034-1054` | `dsr_same_structure`, on |
| Extra cards at 1a | `campaign_config.yaml:1055-1064` | `extra_cards_at_1a`, off |
| All costs in the cost bar | `campaign_config.yaml:1065-1085` | `cost_bar_all_costs`, on |
| IC horizons | `campaign_config.yaml:1086-1102` | `forecast_ic_horizons`, on |
| Residual IC only with a block | `campaign_config.yaml:1103-1112` | `residual_ic_requires_block`, on |
| The readers, one per switch | `run_campaign.py:3709-3747` | 33 switches mapped to their reader |
| Launch pre-flight | `run_campaign.py:3750-3824` | Parse once; mapping check (`:3784-3790`); every reader (`:3791-3797`); unowned switches (`:3799-3805`); quarantine bool (`:3806-3811`); repeat-check dependencies (`:3812-3823`) |
| Pre-flight call | `run_campaign.py:4508-4525` | Runs on every step; values feed the step |
| Generic strict reader | `run_phase1_research.py:5687-5723` | Absent means off; non-bool raises; dependencies named |
| Run start re-check | `run_phase1_research.py:19672-19766` | Grid route, analyst, regroup, bars, bars v2, provenance, routing retired, parked marker; failure sets `failed` before any spend |

Remarks? Mark a remark "direct" for an answer before the next stop; say "next" to continue.

## Operator remarks (verbatim, with the guide's direct answers)

Indeed, i would really propose to clean this file : 
- removing the flags not used
- removing the flags that we consider as "core" functionality of the workflow (mostly flagged initially to secure the delivery, but that would never be switched back again) 
- keep the ones that are aligned with a "modular" workflow approach, eg: when a component is missing, the nearest buildable version is built instead, eg: list of tried ideas shown to AI.
- some that might sound duplicate (eg: pausing when approximation? 
- i would also limit the information wording to a reasonable amount (informing about functionality switched on/ not full history) 
- i would categorize it to make it readable 

 Next
- model and budget makes sense

## Inspector notes

### (1) Design and mechanism

1. The switchboard describes one configuration, not a space of them. Of the 34 switches (33 `enabled:` keys, 30 true and 3 false, plus `halt_policy.quarantine_enabled: false`; counted by awk over `campaign_config.yaml:88-1112`), the off-state of at least twelve is the legacy pipeline that no run has taken since the flags went on: `config_direct_authoring`, `variant_loop`, `grid_evaluation`, `regroup_record`, `decide_next`, `verdict_routing_retired`, `profit_bars_file`, `profit_bars_every_backtest`, `profit_bars_v2`, `data_availability_gate`, `analyst`, `folds`. Their dependency chains (`regroup_record` needs the grid `:585-587`; `decide_next` needs regroup and config-direct `:655-658`; `verdict_routing_retired` needs decide-next and bars `:706-709`; `composition_runs` needs four `:755-757`; `operator_approval` needs decide-next and routing-retired `:942-946`) mean no one of them can be turned off alone without reviving the retired routing. The pipeline's live shape is therefore fixed by this file and cannot be read from the registry (stop 00 note 1.3): a new joiner must read 1,145 lines of YAML to learn that there is exactly one path. The operator's proposal (fold the "core" switches into code, keep the modular ones) matches this reading.
2. The three off switches and quarantine are the only real choices left: `deviation_gate` (pause 1b on any approximation, `:983-995`), `zero_trade_windows_not_computed` (grid grading, `:823-842`), `extra_cards_at_1a` (`:1055-1064`), `halt_policy.quarantine_enabled` (`:121-141`). Of these, quarantine is the one that bears on "run continuously": with it off, every halt reason (27 classified at stop 23) stops the campaign process until a person resumes, including the four the S1 taxonomy found quarantine-safe (`:132-134`). The switch exists, is tested, and is off by the operator's choice; it is the single largest autonomy limiter in this file after `operator_approval` (stop 02 note 1.2).
3. The checks are sound where they run: `_flag_preflight` parses the file once, hands the parsed dict to all 33 readers (`RC:3775-3797`), type-checks unowned flags and quarantine (`:3799-3811`), and refuses (never crashes) before any launch (`:4508`, `:4522-4523`). The run-start re-check (`RP:19680-19749`) calls seven readers without `cfg`, so each re-parses the YAML (`_orchestrator_config`, `RP:3343-3355`, no cache); and the per-stage readers are called from 19 (`_config_direct_authoring_enabled`), 18 (`_variant_loop_enabled`), 10 (`_analyst_enabled`) ... call sites, each a file read (grep counts over `RP`). Correct, cheap, but a sign that the flag values are not a run-level fact held once; a run cannot record "the flags I ran under" except by implication (stop 00: `pipeline_state.flags` is a different thing).
4. Model choices (`stage_models :878-893`, `analyst.model :845`): 1a and 1b on Sonnet, the analyst on Sonnet, `innovation_expansion` (step 2, which decides what variants get backtested) on Haiku by default (`RP:1140`). The file records cost figures for the Haiku 1a/1b (`:891-892`) and says quality on Sonnet is "not measured" (`:893`). For the goal, the step that most shapes what a run tests (2) is on the cheapest model with no measurement either way; a fact for stop 15.
5. The token budget (`:92`, `_load_token_budget` `RP:983-998`, enforced at `RP:5030`, `:17981`, `:19805`, `RC:2692`) is the one numeric knob read at runtime. Its rationale text (`:97-115`) is a 2026-07 history with two corrections layered on; the live sentence is one line. Same pattern as the flags: the file is a decision log pretending to be a config.
6. Comments contradict the live state in at least six places, and the pipeline's AI steps never read this file (stop 00), so the cost is to people only: "Held off_incomplete" on `profit_bars_file :384-387`, `config_direct_authoring :537-540`, `variant_loop :578-579`; `grid_evaluation :342-348` says its routing is "NOT yet wired" and "Blocked on slice 3+"; `profit_bars_file :376-383` says the bars file is an unratified DRAFT whose result "can never currently be PASS" (the operator signed the bars, stop 20); `regroup_record off, today's default` at `:169-170`; `profit_bars_every_backtest :421` "Still blocked on ratified bar values"; `score_provenance :637-648` describes a check on reader proposals the D-198 deletion removed. A reader trusting the comments would believe the live path is the flag-off one.

### (2) Legacy or simplifiable (leads)

1. No reader in `workflow/` or `tools/`: `token_budget_per_run :89-91`, `max_refinements_default :116`, `review_every_n_runs_default :117`, `distinct_failed_families_trigger :118`, `below_floor_pct_threshold :119` (grep for each key: hits only in the speech's named sync test; `run_protocol.py:1881-1884` computes its own `below_floor_pct`, it does not read the key). Five dead keys at the top of the section.
2. `stale_input_path_fix :177-205`: a path correction kept as a switch; its off-state is a known bug. Fold into code.
3. `exclusion_digest_input :142-176`: with `campaign_memory.yaml` present the digest is never used (`:163-172`, `tried_ideas` replaces it); the flag's name and half its text describe the dead half. The live behaviour is "show tried ideas to 1a and 2", one of the operator's keep-as-modular items, under a misleading name.
4. `variant_selection_record :206-246`: on, inert on the config-direct path (itinerary lead); its only live role is as a dependency of the anti-adjacency gate's legacy call site (`RC:3812-3817`). Checked: `_variant_selection_record_enabled()` has 2 call sites in `RP`. Not checked which.
5. `profit_bars_file`, `profit_bars_every_backtest`, `profit_bars_v2 :349-462`: three switches for one feature, chained; the v1 promote-path check (`:357-374`) is unreachable under routing-retired. One switch, or none.
6. `score_provenance :613-648`: the stamping half is live; the "C5.7b-2 rubric_version" half (`:637-648`) checked reader proposals that D-198 deleted. Not checked whether the code half is also gone.
7. `grid_evaluation` is read through two names, `_grid_evaluation_enabled` (6 call sites) and `_grid_route_enabled` (7, an alias since D-198, `RP:4011-4018`). One name.
8. The behavioural switches with no dependency and a byte-identical off-path (`brief_criteria`, `exact_config_1b`, `config_replay_gate`, `dsr_same_structure`, `cost_bar_all_costs`, `forecast_ic_horizons`, `residual_ic_requires_block`, `forecast_size_probe`): candidates for the operator's "keep" list, but each carries an off-path with its own byte-identity test; if never switched back, the test and the branch are both weight. Not checked which have tests.
9. `composition_runs :750-774` is on while the registry holds one active block (stop 22) and `residual_ic_requires_block` exempts ideas on a timeframe with no block: the composition machinery runs on every run with nothing to compose. Lead for stops 19 and 22.
10. The analyst caps "as comments" (`:874-877`): documentation of code defaults inside the config, not values. Either real keys or removed.
11. File length 1,145 lines, of which the orchestrator section is ~1,025; a reading of the switches' live values is 34 lines. The operator's "limit wording, categorise" is a 30x reduction.

### (3) Disagreements between the speech and the element

1. The itinerary (`00_itinerary.md:24`) says "Flags on (31) and off (3)"; the speech says 34 switches, 30 on, 4 off. The file has 30 `enabled: true`, 3 `enabled: false`, and `quarantine_enabled: false`: the speech is right, the itinerary over-counts by one.
2. Reading map "Stage models ... `_stage_model` (`run_phase1_research.py:1143-1153`)": the function runs to `:1167`; short range, not wrong.
3. Section 6 lists three "held off" comments; the stale `grid_evaluation :342-348`, `profit_bars_file :376-383`, `profit_bars_every_backtest :421` and `score_provenance :637-648` texts (note 1.6) are not named. Omission under "facts only".
4. Section 4 step 5 "the run re-checks the switches it depends on": seven readers (`RP:19680-19749`, the reading map names them), each re-parsing the file (note 1.3). The speech does not say the file is read once per launch step but many times per run; a fact, not an error.
5. "33 switches mapped to their reader" (`RC:3709-3747`): 33 entries, correct; quarantine is the 34th, read at `RC:3806-3811` and `:1993-2007`. Consistent with "34 switches".
6. Verified as stated: `:84-88`, `:89-91`, `:92-115`, `:116-120`, `:121-141`, every flag block's line range in the reading map (checked against the file's key positions), `RC:3709-3747`, `:3750-3824`, `:3784-3790`, `:3791-3797`, `:3799-3805`, `:3806-3811`, `:3812-3823`, `:4508-4525`, `:1993-2007`; `RP:983-998`, `:5687-5723`, `:19672-19766`, `:1140`.
