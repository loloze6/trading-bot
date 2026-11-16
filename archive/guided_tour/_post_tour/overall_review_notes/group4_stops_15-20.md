# Group 4 notes: stops 15 to 20 (step 2, step 5a, data gate, backtest wrapper, grid, profit bars)

Note taker's remit: the extraction brief of 2026-11-05. Sources: the six stop files only. Inspector part (3) skipped. Stops 15, 16, 17 and 18 carry no operator remarks; for those the inspector is the only voice and the notes say so.

---

## Stop 15: Step 2, innovation expansion

**Element.** An AI (the cheapest model) writes three or four variants of the base strategy before any backtest: the base unchanged, one "design" variant that halves a weight, one or two "asset" variants on another coin.

**Operator themes.** No operator remarks.

**Inspector design themes (part 1).**
- The step decides what gets backtested, yet two of its three outputs are read by nobody on the live path, and most of its cost (the largest output of any stage call) goes into prose with no reader (note 1.1). The schemas for those two files contradict the skill that writes them, so every run warns and the warning is noise (1.2).
- The one design variant is a recipe (D-195: halve the modifier weight). Over three runs the campaign walked one weight ratio up and down, about 8 USD and 24 backtests each; "the campaign's exploration of a two-component idea is a weight ratio" (1.3).
- The diversity audit cannot fail in this flow yet must be written (1.4). The asset variants are the real test, and the model chose coins with care (1.4). The shape check is right-sized, but D-195 itself is enforced by prompt only (1.5).
- "Written before any backtest" holds inside a run, not across the lineage: the base of each run is the analyst's change from the last result (1.6). Step 2 caught a step-1a error and nothing acts on it because it lands in an unread file (1.7).

**Inspector legacy themes (part 2).**
- Lead 2.1: if the analyst does not read them (stop 21), delete the expanded card, the notes, their schemas and the skill sections that fill them; keep the "tried ideas" text as a field of the variant patches.
- Leads 2.2 to 2.4: the skill carries old era labels, a dead exclusion digest, a `constraints` field that now means something else, and three passages on a flag branch; "With the flag folded in, the skill is the IMPROVEMENT 07 section plus the asset rule."
- Lead 2.5: the exact-config code path is reachable only with the variant loop off, which no live run has.

**Convergence.** No operator voice; the inspector alone. The inspector sees a step that works mechanically but spends its budget and its best thinking on files nobody reads.

**Feeling.** simplify. The variant idea is sound and cheap; the deliverables, schemas and skill should shrink to the one file code reads, and the design axis deserves to be more than one fixed recipe.

---

## Stop 16: Step 5a, backtest specification

**Element.** A code-only step that turns the AI's variant edits into finished configs and protocols, validates each one, and drops any variant that is an exact repeat of something already tested.

**Operator themes.** No operator remarks.

**Inspector design themes (part 1).**
- "This is the step the pipeline needed and it is built right" (1.1): code, not a model, applies the patches, runs the engine validator per variant, freezes the protocol with its hash, resolves one coin per variant.
- The repeat gate "refuses only a byte-identical re-run" (1.2). A changed weight, coin or fold is novel by construction; the lineage of stop 15 (one weight walked up and down) passes every time. "The gate is named for a design it does not implement; 'exact-repeat check' is what it is."
- Memory starts at the regroup stage, so everything tested before it is novel to this gate; 28 of 102 runs are in memory (1.3).
- "Component requests" holds every build failure of any kind, with no status field, so the one file that could tell the operator which engine pieces are missing cannot (1.4). Every "perp" brief is in truth a spot-price backtest with futures fees and no funding; the per-variant protocol says so, the brief and memory do not (1.5).
- The route and its floors are placed well (1.6).

**Inspector legacy themes (part 2).**
- Lead 2.1: the knowledge-base advisory layer of the anti-adjacency gate reads a retired field and answered "no opinion" on every variant; keep the exact-match layer, delete the layer and rename the module.
- Lead 2.4: the variant-selection record and its route exist only for the old flow; fold the flag and both go.
- Leads 2.2, 2.3, 2.5, 2.7: small tidy-ups (path style, two symbol conventions in one index, a check called twice, refusals written to three places instead of one).

**Convergence.** No operator voice. The inspector approves of this step more than of any other in the group.

**Feeling.** keep. The core is right; the only real design gap is that the "repeat" gate protects against accidents, not against the campaign re-testing near-identical ideas, and the operator should know that when reading `repeats: []`.

---

## Stop 17: The data availability gate

**Element.** A no-AI check that, for each variant and window, the price bars and extra feeds really exist and are nearly complete before a backtest is spent on them.

**Operator themes.** No operator remarks.

**Inspector design themes (part 1).**
- Sound core: the gate uses the engine's own loader and end rule, so "available" means what the backtest means (1.1). "Good for the goal: no backtest spends on holes."
- The three-tier outcome is two tiers in practice: "refine" ("usable with care") is sent to "not tested" exactly like "decline"; "a 0.1% gap and a 100% gap produce the same `not_tested`" (1.2). The request file holds whole variants set aside for 0.2 to 4.9% missing bars, "requests nobody can act on".
- The gate is stricter than the engine it protects: a single 4-bar gap throws the whole variant out while the engine would handle it and keep running; the promised narrowing to good windows is not built (1.3). Warm-up is checked by calendar only, train windows are not checked (1.4, 1.5).
- The gate is not read-only: it builds caches with a known non-atomic writer, and for the venue in use a decline means "not in our cache", not "not obtainable" (1.7). The request file is append-only, no status, no consumer (1.9; same shape as stop 16's component requests).
- Verdict 1.10: "the gate stops false findings (good) at the price of stopping real ones ... as built it is `decline` with a kinder reason."

**Inspector legacy themes (part 2).**
- 2.1: either implement narrowing or collapse to two outcomes and delete the 5% constant.
- 2.2: the flag-off single-gate branch and its exit codes are unreachable with the variant loop on.
- 2.3: a second ambient read of the bot's config decides which cadence to measure in; both should come from the protocol.
- 2.4, 2.5: `available_feeds.yaml` is a stale duplicate nobody but step 2's paste reads; the capability table mixes a durable venue audit with "our cache" facts.

**Convergence.** No operator voice. The inspector is for the gate and against its silent removal of variants.

**Feeling.** simplify. Keep the check, collapse "refine" into one honest outcome or build the narrowing it promises, and give the request file a reader.

---

## Stop 18: Protocol execution, the backtest wrapper

**Element.** The step that runs the real backtests: each validated variant on every window of its fold in a separate process, then one trial row per variant in the ledger that feeds the luck correction.

**Operator themes.** No operator remarks.

**Inspector design themes (part 1).**
- "The wrapper is sound where it matters" (1.1): config hashed and snapshotted before any window runs, a complete refusal/failure ladder, trial rows replaced in place with the old attempt kept. "The luck-correction count cannot silently lose a look."
- The weakness is in what is written, not how it runs (1.10). Three cost figures in one record, two of them wrong for the venue, and the wrong one yields `pass: false` on every window beside the "real" `pass: true` (1.2). Two Sharpes for one trial in one row, neither labelled on the row; the ranking reads one, the profit bars the other (1.3).
- Exit-reason diagnostics are a default label (every non-end exit is "signal_flip"), so the fee-reduction advice "has no way to say which trades to remove" (1.4). PnL concentration divides by a near-zero total: "noise shaped like a finding" (1.5).
- Retired route labels are still computed and written on every window; "A reader that trusts the record must know which field is live; nothing in the record says so" (1.10).

**Inspector legacy themes (part 2).**
- 2.2, 2.3: the legacy verdict path (promote/refine/kill) is retired via two flags and three CLI switches, yet the record still carries its fields as nulls and prose, and the schema still enumerates its verdicts; the retired verdict-interpreter's inputs are computed on every run.
- 2.4: holdout mode shares a 500-line `main()` with the walk-forward loop and is never reached from the live loop; a separate entry point would shrink the research tool's surface.
- 2.6: the research cost table's only live effect is the stale 18.5 bps figure; its other blocks are "NOT yet read by any code path" by their own words.
- 2.1: a dead budget counter.

**Convergence.** No operator voice. The inspector trusts the runner and distrusts the record it leaves for the analyst.

**Feeling.** keep. The mechanism is reliable; the clean-up is to strip the record to live fields with one cost and one Sharpe each, so the analyst (stop 21) reads the truth.

---

## Stop 19: Branch 1, the grid (pass/fail)

**Element.** The code judge: it grades every pre-registered criterion on every variant and writes one status (validated, refuted, inconclusive). A second check, fold confirmation, re-measures the parent run's claim on this run's fold.

**Operator themes.**
- Theme: fold confirmation is unwanted; one fold proves the idea, it should not be reopened.
  "Disagree with fold confirmation. We build something to prove an idea on a unique fold. I do not expect the claimed idea to be reopened for "confirmation"." `[stop 19]`
- Theme: the overlap (residual-IC) criterion is unexplained complexity, suspected to come from the criterion-definition step.
  "I also do not get the point about overlap criterion applied. Again a complexity added by the criterion definition step ?" `[stop 19]`
- No "direct" answer from the guide. The inspector's note 1.11 answers the second question: the overlap criterion is added by code, not by the criterion-definition step; it is the composition machinery, and on the live loop it has graded no cell.

**Inspector design themes (part 1).**
- "The grid itself is the sound judge the speech describes" (1): malformed criteria short-circuit, FAIL dominates, three readers re-check the status; "A story cannot change the status after the fact."
- The live criterion has no significance gate while the criterion that never runs has one; the day a variant passes, the grid cannot say whether the median is noise (2).
- The status is of the idea on every coin step 2 picked, not of the idea: an asset variant can refute the base idea, and the loop "cannot tell that from 'the idea failed'" (3). "Could not tell" and "told no" reach decide-next as the same word (5).
- Fold confirmation "grades a claim and nothing acts on the grade" (6): decide-next and the block registry do not read it; "it is reopened, measured, graded, and the grade changes nothing but what the analyst reads." The looks are counted and never applied (8); the noise rule is sign-only, "useless for choosing" (9); it depends on files git does not track (10).
- The residual-IC code is built to a high standard and is "waiting for a block to be residual to" (12).

**Inspector legacy themes (part 2).**
- 2.1, 2.2: the pre-grid evaluator and its provenance roll, and the status file's routing columns, exist for a retired routing; live content is four keys.
- 2.7, 2.8, 2.9, 2.11: `explore_confirm.py` (1,214 lines) is mostly the deleted exploration route; every ledger row carries the whole rule text and window labels; "Either wire a confirmed claim into something ... or say in the docstring that it is information for the analyst"; either apply the look count or drop it.
- 2.6: the deleted "specialist readers" stage still names the live grid path.

**Convergence.** Agree on fold confirmation, from opposite directions: the operator does not want it, the inspector shows it changes nothing. On the overlap criterion they talk past each other: the operator blames the criterion step, the inspector shows it is unreached composition code.

**Feeling.** simplify. Keep the grid; remove or wire fold confirmation; keep the residual-IC code parked until a block exists.

---

## Stop 20: Branch 3, the profit bars

**Element.** The campaign's one signed definition of "profitable enough": eight thresholds every variant is graded against after its backtests, with a luck correction (deflated Sharpe), and the only door to the sealed holdout.

**Operator themes.**
- Theme: the deflated Sharpe is unneeded complexity, because the workflow already refuses to re-test an idea; and its blocking status is inconsistent.
  "Deflated sharp -- i honestly would challenge the need and complexity it brings knowing that we control we do not test an idea already generated before in the workflow.. plus if not claculated it is already a warning, why would it be blocking when calculated. " `[stop 20]`
- Theme: the branch should only test profitability of the tested variants; information-only outputs add nothing.
  "Here the branch should be simple: testing profitability over the tested variants. Step 3 / 5 / 7 (why information if not deciding, what does it add)." `[stop 20]`
- Theme: the holdout decision is the operator's own; the mechanical checks on a spend are not wanted.
  "Step 10 could persist but i do not care about mechanics checking for me: if i want to test on holdout, i would test on holdout." `[stop 20]`
- No "direct" answer from the guide.

**Inspector design themes (part 1).**
- "This is the best-guarded judge in the pipeline, and it is built to refuse rather than flatter" (1): loud loader, basis and comparator on every row, sha of the bars file stamped at grading and compared at spend, DSR recomputed on today's ledger. "For 'without fooling ourselves' this element does its job."
- The DSR's N counts repetition of a shape, not the search across shapes: the first trial of a new shape "is corrected for nothing, although the campaign chose that shape among the others it tried" (3). This bears directly on the operator's challenge: the inspector's doubt is that the correction is too narrow, the operator's that it is unnecessary.
- The grid's status does not gate the holdout spend: a refuted idea whose base clears every bar can be spent (4); "the operator is the only check that the money and the belief point the same way." The stop is "the one place in the loop where autonomy ends on purpose" and has never fired in 102 runs (5).
- The buy-and-hold row makes the bar era-dependent: the same strategy passes or fails by which fold was drawn (6). On the live loop the bars inform the next choice through five numbers of the base variant only (9).
- Bars were moved after seeing results and signed; the sha protects against a silent move, not a signed one (10).

**Inspector legacy themes (part 2).**
- 2.1: the whole v1 path (grading, promote route, portfolio metrics, 0.95 threshold, 95 lines of file header) is unreached with v2 on.
- 2.2, 2.3: four off bars kept as keys and code; a Binance-era `target_instrument_set` "consumed by neither" but required non-empty.
- 2.4: three flags plus one for a single feature; with one path the evaluator "loses a third of its branches".
- 2.6: forecast shape and window economics are computed here and again by the analyst's query; two copies of each figure per run. This is the inspector's answer to the operator's "why information if not deciding".

**Convergence.** Diverge on the DSR (operator: drop it; inspector: it is well built but corrects for the wrong thing). Agree on the information-only rows (duplicates). Diverge on the holdout mechanics: the operator wants no checks on their own decision; the inspector finds the checks are the only thing that keeps money and belief aligned.

**Feeling.** rethink. The operator wants a plain profitability test and their own hand on the holdout; the inspector finds a strong guard that is complex, era-dependent and never fired. The thresholds stay; the surrounding machinery is the question.

---

## Group synthesis

### Cross-stop themes

1. **Outputs with no reader (inspector-led; stops 15, 16, 17, 18, 19, 20).** Step 2 writes two files nobody reads (15-1.1); component requests and data requests are append-only with no status and no consumer (16-1.4, 17-1.9); the backtest record carries retired verdict fields, three costs and two Sharpes (18-1.2, 1.3, 1.10); fold confirmation is graded and nothing acts on it (19-6); forecast shape and window economics are computed twice (20-2.6). The operator's "why information if not deciding, what does it add" `[stop 20]` is the same point in their own words.

2. **Gates that guard against the wrong thing (inspector-led; stops 16, 17, 20).** The repeat gate catches only byte-identical re-runs (16-1.2); the data gate drops real variants for small gaps while promising to narrow (17-1.10); the DSR corrects for repetition of a shape, not the search across shapes (20-3). The operator's challenge to the DSR `[stop 20]` rests on the repeat gate doing what its name says; the inspector shows it does not.

3. **Falsification is of the variant set, not the idea (inspector-led; stops 15, 19).** Haiku picks the coins from coverage prose (15-1.4), unanimity across coins decides the status (19-3), and decide-next reads one word. The loop remembers "the variant set failed" as "the idea failed".

4. **Confirmation and overlap: machinery for a path that is not wired (both; stop 19).** The operator rejects fold confirmation outright; the inspector shows nothing reads its grade. The operator asks why the overlap criterion exists; the inspector shows it is composition code that has never graded a cell.

5. **Retired paths still on the live code (inspector-led; stops 15, 16, 17, 18, 19, 20).** Every stop lists a flag-off or pre-variant-loop branch that no live run can reach: exact-config step 2, variant selection, the single-gate branch, the legacy verdict and holdout mode, the pre-grid evaluator, the v1 profit bars. Folding the flags is the one clean-up every stop in the group names.

6. **Where autonomy ends and the operator wants it to end (both; stop 20).** The inspector calls the profit-bars stop "the one place in the loop where autonomy ends on purpose" and notes the grid does not gate the spend. The operator says the spend decision is theirs and wants no mechanics checking it.

### Operator remarks about the whole workflow

The operator's remarks in this group are about branches 1 and 3, not the pipeline as a whole, but two of them state what the pipeline is for and what they want to decide themselves:

"We build something to prove an idea on a unique fold. I do not expect the claimed idea to be reopened for "confirmation"." `[stop 19]`

"Here the branch should be simple: testing profitability over the tested variants. Step 3 / 5 / 7 (why information if not deciding, what does it add). Step 10 could persist but i do not care about mechanics checking for me: if i want to test on holdout, i would test on holdout." `[stop 20]`

### What the operator would do differently or wants

- Drop the deflated Sharpe, on the grounds that the workflow already refuses to re-test ideas: "Deflated sharp -- i honestly would challenge the need and complexity it brings knowing that we control we do not test an idea already generated before in the workflow.. plus if not claculated it is already a warning, why would it be blocking when calculated. " `[stop 20]`
- Drop fold confirmation: "Disagree with fold confirmation." `[stop 19]`
- Remove or explain the overlap criterion: "I also do not get the point about overlap criterion applied. Again a complexity added by the criterion definition step ?" `[stop 19]`
- Reduce branch 3 to a plain profitability test and keep the holdout decision in their own hands (quoted above, `[stop 20]`).

Stops 15 to 18 have no operator remarks; the inspector's view there is: step 2 and the data gate should be simplified, step 5a and the backtest wrapper are sound and should be kept with their records cleaned.
