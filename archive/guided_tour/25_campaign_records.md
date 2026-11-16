# Stop 25: The campaign records

## Speech (verbatim)

**Stop 25 of 29: The campaign records.** Open on the side: the folder `strategy-research/campaign_record/` (listed with `ls`; its `composite/` cache is never opened), `workflow/run_campaign.py`, `workflow/run_phase1_research.py`, `tools/campaign_review_retired.py`, `tools/claim_card.py`, `tools/explore_confirm.py`.

**In one sentence.**
The campaign records are the files every run shares, kept in one folder: what was run and what it found, what is wanted and missing, what waits to run next, and how the loop itself is doing.

**Why it exists.**
A run folder knows only itself. Questions across runs need one place: how many backtests looked at the data (so a lucky best-of-many is discounted), which ideas were tried, what was missing, which brief waits for the operator.
Without it, the campaign would pay twice for a test, lose its requests, and the operator could not see it at a glance.

**What comes in, what goes out.**
- Written by the campaign runner at each step: the campaign log, the summary, the loop-health report, the schedulability report (which queue entries can run).
- Written by a run as it goes: the campaign state (the run list and the trial ledger, one row per backtest), the request lists, the claim-test coverage, the confirmations.
- Written at a run's end: the memory, the block registry, the knowledge base (stop 22); the candidate briefs (decide-next, stop 24); the review log (stop 26).
- Kept by hand: the two wishlists, the exclusion digest; one demonstration file.

**What happens here, step by step.**
1. A launch takes the campaign lock (a file saying one campaign is running). Each event (launch, done, halt, approval) becomes one dated line in the campaign log, which is only ever appended to.
2. After each change of a queue entry, the runner rewrites three reports from scratch: the summary (queue, parked and held entries, open requests, trial count), the loop-health report (halts and downtime, from the log and the runs), the schedulability report (entries ready or blocked, and for how long).
3. During a run, steps add rows to the request lists: a missing component (an indicator the engine lacks), missing data, a claim with no test. Each row carries the run. No code closes a row.
4. Each backtest adds a row to the trial ledger in the campaign state; the deflated Sharpe ratio (a Sharpe discounted for how many tries were made, stop 20) counts them. At the run's end, the run joins the run list.
5. The claim test (the idea's measurable statement, stop 09) records per run whether it was usable and measured; the fold check (does the claim hold on a fold, a fixed set of test months, it was not seen on) adds a confirmation row.
6. At the end: memory, registry and knowledge base (stop 22). Decide-next writes a candidate brief and a queue entry held for approval. If step 1a wrote several idea cards, the extras are copied to the queued-cards folder.
7. Who reads back: the idea steps see the tried ideas from the memory; the analyst (the AI reading of the backtests) sees the confirmations; decide-next (the code picking the next run) reads the memory, the active blocks, the request counts and the digest; the summary reads requests, coverage and confirmations; the run viewer reads log, state, memory and registry.

run_102's own rows are not in this checkout; the counts below are the committed copy's.

**What it costs and how long it takes.**
No AI call. Committed copy (counted with a read-only script):
Campaign state: 55 runs, 74 trial rows. Campaign log: 1,000 lines. Summary: 155 lines.
Requests: 24 component, 13 data, 6 test. Claim coverage: 23 runs. Confirmations: 4 fold rows.
Candidate briefs: 15. Queued cards: 2 folders.

**What is switched off or not used here.**
- My grep found no code reader of the loop-health file, the schedulability file or the summary: they are rebuilt each step for the operator.
- Test requests and claim coverage: my grep found no reader besides the summary.
- The exclusion digest feeds the idea steps only when no memory file exists; the campaign never runs its builder.
- The wishlists are kept by hand; the writer of their trigger status has no caller by my grep.
- The co-run demonstration file: my grep found no reader or writer.
- Four campaign-state lists (altitude history, failed families, instruments tried, components built) are written only by the retired routing.
- Not in this checkout: `compositions.yaml`, `trial_structure_key_overlay.yaml`, the lock files, `strategy-research/campaign_decision.yaml`. The `composite/` cache is ignored by git and not opened.

**Reading map.**

| Record | Written by | Read back by |
|---|---|---|
| `campaign_log.md` | `run_campaign.py:2816-2822` (`_log`, append-only) | `run_campaign.py:3184-3247` (loop health), `:3502-3592` (schedulability); `tools/run_viewer/loaders.py:464`, `:939`, `:1485`, `:1532` |
| `campaign_summary.md` | `run_campaign.py:3062-3150` (`_regenerate_summary`; requests `:3004-3060`) | my grep found no code reader (operator, stop 29) |
| `loop_health.yaml` | `run_campaign.py:3250-3373` (`_write_loop_health`, e.g. `:346`, `:4876`) | my grep found no reader of the file |
| `schedulability.yaml` | `run_campaign.py:3396-3611` (flag `schedulability_block`; `_write_schedulability`) | my grep found no reader of the file |
| `campaign_state.yaml` | `run_phase1_research.py:262-282` (load, save); `:6627-6646` (runs, `diagnostics_log`); `:12221`, `:12376` (trial rows); `:11511` (invalidation); `:284-359` (retired routing only) | `tools/campaign_memory.py:208`; `tools/deflate_sharpe.py:441-454`; `run_phase1_research.py:7752` (review cadence); `run_campaign.py:3062-3069`; lock path `:6019`; `tools/run_viewer/loaders.py:753`, `:1529` |
| `campaign_state_corun_demo.yaml` | header: synthetic E-025 S4 demonstration | my grep found no reader or writer |
| `campaign_memory.yaml`, `block_registry.yaml`, `campaign_knowledge_base.yaml` | stop 22 (`run_phase1_research.py:8859-8961`) | stop 22 |
| `campaign_review_log.yaml` | `tools/campaign_review_retired.py:161` | `run_phase1_research.py:7759-7778`, `:7797` (stop 26) |
| `candidate_briefs/` (15 files) | `run_campaign.py:5108-5120` via `tools/decide_next.py:2646`; reframe `run_phase1_research.py:7949` | `run_campaign.py:669`, `:955` (registration), `:777` (launch); `tools/decide_next.py:1111`, `:1634` |
| `queued_cards/` (run_061, run_094) | `run_phase1_research.py:8637-8740`, called `:11653` under decide-next | `run_campaign.py:2480`, `:2571`; `tools/decide_next.py:160`, `:767`; `run_phase1_research.py:17644-17687` |
| `component_requests.yaml` | `tools/campaign_review_retired.py:71-120` from `run_phase1_research.py:3059-3066` (5a), `:17242`, `:18938` (1b), `:8086` (review), `run_campaign.py:5165-5170` (decide-next) | `run_campaign.py:3004-3060` (summary); `tools/decide_next.py:1146`; park refs `run_phase1_research.py:19461`, `:19512` |
| `data_requests.yaml` | `run_phase1_research.py:6581-6600` (data gate) | `run_campaign.py:3004-3060`; `tools/decide_next.py:1147` |
| `test_requests.yaml` | `tools/claim_card.py:567` via `run_phase1_research.py:17713` (1a), `:5208` (analyst side finding) | `run_campaign.py:3004-3060` only |
| `claim_test_coverage.yaml` | `tools/claim_card.py:600` (via `run_phase1_research.py:17713`, `:17806`); `tools/claim_measure.py:370` (via `:18524`) | `run_campaign.py:3122-3126` only |
| `confirmations.yaml` | `tools/explore_confirm.py:1082` via `run_phase1_research.py:18591-18625` | `tools/analyst_memory_view.py:447`; `run_campaign.py:3128-3129` via `tools/explore_confirm.py:1125` |
| `exclusion_digest.yaml` | `tools/build_exclusion_digest.py`, by hand (no caller in RP or RC) | `run_phase1_research.py:3775-3813` (only without a memory file); `run_campaign.py:5026-5027` → `tools/decide_next.py:1576` (advisory) |
| `feed_wishlist.yaml` | by hand; status writer `run_campaign.py:1380` (no caller found) | `run_campaign.py:1190-1220`, `:1255-1270`, `:1458-1487` (review pause check, `:1744`); summary |
| `detector_wishlist.yaml` | by hand | `run_campaign.py:1176-1200`, `:1255`; no longer gates (D-052, `:1206-1220`); summary |
| `compositions.yaml` (not in this checkout) | `run_campaign.py:5336-5381` → `tools/composition.py:683` | `tools/composite_cache.py:148`; `tools/decide_next.py:1041`; `run_phase1_research.py:5848`, `:6063` |
| `trial_structure_key_overlay.yaml` (not in this checkout) | `tools/backfill_structure_hash.py --write`, by hand | `run_phase1_research.py:100-104` (DSR, D-185); `tools/structure_key.py:206` |
| `composite/` (not in this checkout; never opened) | `tools/composite_cache.py` | a backtest cache |
| `.campaign.lock` (not in this checkout) | `tools/campaign_lock.py:48`; `run_campaign.py:6014-6028` | the runner itself |
| `strategy-research/campaign_decision.yaml` (not in this checkout) | `run_phase1_research.py:8008-8043` → `tools/campaign_review_retired.py:182`; `:12053` (retired) | my grep found no reader beyond its appender |

Remarks: send them as "stop 25: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Again another record and control stop... 
I feel, if the stops are reflecting the code that we have duplicate and redundancy in the code.. to be checked. 
Knowing that i challenge the deflated sharp, i would challenge the need to keep all, or to harmonize the record steps

## Inspector notes

(Checkout note: the committed `campaign_record/` was listed and counted; `composite/`, the lock files, `compositions.yaml`, `trial_structure_key_overlay.yaml` and `campaign_decision.yaml` are absent here, as the speech says.)

### (1) Design and mechanism

1. Of the twenty files, six are read by the loop to decide or refuse: the memory (repeat gate, tried ideas, review cadence, decide-next), the registry (composition, residual IC), the queue (scheduling, ownership, R2), the campaign state (the DSR's trial ledger, the review cadence), the confirmations (the analyst's memory view) and the data policy's spent list (stop 27). The rest are append-only requests with no consumer (`component_requests`, `data_requests`, `test_requests`, `claim_test_coverage`: stops 09, 10, 16, 17), operator displays rebuilt each step (`campaign_summary.md`, `loop_health.yaml`, `schedulability.yaml`, the log), hand-kept lists (the wishlists, the digest), or history (the KB). The speech's "read by nothing in the live path" rows are confirmed by grep (`loop_health.yaml`, `schedulability.yaml`, `campaign_summary.md`: only `run_campaign.py` names them; `corun_demo`: no reader or writer).
2. The committed records are not the operator's records. `config/campaign_queue.yaml` here holds 5 entries; the tour's 76 live on the PC (stop 24a note 6). The run folders stop at run_060. So the three things decide-next needs beyond the memory (queue ownership, the source run's `proposals/`, `pre_registration.yaml`, `research_brief.yaml`, `block_manifest.yaml`: `decide_next.py:1024-1075`) and the two things fold confirmation needs (stop 19 note 1.10) are on one disk. The house rule commits `campaign_record/` per session (SR/CLAUDE.md `:119`); the queue sits under `config/` and is not named by that rule. For a campaign meant to run continuously, the recoverable state is the memory, the registry and the KB; the loop's position (what is in progress, held, exhausted) is not.
3. `campaign_state.yaml` is two files in one: the trial ledger the DSR reads (75 `trial_id` lines, 55 runs in `runs`) and a 2026-07 campaign's header (`campaign_id: rsi_mean_reversion_low_er`, `research_question: Does RSI(14) ...`, `:1-2`), with the retired lists (`altitude_history :62`, `failed_families :280`, `instruments_tried :302`, `components_built :307`, `recent_parameter_dimensions_by_family :274`, `notes :583`, `last_escalation`) written only by the retired routing (`RP:284-359`). The live writers touch `runs`, `diagnostics_log`, `trial_sharpes` and `review_every_n_runs`. The file's identity says one campaign; its ledger spans three.
4. The request files are the loop's only channel for "the engine lacks X" and none has a status or a consumer (stops 10 note 1.4, 16 note 1.4, 17 note 1.9, 09 note 1.5): 24 component rows, 13 data rows, 6 test rows, read by the summary (newest three per file, `RC:3004-3012`) and by decide-next as counts (`decide_next.py:2563-2564`). A request is filed; nothing closes it, nothing re-reads it when the piece exists. The campaign cannot tell the operator which requests are still open.
5. The derived displays are honest instruments: the log is append-only (`_log :2816-2822`), loop health re-derives halts and downtime from the log (`:3250-3262`), schedulability is behind its flag (`:3396-3410`), the summary is rebuilt from the queue, the state and the request files (`:3062-3130`). They cost one rewrite per step and feed nobody; they are what the operator reads (stop 29).
6. Three writers, three locks: the memory, the registry and the KB each take their own lock file through `campaign_memory._file_lock` (stop 22a), the confirmations through `campaign_review_retired._lock` (stop 19), the queue and the state through the campaign lock. Consistent; `register` is the one writer outside every lock (stop 02 note 1.4).

### (2) Legacy or simplifiable (leads)

1. `campaign_state_corun_demo.yaml` (104 lines): no reader, no writer; delete.
2. `exclusion_digest.yaml` (264 lines) and `tools/build_exclusion_digest.py`: read only when no memory exists (`RP:3775-3813`) and as an advisory decide-next never acts on (`decide_next.py:1576`); the campaign never runs the builder. Delete both with the `exclusion_digest_input` flag's digest half (stop 03a lead 2.3).
3. `feed_wishlist.yaml`, `detector_wishlist.yaml` and `evaluate_and_persist_wishlist_predicate` (`RC:1380-1455`, no workflow caller): the 2026-07 wishlist mechanism; read by the review's pause check only when a review writes `campaign_review.yaml` (stop 23 lead 2.2).
4. `campaign_state.yaml`'s retired lists and header (note 3): the ledger (`trial_sharpes`, `runs`, `diagnostics_log`, `review_every_n_runs`) could stand alone.
5. `test_requests.yaml` rows labelled `specialist_readers` (stop 21b lead 2.2), `claim_test_coverage.yaml`'s duplicate `tests`/`looks` lists (stop 09 lead 2.6).
6. `loop_health.yaml` and `schedulability.yaml`: E-030/E-031 instruments built for a halt study; if the study is over, one of the two (or the summary) carries the same facts.
7. Not checked: `run_viewer/loaders.py` reads named in the map; `RC:3184-3247`, `:3502-3592`; `RP:12221`, `:12376`, `:11511` (stop 18); `campaign_review_retired.py:71-120`.

### (3) Disagreements between the speech and the element

1. Section 5 counts: "55 runs, 74 trial rows" (55 verified; 75 `trial_id` lines by grep, one may be a non-row mention); "Campaign log: 1,000 lines" (verified); "Summary: 155 lines" (verified); "24 component, 13 data, 6 test" (verified); "Claim coverage: 23 runs" (verified); "Confirmations: 4 fold rows" (verified, stop 19); "15 candidate briefs" (verified); "Queued cards: 2 folders" (run_061, run_094; verified).
2. Step 3, "No code closes a row": confirmed for all four request files (greps at stops 09, 10, 16, 17).
3. Section 6: "no code reader of the loop-health file, the schedulability file or the summary": confirmed by grep. "The wishlists ... the writer of their trigger status has no caller": `evaluate_and_persist_wishlist_predicate :1380`; not re-grepped for callers here (stop 28's map says a test names it). "The co-run demonstration file: no reader or writer": confirmed.
4. Reading map rows: `RC:2816-2822`, `:3004-3012`, `:3062-3070`, `:3110-3130`, `:3250-3262`, `:3396-3410`; `RP:262-290`, `:100-104`, `:6627-6646` (stop 23), `:7752`; `campaign_memory.py:208`; `decide_next.py:1024`, `:1146-1147` (seen as `component_requests_count`/`data_requests_count` at `:2563-2564`); verified. The campaign-state writers of the four retired lists (`RP:292-343`) verified as the retired `update_campaign_state_after_run`. Everything else in the map was verified at its own stop or not opened (noted in lead 2.7).
5. Step 7, "the analyst sees the confirmations": through the memory view (`analyst_memory_view.py:447-474`); correct. "decide-next reads ... the request counts and the digest": `decide_next.py:2563-2564`, `RC:5026-5027`; correct.
