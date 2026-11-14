# Design premises verification: brief (approved by the operator, 2026-11-04)

## Purpose
During the guided tour, an inspector wrote, for every stop, a section "(1) Design and mechanism":
whether the element, run autonomously and continuously, would let the pipeline reach a profitable
automated strategy, and where not, why. These findings will weigh most in the post-tour analysis
(the direction session leads it). Each rests on factual premises ("no code reads X", "Y is refused
while Z is on", "the score is computed in-sample"). You check THOSE PREMISES against the files.
You never judge the design itself: whether a design is good stays with the direction session and
the operator.

## Repo, flag set, checkout limits, hard rules
Same as ../BRIEF.md: read its sections "Repo and flag set" and "Hard rules" and follow them
(repo /home/user/trading-bot, master 78790e5f; the tour's flag set: all `orchestrator:` flags on
except `deviation_gate`, `zero_trade_windows_not_computed`, `extra_cards_at_1a`; run_102's files and
the PC's records after run_097 are not here; read-only; never open TB/local_data/, holdout_sealed,
SR/campaign_record/composite/, SR/quarantine/; no dates from the data policy, no window labels).

## Per item
1. Read the item in the stop file's "## Inspector notes" -> "(1) Design and mechanism" section.
   Items are numbered "1.", "2." or "1.1", "1.2": use the item number as written (1.3 -> 3).
2. Split it into its factual premises (each a checkable statement about code, config, docs, records)
   and its judgment (the "so this is good/bad / cannot reach the goal" part). Restate the item in
   one line.
3. Verify every premise against the files: read the cited lines (real ones if drifted), grep for
   readers/callers/conditions, check reachability under the flag set.
4. Verdict for the item, exactly one of:
   - PREMISES HOLD: every factual premise is true.
   - PARTLY HOLD: some premises true, some false or overstated; say which.
   - PREMISE FALSE: a premise the finding depends on is false; give the correct fact with file:line.
   - PURE JUDGMENT: the item contains no checkable premise.
   - NOT CHECKABLE HERE: the premises need run data or the PC's state.
5. Do not say whether the judgment is right. You may say "the judgment no longer follows" only when
   a premise it depends on is false.

## Output
Write ONLY design_premises/p_batch_<NN>.md:

# Design premises, batch NN: stops <list>
| ID | Finding (one line) | Verdict | Premises checked: true / false (with correct fact) | Evidence (file:line, searches, hits) |
|---|---|---|---|---|
ID = <stop>-<item number>. Do not use "|" inside a cell. After the table: "## Not checked".
