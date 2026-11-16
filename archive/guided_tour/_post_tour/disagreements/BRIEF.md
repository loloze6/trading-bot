# Disagreements verification: brief (approved by the operator, 2026-11-04)

## Purpose
During the guided tour, an inspector wrote, for every stop, a section "(3) Disagreements": places
where the stop's speech and the element (the code, configs, docs it describes) differ: a part
described that is not there, a part left out, a wrong line, a wrong reader or writer, a wrong count.
You verify each one against the files and say who is right. The result is a list for the direction
session and the operator to rule on; a verified speech error may later get a dated "Correction"
paragraph under that stop's speech (the tour never rewrites a speech). You change nothing.

## Repo, flag set, checkout limits
Same as ../BRIEF.md (read its sections "Repo and flag set" and "Hard rules"): repo
/home/user/trading-bot, code master 78790e5f (2026-10-28); judge under the tour's flag set (all
`orchestrator:` flags on except `deviation_gate`, `zero_trade_windows_not_computed`,
`extra_cards_at_1a`), not this checkout's committed values. Not in this checkout: SR/runs/ after
run_060 (so run_102's files), the live queue and campaign records after run_097. Stops 00 to 18 were
inspected on the operator's PC where run_102 existed; claims about run_102's files are
NOT CHECKABLE HERE unless the code alone settles them.

## Per item
1. Read the item in the stop file's "## Inspector notes" -> "(3) Disagreements" section, and the
   part of the stop's "## Speech (verbatim)" (including its reading map table) that it disputes.
2. Read the element's files at the lines involved (use real lines if they drifted).
3. Verdict, exactly one of:
   - SPEECH WRONG: the speech states a fact the files contradict (wrong behaviour, reader, writer,
     count, value, on/off state).
   - SPEECH INCOMPLETE: the speech or its reading map leaves out a part of the element that matters.
   - LINE DRIFT ONLY: the speech's content is right; only line numbers or ranges are off.
   - INSPECTOR WRONG: the speech is right; the inspector misread.
   - PARTLY: the item mixes the above; say which part is which.
   - NOT CHECKABLE HERE: needs run data or the PC's state.
4. For SPEECH WRONG / SPEECH INCOMPLETE / PARTLY: write the correct fact in one or two plain
   sentences, with file:line ("Correct fact"). This is a fact, not a proposal.
5. Evidence: file:line for what you read, searches run and hit counts. Say what you did not check.

## Output
Write ONLY your file guided_tour/_post_tour/disagreements/d_batch_<NN>.md:

# Disagreements, batch NN: stops <list>
| ID | Disagreement (one line) | Verdict | Correct fact (if speech wrong/incomplete) | Evidence (file:line, searches) |
|---|---|---|---|---|
ID = <stop>-<item number as numbered in the inspector's section 3>, e.g. 05b-3. If the items are
bullets, number them in order. Do not use "|" inside a cell. After the table: "## Not checked".

## Hard rules
Read-only everywhere except your file. No git commands that change anything; no runs, backtests,
tests, pipeline scripts, hooks or servers; python3 only for read-only searching/counting. Never open,
list or glob TB/local_data/ or anything named holdout_sealed; never open SR/campaign_record/composite/
or SR/quarantine/. Never write any date from SR/config/campaign_data_policy.yaml, any protocol window
label, or any date range: fold ids (A-D) and years only. Never copy secrets. Do not edit stop files.
Facts and evidence only, no design proposals.
