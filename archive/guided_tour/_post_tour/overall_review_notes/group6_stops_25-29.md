# Group 6 notes: stops 25-29 (campaign records, campaign review, holdout, registered-but-not-reached, operator's surface)

Note taker output for the first post-tour overall review (2026-11-05). Sources: the five stop files only. Inspector part (3) skipped at every stop. Operator quotes are verbatim, spelling and typos kept.

---

## Stop 25: The campaign records

**Element.** The shared folder every run writes to and reads from: the trial ledger, the run list, the request lists, the memory and registry, the queue briefs, and the operator's rebuilt scoreboards.

**Operator themes.**
- The stop reads like one more record-and-control layer, and that repetition is itself a signal of duplicated code.
  "Again another record and control stop... "
  "I feel, if the stops are reflecting the code that we have duplicate and redundancy in the code.. to be checked. "
- The operator links the records to the deflated Sharpe they already challenged: if the DSR goes, the ledger's reason to exist is questioned too; otherwise harmonise.
  "Knowing that i challenge the deflated sharp, i would challenge the need to keep all, or to harmonize the record steps"
- No direct answer from the guide recorded at this stop.

**Inspector design themes (part 1).**
- Of about twenty files, only six are read by the loop to decide or refuse (memory, registry, queue, campaign state, confirmations, the spent list); the rest are append-only requests with no consumer, operator displays rebuilt each step, hand-kept lists or history (note 1).
- The committed records are not the operator's records: queue, run folders and the inputs decide-next and fold confirmation need live on one PC. For a campaign meant to run continuously, the loop's position (in progress, held, exhausted) is not recoverable state (note 2).
- `campaign_state.yaml` is two files in one: a live trial ledger and the header of an earlier (mid-2026) campaign plus retired lists; its identity says one campaign, its ledger spans three (note 3).
- The request files are the loop's only channel for "the engine lacks X" and nothing closes or re-reads them; the campaign cannot tell the operator which requests are still open (note 4).
- The derived displays are honest but feed nobody; they are what the operator reads (note 5). Locking is consistent except `register` (note 6).

**Inspector legacy themes (part 2).**
- Delete `campaign_state_corun_demo.yaml` (lead 2.1); delete the exclusion digest and its builder with its flag half (lead 2.2); the wishlist mechanism and its uncalled status writer (lead 2.3).
- Split the ledger out of `campaign_state.yaml`, dropping the retired header and lists (lead 2.4).
- Loop-health and schedulability are instruments from a finished halt study; one of them (or the summary) carries the same facts (lead 2.6).

**Convergence.** Agree. The operator feels duplication; the inspector counts it (six live files out of twenty) and names what to drop.

**Feeling.** Simplify. The six files the loop actually reads are the element; the rest is weight, and the ledger's fate rides on the DSR ruling.

---

## Stop 26: The campaign review (stage 12)

**Element.** A periodic step back: every six recorded runs one AI call reads a digest of recent runs and says continue, escalate, reframe or terminate.

**Operator themes.**
- Confirms the earlier feeling that this step is legacy.
  "Ok, linked to my remarks a few stop ago on the campaign review. "
  "Confirmed it seems a bit legacy, no ? "
- Keeps the idea of a periodic step back, but changes its object: from "the ideas" to "the process" (unexpected behaviour, loops, parked backlog).
  "Overall, i agree on a step back each X runs. But the step back should be on the process workflow results seeking for unexpected behavior / loop / backlog of parked elements. "
- Wants it manual, on a strong model, as an external review that stores an analysis with four parts.
  "Here it could be a simple manual AI call on complex model getting an external review on previous runs and simply providing and storing an analyzis on :"
  "/ Observations on past results"
  "/ Challenge across the workflow mechanisms "
  "/ Potential improvments on the workflows"
  "/ Suggestions of manual entries or suggestion of financial trading adaptations"
- No direct answer from the guide recorded.

**Inspector design themes (part 1).**
- The cadence and the routing are built right; every branch ends in a known state (note 1).
- In 21 runs the review has said `continue` three times, and that is the honest answer to its input: a digest of one word per run with grid counts, no reasons, no claim results, no analyst prose; the checklist asks for trends the digest does not carry (note 2).
- The one step whose job is to step back runs on the default (cheapest) model while 1a and 1b run on a stronger one (note 3).
- Its only redirecting lever, `reframe`, is held for operator approval and pinned to the asking run's protocol; `terminate` waits for an override. The autonomy valve is closed here as elsewhere (note 4).
- Skill and routing note contradict each other where the note does not override (note 5).

**Inspector legacy themes (part 2).**
- Fold the retired-routing note into the skill and drop the flag-off content (lead 2.1); drop the replaced handoff template (lead 2.2).
- Remove the older trigger and route, the wishlist pause, the legacy decision wrapper (lead 2.3); the dead switchboard cadence key (lead 2.4).
- The digest pastes about 2,500 lines of YAML to produce five words (lead 2.5).

**Convergence.** Agree on the diagnosis, and the operator goes further: the inspector shows the review cannot see a pattern from its input; the operator wants it re-aimed at the workflow itself and run by hand on a strong model.

**Feeling.** Rethink. The cadence is worth keeping; the input, the model and the object of the review all change under the operator's proposal.

---

## Stop 27: The holdout (never opened)

**Element.** The sealed stretch of market history that research never touches: one single-use final exam per idea, opened only by an operator decision, with guards in the backtester, the data feed, the viewer and the commit check.

**Operator themes.**
- The unlock machinery is too much for a check the operator can do by hand.
  "Overcomplexity for a check i can do on my own. "
- Wants a three-step manual mechanism driven from the CLI.
  "I would really simplify the mechanism into : "
  "Indicating a strategy config and the need to test on holdout"
  "Testing it"
  "Recording the results (branch 3) "
  "Having a way to do it via manual command CLI and that's it.."
- No direct answer from the guide recorded.

**Inspector design themes (part 1).**
- The seal is the pipeline's strongest invariant; each layer enforces it on its own and is tested: belt, braces and a third belt (note 1). The unlock is a careful one-way door: twelve refusal codes, record-first, result bound by hash (note 2).
- The exam has never been sat and, by the operator's own one-pager, is not ready: three tickets block the first real spend. A strategy that passed the bars would wait on a person and three fixes (note 3).
- The grid plays no part at the door; the operator is the only check that the money and the claim agree (note 4).
- The exam is one draw in one regime; a fail is terminal, so a true edge out of favour in that stretch dies, and nothing records that the exam was one regime (note 5).
- The one moment that matters most has a manual copy in it: the tool writes JSON, the orchestrator reads YAML the operator transcribes (note 7). Two enforcers spell the range in their own comments (note 8).

**Inspector legacy themes (part 2).**
- The older gate, promotion-audit path and legacy pause rows (lead 2.1); pre-reference protocols with literal holdout blocks (lead 2.2).
- One writer for the result file would remove the hand copy (lead 2.3).
- The exemption registry grows with every timestamped artifact (lead 2.4); a separate entry point for the exam would shorten the research tool's `main()` (lead 2.5).

**Convergence.** Diverge on the door, agree on the seal. The inspector values the twelve-way guard and the deny-by-default seal; the operator wants the unlock collapsed to three manual steps. Neither disputes that the seal itself must stay.

**Feeling.** Simplify. Keep the seal layers (reader, feed guard, viewer mask, commit gate); replace the unlock choreography with the operator's three CLI steps and one result writer.

---

## Stop 28: Registered but not reached

**Element.** The inventory of what the process carries but does not run: skipped stages, unloaded role sheets, old post-verdict routes, launcher branches, config sections of removed steps.

**Operator themes.**
- The legacy load is heavy and it taxes both the operator and the engineering process.
  "Lot of legacy stuff. "
  "Here again we are weighting ourself and the engineering process keeping those"
- The operator raises rebuild-from-scratch as a live option. Complete and verbatim:
  "I am even at the step of wondering if we should not even recreate a workflow from scratch knowing the amount of legacy stuff / comment / extra cleaning necessary identified over the stops.."
- No direct answer from the guide recorded.

**Inspector design themes (part 1).**
- The inventory is right and has one cause: "bypass, not delete" (D-008). It is not a correctness risk; it is a velocity tax, because every old branch has a flag-off test pinning its shape and the working rule "build only what a run asked for" makes that cost binding (note 1).
- The guards hold in code (a run landing on an unreached stage stops before spend), but not in prose: role sheets, config comments, register texts, README and summary all describe the flag-off pipeline as current (note 2).
- The fold re-run (`refold`) is refused while `variant_loop` is on, and it is on; the operator has no confirmation tool that runs (note 3).
- Only three switch decisions are real (deviation pause, extra cards at 1a, quarantine); the other 31 are history (note 4). The archived stage list's fate has been pending since 2026-08 (note 5).

**Inspector legacy themes (part 2).**
- Registry entries, skill map duplicates and closed-book input lists for unreached stages (lead 2.1).
- The 17 marked routing blocks and the old route functions (lead 2.2); launcher branches for refinement briefs, legacy continuations, split children, quarantine, and `refold`'s requirement (fix or accept) (lead 2.3).
- Five config sections, dead top keys, stale register texts (lead 2.4); five skills (1,889 lines), empty and unreached templates, eight schemas, archive folders (lead 2.5).

**Convergence.** Agree on the weight; they frame the remedy differently. The operator asks "rebuild from scratch?"; the inspector gives a per-row deletion list and names the real cost as velocity under the current rules.

**Feeling.** Remove. The inspector's list is concrete enough to delete in place; whether that is cheaper than a rebuild is the operator's whole-workflow question (see synthesis).

---

## Stop 29: The operator's surface

**Element.** What the person reads and types to steer: manual, run viewer, summary scoreboard, decision log, roadmap, session log, plan and lessons, house rules, CI gate.

**Operator themes.**
- Wants the discussion remembered, and in particular their own manual inputs stored in their words so they stop repeating themselves.
  "Happy to keep memory of our discussion. Special focus should be done on the manual input i do in the discussion session with my inputs stored by words, so that i do not repeat myself. "
- The decision log is too rich and partly conflicting or legacy.
  "Decision log is maybe a bit too rich and some might be conflicting, legacy '.."
- No direct answer from the guide recorded.

**Inspector design themes (part 1).**
- This surface is where the pipeline's missing feedback loops close by hand (no "why" in memory, claims not graded, no second candidate, stops at every pause). It works because one person reads all of it; it is the opposite of "run autonomously" (note 1).
- The one spend figure the operator sees is wrong by the analyst's cost (an estimate at a fixed rate), and the scoreboard shows retired labels: the first page stands in two eras (note 2).
- The decision log is the real memory of why, and its status column drifts (D-015 marked not built while the grid implements it) (note 3).
- The run viewer is the best-built tool: read-only, masked, loopback (note 4). The test gate is partly a documentation gate; market-data paths are tested only by hand (note 5). The manual documents both pipelines and its pointer graph is broken on the first page (note 6).
- Session log and lessons are a disciplined handover read by the next session, not by the pipeline (note 7).

**Inspector legacy themes (part 2).**
- Scoreboard: drop retired route labels and the deleted-stage section; use metered cost or drop the spend line (lead 2.1).
- `DOC_INDEX.md`: delete or maintain, with eight live pointers re-pointed (lead 2.2); manual's retired pause rows and flag-off launch text (lead 2.3).
- Decision log: audit the status column against code, or drop it and keep the where-in-code pointer (lead 2.4). Roadmap index twelve epics behind (lead 2.5); plan file whose header is history (lead 2.6).

**Convergence.** Agree on the decision log; talk past each other on the rest. The operator's remark is about memory of their own words; the inspector's is about the surface being the hand-run substitute for autonomy.

**Feeling.** Simplify. Keep the viewer, the session log and the lessons file; thin the decision log and the summary; add the operator's own-words memory they ask for.

---

## Group synthesis

### Cross-stop themes

1. **The whole-workflow weight is now the operator's main concern, and both voices see it.** [stops 25, 26, 28, 29] The operator feels "duplicate and redundancy" (25), "a bit legacy" (26), "Lot of legacy stuff" (28), a decision log "too rich" (29). The inspector gives it one cause, "bypass, not delete" (D-008), and one cost: a velocity tax on a loop that still needs changes (28 note 1). The inspector's per-row deletion leads at 25, 26, 28 and 29 are the clean-up-in-place path.

2. **The operator wants manual, simple, CLI-driven control at the moments that matter; the inspector shows the current automation at those moments is either closed or not ready.** [stops 26, 27] At 26 the operator wants a hand-run review on a strong model; the inspector shows the automated review runs on the cheapest model on an input it cannot read a pattern from. At 27 the operator wants three CLI steps; the inspector shows the exam has never been sat, waits on three tickets, and contains a manual JSON-to-YAML copy anyway.

3. **Autonomy is closed by design at every gate in this group.** [stops 26, 27, 28, 29, inspector-led] Reframe is held for approval, terminate waits for an override (26); the holdout opens only by an operator decision file (27); the only confirmation tool, refold, refuses under the live flags (28 note 3); the operator's surface is "the opposite of 'run autonomously'" (29 note 1). Against the goal (pipeline discovers, operator decides), the discovering side has fewer levers than the deciding side.

4. **The records and displays describe a pipeline that no longer runs.** [stops 25, 28, 29, inspector-led] The campaign state carries an earlier campaign's header and retired lists (25 note 3); prose everywhere describes the flag-off pipeline as current (28 note 2); the scoreboard shows retired labels and an under-counted spend, the decision log's status column drifts, the first page has dead links (29 notes 2, 3, 6). The operator reads the surface to rule; the surface stands in two eras.

5. **What the loop records is not what a reviewer, human or AI, needs.** [stops 25, 26, 29] Request files have no status or consumer (25 note 4); the review digest is one word per run (26 note 2); the lessons the pipeline keeps are one word per run while the operator's lessons live in a hand file (29 note 7). The operator's stop-29 wish, their own inputs "stored by words", and their stop-26 four-part review are both asks for richer, human-readable memory.

6. **The DSR ruling pulls on the records.** [stop 25, operator-led] The operator ties the keep-or-harmonise question for the records to their earlier challenge of the deflated Sharpe; the trial ledger exists mainly for the DSR.

### Operator remarks on the whole workflow (verbatim and complete)

Rebuild from scratch versus clean up in place [stop 28]:
"Lot of legacy stuff. "
"Here again we are weighting ourself and the engineering process keeping those"
"I am even at the step of wondering if we should not even recreate a workflow from scratch knowing the amount of legacy stuff / comment / extra cleaning necessary identified over the stops.."

Duplication across the code, to be checked [stop 25]:
"Again another record and control stop... "
"I feel, if the stops are reflecting the code that we have duplicate and redundancy in the code.. to be checked. "
"Knowing that i challenge the deflated sharp, i would challenge the need to keep all, or to harmonize the record steps"

What the operator wants to see, read or decide, and memory of their own words [stop 29]:
"Happy to keep memory of our discussion. Special focus should be done on the manual input i do in the discussion session with my inputs stored by words, so that i do not repeat myself. Decision log is maybe a bit too rich and some might be conflicting, legacy '.."

### What the operator would do differently or wants

Campaign review [stop 26]:
"Overall, i agree on a step back each X runs. But the step back should be on the process workflow results seeking for unexpected behavior / loop / backlog of parked elements. "
"Here it could be a simple manual AI call on complex model getting an external review on previous runs and simply providing and storing an analyzis on :"
"/ Observations on past results"
"/ Challenge across the workflow mechanisms "
"/ Potential improvments on the workflows"
"/ Suggestions of manual entries or suggestion of financial trading adaptations"

Holdout [stop 27]:
"Overcomplexity for a check i can do on my own. "
"I would really simplify the mechanism into : "
"Indicating a strategy config and the need to test on holdout"
"Testing it"
"Recording the results (branch 3) "
"Having a way to do it via manual command CLI and that's it.."

Records [stop 25]:
"Knowing that i challenge the deflated sharp, i would challenge the need to keep all, or to harmonize the record steps"

Decision log and memory [stop 29]:
"Special focus should be done on the manual input i do in the discussion session with my inputs stored by words, so that i do not repeat myself. Decision log is maybe a bit too rich and some might be conflicting, legacy '.."

### Note taker's reading of the rebuild question (not a ruling)

The operator asks it at stop 28; the inspector never says "rebuild" but gives the material for either answer: the guards in code are sound (27 note 1, 28 note 2), the viewer is the best-built tool (29 note 4), the seal layers are worth keeping in any version; what is legacy is listed row by row (28 part 2) and is prose, routes, templates, schemas and config, not the live six-branch run. The cost the inspector names is not the legacy code itself but the flag-off tests and the "build only what a run asked for" rule that together make deleting it slow (28 note 1). That rule, and D-008, are the two things the operator would have to change for either path.
