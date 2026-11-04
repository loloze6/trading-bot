# Rectifications

## Rectification 1 (applied from stop 02, received after stop 02)

RECTIFICATION 1 (direction, 2026-10-29), from the operator's feedback after stops 00-02.

Record this text verbatim in guided_tour/00_rectifications.md, then apply it.

## What is wrong

Your speeches are technical inventories: a list of code names, keys and line ranges, in the
order of the file. The operator cannot read them. A guided tour speaks to a new joiner of any
background: plain words, the business first, the files second. The itinerary's rule "every part
named with its file and line" stays true, but it is satisfied by a reading map at the end of
each stop, not by the speech itself.

## The new shape of every stop (from stop 02 on)

Open as before: "Stop NN of 29: <element>. Open on the side: <file names only>."

Then the speech, as sub-speeches under these fixed headings, in this order:

1. **In one sentence.** What this element is, in the words of the research business: an
   idea, a form, a queue of work, a test, a verdict, a record, a decision. No code name.
2. **Why it exists.** The business need it answers, and what would go wrong without it
   (money spent on an idea already tried, an idea tested on the bars where it was seen, a
   result nobody can find again, a strategy that fools us). Tie it to the campaign's purpose:
   finding a profitable strategy by itself, the operator deciding, the pipeline discovering,
   without fooling ourselves.
3. **What comes in, what goes out.** The inputs and outputs in plain words (a brief, a card,
   a config, a backtest, a verdict, a memory entry), who produces each and who uses it next.
   One short list.
4. **What happens here, step by step.** The mechanism as a story a person could retell: "the
   runner takes the first ready brief, checks that the venue is one we may trade, writes the
   first files of the run, and hands over to the orchestrator". No function names, no key
   names, no flag names in this section. A technical term that cannot be avoided is glossed in
   brackets the first time it appears in the tour ("a fold (a fixed set of test months)").
5. **What it costs and how long it takes.** Only when the run's record has the figure
   (model cost and duration from run_102's audit log, number of files, number of entries).
   Figures on their own line, with the source file. Skip the heading when there is no figure.
6. **What is switched off or not used here.** Plain statement, one line each. Facts only; no
   judgment, as before.
7. **Reading map.** A table: part | file:line | one line on what it does. This is where
   completeness lives: every part of the element, nothing described in sections 1-6 that is
   not here, nothing here that is not in the element. The operator reads it with the file
   open; they skip it if they want.

Length: sections 1 to 6 together at most about 700 words. Short sentences, one idea each.
Bold only the heading words. An example from run_102 is welcome in sections 3 and 4 when it
makes the story concrete ("run_102's brief asked for BTC on hourly bars, fold B").

Everything else in the opening prompt stays: one stop at a time, write the file before the
chat message, record remarks verbatim, "direct" answered from the files with file:line, the
inspector continued after each stop, the hard rules.

## Now

1. Regenerate stop 02 in the new shape: replace the "Speech (verbatim)" section of
   guided_tour/02_registration_and_queue.md with the new speech (keep the correction to
   stop 01 that opens it, in one sentence), leave the two other sections as they are, send
   the new speech in chat, and wait for the operator's remarks as usual.
2. Do not regenerate stops 00 and 01: they are delivered and remarked. The post-tour
   analysis reads their reading maps.
3. Send the inspector its usual continuation for stop 02 only after the operator's remarks on
   the regenerated speech are recorded.

## Rectification 2 (received after stop 05a was written, 2026-10-30)

RECTIFICATION 2 (direction, 2026-10-30): the tour becomes asynchronous.

Record this text verbatim in guided_tour/00_rectifications.md, then apply it. Rectification 1
(the business-first shape of every speech) stays in force.

## What changes

The operator reads the stops later, one by one, and sends remarks then. You write the whole
tour now, stop after stop, without waiting for remarks between stops.

1. **No wait after a stop.** After writing a stop file and sending its speech in chat, send
   the inspector its continuation for that stop and go straight to the next stop. Do not wait
   for the inspector's "stop NN noted": it works in the background and handles the stops in
   the order it receives them.
2. **One checkpoint, then the full run.** Regenerate stop 02 in the rectification-1 shape and
   write stop 03 (both parts), then stop and say: "Checkpoint: stops 02 and 03 written. Say
   'go to the end' to continue." On the operator's "go to the end", write stops 04 to 29 in
   one go, every stop a file and a chat message as before, and finish with: "All stops
   written. Send remarks as 'stop NN: <remark>'; mark 'direct' for an answer."
3. **Remarks arrive later.** When a remark comes, whatever stop it names, record it verbatim
   under that stop's "Operator remarks" with the Edit tool, leaving the inspector's section
   untouched. A remark marked "direct" is answered at once from the files, with file:line,
   under the remark. If the remark questions a speech, do not rewrite the speech: add a
   "Correction (<date>)" paragraph under it only when the speech was wrong on a fact.
4. **Keep the rules through a long session.** Before every fifth stop (05, 10, 15, 20, 25)
   and after any context compaction, re-read guided_tour/00_guide_opening_prompt.md,
   guided_tour/00_rectifications.md and the itinerary row of the stop you are about to write.
   Every speech is still built from a fresh read of the element's files, never from memory.
5. **Each stop stands alone.** A reader opens stop 17 cold: gloss again, in brackets, any
   term you glossed at an earlier stop, and do not refer to "as I said at stop 09" without
   saying in a few words what it was.
6. **Chat messages stay short.** The chat copy of a speech is the file's Speech section,
   nothing more; no progress narration between stops beyond the stop opener.

Everything else holds: one file per stop (parts as NNa, NNb), the three headings from the
start, the inspector continued after every stop with the same brief, read-only on the
pipeline, no runs, no tests, nothing under local_data/, no sealed dates, fold ids and years
only.

## Now

Regenerate stop 02, write stop 03a and 03b, send the inspector both continuations, then stop
at the checkpoint.

### Rectification 2a (received 2026-10-30, amends rectification 2's "Now")

RECTIFICATION 2a (direction, 2026-10-30): amendment to rectification 2's "Now" section.

Record this text verbatim in guided_tour/00_rectifications.md under rectification 2, then
apply it.

Rectification 2 was written as if the tour stood at stop 02. It stands at stop 05a (written,
no remarks yet). So:

1. Ignore rectification 2's "Now" section. Do not regenerate stop 02 or 03; do not stop at a
   checkpoint. Stops 02 to 04 already have the rectification-1 shape and are remarked and
   inspected; they stay as they are.
2. If you have not yet sent the inspector its continuation for 05a, send it now. Then write
   05b, send its continuation, and go on through stops 06 to 29 without a pause, as
   rectification 2 points 1, 3, 4, 5 and 6 say. Finish with: "All stops written. Send remarks
   as 'stop NN: <remark>'; mark 'direct' for an answer."
3. Remarks on 05a and later arrive after that; record and answer them as rectification 2
   point 3 says.

### Guide's note on applying rectification 2 (2026-10-30)

When rectification 2 arrived, stop 02 had already been regenerated in the rectification-1 shape, and stops 03a, 03b, 04 and 05a had already been written in that shape, each with remarks recorded (05a has none yet). The inspector had received 02, 03a, 03b and 04. So nothing was regenerated or overwritten: the inspector received 05a, and the checkpoint was given at 05a instead of 03. After "go to the end", the tour resumes at 05b.

## Rectification 3 (received after stop 05b, 2026-10-30)

RECTIFICATION 3 (direction, 2026-10-30): relaunch the inspector yourself; do not stop before stop 29.

Record this text verbatim in guided_tour/00_rectifications.md, then apply it.

1. **Relaunch the inspector now, without asking.** Launch a new inspector sub-agent in the
   background (Agent tool, model `fable`) with the inspector brief of your opening prompt,
   section 6, verbatim, plus this first instruction at the end of the brief:
   "First, read every stop file already in guided_tour/ in order (00 to 05b) to build your view
   of the system. Then write your notes for every stop whose '## Inspector notes' section is
   still empty (today 05a and 05b), each under its own file, before handling the stops the
   guide sends you next."
   Then continue it with SendMessage after each new stop, as before.

2. **Standing rule: an inspector lost is relaunched, not reported.** If at any later stop the
   continuation fails (the agent was stopped or cannot be resumed), launch a fresh inspector
   at once with the same brief and the same first instruction (read every stop file, then
   fill every empty "Inspector notes" section), note one line in
   guided_tour/00_rectifications.md ("inspector relaunched at stop NN"), and go on. Never ask
   the operator whether to relaunch.

3. **Do not end your turn before stop 29 is written.** From now, write 06, 07, ... 29 in one
   continuous turn: for each stop, read the element's files, write the stop file, send the
   speech in chat, send the inspector its continuation, and start the next stop. No question,
   no checkpoint, no "say next". The only reasons to stop early are a hard error you cannot
   work around (say which stop and why) or an explicit message from the operator telling you
   to stop. Remarks on earlier stops that arrive while you write are recorded when you finish
   the stop in hand, then you continue.

4. **Remember the asynchronous rules** (rectification 2): each stop stands alone (gloss again),
   chat copies are the Speech section only, re-read the opening prompt and the rectifications
   before stops 10, 15, 20 and 25 and after any compaction.

Finish with: "All stops written. Send remarks as 'stop NN: <remark>'; mark 'direct' for an
answer." Then, and only then, wait.

inspector relaunched at stop 05b

## Pause (operator, 2026-10-30)

Tour paused by the operator after stop 19 was written (stops 20 to 29 not yet written). The operator will comment the earlier stops in the form "Speech XXX: comment (...) / Next"; each comment is recorded verbatim under that stop, "direct" ones answered from the files.

## Resume (operator, 2026-11-02)

Tour resumed by the operator in a cloud session (the PC was unreachable), on a copy of guided_tour/ rebuilt from the session transcripts. Checkout: /home/user/trading-bot at master 78790e5f (2026-10-28, PR #558). In this checkout the run folders under SR/runs/ stop at run_060 (they are not tracked in git) and the committed SR/campaign_record/ files stop at run_097; run_102's own files are not available, so stops 20 to 29 take run_102 facts only from earlier stop files and say so where an example is missing. Operator remarks recorded for stops 08 to 14 and 19; none for 15 to 18; no "direct" asked. Stops 20 to 29 written in one go (rectification 3).

inspector relaunched at stop 19
