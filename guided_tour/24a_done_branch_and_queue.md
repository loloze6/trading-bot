# Stop 24, part a: The DONE branch and the queue

## Speech (verbatim)

**Stop 24 of 29, part a: the DONE branch and the queue.** Open on the side: `run_campaign.py`, `docs/RUNBOOK.md` (approval mode), `config/campaign_queue.yaml`. Two parts: 24a, what the campaign runner does when a run ends, and how the next queue line is made and held (this speech); 24b, the decide-next tool that makes the choice (next).

**In one sentence.**
The DONE branch is the campaign's closing desk: when a run ends, it writes on the queue line what the idea became, asks decide-next what to run next, files that decision, and puts any new line on the queue, held until the operator approves it.

**Why it exists.**
The campaign chains runs by itself, the operator deciding. So each finished run must leave a closed line, a written reason for the next run, and that run waiting on the list.
Without it, a finished idea could run again, a follow-up could start with nobody able to say why, and an agent-made idea could spend money without the operator's yes.

**What comes in, what goes out.**
- In: the run's state file (where it ended); its status from the grid (the pass/fail judge: validated, refuted or inconclusive, stop 19); the queue (the campaign's to-do list of briefs, stop 02).
- Out: the line closed as done, with its outcome; a decision record in the run's folder; for a new idea, a candidate brief (a brief the pipeline writes, stop 01) and a new queue line, held.
- Next: the operator approves or rejects; the launcher (stop 04) runs it.

**What happens here, step by step.**
1. The run's loop returns; the runner re-reads its state and logs where it stopped.
2. A run parked for a missing component or data: its line is marked parked, and decide-next still runs.
3. A run stopped on a fault pauses the campaign (stop 23).
4. Two safety checks: a follow-up made by the old, retired verdict routing is never followed; and a run ending "completed, refuted" must have a status file saying refuted. Otherwise the campaign halts.
5. A new framing written by the campaign review (stop 26) goes on the queue first.
6. The line is marked done, its outcome the grid's status, citing the status file. A run that ended before the grid keeps its old outcome, marked not judged.
7. After an operator re-run on another fold (a fixed set of test months), decide-next does not run.
8. Brief bookkeeping: a brief closes when step 1a (the idea-writing step) twice in a row says nothing is left, or when two follow-up requests in a row bring no new idea.
9. Decide-next chooses (part b). For a new candidate, the runner refuses a name or brief file already taken, writes the brief, and registers the line at priority 999 (behind operator lines), as agent-written, citing the proposal and the record. If registration fails, the brief is deleted.
10. In approval mode, every line the agent makes, or would make ready, is held: "waiting for operator approval".
11. Then the decision record is saved and the queue is re-read, updated and saved. A crash before this leaves the line in progress, and the next launch redoes the decision.
12. Missing pieces a candidate waits on are filed as requests.
13. The next turn finds nothing ready and stops: "Queue exhausted ... Awaiting operator approval". The campaign summary lists held lines.
14. The operator approves with one command, under the campaign lock (one writer at a time): the line becomes ready, priority kept. To reject, the operator sets it superseded by hand. No command picks another candidate from the record.

Example: the grid called run_102 refuted (stop 19), so its line closes as refuted. Stop 02 read two lines made after run_102: trade_efficiency-run_102-1, superseded, and forecast_power-run_102-2 (a candidate id, `<lens>-<run>-<n>`: the analyst's forecast_power lens, run_102, proposal 2), held for approval. run_102's decision_record.yaml is not in this checkout.

**What it costs and how long it takes.**
No AI call and no backtest: this desk and decide-next are code.
15 candidate briefs in `campaign_record/candidate_briefs/` in this checkout (counted with ls).

**What is switched off or not used here.**
- Quarantine is off: its decide-next call is not reached, skipped at RC:4683.
- Continuing a lineage (refine, pivot, escalate) is not reached under retired routing; an old continuation halts at RC:4797-4805.
- Extra ideas at step 1a are off: no waiting extra-idea line is made.
- In this checkout the committed switch file reads decide-next, approval mode and their dependencies as off; the states here are the tour's flag set (stop 03a). Its committed queue holds 5 older lines, none from decide-next.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| After the loop | `run_campaign.py:4659-4660`; `:2901-2909` | Re-read `pipeline_state.yaml`; `STAGE` log line (`_log_transition`) |
| Park | `run_campaign.py:4662-4666` → `:4949-4994` | `_park_entry`: `paused:waiting_for_<kind>`, decision at `parked/park_<n>/decision_record.yaml` |
| Pause, quarantine | `run_campaign.py:4668-4790` | `_hard_pause_reason`; quarantine gate `:4683`; decide-next on quarantine `:4732-4737` |
| Retired-routing checks | `run_campaign.py:4792-4811`; `:295-310`; `:333-349` | Old continuation halts; `_idea_status_blocker`; `_halt_retired_routing` |
| Reframe first | `run_campaign.py:4812-4831` | Campaign review's brief registered before deciding |
| Continuation | `run_campaign.py:4832-4845` | Appends a continuation run; not reached |
| Done | `run_campaign.py:4847-4879` | Refold `:4849-4861`; decide-next `:4862-4865`; flag off `:4866-4868`; summary, `DONE`, loop health, schedulability |
| Outcome from grid | `run_campaign.py:4893-4920` | `_apply_idea_status_outcome`: `pass_rule_evaluation_ref`, or `verdict_status: ungated` |
| Approval notes | `run_campaign.py:4923-4946` | `_approval_note`, `_parked_note` on the stop lines |
| Decide and persist | `run_campaign.py:4997-5172` | `_finish_lineage_with_decision` (docstring `:5000-5011`) |
| Refold, no decision | `run_campaign.py:5014-5019` | D-122 (a row of `engineering/DECISION_LOG.md`) |
| Brief bookkeeping | `run_campaign.py:5023-5024`; `:5201-5264` | `_brief_updates`: two exhausted answers (O-20), empty-R2 streak, `[obsolete]` title |
| Inputs | `run_campaign.py:5025-5043` | Exclusion digest, component classes, feeds (lazy), composition, folds, fold data |
| Decide | `run_campaign.py:5045-5064` | `dn.load_inputs`, `dn.decide` with trigger and `_select_entry` |
| Combination (R1) | `run_campaign.py:5065-5078`, `:5099-5100`; `:5317-5452` | `_prepare_r1`, `_record_r1_failure`, `_register_r1` |
| Approval | `run_campaign.py:5079-5087`; `:3411-3438` | `_operator_approval_enabled`, `_approval_status`, `_log_awaiting_approval` |
| Extra card pick | `run_campaign.py:5090-5096` | `queued` → `ready` or held |
| More ideas (R2) | `run_campaign.py:5097-5098`; `:5267-5308` | `_apply_r2`: registers `<owner>__more_<n>` |
| Candidate | `run_campaign.py:5104-5137` | `dn.candidate_brief`; collision refusal `:5113-5116`; write `:5119`; `register_hypothesis` priority 999, `source: agent`, `origin: reader` `:5121-5128`; rollback `:5132-5134` |
| Stop, or scheduled line | `run_campaign.py:5138-5146` | `DECIDE stop` or "the scheduler runs ... next" |
| Warnings | `run_campaign.py:5147-5152`; `:5175-5194` | `_candidate_warning_lines` |
| Record, queue | `run_campaign.py:5154-5163` | `decision_record.yaml` via `save_yaml` (checked by `decision_record.schema.json`); re-read, update, save queue |
| Component requests | `run_campaign.py:5164-5170` | `component_request_rows` → `campaign_record/component_requests.yaml` |
| Queue exhausted | `run_campaign.py:4526-4535` | Stop line with held and parked names |
| Summary section | `run_campaign.py:3110-3119` | "Awaiting operator approval" table |
| Approve | `run_campaign.py:2772-2809`; CLI `:5944-5947`, `:6002-6004` | Lock, status must be `blocked_on_operator_approval`, set `ready`, `APPROVE` |
| Status constant | `run_campaign.py:148` | `OPERATOR_APPROVAL_STATUS` |
| Commands | `run_campaign.py:5931-5975` | No `pick` command |
| Runbook | `docs/RUNBOOK.md:1015-1054` | Approval mode; reject by `superseded`; reopen a brief |
| Flags (tour set) | `config/campaign_config.yaml:649`, `:699`, `:750`, `:894`, `:939`, `:1055`; quarantine `:121-141` | decide_next, verdict_routing_retired, composition_runs, folds, operator_approval, extra_cards_at_1a |

Remarks: send them as "stop 24a: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Global feeling on this one: seems a bit complex, but maybe for good. Here objective is to decide xhat's next based on the claim proposal. Again to avoid complexity, we should ensure we do not have repeated controls or overcomplexifying check that control edge case.

## Inspector notes

(Checkout note: no `SR/runs/run_102/`; the committed `campaign_config.yaml` has `decide_next`, `operator_approval`, `verdict_routing_retired` off; the committed `config/campaign_queue.yaml` holds 5 entries (4 done, 1 hand-blocked), not the 76 stop 02 read on the operator's machine. Notes judge the mechanism under the tour's flag set.)

### (1) Design and mechanism

1. The closing desk is ordered for crash safety and says so: decide on the final in-memory queue, write the brief, register it (the brief deleted if registration refuses), write the decision record, then re-read the disk queue, put the finished entry in and save (`RC:4997-5011`, `:5104-5163`). A failure before the last save leaves the entry `in_progress`, and the next step retries the decision (`:5000-5003`). Sound, with one edge: a crash between `register_hypothesis` (which saves the queue with the new candidate, `:5121-5128`) and `save_yaml(decision_ref)` (`:5154`) leaves a registered entry with no record; the retry then refuses the colliding id (`:5113-5116`) and the lineage is stuck until a person removes the entry. The docstring's promise ("no record ever claims a pick that has no queue entry", `:5010-5011`) holds; its converse does not.
2. Approval mode is the autonomy valve, and it is closed: every entry the agent creates or would make ready is held (`:5079-5087`, `_approval_status :3434-3436`), the scheduler never picks a held entry, so each run ends with "Queue exhausted ... Awaiting operator approval" (`:4923-4932`, runbook `:1027-1030`). One run per `--approve`. The operator's D-071; the mechanism is exact. The approval command works with the flag off too (`:2772-2780`), and rejection is a hand edit to `superseded` (runbook `:1043-1044`).
3. The queue's `outcome` is the grid's one word with its provenance (`_apply_idea_status_outcome :4897-4920`): validated/refuted cite `idea_status.yaml`, inconclusive cites nothing, a run that ended before the grid keeps its legacy outcome marked `ungated`. Consistent with the provenance gate of stop 02 note 1.5; and it means the queue, like the memory, remembers one word per run.
4. Brief bookkeeping can close a brief on the operator's own rejections: a `superseded` R2 request counts as an empty answer in the streak, and two in a row set `brief_status: exhausted` (`_brief_updates :5207-5264`; runbook's caution `:1044-1053`). The reopen marker exists (`brief_reopened_after`), by hand. For a loop meant to run on, "the operator said no twice" and "1a found nothing twice" are the same signal.
5. No `pick` command (D-pick gap, itinerary): to run candidate 2 instead of candidate 1 the operator supersedes 1 and waits for the next run's end, when decide-next re-ranks the pool (a superseded entry's proposal is `named` and out of the pool, `decide_next.py:2440-2441`, `:2453-2454`). The only way to trigger a new decision without a run is `retry-analyst` (stop 21b), which re-reads the run. So the operator can veto but not choose; the pipeline chooses again.
6. The committed queue is not the campaign's queue. This checkout's `config/campaign_queue.yaml` has 5 entries, all from the first campaign (`P4_ts_trend` and four done lines); the 76-entry file stop 02 read lives only on the operator's machine, like the run folders. Decide-next's ownership, R2 and exhaustion rules read that file (`:5025-5064`); the memory and the KB are committed each session (SR/CLAUDE.md `:119`), the queue is not. A restore from git gives a memory with no to-do list and no lineage ownership. Lead for stop 25 and for the operator: the queue is the one campaign record that `.gitignore`-style practice leaves on one disk.
7. A parked run also reaches this desk (`_park_entry`, stop 23), with `trigger.parked`: decide-next runs on a run that produced no grid and no proposals, so it can only pick an existing entry, raise R2 on open briefs, or stop. The campaign continues past a park on another lineage, which is the point; a park on the only open lineage ends in a stop (`decide_next.py:2540-2548`).
8. R1 (composition) is armed on the live path: `composition_runs` on in the tour's flag set (`:5028-5029`), `_prepare_r1`/`_register_r1` wired (`:5065-5078`, `:5099-5100`), and it fires when two forecast blocks share a bar size (`decide_next.py:2478-2491`). The registry holds one active block (stop 22b), so it has never fired. The operator said at stop 12 that the design of a combined-block run is not agreed; the mechanism exists, is on, and waits for a second block. Worth a ruling before the second block arrives.

### (2) Legacy or simplifiable (leads)

1. Continuation append (`RC:4832-4845`, `_LINEAGE_CONTINUATION_STAGES`), the legacy continuation blocker (`:4792-4805`), `_check_generate_protocol_has_promotion` descendants (stop 02 lead 2.1), `split_child_ids` and `_record_run_loop_children` (`:4656-4657`; sibling splits replaced by queued cards): the flag-off DONE branch.
2. The quarantine decide-next call (`:4732-4737`) and its `_QUARANTINE_OUTCOME` / `blocked_on_component:` statuses: off.
3. `_brief_updates`' `[obsolete]` tagging of legacy briefs on every decision (`:5258-5261`, `dn.needs_obsolete_tag`): a one-time migration run at every DONE.
4. Two writes of the queue per candidate (`register_hypothesis` then `_save_queue(disk_queue)`, `:5121`, `:5160`) and the collision check against `_load_queue()` (`:5112`): the registration save could be folded into the final save, which would also close the edge of note 1.
5. `decide_next_enabled` off branch (`:4866-4868`): `outcome = pending`.

### (3) Disagreements between the speech and the element

1. Step 11, "A crash before this leaves the line in progress, and the next launch redoes the decision": true, except after a registered candidate with no record (note 1), where the redo refuses. Omission that matters for an unattended loop.
2. Step 14, "No command picks another candidate from the record": confirmed (`:5931-5975`); not stated that superseding counts toward the brief's exhaustion (note 4).
3. Step 9, "registers the line at priority 999 (behind operator lines), as agent-written, citing the proposal and the record": `:5121-5128`, `AGENT_PRIORITY` (`decide_next.py:132`); correct. "If registration fails, the brief is deleted": `:5132-5134`; correct.
4. Section 5, "15 candidate briefs": verified (`ls`). Section 6, "Its committed queue holds 5 older lines, none from decide-next": verified (5 entries, 2 `source: agent` on legacy lines, no `origin: reader`).
5. Reading map verified: `RC:4659-4660`, `:2901-2909` (not opened; `_log_transition` call seen), `:4662-4666`, `:4949-4994`, `:4668-4790`, `:4683`, `:4732-4737`, `:4792-4811`, `:295-310`, `:333-349`, `:4812-4831`, `:4832-4845`, `:4847-4879`, `:4893-4920`, `:4923-4946`, `:4997-5172`, `:5014-5019`, `:5023-5024`, `:5201-5264`, `:5025-5043`, `:5045-5064`, `:5065-5078`, `:5099-5100`, `:5079-5087`, `:3411-3438`, `:5090-5096`, `:5097-5098`, `:5267-5308`, `:5104-5137`, `:5138-5146`, `:5147-5152`, `:5154-5163`, `:5164-5170`, `:2772-2809`, `:148` (stop 02), `:5931-5975`, `:5944-5947`; `RUNBOOK.md:1015-1054`; `decision_record.schema.json:7` (nine required keys not counted; the `required` line exists). Not opened: `:4526-4535`, `:3110-3119` (seen at stop 25's read), `:5175-5194`, `:5317-5452`, `:6002-6004`.
