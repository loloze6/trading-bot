<!-- recovered from direction session; original path: C:\Users\alauz\Documents\Projects\trading-bot\guided_tour\rectification_02_asynchronous_tour.md; written 2026-10-30T05:31:25.706369Z -->
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
