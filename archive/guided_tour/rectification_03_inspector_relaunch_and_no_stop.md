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

