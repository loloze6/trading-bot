# Pilot A4 (2026-11-27): the whole new chain, watched, in two short runs (written before the runs)

**The operator (2026-11-26, next steps A4 part 7):** "a watched pilot of the whole chain before the next batch";
2026-11-27: "Go with B": two runs in parallel, 2 hours, about 12 USD each. Standing rules: `NIGHT_RULES.md`.

## Purpose
One question: **does every piece built on 2026-11-26 and 27 work on real data, in one run, in the order the cards say?**
Not: does the run find a strategy (the pilot is too small to say).

## The runs
| | Run 1 | Run 2 |
|---|---|---|
| Run | `pilot_a4_auto_run`, branch `pilot-a4-auto` | `pilot_a4_named_run`, branch `pilot-a4-named` |
| Box | `--target-box auto` (the rule on the 25 portfolio coins: falling calm, long at the start) | `--target-box "rising agitated, short"` (named by the operator) |
| Brief | written by step 1 from the box alone, with the box's note: `--theme` names only the box | the same |
| Data | `--data-use 2`: 8 research coins drawn by the run's name, the 32 windows 2016-2026, explore half to the analysts, check half for step 5's direction | the same |
| Budget, time | 12 USD; no new idea after 21:30 UTC (22:30 Paris), the idea in progress finished | the same |
Each run in its own session, on its own branch from the working branch at 7faa7092853 (never on the working branch while it runs); the designer reads both journals.

## What must be seen (one line each, from the run's files)
| # | Piece | Seen when |
|---|---|---|
| 1 | Data use 2 | `data_use.json`: 8 coins, one per category plus one; step 4's records on those coins and the 2016 windows; coins' first 90 days and holes left out, counted |
| 2 | Explore and check halves | step 7's exploration on w1-w18 only; step 5's direction on w19-w32 |
| 3 | The box | `target_box.json`; the brief's `profile:` and `side:` holding it; the box's note in step 1's, 2's and 7's prompts; `in_box` on every turn |
| 4 | B13 | the untested ideas naming the box taken before the first turn (`taken` lines), ranked with the run's own |
| 5 | B11 | at least one answer "no effect", and its follow-up written by 7.c, not 7.b |
| 6 | B12 | a confirmed, unprofitable strategy failing 3 or more measures gets no 7.d call (if one occurs) |
| 7 | B10 | at least one "not called" line for 7.g, with its scores |
| 8 | Steps 9 and 10 | a candidate (confirmed and profitable) gets its common record, then `update.py` (a new version only if the list changed) |
| 9 | No unseen test | no `unseen_test` call in the run |
| 10 | Cost and time | every step's USD and seconds in the table; nothing refused or failed without a line saying why |

## Expected outcomes
| # | Outcome | Shown by |
|---|---|---|
| P1 | The chain works | rows 1 to 4, 9 and 10 seen in both runs; rows 5 to 8 seen in at least one, or "did not occur" with the reason (then covered only by the builds' proofs on stored files) |
| P2 | A piece fails | a row not seen where its case occurred: named, fixed by its rule, the pilot rerun on that piece |
| P3 | The machinery stops | a failed turn, a refusal, a step with no output |
Also counted: ideas tested, confirmed, profitable; ideas outside the box (`in_box` false); spend per step.

## Reading
(2026-11-27, about 22:35 Paris; from the two sessions' reports and the branches' files: `pilot-a4-auto` at bf9b1cbca03,
`pilot-a4-named` at 61b0d43dfcd; neither merged)

**Outcome: P1 for the pieces that could occur, with four defects found (P2); three pieces never occurred.** Both runs
stopped at their budget (12.19 and 12.04 USD), no failed turn, no refusal, no resume.

| # | Piece | Run 1 (auto: falling calm, long) | Run 2 (named: rising agitated, short) |
|---|---|---|---|
| 1 | Data use 2 | seen: 8 coins, one per category plus one; **119 of 256 coin-windows run** | seen; **103 of 256** |
| 2 | Explore and check halves | explore half seen (7.g on w1-w18); the direction check did not occur (no confirmation) | the same |
| 3 | The box | seen: chosen by the rule; briefs 086 and 087 name it; every idea tested in the box | seen: named; all 31 ideas written name the profile |
| 4 | B13 | seen: 52 taken, 9 of the 12 ideas tested | seen: 8 taken, 3 tested |
| 5 | B11 | seen: 9 "no effect", each followed by 7.c; 3 unclear, by 7.b | seen: 8 and 2 |
| 6 | B12 | **did not occur** (nothing confirmed) | **did not occur** |
| 7 | B10 | seen: 7.g not called 6 times, with its scores | seen once |
| 8 | Steps 9 and 10 | **did not occur** (no candidate) | **did not occur** |
| 9 | No unseen test | seen | seen |
| 10 | Cost and time | seen; the components step built one setting (0.84 USD) and its idea was then tested | seen |

**Counts:** 22 ideas tested (12 and 10), **0 confirmed**, 17 "no effect", 5 unclear; 12 of the 22 taken from earlier
runs; 0 outside the box by the journal's reading; 3 discoveries, all in their run's box (1 briefed and tested in run 2,
1 briefed and 1 not, for the budget, in run 1). About 0.7 to 1.1 USD and 8 minutes an idea; lines 7.c and 7.g are more
than half of the spend.

**Defects found (each a rule to fix, none stopped a run):**
1. **The side is read on the brief, not on the idea.** A brief without a `side:` line reads as "both sides", so a long
   box took ideas that bet short (run 1: 032-01.b1 and 032-02.b1, measured in the short direction by step 5; the "fade"
   ideas 061-01, 064-01, 060-02), and the short box took a "rise continues" idea (run 2: 041-01.b1). `in_box` said
   true for all of them.
2. **Less than half of the run's data exists.** Of 256 coin-windows (8 coins, 32 windows): 109 (run 1) and 120 (run 2)
   left out by the rule, almost all because the coin was not listed yet; then 28 and 33 more refused by the engine as
   errors ("the dates were not fetched", "the engine stopped"): the market-profile detector needs 395 days and the
   wrapper loads twice that before each window, so a coin is first tested about 2.2 years after its listing, not 90
   days. BTC runs 32 windows, TAO 3, INJ and DOT 11. The rule's count and the engine's refusals should be one count,
   made before the engine runs.
3. **The explore half is thin.** The analysts read 2016-2021 only, where 3 of run 2's 8 coins have days in the box's
   profile (7.g says so in its analyses).
4. **A discovery's brief names final-group coins** as instruments (brief 087 of run 1: LINK, UNI, SOL). The backtests
   ran on the run's 8 coins all the same; the final coins should not be named anywhere in a run.
Also to check before any merge: the components step's build renamed `VolatilityScaledDistanceFromHighComponent`'s
default name and debug keys (its checks passed; no other file uses the old name, by the session's search).

**Step back: what does it show, and what one change would a practitioner make?**
- The machinery of today's rules works. The search found nothing: 0 of 22 confirmed (nights 7 to 9: 1 in 3). Three
  readings, not separated by this pilot: the two boxes bet against the market's direction (long in falls, short in
  rises); half of the ideas taken were not even on the box's side (defect 1); and each test stood on little data
  (defect 2), which lowers every t.
- **The one change: give a run data that exists.** The research coins should be drawn among coins that have the windows
  (their history counted with the warm-up the profile needs), and the windows counted by one rule. Then defect 1 (the
  idea's own side). Both before the next batch.
- Not yet seen on real data: a repair skipped by B12, a common record and a portfolio update called by `run_idea`, the
  direction check on the check half. A seeded run (a known candidate's plan and verdict, no model call) can show them
  at no model cost.
