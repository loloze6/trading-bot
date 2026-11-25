# Topics: one card per improvement, open or decided

Every improvement noted while designing, running and trading (research, engine, live, hosting, viewer) is one topic
card here, in one shape (`TEMPLATE.md`), with its decisions and their reasons. `NEXT_STEPS.md` is the one list: the plan's steps and every topic (sections E and F).
Run briefs, one per run, are in `../runs/`; the cards of the steps and functions are in their own folders.

- **A topic is noted:** a card `NN_short-name.md` (the next number) with what was seen and why it matters, and a row
  in `NEXT_STEPS.md` (a step of the plan, or section E). Nothing is built: it waits for the operator's go (CLAUDE.md, "Build only what was asked").
- **A topic is opened:** the operator says go. If it becomes a step or a function, its card is designed by
  `../HOW_WE_DESIGN_A_CARD.md`, starting from the topic's question and decisions; the topic's status says "designing"
  and names that card. The topic card keeps the why (the decisions and their reasons); the step's card holds the how.
- **A topic is closed:** decided, built, solved or dropped. The card stays, status closed, with the decision and where
  its result lives: the reasons are kept, so a question asked again finds its answer.
- **A topic's working files** (its analysis scripts, tables, discovery tools, reviews) are in a folder `NN_review/`
  next to its card (`30_review/`, `34_review/`, `36_review/`): what helps decide a topic, not a step of the workflow. A
  tool that becomes part of a step moves to that step or to `../common/` (2026-11-21).
- **Decisions** are one row each: date, decision, by whom, why, and what was rejected and why. A ruling the operator
  gives in conversation is written there the same day.

Started 2026-11-19 (operator): the 15 open items of the former `POTENTIAL_ADJUSTMENTS.md` (removed; git keeps it) and
the topics decided since 2026-11-18, written back from their files, commits and the operator's words. Older decisions
live in the cards and the run briefs that made them.
