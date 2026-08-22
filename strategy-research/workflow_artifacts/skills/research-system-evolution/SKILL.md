---
name: research-system-evolution
description: Steps back from doing research to ask what capability the research SYSTEM is missing so it can autonomously find a profitable, tradeable strategy. Use at strategic checkpoints -- "what should we build next", "the workflow isn't finding anything", "is there a feature filling a long-term gap" -- NOT for running, tuning, auditing, or re-grading strategies. Produces durable capability proposals, never one-shot fixes.
---

# Research System Evolution

## Mission

Improve **the machine that finds strategies**, not the strategies.

Every output is a proposal for a durable capability -- information or logic the
system lacks -- that makes **every future run** better. The end state this
serves: a workflow that finds, validates, and promotes a profitable, tradeable
strategy with **less operator intervention each iteration**. If a proposal's
benefit is consumed once, it does not belong here.

## At a glance

The seven filters, one line each -- full definitions below:

- **F1 DURABILITY** -- benefit lasts across every future run (one-shot effort passes, one-shot benefit fails)
- **F2 BINDING CONSTRAINT** -- unblocks what is stuck today, or defer out loud with a revisit condition
- **F3 INSTRUMENT SHAPE** -- a standing measurement the loop consumes; every ad-hoc script you ran is a candidate
- **F4 EVIDENCE CLASS** -- MEASURED / RECORDED / INHERITED / INFERRED, labelled; the constraint itself needs a primary-artifact measurement
- **F5 PROMOTION PATH** -- a win must be able to reach production and a tradable venue
- **F6 AUTONOMY** -- less operator work per run, never more
- **F7 MECHANISM TEST** -- attack your own causal story before presenting it; every count states its denominator ("36 of 59") and reconciles against the most exhaustive enumeration, not the log you happened to have open

Output always ends with five sections: candidates (each with a pre-registered
success signal), instrument candidates from your own working, board actions on
existing epics, deferrals (each with a revisit condition), one recommendation.

## Portability

This file is the reusable method. Anything marked **[LOCAL]** is calibration
from the project where it was written (a crypto strategy-research loop) --
rewrite those parts when porting this skill to another agent or project.
Everything unmarked is the method itself; port it unchanged.

## Altitude: the single most important rule

You are **not** the researcher. You do not run backtests to find edge, tune
parameters, re-grade past verdicts, or fix old results.

You reason about **why the system as built cannot yet find profit**, and what
must be added so it can.

> Operator, 2026-08-21: *"here you are deep diving into old results, and acting
> as per the research-workflow. i do not want this. but to step back and see
> what we need to do next?"*

When you notice yourself doing research, stop. Ask instead: *what capability
would have made that research unnecessary, automatic, or trustworthy?*

The boundary, precisely: measuring the system's primary records to explain the
SYSTEM'S behaviour is this skill's job (F4's floor requires it). Judging,
tuning, or proposing strategies from those same records is the researcher's job
and off-limits (A1). The same bars.csv can serve either -- what question you are
asking of it decides which side you are on.

## When NOT to use this skill

- Object-level work -- designing a hypothesis, choosing a search direction,
  interpreting one run's result -- belongs to the workflow's own stages.
  **[LOCAL]** routing here: `hypothesis-design`, `campaign-review`,
  `verdict-interpreter`.
- A direct operator instruction to fix, re-run, or re-grade past results is not
  yours to refuse -- but it is outside this skill. Say so plainly, then either
  do it outside the skill or offer the durable version (F1) and let the
  operator choose.

## The seven filters

Every candidate must pass all seven, in writing. State the verdict for each.

### F1 -- DURABILITY. Does this improve every FUTURE run?

One-shot benefit is disqualifying, however valuable it looks.

> Operator: *"i do not want you to act on past results: audit, change, etc.. it
> would only bring benefit one shot on missing info that would last at new run.
> the past proposal should be switched to: 'is there a feature that need to be
> added that is filling an identified gap of info or logic long-term'?"*

**One-shot refers to the benefit's lifetime, not the effort's.** A one-time act
with a permanent consequence -- a decision that unblocks a chain for good, a
feed wired once and used forever -- passes. A one-time answer that goes stale
with the next run -- an audit, a retro-grade -- fails.

**The distinction that makes this workable:** past data is *read-only evidence
used to identify the gap*. It is never a work item. Reading a recorded failure
field to learn what the system cannot see = allowed and encouraged. Proposing to
re-audit, re-grade, or re-run that history = rejected.

### F2 -- BINDING CONSTRAINT. Does this help escape the CURRENT dead end?

A genuinely good improvement that does not address what is blocking progress
right now must be **explicitly deferred, with the reason stated** -- not silently
included because it is best practice.

> Operator: *"today we have only strategies failed, developing slippage is
> important but would not help putting us out of this dead end"*

Slippage modelling makes bad numbers more accurately bad. When nothing passes,
higher-fidelity costs change no decision. Correct, valuable, and deferred.

Ask literally: *if this shipped tomorrow, would anything that is currently stuck
become unstuck?* If no -> defer and say so.

**Deferral is a verdict about today, not forever.** Keep deferred items on a
revisit list keyed to the constraint that deferred them, and re-run this filter
when the constraint changes. (The day one strategy passes, slippage stops being
deferrable and may become the binding constraint.)

### F3 -- INSTRUMENT SHAPE. Can this be a standing measurement instead of an investigation?

This is the highest-leverage transformation available to you.

A one-time diagnostic ("let's check whether regime gating is strangling sample")
is worth one answer. The same insight built as a **standing instrument** ("every
run reports gating quality automatically") is worth an answer on every run
forever, and it catches the regression the one-time check cannot.

> Operator: *"an epic allowing to check for all new run the regime gating
> quality"*

**An instrument only the operator reads leaves the loop as blind as before.**
Wire it into the workflow's own decisions wherever possible -- e.g. a verdict
stage that can return "starved / not evaluable" instead of "refine" because the
instrument told it so. Report-only is the fallback, not the goal.

**Whenever you find yourself proposing an investigation, try to convert it into
an instrument before presenting it.** If it cannot be converted, say why.

#### F3's blind spot: it audits your proposals, not your own working

The rule above fires on things you are about to *recommend*. It does not fire on
the dozen things you *did* to reach the recommendation -- and those are where the
missing instruments actually show up.

> Operator, 2026-08-21: *"here for example you propose an epic as soon as you
> found interesting data manually while doing analysis, and it could be useful to
> integrate it into the run workflow."*

**Standing rule: every ad-hoc computation you run against project data is a
candidate instrument, and the script you wrote is its specification.** If you had
to compute something by hand to answer a question, that is direct evidence the
system cannot answer it. Keep a running list as you work -- one line per
measurement: what you asked, what you ran, what it returned.

Before presenting, review that list and promote the ones that clear all three:

1. **It changed a conclusion.** A measurement that only confirmed what you
   already believed is not automatically worth shipping.
2. **The next session would need it again.** If you would rewrite this script
   cold in a month, so would anyone else.
3. **The loop can consume it, not only a human.** Otherwise it is a report, and
   F6 applies -- say so and rank it lower.

Do NOT promote everything you ran; that is A6 (good-practice creep) wearing a
new hat. A list of twenty instrument candidates is the same as none. Promote the
ones that pass all three and say plainly why the rest did not.

**Writing the same throwaway script twice is not a workflow quirk. It is the
finding.**

### F4 -- EVIDENCE CLASS. Label every load-bearing claim.

Tag each as one of:

- **MEASURED** -- you executed something and read the output. Quote it.
- **RECORDED** -- read from an existing artifact (verdict file, ledger, config).
  Quote it and cite the file.
- **INHERITED** -- asserted by project docs/notes but not verified by you.
  Say so. Inherited beliefs are hypotheses, not facts.
- **INFERRED** -- your reasoning from the above. Mark it plainly.

> Operator: *"your proposal of improvments idea should be coherent and based on
> fact, not assumptions"*

The classic failure: dressing an INHERITED belief ("breadth is where the edge
is") as a justification, when the real support is a MEASURED fact ("test count
multiplies ~10x"). Same proposal, honest reason.

**Floor: the constraint you name must rest on at least one MEASURED claim, and
that measurement must come from PRIMARY artifacts.** A system's verdict files,
ledgers, epics and status notes are its account of *itself*. They tell you where
to look; they never tell you what is true. A constraint assembled entirely from
RECORDED summaries inherits every misattribution those summaries contain --
which is the exact failure this project has already made, twice, in the episode
below.

**[LOCAL]** primary here means: per-bar records (`runs/*/results/*/bars.csv` --
forecast, regime, allocation before/after, approval flag), and the engine source
that produced them. Secondary means verdict YAML, `TRIALS.csv`, epics, ledgers.
If you cannot measure, say the constraint is UNVERIFIED and name the measurement
that would settle it. Do not upgrade it by confidence.

**[LOCAL]** that list is calibrated for questions about a STRATEGY's signal
quality. A different class of question -- how much has the SYSTEM itself done,
how often does it stall, how fast does it run -- has a different primary
record, and picking the wrong one is a live failure mode, not a hypothetical
one (see F7's Source coverage check). For system-history questions, primary
means the exhaustive per-unit enumeration: every `runs/run_*/pipeline_state.yaml`
(one per run, whatever drove it), or a raw `runs/` directory listing -- NOT
`campaign_record/campaign_log.md`, which is one orchestrator's own append-only
log and only covers the era after that orchestrator existed. A hand-maintained
log is secondary evidence for a system-history claim even though it is a
primary artifact for reconstructing what that orchestrator itself did.

### F5 -- PROMOTION PATH. If this succeeds, can the result ever be traded?

A capability that produces unpromotable results is worth less than it looks.
Check that a win can actually reach the production engine and a tradable venue.
If it cannot, the missing promotion path IS the higher-priority proposal.

### F6 -- AUTONOMY. Does this reduce the operator's per-run involvement?

The goal is a workflow that finds a profitable strategy **autonomously**. A
capability that adds a recurring manual step -- a report someone must remember
to read, a checklist someone must fill in per run -- moves away from that goal
even if it passes every other filter. Prefer capabilities the loop consumes
itself. Reserve human decision points for judgment the operator has explicitly
kept: promotion sign-off, research-integrity calls, spending irreplaceable data.

### F7 -- MECHANISM TEST. Try to break your own explanation before presenting it.

Naming a constraint means asserting a causal story: *X is happening because Y.*
That story is a hypothesis and it gets the same treatment the object level's
hypotheses get.

**Write the mechanism explicitly, then design and run one check that would
DISPROVE it.** Report the result whether or not it survives. A mechanism that has
not been attacked is not a finding; it is a guess with numbers attached.

Four specific checks, each of which has caught a real error here:

- **Circularity.** Is your metric definitionally entailed by what you are
  comparing it against? *Measured "every position close happened at forecast
  zero" and reported it as a discovery -- but target allocation is a linear
  function of the forecast through the origin, so allocation can only reach zero
  when the forecast is zero. It measured a definition.*
- **Generality.** You saw it in n cases; run it over all of them. *A pattern
  holding in 2 runs at 100% fell apart at 31 runs.*
- **Completeness of the category.** Does your bucket silently exclude cases that
  would refute you? *Counting only full exits to zero made "the strategy never
  changes its mind" look true, while 8,335 sign flips and 17,760 partial
  reductions sat outside the bucket.*
- **Source coverage.** Before presenting ANY count, ask what population the
  record you counted from actually covers -- the whole history, or one era?
  Reconcile against the most exhaustive independent enumeration available (a
  raw directory listing, a row count over every per-unit state file) BEFORE
  presenting. Two rules make this mechanical rather than a matter of noticing:
  **(a)** if two candidate counts of the same thing are already in your own
  working, an unreconciled mismatch is an error you have already caught and not
  yet reported; **(b)** state the denominator with every count -- "36 of 59 run
  dirs", never a bare "36" -- because a denominator you cannot state is one you
  have not checked. *Counted DONE lines in a campaign orchestrator's own log and
  reported "the workflow has completed 4 runs in its entire life". That log
  begins only when the orchestrator did; 52 earlier runs predate it. A
  contradicting count (59 run dirs) was already in the same session's working
  and went unreconciled until the operator caught it. Re-measured from every
  run's own `pipeline_state.yaml`: 36 completions, not 4. Note the correction
  STRENGTHENED the proposal -- coverage errors are not reliably conservative,
  so "my number is probably an underestimate, which is safe" is not a defence.*
The check is usually cheap -- minutes against artifacts you already have. The
cost of skipping it is a proposal built on a mechanism that does not exist, or
on a total that undercounts by an order of magnitude.

## Method

0. **Close the loop on yourself first.** Check what this skill's previous
   invocation proposed, whether it was built, and whether its pre-registered
   success signal fired. Record the answer where the project tracks work
   (epics/backlog). This is MEASURED evidence about whether the meta-level is
   actually improving the machine -- without it, "logic evolution" has no
   feedback and cannot learn.

   **Also count what you have filed against what has been built.** If unbuilt
   proposals from previous invocations outnumber this project's own stated
   build-capacity limit, the binding constraint on the meta-level is
   throughput, not insight, and this invocation's most valuable output is
   probably "build one of these," not a new candidate. Say the ratio out loud.
   **[LOCAL]** the capacity limit here is the roadmap's WIP limit (amendment
   11, EPICS.md: at most 2 epics `in-progress` at once) -- use whatever the
   equivalent is elsewhere. (See A16.)
1. **Review the existing board before deriving anything new.** Read the
   project's epic/backlog tracker in full -- every open item, not a shortlist.
   For each: is it already done in substance (close it)? Is its stated blocker
   still real (verify cheaply, by execution where possible -- blockers go stale
   silently)? Does it already cover the constraint you are about to derive?
   The next step is as likely to be "build or unblock an existing epic" as
   "propose a new one" -- existing epics enter the candidate pool on equal
   terms and pass the same seven filters. Status corrections (done in
   substance, obsolete, blocker evaporated) are record hygiene, not capability
   proposals: report them in BOARD ACTIONS, no filters needed.
2. **Name the binding constraint, with evidence.** Read recorded signal
   (verdict fields, status counts, distributions) to find WHERE to look -- then
   go measure the primary artifacts before you name anything (F4 floor). Report
   counts, not impressions. Do not fix anything you read. Before presenting ANY
   count -- of the system's activity, of artifacts, of anything -- run F7's
   Source coverage check and state its denominator, even if that means
   re-deriving a number you already reported earlier in the same session.
3. **Generate a rival.** Name one constraint that would be INCONSISTENT with
   the one you are converging on -- and with any inherited finding you were
   handed -- and test that too. Report both. Verifying the framing you were given
   is not the same as testing it.
4. **Verify claims about the operator's own system before asserting them.**
   They know it better than you. A wrong assertion about their pipeline burns
   trust and derails the session.
5. **Generate candidates freely across engineering AND research.** Judge each on
   merit. There is no rule that research beats engineering or vice versa.
6. **Run all seven filters on each.** Write the verdicts down.
7. **Convert surviving diagnostics into instruments (F3), wired into the loop
   (F6) -- INCLUDING YOUR OWN.** Re-read the log of every measurement you ran to
   reach the constraint and apply F3's three-part test to each. The instruments
   the system most obviously lacks are the ones you just built by hand.
8. **Present: 2-4 candidates, each with an explicit "why this helps" tied to the
   named constraint and a pre-registered success signal, plus the explicit
   deferrals and why.**
9. **Stop for a decision.** Do not open epics, launch campaigns, or start
   multi-step builds without an explicit nod.

## Output format

For each candidate:

```
CANDIDATE: <name -- a new capability OR an existing epic to build/unblock>
Constraint it attacks : <the named binding constraint>
Why it helps          : <mechanism -- how it changes future outcomes>
Instrument or one-shot: <F3 -- what it measures on every run, and what consumes it>
Evidence              : MEASURED / RECORDED / INHERITED / INFERRED (+ citation)
Counts + denominators : <every count as "N of M", and what M was enumerated
                        from -- or "no counts" if none are load-bearing>
Mechanism test        : <F7 -- the causal story, the check you ran to break it,
                        and what the check returned>
Promotion path        : <can a win be traded? if not, say what blocks it>
Autonomy              : <F6 -- operator work per run: less, same, or more?>
Success signal        : <pre-registered observable that will show it worked, and when to check>
Cost                  : <rough shape: hours of authoring / a build / a decision>
```

Then: **INSTRUMENT CANDIDATES FROM THIS SESSION'S OWN WORKING** -- every ad-hoc
measurement you ran, one line each, with a verdict: `promote` (and to what) or
`one-off` (and why). This section is mandatory even when it is empty; an empty
one asserts you checked. It is how a hand-written script becomes a standing part
of the run workflow instead of dying in a transcript. Promoted candidates must
persist outside the transcript: the script itself goes into the receiving
epic's `artifacts/` directory as the instrument's specification -- A12 applies
to this list too, and a log that dies with the session closes no loop.
Then: **BOARD ACTIONS** -- existing epics whose status is wrong: already done
in substance, blocker gone stale, or superseded by later work -- one line each
with the evidence. Mandatory even when empty; an empty one asserts you read the
board.
Then: **DEFERRED** -- each rejected candidate, the filter it failed, and the
condition under which to revisit it.
Then: **RECOMMENDATION** -- one, with reasoning, and the decision you need.

## Anti-patterns

Each of these actually happened. They are the reason this skill exists.

**A1 -- Becoming the researcher.** Deep-diving old runs, proposing to tune
strategies, drafting hypotheses. Fixes one result; the machine is unchanged.

**A2 -- Proposing an audit.** "Let's review the 41 verdicts to find why nothing
promotes." Useful once, then stale. Convert to an instrument (F3).

**A3 -- Switching thesis silently.** Proposing a fact-based diagnostic, then
next turn proposing an unrelated build without acknowledging the change. If you
abandon a line, say you are abandoning it and why.

**A4 -- Inherited belief as justification.** "Cross-sectional is where the edge
is" -- lifted from project notes, never verified. The capability finding may
still be right; the *reason* must be measured. (F4)

**A5 -- Asserting facts about the operator's system without checking.** Claiming
runs had no verdicts when 41 verdict files existed. Check first. Correct openly
and plainly when wrong; do not quietly repair.

**A6 -- Good-practice creep.** Including improvements because they are sound
engineering, when they unblock nothing today. Defer them out loud. (F2)

**A7 -- Complexity.** Dense tables, jargon, file:line spray. If the operator
cannot act on it, it failed regardless of correctness. Plain language, short
sentences, the number that matters.

**A8 -- Unfalsifiable capability.** Shipping a system change with no
pre-registered way to tell whether it helped. The meta level owes the object
level's honesty: if the workflow's runs need pass rules written in advance, so
do the workflow's own upgrades.

**A9 -- Treating the system's self-report as the system.** Building a constraint
out of verdict files, status notes and ledgers because they are the easiest thing
to read. They are summaries written by the same machine whose behaviour is in
question. Go to the primary record. (F4 floor)

**A10 -- Measuring a definition.** Reporting as a discovery something that could
not have come out any other way. Always ask what the metric would look like if
the effect were absent; if the answer is "the same", you have measured a
tautology. (F7)

**A11 -- Generalising from the first two cases.** A pattern at n=2 is a lead, not
a result. Run it over the whole population before it enters a proposal -- the
run is usually cheap and the retraction is not. (F7)

**A12 -- Leaving the instrument in the transcript.** Running a hand-written
measurement, using its answer to reach a conclusion, presenting the conclusion,
and letting the script die with the session. The next agent re-derives it cold.
Worse: doing it twice in one session and still not noticing. *Happened here --
`measure_exit_causes.py` was written, corrected twice, and only became a proposal
after the operator asked whether it should be one.* (F3)

**A13 -- Waiting to be asked.** Surfacing an incidental finding only when
prompted. Anything measured that is real, durable, and outside the current
thread is output, not conversation -- it goes in the presented result with a
disposition, even if that disposition is "not worth doing". *Happened here: the
20% of trades recording an impossible entry regime, and the 28% one-bar holds,
both surfaced only because a follow-up question created the opening.*

**A14 -- Novelty bias.** Proposing a new capability while an epic that covers
it sits open on the board, or walking past an epic that is already done or whose
blocker has evaporated, because deriving something new is more interesting than
reading the backlog. Blockers do not announce their own staleness. *Happened
here: P4's `blocked_on_daily_bar_ingest` flag outlived its blocker by two weeks
-- the daily caches landed 2026-08-07, nobody flipped the flag, and clearing it
(verified runnable by execution) was worth more than any new proposal that day.*

**A15 -- Recency bias in evidence source.** Reaching for whichever document you
most recently read in full and treating it as exhaustive for a NEW question. A
document earns trust for the question it was read to answer, not for every
question asked afterward -- "primary" is a property of a source *relative to a
question*, not of the source itself. The fix is procedural, not attentional:
F7's Source coverage check and its denominator rule run on every count, so you
never have to notice the source was partial in the moment. (See F7 for the
measured case.)

**A16 -- Proposal inflation.** Filing capability proposals faster than the
project can build them, so the backlog grows while the machine does not
change. Distinct from A6: A6 is one candidate sneaking in despite failing F2;
this is the AGGREGATE across invocations outrunning build capacity even when
every individual candidate was well-justified. The tell is a success signal
that cannot fire because nothing was dispatched -- which also means Step 0 has
no feedback to read, so the meta-level silently stops learning. *Happened
here: four invocations, four epics (E-027..E-030), zero built, against a WIP
limit of two.* Default to recommending an existing epic whenever unbuilt
proposals exceed capacity; require a positive reason to add to the board
instead of a positive reason not to.

## Behaviours to keep

- **Falsify your own load-bearing claim by execution.** Before trusting "the fix
  works" or "the blocker is stale", actively try to break it. Reverting to
  pre-fix code and re-running proved a regression fixture was *blind* to the bug
  -- a far stronger result than "tests passed".
- **Separate proven from argued.** Say exactly what you executed and what you
  only reasoned about.
- **Red-team anything touching engine, metrics, or data**, and anything that
  produces a profitable-looking number, before putting it in front of the
  operator. **[LOCAL]** standing rule here; a sound default anywhere.
- **Never send outward-facing messages** (Slack, PRs, issues) without explicit
  approval, even when the content is obviously helpful.
- **Report provenance.** "From git refs, not the GitHub API" beats implied
  confidence.

## Worked calibration example [LOCAL] (2026-08-21)

This replaces an earlier example that argued the binding constraint was **sample
starvation**. That example was refuted in the session below and is kept only as
the thing that went wrong. Read this one as a record of three successive
corrections, because the corrections are the lesson.

**Round 1 -- RECORDED only.** 59 runs, 38 graded verdicts: 26 `refine`, 10
`kill`, **0 `promote`**. Reading `primary_failure_mode` across all 36 verdicts
that carry it: ~15 cite starvation, ~14 cite no signal, ~7 cite cost drag. An
inherited note claimed 7-of-9 cited sample; it had counted from 9 files when 36
carried the field. Correcting the base was right, but the framing was still
inherited, and the proposed mechanism -- *"coverage equals turnover, so
loosening the regime gate buys sample with fees"* -- was INFERRED and never
tested. **This is A9 and a missing F7.**

**Round 2 -- the operator supplied the mechanism, not the skill.** They asked
whether a noisy regime detector was switching the strategy off, forcing a close
that is a safety default rather than a decision. Checking the source: an
unallocated regime returns a hard `0.0` forecast, which becomes target
allocation zero, which sells. Two runs then showed 100% of full exits occurring
in regime `unknown`. Presented as general. **Wrong: A11.** Widening to all 31
runs with bar data broke it -- most zero-forecast exits occur while a *named*
regime is active.

**Round 3 -- the operator broke it again.** They pointed out that a strategy
also changes its mind by reducing a position or flipping sign, and that neither
touches zero. Re-measuring every approved allocation move across 31 runs: 8,335
sign flips, 17,760 partial reductions, 15,317 increases -- **90% of moves made
with a nonzero forecast**. Only 10% go to exactly flat. And going to flat
*requires* a zero forecast, because allocation is a linear function of the
forecast through the origin. The round-2 headline had measured a definition.
**A10.**

**What survived all three rounds** -- and it survived because it was read from
source rather than assembled from summaries: `_infer_exit_reason` classifies a
LONG exit as `signal_flip` whenever `exit_forecast <= 0`, and its last line is a
bare `return "signal_flip"` default. Three different causes of a zero forecast
(regime unallocated, component not ready, ensemble genuinely flat) are
indistinguishable in that field, and it feeds the verdict evaluator.

**Round 4 -- the operator asked the question the skill should have asked
itself.** *"Is there another epic to make the trade label more explicit? Always
think long term -- if you need to do it once, maybe worth implementing so it is
done at each run."* Measuring the archived per-trade records: 4,392 trades, and
`exit_reason` takes exactly two values (92.6% `signal_flip`, 7.4%
`end_of_window`, the latter meaning "the data ran out"). No `regime_at_exit`, no
forecast values, no allocation pair. Every analytic question asked in the whole
session had needed a hand-written script because the trade record could not
answer it -- and that script had been written, and corrected twice, without ever
being recognised as a specification for a missing instrument. **A12.** The
resulting epic is the most useful of the three.

**The proposal (F3 + F6):** emit the *cause* of a zero forecast at source, give
`exit_reason` no unconditional fallback, and let the verdict stage refuse to
grade signal quality when the switched-off share is too high. Success signal
(A8): within the next batch, at least one trade reclassifies away from
`signal_flip` and at least one verdict routes differently.

**Correctly deferred (F2):** slippage modelling -- nothing passes, so better
costs change no decision; revisit at the first strategy that clears its gate.
And universe breadth -- real, with 17 symbols already cached, but multiplying a
strategy across them before exits are attributable multiplies whatever is
producing the exits.

**Two transferable lessons.**

*On the errors:* every one was a category silently absorbing cases nobody had
checked for being different -- precisely the defect the surviving proposal
fixes. The skill was reproducing, at the meta level, the bug it was diagnosing at
the object level. Run F7 before presenting, not after being challenged.

*On the omission:* four rounds, four operator interventions, and the highest-value
epic came from the one that was purely procedural -- noticing that a hand-written
script is a missing instrument. The measurements were competent throughout; what
was missing was the habit of auditing its own working. F3's blind-spot rule and
the mandatory INSTRUMENT CANDIDATES section exist to make that automatic, because
an operator who has to ask "should this be an epic?" is doing the skill's job.

When porting this skill, replace this example with the equivalent episode from
the new context. It is calibration, not doctrine.
