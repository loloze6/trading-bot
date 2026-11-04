# Stop 10: Step 1b, strategy_config_authoring

## Speech (verbatim)

**Stop 10 of 29: Step 1b, strategy config authoring.** Open on the side: `workflow_artifacts/skills/strategy-config-authoring/` (4 files), `workflow_artifacts/skills/quant-fundamentals/SKILL.md`, `templates/handoffs/hypothesis_to_strategy_config_authoring.yaml`, `run_phase1_research.py`, `tools/forecast_rules.py`, `tools/block_manifest.py`, `tools/nearest_build.py`, run_102's 1b files.

**In one sentence.**
Step 1b is where an AI turns the hypothesis card (the one-page statement of the idea, from step 1a) into one base strategy config: the exact recipe the trading engine will run.

**Why it exists.**
The engine does not read ideas; it reads a config file built from fixed components (indicators) and transforms (operations on their output).
Someone must translate the idea into that recipe faithfully, and say plainly where the recipe differs from the idea. A config that quietly tests something else would make the run's verdict about the wrong idea.
Code then checks the recipe before any money is spent on backtests.

**What comes in, what goes out.**
- In: the hypothesis card; the strategy design guide and the component catalogue (stop 11); the pre-registration (the criteria and test settings fixed before any result); a sheet of trading facts (quant fundamentals); for a follow-up run, the source run's config and its block manifest; under the current switches, the "build the nearest version" note and the claim note.
- Out: the base config (inside `backtest_spec.yaml`), a decision record (ready, or a missing component), the block manifest (which parts of the config are the idea, which are scaffolding), and check records: forecast size probe, deviations, and a replay check when the brief gave an exact config.
- Next: step 2 (stop 15) writes variants as small edits of this base config.

**What happens here, step by step.**
1. If the brief carries an exact config, code writes 1b itself, copying the config and manifest unchanged: no AI call. Otherwise the AI (Sonnet 5.5) writes it.
2. The skill's rules: only components from the catalogue; every component graded (on/off conditions go in the regime detector, the part of the config that labels market states); every component's forecast standardised first (a rolling rescale to a typical size of 10, capped at 20; decision D-149, a row of the decision log); every card quantity and the statement mapped to a config element; anything not built as written marked "DEVIATION:".
3. A missing component is declared only after trying combinations of existing ones. Under the current switches the AI builds the nearest version instead and lists each difference.
4. For a follow-up run, the AI starts from the source run's config, keeps it unless the card truly needs a change, and lists every change.
5. Code then checks, in order: the block manifest is valid; the graded and standardised rules hold; the forecast's size on invented prices is sane (not tiny, not stuck at the cap, not empty). A failure sends 1b back once with the error; a second failure pauses the run.
6. Code records the deviations, compares the config with the start config of a follow-up run, and compares the claim with the block built (stop 09).
7. With an exact config in the brief, code replays the AI's config against it; any difference pauses before step 2.
8. A declared missing component that cannot be approximated parks the run (it waits, off the queue, until the piece exists) and is written to the component request list.

Example: run_102's 1b received run_101's base config with the weight change already applied. It answered `spec_ready`, kept the config and manifest unchanged, and declared no deviation (`deviations.yaml`: `status: exact`). The size probe passed on all 4 configs (largest forecast about 19, under the cap of 20).

**What it costs and how long it takes.**
run_102: one call, 0.45 USD, 32 seconds, one turn (`runs/run_102/pipeline_state.yaml`, audit_log `strategy_config_authoring_attempt_0`).

**What is switched off or not used here.**
- The deviation gate (pause on any approximation) is off: deviations are recorded only.
- The exact-config path and the replay gate are on but were not used by run_102 (its brief had no exact config).
- The skill still names a "variant selection" section, marked removed for this flow, and a parameter-bracket input (`findings_carryover.yaml`) that only the old continuation path copies into a run (`run_phase1_research.py:11823-11892`), not reached today.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Skill | `skills/strategy-config-authoring/SKILL.md:1-317` | Mission (`:8`), inputs (`:20`), outputs (`:39-96`), pass-through (`:97`), removed selection (`:108`), design rules D-051/O-7 (`:128-192`), checklist (`:193`), ungated pattern (`:235`), replication guard (`:285`), forbidden (`:294`) |
| Claim note | `skills/strategy-config-authoring/CLAIM_NOTE.md` (13 lines) | Claim vs block manifest |
| Nearest build | `skills/strategy-config-authoring/NEAREST_BUILD.md` (38 lines) | Build the closest config, list deviations |
| Start from config | `skills/strategy-config-authoring/START_FROM_CONFIG.md` (18 lines) | Follow-up runs |
| Quant fundamentals | `skills/quant-fundamentals/SKILL.md` (171 lines) | Added at `run_phase1_research.py:3196` |
| Handoff template | `templates/handoffs/hypothesis_to_strategy_config_authoring.yaml` | Card, design guide, catalogue required |
| Pre-registration added | `run_phase1_research.py:3092-3115` | B7 stages and deference sentence |
| Model | `config/campaign_config.yaml:880` | Sonnet 5.5 |
| Nearest build input | `run_phase1_research.py:16775` | `NEAREST_BUILD.md` |
| Start config input | `run_phase1_research.py:16794-16833`; `tools/nearest_build.py:197-198` | `start_config.json`, `start_block_manifest.yaml` |
| Exact config by code | `run_phase1_research.py:17089` | Flag `exact_config_1b` |
| The route | `run_phase1_research.py:18894-18959` | spec_ready → checks; component gap → retry, park or pause |
| Pass-through manifest | `run_phase1_research.py:8517` | Code-written manifest for a patch |
| Manifest and rule check | `run_phase1_research.py:16587-16651`; `tools/block_manifest.py` | One retry, then pause |
| D-149 rule | `run_phase1_research.py:16525`; `tools/forecast_rules.py:131-170`, rule text `:55-60` | Graded, standardised, no dead-zone op |
| Size probe | `run_phase1_research.py:16539`, `:5551-5596`; `tools/forecast_size_probe.py`; `trading-bot/tools/validate_config.py` | Invented prices; `forecast_size_probe.yaml` |
| Nearest build record | `run_phase1_research.py:17223-17256` | `deviations.yaml`, `component_requests.yaml` |
| Claim match | `run_phase1_research.py:17883` | Stop 09 |
| Deviation gate | `run_phase1_research.py:18919` | Off |
| Replay gate | `run_phase1_research.py:17186-17220` | Exact config briefs |
| Park | `run_phase1_research.py:18930-18948`, `:6605` | `paused:waiting_for_component` |
| Schemas | `workflow_artifacts/schemas/backtest_spec`, `decision`, `block_manifest` | Checked on read-back |
| Examples | `runs/run_102/artifacts/backtest_spec.yaml`, `decision.yaml`, `block_manifest.yaml`, `forecast_size_probe.yaml`, `deviations.yaml`, `start_config.json`, `start_block_manifest.yaml` | spec_ready, exact, probe ok |

Remarks: send them as "stop 10: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop 10
No remark, seems aligned with my vision.

## Inspector notes

### (1) Design and mechanism

1. On the live loop, 1b is a copy with commentary. For a side-finding child the instruction is "your config is that config, unchanged, unless the card truly needs a change ... never build a different signal" (`START_FROM_CONFIG.md:7-14`); run_102's `backtest_spec.yaml:2-44` equals `start_config.json` key for key, the manifest's pointers equal the start manifest's (`block_manifest.yaml:1-8` vs `start_block_manifest.yaml:1-8`), and `decision.yaml:4` says "emitted unchanged". What the 0.45 USD Sonnet call added is ten `config_rationale` entries (`:45-65`), seven of which say "Not a config element". Code already does this copy for an exact-config brief (`_exact_config_1b :17089-17140`); for a start-config brief the model is asked to copy and code diffs afterwards (`_record_start_config_deviations :16836`). Same shape as stop 07 note 1.1: the AI step decides things only on an operator brief or a new-block candidate; on the common path its product is prompt text for the analyst.
2. The checks after 1b are real, ordered and bounded: manifest shape and pointer resolution (`block_manifest.py:99-120`, one implementation shared with 5a and the registry, `:6-17`), D-051/D-149 by code against the catalogue's Kind column (`forecast_rules.py:86-100`, `:141-168`), the size probe on an invented random walk at the coin's price level (`forecast_size_probe.py:11-35`; run_102 `max_abs` 18.96, `:10`), one retry then a pause (`RP:16587-16651`). A pass-through config that breaks a rule stops at once, since a retry cannot change it (`:16613-16614`, `:16636-16642`). The manifest contract ("block or scaffolding, never both", kind by pointer location, `block_manifest.py:31-41`) is what makes an idea a reusable unit for stop 22. This is the right place for these checks, and they are the right checks.
3. D-149 fixes what a forecast can be. Every strategy component is standardised first (target 10, cap 20, rolling window) and no scale op follows (`forecast_rules.py:56-61`, `:131-138`); sizing is the one `vol_target` block (`SKILL.md:210-217`). run_102's forecast is `(standardise(trend) + 0.25 x standardise(stretch)) / 1.25` (`backtest_spec.yaml:51`), and on an invented random walk its largest value reaches 19 on all four configs (`forecast_size_probe.yaml:10`, `:26`, `:42`, `:58`). So by construction every idea the campaign tests is a rank-of-the-last-500-bars signal at near-full exposure whose turnover is its rank flips; the forecast's size says nothing about conviction across regimes, only within the window. That is the operator's campaign rule (D-149, D-176), and it is consistent. The consequence for the goal is that one strategy class is being searched, and the profit bars (stop 20) judge that class's cost structure every time.
4. The engine grows only through a human. A `component_gap` parks the run and appends to `component_requests.yaml` (`RP:18930-18948`); NEAREST_BUILD.md (2026-10-05) now tells 1b to approximate instead and park "only when the core is lost" (`:9-12`, `:30-38`). The memory's `approximation: n` rows (8 of 28 runs, up to 5 deviations on run_101; stop 07 `tried_ideas.yaml`) are the result: the campaign increasingly tests approximations of ideas, the finding says so first (`nearest_build.py:15-18`), and the request file records the missing pieces with no status field and no reader that builds them (`component_requests.yaml:1-60`: run_061 and two run_070 rows name an ATR-normalised shock component; whether it was built was not checked). For autonomy: the pipeline can discover a missing piece and cannot add one; the request list is append-only, like stop 09's test requests.
5. Four documents each say they win. The skill (`SKILL.md`), NEAREST_BUILD.md ("where it differs from your skill ... this note wins", `:4`), START_FROM_CONFIG.md (same, `:4`), and quant-fundamentals ("authoritative", `:16-18`, `SKILL.md:124-126`). The live member of the quant-fundamentals file is two identities and the 0.20 band (`:28-56`, `:60-69`, `:73-92`); the rest cites the unreached verdict interpreter's Rule 4 (`:103-106`, `:154`), a provisional 15-trade floor from [holdout dates — see campaign_data_policy.yaml] on a "22-window protocol (2 symbols x 11 windows)" (`:115-129`), and run_017-era examples (`:136-150`). With the design guide (658 lines) and the catalogue (182), 1b reads about 1,350 lines of rules to copy a config (its prompt: 53,685 cache-creation tokens, stop 05a). The rules are not wrong; they are layered by date, and a model reading them resolves the layers as a person would, by the last "this note wins".
6. Replay gate and exact-config-by-code overlap. `_route_config_replay_gate` (`:17186-17220`, D-109) replays "1b's config against the brief's exact config"; with `exact_config_1b` on (D-110, `campaign_config.yaml:1008-1009`) 1b is code copying that very config (`:17136-17137`), so the gate compares a config with its own source and can fail only on a code bug. Two flags, one of which made the other a self-check. The deviation gate (off) is the opposite policy of nearest-build (on): a pause on any approximation beside a note that says approximate; one of them is weight.
7. What is sound beyond note 2: the pass-through manifest is written by code from the brief and hash-checked (`:8517-8560`), the code note appended to a patch's rationale (`:8541-8550`) keeps the text honest, deviations are bounded in count and length before they reach memory and prompts (`nearest_build.py:36-39`), and the size probe never reads a market bar (`forecast_size_probe.py:26-35`).

### (2) Legacy or simplifiable (leads)

1. `SKILL.md:34-37` (`findings_carryover.yaml`, `parameter_bracket`) and `:285-292` (replication guard, `run_type: replication_diagnostic`, `campaign_state.yaml`), with the template's optional inputs `:24-27`: inputs of the retired routing; `findings_carryover.yaml` is written only in the unreached verdict-interpreter route (`RP:20557`). Not checked: `run_context.yaml` ever carrying `replication_diagnostic` on a live run (stop 05b: it carries `forced_diagnostic`).
2. `SKILL.md:56-62` (`significance_methodology` copy rule): run_102's brief has no such key; the reader is the legacy 5a branch (`RP:20275-20276`). Not checked on the tool-only 5a.
3. `SKILL.md:108-119`: twelve lines on a field not to write (`selected_variant_id`), for a flag-off stage.
4. `quant-fundamentals/SKILL.md:96-154`: Gate A (verdict interpreter), the 15-trade floor and its update protocol, the 22-window protocol, the run_017 worked example. Keep the identities; the rest belongs in the decision log.
5. The replay gate (`:17186-17220`, `tools/config_replay.py`, flag `config_replay_gate`) under `exact_config_1b` (note 1.6); and the deviation gate (`_route_deviation_gate`, flag off) under `nearest_build` on.
6. `component_requests.yaml`: rows of three kinds in one list (parks, 5a validator failures, nearest-build deviations with `kind: deviation`), no status/closure field, three rows from runs 061-070 whose pieces may since exist. Same pattern as `test_requests.yaml` (stop 09 note 2.7).
7. CLAIM_NOTE.md (14 lines): one rule ("you decide the block kind; the mismatch is a warning"), which the skill's manifest section already implies; could be a sentence in the skill.
8. The skill's "Context rule" (`:315-317`: read only the card, the guide and the catalogue) is overridden by five further required inputs on the live path (pre-registration, quant-fundamentals, the three notes, the start config and manifest); the rule text is stale.

### (3) Disagreements between the speech and the element

1. Step 1, "Otherwise the AI (Sonnet 5.5) writes it": for a side-finding child the AI is instructed to copy the start config (`START_FROM_CONFIG.md:7-9`), which run_102 did; "writes" is the flag-off and new-block case. Omission that matters (note 1.1).
2. Step 5, "A failure sends 1b back once with the error; a second failure pauses the run": a second manifest failure raises, so the run ends `failed`, not paused (`RP:16643-16646`); a second rule or size failure pauses (`:16614-16627`); a pass-through config gets no retry at all (`:16613`, `:16636-16642`). Three outcomes, not one.
3. Step 7, the replay gate: correct as described; not stated that with `exact_config_1b` on it checks code against its own input (note 1.6).
4. Example, "kept the config and manifest unchanged": the config and the manifest's pointers, yes; the manifest's `rationale` was reworded (`block_manifest.yaml:9` vs `start_block_manifest.yaml:9-11`). Fine.
5. Section 6, "The exact-config path and the replay gate are on but were not used by run_102": correct; its brief carried `start_config`, not `constraints`.
6. Reading map "Skill `:1-317`": the file has 318 lines; CLAIM_NOTE 14 (speech 13), NEAREST_BUILD 39 (38), START_FROM_CONFIG 19 (18), quant-fundamentals 172 (171): the one-line counting difference of earlier stops. "D-149 rule ... `tools/forecast_rules.py:131-170`, rule text `:55-60`": the function is `:131-138` and `:141-168`, the sentence `:56-61`; close enough.
7. Verified as stated: `RP:3092-3115`, `:3196`, `:16775`, `:16794-16833`, `:17089`, `:18894-18959`, `:8517`, `:16587-16651`, `:16525`, `:16539`, `:5551-5596`, `:17223-17256`, `:17883`, `:18919`, `:17186-17220`, `:18930-18948`, `:6605`; `nearest_build.py:197-198`; `campaign_config.yaml:880`; the handoff template; the seven example files; `pipeline_state.yaml:61-73` (0.45 USD, 31.9 s, one turn).
