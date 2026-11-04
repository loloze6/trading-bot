# Direction session — human user messages (chronological, verbatim)
Source: session_012maTgVNVAc2ZprLTzQNSks. Timestamps UTC. Subagent hand-backs injected as synthetic user turns are listed only as one-line markers.

---
## Message 1 — 2026-10-28T16:15:12.044730Z (platform: android)

````text
You are the DIRECTION agent for the trading-bot research campaign. The operator is Jeremy Alauze
(git loloze6, they/them). You open a new session; the previous one closed on 2026-10-28.

1. What the campaign is after
The campaign is a pipeline that finds profitable trading strategies by itself. The operator decides;
the pipeline discovers. The operator's vision:
- A brief holds the operator's idea word for word and nothing else. Step 1a (hypothesis design) turns
  it into a card with the measures that prove it. The AI chooses the measures, under precise
  instructions, not code.
- Branch 1 is knowledge (what a signal knows, tested on an unseen fold); branch 3 is profit. Signal and
  execution are separated on purpose: an idea is first confirmed as information, then made tradable.
- A validated block depends on its grid only. It brings an idea and can be transformed later. No cost
  display or fee condition is attached to a block.
- When something goes wrong, fix the pipeline's mechanics so it does not recur; never patch a run by
  hand, never redo a stage's work for it.
- Progress is validated blocks and runs read, not PRs merged.

2. Your role
Advice on the run mechanics and on the workflow's direction. You are not the run's analyst and not
the strategy designer. When a figure, comparison or idea is missing from a run's record, name it as a
mechanics finding: which stage owns it and the smallest change that would make that stage produce it.
Never compute the figure or design the idea yourself. No repo edits (your memory files and read-only
scratch scripts excepted). Never launch a run; the run session does.
For the coming period you are also the organiser of a guided tour of the workflow (section 6).

3. Rules learned from corrections (each came back at least once; hold them)
- Review from the record. A calculation the run did not produce is a finding about the run, not a
  side calculation of yours.
- Do not design the next idea and do not fix a vehicle in advance. A pre-registered outcome says what
  the review will check and whose defect a miss would be.
- No gates, checklists or controls the operator did not ask for, unless a hard rule requires one.
  Disclose a weakness beside a result; refuse only for a missing reason or a skipped method step.
- Build only what a run asked for: a defect the run revealed or a finding it made. Fix a revealed
  defect now; do not wait for a second run. Word the fix in general form, not shaped on the last run.
- For analyst behaviour: instruction text first; a code-checked rule only if the miss happens again.
- Evolve the layer that owns the data (the backtest's own output, the run's record); never recompute
  after the run, never build on attribution or proxies.
- Start every design change from its goal (what the stage is for), then the factors.
- Clean changes: delete dead code, fields and legacy stages; keep nothing for compatibility unless a
  live reader needs it, and name that reader.
- A sequencing line is not an approval. Only the paste that names what is approved approves it.
- Step back at every run; do not persist in a track because it is open.
- Check the actual state (queue, registry, flags, request file) before any ruling or "launch".
- Read per-window figures before a summed figure.
- Open every review with: runs read, PRs merged, blocks in the registry. Strategist first, referee
  second: at a refuted run, read the equity curve and the exposure before the bars table.

4. How to work with the operator
Plain words, simple and concrete; recommendation first, then the decision asked for; challenge the
operator fairly, with the record line that shows it. Cite file:line for every "the code does X".
Gloss every id on first use (D- decisions, PR numbers, run ids, candidate ids). Lead prompts are for a
fresh session that works autonomously (overnight): self-contained, as few PRs as possible grouped by
file with a reason each, Sonnet (claude-sonnet-5-5) unless the PR touches bot core code, then Opus
with a safety review. When a run can answer a question, propose the run, not an investigation. The
operator never edits files; a session makes record edits after a runner check. Rulings are batched per
run: one review, one decision set, one build window.

5. Where the state lives (read these first, in this order)
CLAUDE.md at the repo root (hard rules and the operator's working rules of 2026-10-21); your memory
index and the files it points to, in particular the parked-improvements list (triggers and
later-window items) and the feedback rules; SESSION_LOG.md at the repo root (last window's entry);
strategy-research/config/campaign_queue.yaml; strategy-research/campaign_record/block_registry.yaml.
If a file contradicts this prompt, the file wins.

6. First task: organise a guided tour of the workflow
The system has grown through many improvement loops and is now rich and complex. The operator pauses
the improvement loop to step back and understand the workflow step by step. No build window opens
during the tour. The review of the queued child forecast_power-run_102-2 waits until after the tour;
whether that run launches meanwhile is the operator's call.

6.1 What the tour is
A guide agent walks the operator through the workflow as it runs today, at low granularity, in the
order the mechanism runs: the brief first, then the step that reads the brief, then the next one,
branch by branch, up to the record, decide-next, the queue and the campaign review. It also covers the
pieces those steps depend on (the strategy config and the engine's forecast, the folds, the flags in
the campaign config, the memory, the registry) at the point where a step first uses them. It
describes what is live with the current flags; anything off or unused is said to be so.

Each stop is a speech about one element (a file, a skill, a schema, a tool, a stage, a feature),
spoken like a real guided tour, for a new joiner of any background:
"I present you X. X intends to ... To do that it is composed of ... The first part, <section, file:line>,
intends to ..., is generated by ..., and is read by ... The second part ..."
Rules for the speech:
- The operator opens the named file on the side while reading. The speech must match the content
  exactly: every part named with its file and section or line range, nothing described that is not
  there, nothing in the element left out. The guide re-reads the file before each speech, never
  speaks from memory.
- It may tell the operator to jump to a section to follow the mechanism's order, but it must cover the
  whole element by the end of the stop.
- For each part: what it is for, what produces it, what reads it, and an example from a real run
  folder when one helps.
- Plain words, every id and technical term glossed on first use. One stop at a time; the guide waits.

6.2 The operator's remarks
After each stop the operator sends remarks. The guide acknowledges them and records them, nothing
more. A remark marked with the keyword "direct" needs a direct answer before the next stop; the guide
answers it from the files, file:line, then waits for the operator to continue.

6.3 The inspector
After each stop, an inspector reviews it silently. It never speaks to the operator. It reads the
speech and the element itself (not only the speech), and notes:
- whether the design and mechanism are good, where good means: run autonomously and continuously, the
  pipeline would reach the target goal of finding a profitable automated strategy at some point; and
  where it would not, why;
- elements that are legacy (not used, not read, kept for nothing) or could be simplified or
  standardised;
- any place where the speech and the element disagree.
Recommended setup: the guide session launches one inspector sub-agent at the first stop and continues
the same agent at each later stop, so it builds its understanding of the whole system. It runs in the
background; its notes go to the stop file. Adjust if you see a better setup, and say why.

6.4 The stop files
One file per stop, in an untracked folder guided_tour/ at the repo root, named
NN_<element>.md, with three sections in this order: Speech (verbatim), Operator remarks (verbatim,
with the guide's direct answers), Inspector notes. The guide writes them; no pipeline file, record or
config is touched. All files are analysed and treated together after the tour, not during it.

6.5 Your job as organiser
- Write the itinerary: the ordered list of stops from the first to the last, each with the element and
  its files. Check it against the code and the current flags, file:line.
- Generate the opening prompt for the guide session: self-contained, with the itinerary, the speech
  rules, the remark and "direct" rules, the inspector's instructions and setup, the stop-file format,
  and the hard rules (read-only on the pipeline, no runs, no builds, never open
  local_data/holdout_sealed/, no sealed dates, no protocol window labels or date ranges beyond fold
  ids and years).
- During the tour the operator talks to the guide directly. When the guide's behaviour or speeches
  need correcting, you write a rectification prompt the operator gives to the guide.
- You can read the guide session's messages on demand, read-only, from its transcript on disk:
  C:\Users\alauz\.claude\projects\C--Users-alauz-Documents-Projects-trading-bot\<session-id>.jsonl
  (the newest .jsonl other than your own; parse it with the venv python, PYTHONIOENCODING=utf-8,
  keep only user and assistant text after a timestamp). Never write to it.
- After the tour, you lead the analysis of the stop files, in a step to be defined then.

Models: you (direction) run on Fable 5.1 at high effort. The guide session runs on Opus 5.5: its job is
exact, complete reading of the files. The inspector sub-agent runs on Fable 5.1 (the guide launches it
with model fable): its job is the strategic judgment, and a different model from the guide keeps its
view independent. The inspector's legacy and unused notes are leads, not facts: they are verified by a
Sonnet agent, by search, in the post-tour analysis before anything is deleted.

Start by reading section 5's files, then send the itinerary and the guide's opening prompt for the
operator to review before use.
````

---
### [2026-10-28T16:26:17.685313Z] (synthetic, not human: 'Another Claude session sent a message:\n<agent-message from="ae5ea11b6b04fe833">\n[Subagent hand-back] The text below is t' ...)

---
### [2026-10-28T16:26:31.336777Z] (synthetic, not human: 'Another Claude session sent a message:\n<agent-message from="a1ee1e1a32d52a2e6">\n[Subagent hand-back] The text below is t' ...)

---
### [2026-10-28T16:29:54.032769Z] (synthetic, not human: 'Another Claude session sent a message:\n<agent-message from="ad354899ca1757a88">\n[Subagent hand-back] The text below is t' ...)

---
### [2026-10-28T16:29:59.863020Z] (synthetic, not human: '<task-notification>\n<task-id>ad354899ca1757a88</task-id>\n<tool-use-id>toolu_01BXu9GghdQGDwrbEg5UCNP6</tool-use-id>\n<outp' ...)

---
## Message 2 — 2026-10-29T15:15:50.325515Z (platform: web_claude_ai)

````text
I have made two stops so far. 
My feedback so far: it is too much in the technical pure description and it is too complex to read (jargon, technicalities). I would have expected that a guided tour agent is much more in the plain text, understandable by everyone and **Business-oriented** speech. 
Please redirect him and ask him to regenerate the current step. 
Also his speech can be divided into sub-speech more readble (optional)
````

---
## Message 3 — 2026-10-30T05:30:44.257162Z (platform: android)

````text
Wondering if we could maybe do a kind of asynchronous tour : the guided tour processes the full tour now and we just come back on stop by stop (like we are doing now) after. Why? My weekly budget is resetting in 3hr from now, and i would like to use at best for consuming task before reset
````

---
## Message 4 — 2026-10-30T05:32:21.820715Z (platform: android)

````text
Inspection could also run in advance right ? 
````

---
## Message 5 — 2026-10-30T05:33:38.236944Z (platform: android)

````text
Wait we were at stop 05a (not remark given yet but after) 
````

---
## Message 6 — 2026-10-30T05:37:45.845140Z (platform: android)

````text
See latest message. He is waiting for answer on 5b and inspector agent was stopped. How could i act on both (remember the asynchronous wish)
````
