<!-- recovered from direction session; original path: C:\Users\alauz\Documents\Projects\trading-bot\guided_tour\rectification_01_business_speech.md; written 2026-10-29T15:17:07.827930Z -->
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
