# Stop 22, part b: The block registry, the knowledge base, the findings, the scoreboard and the registry summary

## Speech (verbatim)

**Stop 22 of 29, part b: The block registry, the knowledge base, the findings, the scoreboard and the registry summary.** Open on the side: `tools/block_registry.py`, `tools/grid_kb_writer.py`, `tools/claim_findings.py`, `tools/near_miss_scoreboard.py`, `workflow/run_phase1_research.py`, `campaign_record/block_registry.yaml`, `campaign_record/campaign_knowledge_base.yaml`, `engineering/roadmap/E-018/artifacts/near_miss_scoreboard.md`.

**In one sentence.**
Besides the memory entry (22a), the record-keeping step (stage 17, a program run after every run's backtests, deciding nothing) keeps four records: the shelf of proven pieces (the block registry), the campaign's notebook (the knowledge base), the claim's measured finding, and a ranked list of near misses; plus a summary of the shelf for the run.

**Why it exists.**
A piece that works must be kept in a form the campaign can reuse: the exact slice of config, the numbers it passed with, the config's fingerprint. That is a block (a proven piece of strategy). Later runs combine blocks and measure new ideas against them.
The knowledge base keeps one line per run on the idea's fate, beside the older hand-kept history. The finding and the scoreboard keep what was measured but not proven, so a failed idea is not lost.
Without them, the campaign would rediscover its own results, or reuse a piece it cannot reproduce.

**What comes in, what goes out.**
- In: the memory entry being written (22a); the block manifest (step 1b's note of which part of the config is the idea, stop 10); the tested base config; the claim measurement (stop 09); every run folder.
- Out: a block in `campaign_record/block_registry.yaml` (validated runs only); an entry `grid_<run>` in `campaign_record/campaign_knowledge_base.yaml`; a finding inside the memory entry, and the run's `findings_summary.yaml`; the scoreboard; the run's `registry_summary.yaml`.
- Next: decide-next (the code picking the next run) and the combination step read the active blocks (stop 24); variant building reads the knowledge base (stop 16); the run viewer shows both summaries (stop 29).

**What happens here, step by step.**
1. Registry summary, first: before this run's block is added, code lists what earlier runs proved (kind, indicators, bar size, coins) and how each relates to this run. Voided blocks are left out.
2. Block registry: only a validated run (the grid, the pre-registered pass/fail table, said validated) with a block manifest gets a block. Code checks the base config still has the fingerprint the backtest used, reads the manifest's slice from it, and checks every grid cell passed. The block holds the slice, its market state, the criteria and numbers passed, the coins tested, its source. The file is append-only: code never edits or removes a block, and a different block for the same run stops with an error. A refuted or inconclusive run, a combination run or an operator re-run gets none, with the reason in the memory.
3. Status: the operator voids or reactivates a block with a separate command; the last status record counts.
4. Knowledge base: one entry per run without an engineering fault: the idea, the run, the grid's status and reason, and for a validated or refuted run a pointer to its status file. It never merges into an older entry. Every entry is re-checked before the write; the derived views (coverage by mechanism, banned mechanisms) are recomputed.
5. Finding: the claim (the idea's measurable statement, stop 09), its tests, the effect sizes per variant and a status, labelled "measured, not proven". It never bans, routes or changes the status. The findings summary lists every finding in the memory, newest first.
6. Scoreboard: rebuilt from every run folder, ranking runs by how close they came to passing. An error is printed; the run continues.

Example: run_102 was refuted (stop 19), so by the registry's rule it got no block; its grid skipped the overlap measure as no block is registered on its bar size. run_102's knowledge-base entry is not in this checkout. Its findings summary listed 26 findings (stop 09).

**What it costs and how long it takes.**
No AI call.
Block registry, committed copy: 3 blocks; 1 active (run_084), 2 voided by the operator.
Knowledge base, committed copy: 43 findings, 24 of them grid entries (18 refuted, 3 inconclusive, 3 validated); no banned mechanism.
Scoreboard, committed copy: 59 run folders scanned (all counted with a read-only script).

**What is switched off or not used here.**
- My grep found no reader of the scoreboard on the live path: only the verdict-interpretation stage's instruction sheet names it, and that stage is not reached under the current flags.
- My grep found no reader of `findings_summary.yaml` or `registry_summary.yaml` besides the run viewer.
- The older knowledge-base writer runs only on the retired routing.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Stage calls | `workflow/run_phase1_research.py:8876-8882`, `:8937-8961` | Summary first; then registry, KB, finding, memory, scoreboard, findings summary |
| Registry summary call | `workflow/run_phase1_research.py:5303-5320` | `artifacts/registry_summary.yaml`, before this run's block (D-198: the viewer reads it) |
| Registry summary | `tools/block_registry.py:449-458`, `:623-695` | Earlier blocks, relation to this run; grouped by type above 50 |
| Registry rules | `tools/block_registry.py:1-60` | Validated, manifest, append-only; statuses (D-125) |
| Load, active view | `tools/block_registry.py:105-197` | `load_registry`; voided left out (`load_active_registry :194`) |
| Status command | `tools/block_registry.py:199-216`, `:698-719` | `set_status`; `python tools/block_registry.py status ...` |
| Build a block | `tools/block_registry.py:288-348` | Fingerprint check, manifest check, numbers |
| Append | `tools/block_registry.py:355-383` | Lock; a changed re-run refused |
| Record a run | `tools/block_registry.py:394-446` | `record_run`; skipped: `not_validated`, `no_manifest`, `composition`, `refold` |
| Registry path | `workflow/run_phase1_research.py:8964-8966` | `campaign_record/block_registry.yaml` |
| Registry file | `campaign_record/block_registry.yaml` | `blocks :4-162`, `marks :163-168`, `statuses :169-187` |
| Registry schema | `workflow_artifacts/schemas/block_registry.schema.json` | 114 lines; checked at write |
| Registry readers | `tools/decide_next.py:1068`; `tools/composite_cache.py:451`; `workflow/run_phase1_research.py:5837-5850`, `:6137-6141`; `tools/run_viewer/loaders.py:720-728` | Combination, overlap measure, viewer |
| KB writer | `tools/grid_kb_writer.py:1-46`, `:70-93`, `:121-167` | Rules; `build_kb_entry`; `write_kb_entry` |
| KB views | `workflow/run_phase1_research.py:12567-12616` | `coverage_matrix`, `exhausted_mechanisms` (D-055) |
| Older KB writer | `workflow/run_phase1_research.py:12619`, called `:16255` | Retired routing only |
| KB file | `campaign_record/campaign_knowledge_base.yaml` | `findings :46`; `grid_run_097 :1678`; `coverage_matrix :1825`; `exhausted_mechanisms :2002` |
| KB readers | `workflow/run_phase1_research.py:9364-9412` (5a repeat gate); `:7826-7850`, `:8097` (campaign review); `workflow/run_campaign.py:3072-3076` (summary count) | Who reads it back |
| Finding | `workflow/run_phase1_research.py:18630-18689`; `tools/claim_findings.py:1-34`, `:296-385` | `_claim_finding`, `build_finding`; information only |
| Findings summary | `tools/claim_findings.py:432-458`; reader `tools/run_viewer/loaders.py:1352` | `artifacts/findings_summary.yaml` |
| Scoreboard | `workflow/run_phase1_research.py:8969-8990`; `tools/near_miss_scoreboard.py:1-60`, `:765-806` | Rebuild; never fails the stage |
| Scoreboard files | `engineering/roadmap/E-018/artifacts/near_miss_scoreboard.md`, `.yaml` | Ranked table |
| Scoreboard's named reader | `workflow/run_phase1_research.py:9918` | `verdict_interpreter` handoff, not reached |

Remarks: send them as "stop 22b: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Same remark. We should sit and review if each element stored is succesfully tagged and identified in a structured way. 
The block logic (validated claim) is partially developed if i am not wrong.

## Inspector notes

(Checkout note: no `SR/runs/run_102/`; the committed registry, KB and scoreboard files were read; `run_viewer/loaders.py` lines were not opened.)

### (1) Design and mechanism

1. The registry is built honestly: a block only from a `validated` grid of a run with a manifest and no fault (`block_registry.py:394-446`), the tested base config re-hashed against the trial row's `forecast_hash` (`:300-308`), the manifest resolved with 5a's own checker (`:311-313`), every cell re-verified `PASS` (`:316-322`), append-only with a conflict that raises before the memory entry is replaced (`:355-383`, `RP:8937-8940`), voiding by the operator with a reason and a name (`:199-216`), and every composition reader taking the active view (`:194-196`). The product shelf cannot be edited by code and cannot hold a block whose config changed after its backtest.
2. The shelf after 102 runs: three blocks on daily bars, two voided by the operator ("graded under step-1a-picked criteria, not the brief's rule", `block_registry.yaml:170-181`), one active (run_084) whose status record reads "criteria: D-108 read by hand" (`:182-186`). So the campaign's one proven piece was confirmed by the operator's reading, and the two automatic validations were struck by the operator's reading. Nothing in the registry re-grades a block when the criterion rule changes; the registry's `marks` note (`:163-168`) and `statuses` are the operator's hand. For autonomy: the shelf is correct because a person audited it, and the memory and KB do not know (22a note 3).
3. A block is "usable on any coin" (`:48-50`; `symbols_tested` is informational, card F). A daily SMA block validated on BTC enters composition (stop 24b R1) and the residual-IC composite (stop 19) for any coin without having been tested on one. A design choice, recorded; its consequence is that composition would combine pieces whose cross-coin behaviour is unmeasured.
4. The KB's grid entry is nine fields (`grid_kb_writer.py:70-93`): outcome = idea_status, provenance through `idea_status.yaml`, and every write re-validates every finding's provenance (`:150-158`), so a hand-typed verdict cannot enter. The derived views are empty of information for these entries by construction: `coverage_matrix` is keyed on `edge_source_category`, which the grid writer never sets, so every grid entry files under `unclassified` (`RP:12578-12591`; `campaign_knowledge_base.yaml:1825-1845`); `exhausted_mechanisms` requires `exhausted: true` plus three runs of evidence or an approved veto (`:12593-12615`), which no grid entry carries, so it is `[]` (`:2002`) and will stay so. The "banned mechanism" mechanism the speech names cannot fire from the live writer.
5. Two generations share the KB: 24 grid entries (`legacy_schema: false`) and the older entries with `mechanism`, several `evidence_runs`, `supplementary_evidence` and prose (`:46-60`), plus `meta_findings` (`:1689`) and `operational` (`:1802`). The old entry says "Keltner mean-reversion in a trending regime, no edge, four runs"; the new one says `grid_run_097 refuted`. The notebook became a ledger when the writer became code; knowledge density per run fell. Nothing on the live path reads the KB for a decision: the repeat gate's Layer 1 (`RP:9410-9412`, stop 16 lead 2.1), the review's optional input (`:7850`), the summary's count (`RC:3072-3076`).
6. The finding (`claim_findings.py:296-385`) is honest and bounded: measured / no events / not measured / stale, the approximation block first (`:367-371`), numbers only from this attempt's bars (`:25-32`), and the summary's `same_spec_hash` "for information, never a ban" (`:450-456`). Its readers are the memory view (stop 21a) and the viewer. Stop 09 note 1.2 stands: a measured finding is never compared with its own `pass_if`.
7. The scoreboard is rebuilt from every run folder on every run (`RP:8976-8990`; 59 folders in the committed table), ranks by the retired `verdict_interpretation.yaml`'s margins (`near_miss_scoreboard.md:7-15`, denominators `:19-25`), its firewall test was removed (`near_miss_scoreboard.py:12-20`), and its one named reader is the unreached verdict-interpreter handoff (`RP:9918`). The idea step it was built for (1a) does not receive it. A disk scan per run for a file nobody reads.
8. The registry summary (`registry_summary :623-695`) is written per run before the run's own block is registered (`RP:5303-5320`), with a `relation_to_this_run` for the readers D-198 deleted; the viewer is its reader (`RP:5305`). Same shape as the scoreboard: a per-run artifact for a display.
9. A caution on the KB write: `write_kb_entry` re-validates provenance of every existing finding (`:150-158`), and a gated legacy finding cites a `pass_rule_evaluation_ref` under a run folder (`:16-21`, run_059); whether `resolve_evaluation_ref` reads that file from disk, so that a missing old run folder would refuse every new KB entry, was not traced. If it does, the KB write depends on folders git does not track (SR/CLAUDE.md `:118`).

### (2) Legacy or simplifiable (leads)

1. `_write_kb_findings_entry` (`RP:12619`, called `:16255`): the retired writer. `_recompute_kb_views` (`:12567-12616`): views keyed on fields the live writer never sets (note 4). Either the grid entry gets a category and an exhaustion rule, or the two views and `KB_VETO_MIN_EVIDENCE` go.
2. `near_miss_scoreboard.py` (830 lines), `_write_near_miss_scoreboard`, the E-018 artifacts: unreached reader, retired ranking key, a scan of `runs/` per run (note 7). Delete, or re-point to the grid's margins (`:430`, `:555` already parse a grid row) and give it a reader.
3. `registry_summary`, `_write_registry_summary`, `RELATIONS`, `GROUP_BY_TYPE_ABOVE` (`:449-458`, `:623-695`, `RP:5303-5320`): built for the readers; viewer-only now.
4. Composition fields on a block and `_composition_fields` (`:28-35`, `:343-347`): for compositions that have not run; `marks` (`block_registry.yaml:163-168`): a hand note outside the status mechanism; not checked against the registry schema.
5. The KB's `verdict_status_legend` (`:10-45`, 36 lines of 2026-07 history), `amended_by`, `meta_findings`, `operational`: a record file carrying its own changelog; the legacy entries' free fields (`mechanism`, `supplementary_evidence`) have no writer today.
6. `findings_summary.yaml` written into every run folder (`claim_findings.py:432-458`, `SUMMARY_MAX_ROWS`): the same campaign-wide summary rewritten per run; one campaign file, or the viewer reading the memory, would do.
7. `_claim_flag_or_none` gating the finding (`RP:8952-8954`, `:8959-8960`): the `claim_tests` flag's off-path.

### (3) Disagreements between the speech and the element

1. Step 4, "the derived views (coverage by mechanism, banned mechanisms) are recomputed": recomputed, and empty of information for every grid entry (note 4). The speech's "no banned mechanism" in section 5 is a structural fact, not a finding.
2. Step 6, "ranking runs by how close they came to passing": by the retired verdict file's margins first; a run without one falls to the last tier by run id (`near_miss_scoreboard.md:7-15`). Under the live flags no run writes that file, so new runs cannot rank. Omission that matters for a "ranked list of near misses".
3. Section 5 counts: "3 blocks; 1 active (run_084), 2 voided": verified (`:5`, `:63`, `:116`, `:170-187`). "43 findings, 24 of them grid entries (18 refuted, 3 inconclusive, 3 validated)": 24 `grid_run_` ids and 24 `legacy_schema: false` verified; the file has 46 `id:` lines across `findings`, `meta_findings` and `operational`, so 43 under `findings` is plausible and not recounted; the status split matches the memory. "59 run folders scanned": the committed table says 59 (`:19`).
4. Section 6, "no reader of the scoreboard on the live path", "no reader of `findings_summary.yaml` or `registry_summary.yaml` besides the run viewer": confirmed by grep (`run_viewer/loaders.py:1352`, `:1527`; `RP:9918` for the scoreboard).
5. "Example: ... its grid skipped the overlap measure as no block is registered on its bar size": consistent with `_residual_ic_exempt_reason` (stop 19) and the registry (all three blocks on `1d`, `:161`); not checkable on run_102 itself.
6. Reading map verified: `RP:8876-8882`, `:8937-8961`, `:5303-5320`, `:8964-8966`, `:8969-8990`, `:12567-12616`, `:12619`, `:16255`, `:7826-7850`, `:8097`, `:9918`, `:18630-18689`; `block_registry.py:1-60`, `:105-120`, `:190-216`, `:288-348`, `:355-383`, `:394-446`, `:449-458`, `:623-695`, `:698-719`; `grid_kb_writer.py` whole; `claim_findings.py:1-34`, `:296-385`, `:432-458`; `near_miss_scoreboard.py:1-60`, `:765-806`; `decide_next.py:1068`; `composite_cache.py:451`; `RC:3072-3076`; registry file `:4-162`, `:163-168`, `:169-187`; KB `:46`, `:1678`, `:1825`, `:2002`. Not opened: `RP:5837-5850`, `:6137-6141`, the registry schema, `run_viewer/loaders.py`.
