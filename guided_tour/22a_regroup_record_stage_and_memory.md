# Stop 22, part a: Stage 17 regroup_record, the stage and the campaign memory

## Speech (verbatim)

**Stop 22 of 29, part a: Stage 17, the record-keeping step, and the campaign memory.** Two parts: 22a, the step itself and the memory entry it writes (this speech); 22b, the block registry, the knowledge base, the findings, the scoreboard and the registry summary (next). Open on the side: `workflow/run_phase1_research.py`, `tools/campaign_memory.py`, `workflow_artifacts/schemas/campaign_memory.schema.json`, `campaign_record/campaign_memory.yaml`.

**In one sentence.**
The record-keeping step writes one entry per run into the campaign memory (one file listing every run since the step was switched on): what was tested, how the pass/fail grid ruled, and where each result lives.

**Why it exists.**
A campaign that forgets what it tried pays twice for the same idea, and can be fooled by a lucky repeat. Later steps look here before they spend: the idea step sees the tried ideas, the variant-building step refuses a variant already tested, the analyst (the AI reading of the backtests, stop 21) sees earlier runs, and decide-next (the code that picks the next run, stop 24) chooses from it.
It decides nothing. It copies the grid's status (the pre-registered pass/fail table's verdict: validated, refuted or inconclusive) and points at the run's files.

**What comes in, what goes out.**
- In: each variant's backtest results (a variant is one version of the idea's config); the grid's status and its cells; the idea card; the trial rows the backtest step already wrote (a trial is one backtest look, counted in the campaign's trial ledger); the analyst's proposal files and recorded observations; the profit-bar results (the campaign-wide profitability bar, stop 20); the claim measurement (stop 09).
- Out: one entry in `campaign_record/campaign_memory.yaml`; in the same pass, the four records of 22b.
- Next: the run's route (the profit-bars stop, then the end at "completed" with the grid's status, stop 23); decide-next (stop 24).

**What happens here, step by step.**
1. The step runs after the backtests and the analyst. A plain program: no AI call, and the run's spending cap never stops it, so every run gets its record and its route.
2. It first looks for component errors (an indicator that failed while a backtest ran). If any, it writes a short "engineering fault" entry with the error lines, nothing else. If an earlier passing attempt of the same run left a block or a knowledge-base entry behind, it says so loudly and a person decides.
3. Otherwise it reads the grid's status and checks that it agrees with the grid's table. It runs the retune check (a regime audit may not cite strategy results) and writes the registry summary (22b).
4. It builds the full entry: the idea's name; the status and its reason; every grid cell (result, value, threshold, windows, trades) and the counts of pass, fail and inconclusive; per variant, whether it was tested, its coins, its number of windows, its config fingerprint and its trial id; the run's protocol file (its test windows); the analyst's proposal ids per lens, never their scores; the profit-bar results; the fold (a fixed set of test months, A to D); the base variant's whole-test figures; and the analyst's observations (measured, not yet a claim).
5. Order: the block registry, the knowledge base, the claim's finding, then the memory entry itself, replaced if the run is recorded again. Then the scoreboard and the findings summary. It writes no trial row.
6. The memory file is written under a lock, all at once, and checked against its schema (a warning, not a stop). A field of the retired routing is refused.

Example: run_102 (fold B, refuted by the grid, stop 19) passed through this step twice, before and after the analyst's hand retry (stop 05b). run_102's memory entry is not in this checkout. The committed copy's last entry, run_097, shows the shape: refuted, fold D, four variants tested (BTC twice, AVAX, LINK), grid counts 3 pass and 5 fail, no block ("not validated"), knowledge-base entry `grid_run_097`, a measured finding.

**What it costs and how long it takes.**
No AI call.
Committed `campaign_record/campaign_memory.yaml`: 24 entries, run_065 to run_097, 6,800 lines (counted with a read-only script).

**What is switched off or not used here.**
- The step is on with the current flags (stop 03); in this checkout's copy of the switchboard the same line reads off.
- Runs before the step was switched on are not in the memory and are never back-filled; their history is the knowledge base.
- The campaign review's whole-memory input is not used on the live path: the review started by the run counter reads a digest written by code instead (stop 26).

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Stage entry | `workflow/run_phase1_research.py:235-245` | `regroup_record` in `STAGE_CONFIGS`: a tool stage, no skill |
| Switch | `config/campaign_config.yaml:580-612`; `workflow/run_phase1_research.py:5466-5510` | `orchestrator.regroup_record.enabled`, needs the grid; `_regroup_record_enabled` (this checkout: `:581` reads `false`) |
| Route in | `workflow/run_phase1_research.py:20177-20187` | Backtests → analyst → `regroup_record` |
| Loop guards | `workflow/run_phase1_research.py:19808-19813`, `:19844-19855` | Budget breaker exemption; flag-off refusal; handoff written |
| Handoff | `workflow/run_phase1_research.py:5485`, `:8834-8856` | `specialist_readers_to_regroup_record.yaml`, written once |
| Dispatch | `workflow/run_phase1_research.py:20074-20078` | Calls the stage body |
| Stage body | `workflow/run_phase1_research.py:8859-8961` | Fault path `:8887-8920`; full path `:8921-8961`; write order `:8937-8961` |
| Checks reused by the route | `workflow/run_phase1_research.py:4568`, `:4583` | Component errors; `idea_status.yaml` |
| Retune check | `workflow/run_phase1_research.py:5288-5300` | `_check_retune_firewall` |
| Memory path | `workflow/run_phase1_research.py:8813-8823` | File path; module loader |
| Route out | `workflow/run_phase1_research.py:20576-20611` | Bars stop, unlock, refold, grid route, review (stop 23) |
| Module purpose | `tools/campaign_memory.py:1-37` | What it records, what it never does |
| Constants | `tools/campaign_memory.py:54-100` | Note on older runs, fault, profit-bar and registry reasons, `RETIRED_FIELDS` |
| Component errors | `tools/campaign_memory.py:629-669` | `protocol_component_errors` |
| Fault entry | `tools/campaign_memory.py:672-696` | `build_fault_entry` |
| Grid block | `tools/campaign_memory.py:165-187` | Cells and counts |
| Trial rows read | `tools/campaign_memory.py:208-237` | From `campaign_state.yaml`, read only |
| Variants | `tools/campaign_memory.py:290-386` | Status, coins, windows, fingerprint, trial id |
| Proposals | `tools/campaign_memory.py:389-406` | Ids and counts only |
| Observations | `tools/campaign_memory.py:408-471` | `OBSERVATION_FIELDS :419` (D-204), `analyst_observations` |
| Profit bars | `tools/campaign_memory.py:474-541` | `profit_bars_block` |
| Base book | `tools/campaign_memory.py:542-609` | `base_book_block` (D-196) |
| Full entry | `tools/campaign_memory.py:772-880` | `build_memory_entry`; fold `:861-866` |
| Load | `tools/campaign_memory.py:887-908` | Malformed file raises, never overwritten |
| Tried ideas view | `tools/campaign_memory.py:911-996` | `tried_ideas`, the 1a and step 2 input |
| Write | `tools/campaign_memory.py:999-1071` | Atomic write, lock, `upsert_memory :1051` |
| Schema | `workflow_artifacts/schemas/campaign_memory.schema.json` | 248 lines; checked at write |
| Readers | `workflow/run_phase1_research.py:3775-3813` (1a, step 2); `:9364-9412` (repeat gate, 5a); `:7759-7778`, `:7789` (review trigger, digest); `tools/analyst_memory_view.py:447`; `tools/decide_next.py:1024`; `tools/run_viewer/loaders.py:1530` | Who reads the memory back |
| Review input | `workflow/run_phase1_research.py:8995-9035` | Adds the memory to a campaign review not started by the counter |
| Committed file | `campaign_record/campaign_memory.yaml` | 24 entries; run_097 at `:6232` |

Remarks: send them as "stop 22a: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Wondering here if the record should be more structured ? Each claim with results associated or not as reference. Reference and results with grid separated. 
Run results as it own. Etc.. with a system of reference to join everything if necessary
Instead of having a big record data storage mixed with everything.

## Inspector notes

(Checkout note: no `SR/runs/run_102/`; `regroup_record` is off in the committed switchboard (`:581`). The committed `campaign_memory.yaml` (24 entries, run_065 to run_097) was read; the notes judge the mechanism under the tour's flag set.)

### (1) Design and mechanism

1. The memory is the loop's only cross-run record on the live path, and it is built to be trusted: one entry per run keyed by `run_id`, replaced on a re-run, written under a lock by atomic replace (`campaign_memory.py:999-1071`), every field a copy of a run artifact with its `ref`, retired routing fields refused (`:85-91`, `:1061-1063`), and loud refusals where a copy would lie: a tested variant without its trial row (`:228-236`), a grid that disagrees with `idea_status.yaml` (`:823-828`), a profit-bars file that does not describe the entry's own variants (`:535-541`), a validated idea that is not whole (`:830-832`). The exact key the repeat gate reads (stop 16) and the fold draw's `protocol_ref` (stop 06) come from here. This is the part of the pipeline that keeps it from paying twice for a byte-identical test.
2. What the memory remembers is a ledger, not a notebook. An entry holds the status, the cells, the variants with fingerprints and trial ids, the proposal ids (never scores, `:19-23`), the bar rows, the fold, the finding and the observations (`:812-862`). It does not hold why a run was refuted beyond the evaluator's one fixed sentence (`idea_status_reason`, identical on all 18 refuted entries), nor a parent id (lineage lives in the `hypothesis_id` string, stop 07 note 1.6), nor any analyst prose. The view the idea steps get, `tried_ideas` (`:911-996`), is id, coins, bar size, status, variant count and the five `base_*` figures. The cells and the book exist for a reader; the loop's own idea step reads a word per run (stop 07 note 1.4).
3. The committed memory shows the campaign the loop sees: 24 entries, 18 refuted, 3 validated, 3 inconclusive, no engineering fault; `fold` on 14 (the folds flag is newer than run_079); `observations` and `base_book` on none (both newer than run_097). The three validations are the three registry blocks of 22b, and the operator voided two of them because they were "graded under step-1a-picked criteria, not the brief's rule" (`block_registry.yaml:170-181`); the memory and the KB still say `validated` for run_083 and run_089, and `tried_ideas` shows that word to 1a. A void lives in the registry's `statuses` only; nothing propagates it to the record the idea step reads. The loop can be told "this validation does not count" and cannot hear it.
4. run_097's entry corrects stop 19 note 1.2: the residual-IC cell with its p-gate does run, on daily bars, where a block is registered. `forecast_ic_median` passed on three of four variants (0.043, 0.057, 0.038 against 0.02) and `residual_ic` failed on all four, two of them "not significant" (`campaign_memory.yaml:6253-6300`); the idea was refuted by the overlap criterion, not by the IC bar. Under D-014 that run and a run whose IC was negative carry the same word, `refuted`, and the same sentence; a reader of `tried_ideas` cannot tell "no edge" from "edge already held by a block". On 1h the residual cell still never runs (no block on that bar size).
5. The stage order is right for crash safety and says so (`RP:8937-8940`): registry first (its append-only conflict raises before the memory entry is replaced), then the KB entry, the finding, the memory entry, then the derived scoreboard and summary; the fault-only path writes the fault entry first and then refuses loudly, inside a try, if an earlier validated pass left a block or a KB entry (`:8898-8920`); the budget breaker exempts the stage (stop 05b). Every run that reaches this stage gets a record.
6. The three deleted reader categories are still recorded: `_proposals_block` lists all five (`:389-406`, called with `READER_CATEGORIES` at `:8925`); an old entry carries `skipped: replaced_by_analyst` for the three because the readers-era stage wrote those files (run_097 `:6354-6386`); a run after D-198 has no such file, so its three rows read `count: 0, ref: null`. The memory's shape still carries the five-reader design (21a lead 2.1).
7. The memory grows about 280 lines per run (6,800 lines for 24) and is read whole by five readers per run: `tried_ideas` for 1a and step 2 (`RP:3775-3813`), the repeat gate at 5a (`:9364-9412`), the review trigger and digest (`:7759-7795`), the analyst view (`analyst_memory_view.py:447-474`) and decide-next (`decide_next.py:1024-1075`). At the current pace that is a few thousand lines per read for a year; fine, and the 200-row cap of `tried_ideas` (`:910`) is the one bound.
8. Runs before run_065 are not in the memory and never will be (`LEGACY_NOTE :55-61`); their history is the KB's legacy entries. So the repeat gate and `tried_ideas` know 24 of 102 runs (stop 16 note 1.3), and the first 64 runs' ideas can be re-tested by the loop without a repeat warning. By design; worth saying once more here because this is the file that was supposed to end that.

### (2) Legacy or simplifiable (leads)

1. The deleted stage's shape in the live memory: the handoff name `specialist_readers_to_regroup_record.yaml` (`RP:243`), the five reader categories in `_proposals_block` (`:8925`, `campaign_memory.py:389-406`), `skipped: replaced_by_analyst` rows (note 6). Record the two lenses; keep the five only in the loader for old entries.
2. Flag-off branches kept beside the live one: `profit_bars: null` + `PROFIT_BARS_NOT_EVALUATED` (`:66-69`, `:841-843`), the single-column variant shape (`:290-305`, "variant loop off"), the "grid written before S2a" branch (`:296-298`), `LEGACY_OBSERVATION_FIELDS` (`:417-421`, pre-D-204 records), `legacy: false` on every entry (`:822`, a constant).
3. `_apply_regroup_record_context` (`RP:8995-9035`): the whole-memory input for a campaign review not started by the cadence trigger; under the retired route every review is trigger-marked, so the branch returns at `:9007-9008`. Unreached (stop 26).
4. `idea_status_reason` (`:825`) and the KB's `outcome_reason`: the evaluator's constant sentence copied twice per run into two record files. A code, not a sentence.
5. `TRIED_IDEAS_NOTE` (`:913-928`, 14 lines) is pasted into every 1a and step-2 prompt; half of it describes the `base_*` columns' null cases.
6. Not checked: `_regroup_record_enabled`'s dependency text (`RP:5466-5510`), `campaign_memory.py:542-609` (`base_book_block` body), `:629-696` (component errors, fault entry), `run_viewer/loaders.py:1530`.

### (3) Disagreements between the speech and the element

1. Step 4, "the analyst's proposal ids per lens, never their scores": the block is per reader category, five of them, with a `skipped` record where a file says so (`:389-406`; run_097 `:6354-6386`). Detail, not error.
2. Step 2, "it says so loudly and a person decides": the stale-record check raises inside a `try` whose `except` prints and continues (`RP:8912-8920`); the run then pauses for the component error itself (`:5435-5444`), and the stale block or KB entry stays. Right in effect; "loudly" is a printed line.
3. Step 6, "checked against its schema (a warning, not a stop). A field of the retired routing is refused": `:1066` and `:1061-1063`; correct.
4. Section 5, "24 entries, run_065 to run_097, 6,800 lines": verified (`:7`, `:6232`; `wc -l` 6800). Example run_097: refuted (`:6237`), fold D (`:6522`), four variants two on BTC (`:6245-6250`, `:6310-6346`), counts 3 PASS / 5 FAIL (`:6306-6309`), `registry: skipped: not_validated` (`:6388-6389`), `kb_entry_id: grid_run_097` (`:6521`), finding `measured` (`:6523-6527`): verified.
5. Section 6, "The campaign review's whole-memory input is not used on the live path": `RP:9007-9008`; correct (lead 2.3).
6. Reading map verified: `RP:235-245`, `:19844-19855`, `:8834-8856`, `:8859-8961` (`:8887-8920`, `:8921-8961`, `:8937-8961`), `:4568`, `:4583`, `:5288-5300`, `:8813-8823`, `:20576-20611`, `:9364-9412`, `:7759-7778`, `:7789`, `:8995-9035`; `campaign_memory.py:1-37`, `:54-100`, `:165-187`, `:208-237`, `:290-386` (to `:330`), `:389-406`, `:408-471`, `:474-541`, `:772-880` (`:861-866`), `:887-908`, `:911-996`, `:999-1071` (`:1051` is inside `_memory_lock`; `upsert_memory` starts `:1054`); `analyst_memory_view.py:447`; `decide_next.py:1024`; the schema's required keys (`campaign_memory.schema.json:7`, `:30`, `:43`, `:62`); `campaign_memory.yaml:6232`.
