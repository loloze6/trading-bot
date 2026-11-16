# Stop 06: The folds and the research period

## Speech (verbatim)

**Stop 06 of 29: The folds and the research period.** Open on the side: `config/folds.yaml`, `tools/research_folds.py`, `config/campaign_data_policy.yaml` (key names only), `tools/run_protocol.py`.

**In one sentence.**
The folds are four fixed sets of test months; every idea is observed on one fold and confirmed on another, never on the months where it was found.

**Why it exists.**
An idea found by looking at some months of prices will always look good on those same months. Testing it there again proves nothing.
So the campaign cuts its history into separate sets of months (folds). A follow-up run of an idea must use a fold its source run did not touch.
A second need: two periods of history are kept away from research altogether, a validation period and a sealed holdout (the final, single-use test). Every place that fixes test months must refuse them.

**What comes in, what goes out.**
- In: the folds file (written by hand), and the data policy (the file that names the research period, the validation period and the sealed holdout).
- Out: a fold's windows (six test blocks) for a run's protocol; a fold drawn for a follow-up run; a refusal when a window touches a forbidden period.
- Used by: the protocol builder at run start, the launcher's pre-flight, the backtest tool, decide-next (stop 24), fold confirmation (stop 19).

**What happens here, step by step.**
1. Each fold is six blocks of exactly 4 calendar months. Fold A: six blocks in a row across 2022-2023. Folds B and C: twelve blocks across 2018-2021, shared out in turn so each fold has a block in every one of those four years. Fold D: six blocks across 2024-2025.
2. The dates of the research period, the validation period and the holdout are never written in the folds file. They come from the data policy.
3. Loading the folds checks every block: six per fold, exact 4-month tiles, no block in two folds, A to C inside the research period, nothing in the holdout. Fold D sits in the period the policy calls validation; there is no validation stage (decision D-115, a row of the decision log), so fold D is allowed there, and only as its exact blocks.
4. A run is "on" a fold when any of its windows overlaps any block of that fold, even by one day.
5. When decide-next proposes a follow-up run, it draws its fold at random among the folds the source run is not on. The draw is seeded by the candidate's name, so it gives the same answer every time and can be replayed (D-123). Folds without data for the coin are left out first. No fold left, or the source's windows unreadable: the candidate is refused.
6. Every place that fixes or uses test windows refuses one that overlaps the validation period, except fold D's exact blocks: the protocol builder, the launch pre-flight, and the backtest tool itself, which every backtest goes through.
7. The run's fold is written into its run-context file, its campaign memory entry and its trial rows.

Example: run_101 was on fold A. Its follow-up, run_102, drew among B, C and D and got fold B. run_102's own candidate follow-up drew among A, C and D and got fold C.

**What it costs and how long it takes.**
No cost: the checks read two small files.
4 folds of 6 blocks, 24 blocks in all (`config/folds.yaml`, 66 lines).

**What is switched off or not used here.**
- The `order` list (A, B, C) is kept for the file's own checks; the random draw does not read it.
- Fold D is not unseen for every idea: earlier runs tested windows in 2024-2025 (the folds file says so).
- Most keys of the data policy concern other things (data stores, a forward recorder, contamination records); they are named in the map only.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Folds file header | `config/folds.yaml:1-35` | D-085, D-123, block shape, B/C split, D-099 swap, D-115 fold D |
| Folds | `config/folds.yaml:36-66` | `version`, `order: [A, B, C]`, `folds` A (`:39`), B (`:46`), C (`:53`), D (`:60`) |
| Module doc | `tools/research_folds.py:1-43` | Where dates come from, which fold a run is on |
| Constants | `tools/research_folds.py:60-71` | Path, `FOLD_ORDER`, `FOLD_D`, 6 blocks, 4 months, label pattern |
| Policy ranges | `tools/research_folds.py:98-136` | Validation, research and holdout ranges from the policy |
| Load and check | `tools/research_folds.py:153-215` | `load_folds` refusals |
| Windows of a fold | `tools/research_folds.py:217-262` | `fold_windows`, hash, span, `load_fold_windows`, `windows_ranges` |
| Run on which folds | `tools/research_folds.py:265-269` | `folds_overlapped` |
| The draw | `tools/research_folds.py:272-321` | `draw_seed`, `draw_fold` (reasons `fold_source_unreadable`, `no_other_fold`) |
| Validation guard | `tools/research_folds.py:324-362` | `assert_windows_clear_of_validation`, fold D exception |
| Flag reader | `tools/research_folds.py:366-387` | `folds_flag_enabled` for `run_protocol.py` |
| Fold of a run | `tools/research_folds.py:389-427` | `load_validation_range`, `check_fold_id`, `fold_of_constraints`, `fold_of_run_dir` |
| Fold to windows | `workflow/run_phase1_research.py:10607-10638` | Generator picks the fold's windows |
| Launch pre-flight | `workflow/run_campaign.py:3970-3991` | Validation overlap |
| Backtest tool | `tools/run_protocol.py:2014-2150`, `:2163-2178` | Refusals before any fetch; validation guard |
| Shared-day check | `tools/holdout_policy.py:229` | `windows_overlap` |
| Policy keys (names only) | `config/campaign_data_policy.yaml:17` `burned_ranges`, `:21` `walk_forward_extension`, `:23` `holdout_range`, `:33` `backward_extension` (research period), `:48` `eras`, `:101` Kraken 19-pair ingest block, `:177` sealed Kraken store block, `:210` contaminated Binance cache, `:288` contaminated runs, `:388` forward recorder, `:535` `holdout_consumed_by`, `:542` `holdout_failure_is_terminal` | The policy's sections |
| Examples | `runs/run_102/artifacts/run_context.yaml` (`fold: B`); `campaign_record/candidate_briefs/forecast_power-run_102-2.md` (fold C, drawn among A, C, D) | A run's fold and a child's draw |

Remarks: send them as "stop 06: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop 6
validation period concept should have been deleted. That's the goal of the holdout. We should also decrease the importance of the holdout.. too much quoted in the design. Ok that's good to keep data for a confirmation test but that's it. 

At longer term, i would really like that we have pure random fold that would respect a certain set of rules. 

## Inspector notes

### (1) Design and mechanism

1. The discipline excludes the source run's fold only, not the lineage's. `draw_fold` reads `run_ranges[run_id]` for the one source run (`research_folds.py:294-299`); `_memory_run_ranges` computes every memory run's windows (`decide_next.py:1173-1187`) but the draw is handed only the source's. So: idea observed on A (run_101), child on B (run_102), grandchild on C (the waiting candidate), and the great-grandchild draws among A, B, D, two of which are the bars the idea was found and refined on. "Never on the months where it was found" holds one generation deep. The memory entry carries `fold` and the parent id (stop 22), so the lineage's folds are computable at draw time. For a loop that refines an idea over several runs, this is the point where a "confirmation" can quietly become a re-test on seen bars; whether `fold_confirm` (stop 19) re-checks lineage at confirmation was not read.
2. Fold D is the validation period and is in the draw, and the code's own text says otherwise twice: the module docstring calls the validation period "single-use" (`:19`), the `FOLD_D` comment says "decide-next never assigns it" (`:63-64`), while `ALL_FOLDS` is what the draw iterates (`:302`) per D-123 and `check_fold_id` accepts D (`:401-407`). Consequence for the goal: the period the policy still calls validation (`campaign_data_policy.yaml` header `:12-15`) is spent by ordinary child runs chosen at random, so after a few lineages only the holdout is unseen. That is the operator's D-115; the note is that the code comments teach the retired rule.
3. The folds confound out-of-sample with regime. A is six contiguous blocks of 2022-2023, D six contiguous blocks of 2024-2025, B and C interleave 2018-2021 (`folds.yaml:39-66`). A draw from A to B changes years, not only months; a refutation on B cannot separate "fit to A's bars" from "works only in A's years". Only the B/C pair samples the same years. The grid (stop 19) attributes both to the idea. A first design can accept this; the record should say which kind of fold change a confirmation crossed, and nothing here records it beyond the fold id.
4. The validation guard is behind a feature flag; the holdout guard is not. All three guard sites return silently with `orchestrator.folds.enabled` off (`RP:10645`, `RC:3976-3977`, `run_protocol.py:2171-2172`), whereas the holdout check always runs (`RP:10569`, `run_protocol.py:2140-2153`). The validation period exists in the policy whether or not the flag is on. On this checkout the flag is on in a working-tree edit of `campaign_config.yaml` (listed `M` in the session's git status) and `tests/test_e077_folds.py:814` asserts the real config's value is `False` ("shipped default"): the committed campaign has no fold discipline, the live one has it only as runtime state. For continuous autonomous running, a discipline that a config edit can switch off is weaker than the seal it sits next to.
5. The research period is keyed to one feed: `research_range_of` reads `backward_extension.BTCUSDT_1h` (`:116-125`) for every coin. Per-coin coverage is decide-next's `_fold_data_reason` (`decide_next.py:1899-1919`), whose docstring says it ignores warm-up (D-169) and aux feeds; a late-listed coin can still draw a fold whose early blocks the data gate then excludes (stop 17), and the grid's per-window floor pays for it. BTC-centric by key name, not by intent.
6. What is sound: `load_folds` refuses every deviation of shape, order, tiling and range (`:153-214`) and withholds the sealed dates in its holdout message (`:206-209`); the draw is seeded by the candidate id and refuses instead of guessing (`:272-275`, `:295-298`, `:310-313`); `fold_windows` emits the generator's exact window shape so a fold run and a hand-generated run on the same blocks share `windows_sha256` (`:217-231`), which is what lets the repeat check (stop 16) see them as the same test. The policy is the one source of the three ranges and the readers never default (`:98-136`); the only downstream copy of the sealed range is `pre_registration.yaml` (stop 04 note 1.7).
7. "On a fold" is any-day overlap (`:139-140`, `:265-269`), so an old run with monthly windows can be on two folds and a child of it loses both. Correct, and the reason D-123 needed the memory's `protocol_ref` for every run (`decide_next.py:1179-1185`): a memory run whose protocol file is gone makes every child infeasible (`fold_source_unreadable`). The protocol files live in the shared `SR/protocols/` directory, outside the run folder (stop 05b note 1.6): the fold draw depends on a directory the backup rule does not name.

### (2) Legacy or simplifiable (leads)

1. `order: [A, B, C]` (`folds.yaml:37`), `FOLD_ORDER` (`research_folds.py:62`) and the order check (`:170-171`): D-085's lineage order, replaced by D-123; now a file-shape rule only. `ALL_FOLDS` (`:67`) is the live list. Delete the key and the check. Checked: `FOLD_ORDER` is used at `:170`, `:214`, `:67`; not checked outside this module.
2. Stale comments: module docstring `:19`, `:23-27`; `FOLD_D` comment `:63-64`; `folds.yaml:1` ("the three fixed folds") and `:28`. Rewrite to D-123/D-115.
3. `fold_span` (`:234-237`): its one production caller is `decide_next.py:2620`, writing the `start`/`end` the generator ignores for a fold brief (stop 01 note 1.4). Goes with that simplification.
4. `folds_flag_enabled` (`:369-386`): a second reader of one flag, for a tool that cannot import the orchestrator; folding the flag into code removes both readers and the `test_e077_folds.py:814` pin.
5. Three parsers of the same window shape: `holdout_policy.check_windows_before` (`:201-226`), `holdout_policy.windows_overlap` (`:229-247`), `research_folds.windows_ranges` (`:249-262`); plus `RC:_windows_overlap_in` (`:3958-3967`) re-reading a file to call the second. One parser returning ranges would serve all. Not checked: `novelty.py`'s own.
6. The data policy file (545 lines) is four keys to this element (`burned_ranges`, `walk_forward_extension`, `holdout_range`, `backward_extension.BTCUSDT_1h`); the record blocks (Kraken ingest `:101`, sealed store `:177`, contaminated cache `:210`, contaminated runs `:288`, forward recorder `:388`) are read by nothing here. Which tools read them is a stop-14/27 question; by name, the forward recorder (`:388-534`) is a reserved data source no stage uses.
7. `tests/test_e077_folds.py:814` pins the real `campaign_config.yaml` to flag-off (note 1.4): with the live set committed, this assertion fails. Lead for the post-tour reconciliation of "runtime, uncommitted" flags (stop 03b note 1.3) with CI.

### (3) Disagreements between the speech and the element

1. Step 5, "among the folds the source run is not on": correct, and the one-generation limit (note 1.1) is not stated. Omission that matters.
2. Step 6 names the launch pre-flight as a guard site: `_validation_overlap_in` needs an existing protocol file (`RC:3978-3981`) and, for a fresh run with a generated protocol, is not reached (stop 04 note 3.1); on the live path the two guards that run are the generator (`RP:10709`) and `run_protocol.py` (`:2156-2179`). The speech's "every place" is the module docstring's claim (`:28-34`), true of the code's call sites, not of the live case.
3. Step 2, "The dates of the research period, the validation period and the holdout are never written in the folds file": true of the ranges; the header does name the years and one Kraken outage day (`folds.yaml:14`, `:16`, `:22-24`, `:31`). Fine.
4. Section 6, "The `order` list ... the random draw does not read it": confirmed (`:302` iterates `ALL_FOLDS`). "Fold D is not unseen for every idea": confirmed (`folds.yaml:34-35`); the speech does not add that the code comments still say D is never assigned (note 1.2).
5. Section 3, "Used by: ... fold confirmation (stop 19)": `fold_confirm.py:549` calls `fold_of_run_dir` (grep). Step 7's three writers: `run_context.yaml` (`RP:10724-10725`), memory (`campaign_memory.py:864`), trial rows (`RP:12184`): confirmed by grep.
6. Figures: "4 folds of 6 blocks, 24 blocks": correct; "66 lines": the file has 67 (the last block is line 67). Reading-map ranges verified: `research_folds.py:1-43`, `:60-71`, `:98-136`, `:153-215`, `:217-262`, `:265-269`, `:272-321` (the function ends `:317`), `:324-362`, `:366-387`, `:389-427`; `RP:10607-10638`; `RC:3970-3991`; `run_protocol.py:2014-2150`; `:2163-2178` is inside `_refuse_validation_period_windows`, which starts at `:2156`; `holdout_policy.py:229`; policy keys at `:17`, `:21`, `:23`, `:33`, `:48`, `:210`, `:288`, `:388`, `:535`, `:542` (grep of top-level keys); `:101` and `:177` taken as block headers from their indented keys at `:102` and `:178`, not read as lines. The two example files were read at stops 01 and 05b (`run_context.yaml:3` `fold: B`; the candidate brief, fold C drawn among A, C, D).
