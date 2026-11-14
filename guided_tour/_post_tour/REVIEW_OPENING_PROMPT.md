POST-TOUR OVERALL REVIEW: opening prompt (operator, 2026-11-05)

You are the first reviewer after a guided tour of the trading-bot research workflow. The operator
(Jeremy Alauze, git loloze6, they/them) wants an overall feeling of the improvement needed. Start
very high, then go into more detail level by level, top to bottom. This is NOT a detail review: do
not chase line numbers, small errors or speech-versus-code disagreements.

## Where things are
Repo `loloze6/trading-bot`, branch `ccr-fd96c37b-b5lc87`; check it out first. On the operator's PC,
the tour folder is brought over with:
`git fetch origin ccr-fd96c37b-b5lc87` then
`git restore --source origin/ccr-fd96c37b-b5lc87 --worktree -- guided_tour`.
SR = strategy-research/, TB = trading-bot/.

- `guided_tour/00_itinerary.md`: the map of the 30 stops (00 to 29; some in parts a/b, 36 files).
- `guided_tour/NN_*.md`: one file per stop, three sections:
  - "Speech": what the element is, in plain words, with a reading map.
  - "Operator remarks": the operator's own words, verbatim. This is the PRIMARY voice. Stops 15 to
    18 and 21a have none.
  - "Inspector notes": an independent reviewer's notes in three parts: (1) design and mechanism (can
    this element help the pipeline reach a profitable strategy?), (2) legacy or simplifiable,
    (3) disagreements with the speech.
- `guided_tour/00_rectifications.md`: how the tour was run, and its closure.
- `guided_tour/_post_tour/`: verification reports. Use them only as described below.
- `night_work_2026-11-04/README.md` and `night_work_2026-11-05/README.md`: what has already been
  cleaned or proposed since the tour, including fact reports that answer several operator remarks.

## The goal everything is judged against
A pipeline that finds a profitable automated trading strategy by itself, run autonomously and
continuously, with the operator deciding and the pipeline discovering, without fooling itself.

## What to read, in this order
1. Root `CLAUDE.md` and `SR/CLAUDE.md` (hard rules and working rules).
2. `guided_tour/00_itinerary.md`, then `guided_tour/00_rectifications.md`.
3. Every stop file in order, 00 to 29. For each: the Operator remarks first, then Inspector notes
   parts (1) and (2). Read the Speech only as needed to know what the element is. Skip Inspector
   part (3) (detail).
4. For weighting only, not as themes:
   - `_post_tour/design_premises/design_premises_verification.md`, section "Findings whose premises
     do not fully hold". Do not build a theme on an inspector finding whose premise is marked false
     or partly true without saying so.
   - `_post_tour/leads_verification.md` counts per stop, as a signal of how much legacy weight each
     part carries.
   Do not go through `_post_tour/disagreements/` or `_post_tour/correction_drafts/`: that is detail
   for later.
5. The two night_work READMEs, so you do not re-propose what is already done or answered.

The material is large (about 36 files of 3-5k words, plus reports). Use sub-agents to extract notes
per group of stops: the operator's themes with verbatim quotes and stop refs, and the inspector's
design and legacy themes with stop refs. Then synthesise yourself. Quote the operator verbatim; never
paraphrase their remarks as if they were yours.

## What to write: `guided_tour/_post_tour/overall_review.md`
Plain words, business first, short sentences. File:line only at levels 2 and 3, and only when it helps.

0. Open with the working-rule line from the root `CLAUDE.md` (runs read, PRs merged, blocks in the
   registry), stating what this checkout lets you check.
1. **Level 0: the verdict, in at most 5 lines.** Where the system stands against the goal, and the
   single biggest thing to change.
2. **Level 1: 4 to 7 improvement themes across the whole workflow.** Each gets one sentence, why it
   matters for the goal, and how strong the signal is: operator, inspector or both, and on how many
   stops.
3. **Level 2: per theme.** The stops it touches; the operator's remarks quoted with stop refs; where
   the inspector converges or diverges; what "improved" would look like in business terms (not code).
4. **Level 3: the workflow, top to bottom.** Brief -> registration, queue, launch -> orchestrator ->
   idea steps (1a, claim, criteria) -> config and engine -> data and backtest -> the three judges
   (grid, profit bars, analyst) -> records -> decide-next -> campaign review and holdout -> the
   operator's surface. For each element: a one-word feeling (keep / simplify / rethink / remove),
   one line of why, and refs.
5. **"Rebuild from scratch or clean up in place?"** The operator raised this at stop 28. Give the
   considerations both ways and what the tour shows. No decision: the operator decides.
6. **Where the operator and the inspector disagree at a high level.**
7. **Open questions for the operator**, at most 7, each answerable in a sentence.

In chat, reply with Level 0 and Level 1 only, plus the file path.

## Rules
- Read-only everywhere except `overall_review.md`, plus scratch notes under
  `guided_tour/_post_tour/overall_review_notes/` if useful. No code, config, doc, skill or stop-file
  edits. No runs, backtests, tests or builds.
- Feelings and proposals only, no rulings. The direction session leads the post-tour analysis; this
  review is its first input.
- The tour was judged under the operator's live flag set: every `orchestrator:` flag on except
  `deviation_gate`, `zero_trade_windows_not_computed` and `extra_cards_at_1a`. The committed
  `campaign_config.yaml` differs (most flags off): do not read it as the live state. Run folders after
  run_060 (including run_102) and the live queue and records are only on the operator's PC.
- Never write a date from `SR/config/campaign_data_policy.yaml`, a holdout date range or a protocol
  window label; fold ids (A-D) and years only. Never open `TB/local_data/` or anything named
  `holdout_sealed`.
- Commit only your output, to your session's own branch. Never to master; no PR unless asked.
