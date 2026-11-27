# Build B10: a discovery is asked for when it would be tested, and counted where it comes from (2026-11-27)

Build session for the designer, branch `build-b10` from `ccr-6624e33e-aakrpv` (7b7f0e8bbd); the operator's go ("M1
ok", next steps B10).

## Purpose and expected outcomes (set by the designer's brief, before the build)
- **Purpose:** when do we want an idea from a discovery rather than keep the line of the idea being tested? When the
  discovery would be the next idea tested. (1) A tested idea of a brief written from a discovery counts as an analysis
  of its own line, "7.g discovery", and the ranking scores that brief's ideas with it; 7.g's on-theme follow-ups keep
  "7.g". (2) Line 7.g is called after a test only when an idea it would write would rank first in the run's queue.
- **Expected:** "7.g discovery" about 0.29 (the designer's 23 of 81), 7.g 0.12, no other line's record changed; on
  night 9's replay, fewer 7.g calls, and **0** skipped calls whose discovery's brief later gave a profitable strategy;
  a seeded run gives the same files with and without the change, the rule's journal line aside; both test suites pass.

## What happened, in short
| | Expected | Found |
|---|---|---|
| "7.g discovery" | about 0.29 (23 of 81) | **0.21 (17 of 82)**: a success counted as for every line, the brief's own ideas; the 23 counted the brief's whole lineage |
| step 2 | | 0.16 (22 of 143) to **0.10 (5 of 61)** |
| other lines | unchanged | unchanged (7.g 0.12, 18 of 154) |
| night 9, 7.g calls | fewer | **52 of 184 skipped, 28.00 of 90.37 USD** |
| profitable strategies lost | 0 | **0 of 11** with a skipped call on their path |
| seeded run, change not in effect | same files | **same files** (1118; 4 differ in allowed ways only) |
| seeded run, rule in effect | | one journal line `not called`, no 7.g analysis, no model call |

A first reading of the rule, built first and rejected: the idea 7.g would write given the tested idea's w and group,
compared by group then priority. It skipped 156 of 184 calls, and **6 of night 9's 11 profitable strategies** had a
skipped call on their path (chopdeep's first test, whose discovery became brief 074 and 5 strategies; fallcalmfade's
074-01.b1, whose 7.g idea is one). The rule kept is the brief's wording: the score, without w, against the best waiting
idea's priority. Its reason, in 7.g's card: w is the tested book's difference from the held books, and what 7.g finds is
a pattern that book does not explain.

## The files (shared files named)
| File | Change |
|---|---|
| `orchestration/select_next/helper/select_next.py` (**shared with build-b2-1**) | `DISCOVERY = "7.g discovery"`; `records()`: a tested idea of a discovery's brief counts there, not in step 2; `briefed_discoveries()`, and `discovery_of()` also reads the loop's line for a brief written before the `discovery:` field; `rank()`: a discovery's brief's own ideas get that record and that line name; `discovery_call()`: the call rule. Nothing in the candidates or the groups changed |
| `orchestration/select_next/helper/test_select_next.py` (**shared with build-b2-1**) | one assertion (a discovery's brief's idea: line "7.g discovery"); two tests: the record, the call rule |
| `orchestration/select_next/card.md` (**shared with build-b2-1**) | the record of a discovery's brief, its numbers; line 7.g's call |
| `orchestration/run_idea/helper/run_idea.py` | `call_patterns()` (the rule, with the loop's failed ideas left out) before the step 7 lines start; `Journal.not_called()` (one line) |
| `orchestration/run_idea/card.md` | "Line 7.g's call" |
| `07g_patterns/card.md` (build-b2-1 changes 7.g's prompt, `helper/line_prompt.md`, not this card) | the entry condition: the rule, where, why, the variant rejected |
| `runs/build_b10/` | `replay.py`, `summarize.py` and `replay_result.txt` (night 9's replay); `fidelity.py` (how exact it is); `run_one.sh`, `compare.py` (the seeded runs) |

Not touched: `loop/`, `run_brief/`, the lines' `line.yaml` and `analyse.py` (build-b11-b12's entry conditions).

## Proof 1: the records, every run of the repository, before and after
| Line | Before | After |
|---|---|---|
| step 2 | 22 of 143, 0.1586 | **5 of 61, 0.0952** |
| 7.g discovery | (in step 2) | **17 of 82, 0.2143** |
| 7.a | 0 of 6, 0.125 | the same |
| 7.b | 49 of 269, 0.1845 | the same |
| 7.c | 1 of 8, 0.20 | the same |
| 7.d | 56 of 223, 0.2533 | the same |
| 7.e | 34 of 46, 0.7292 | the same |
| 7.g | 18 of 154, 0.1218 | the same |

82 of the 143 analyses of step 2 move (82 briefs in a run, 17 of them with a success); nothing else moves. Which
briefs: 29 carry the `discovery:` field (2 with a success); 53 were written by the loop from a discovery before the field
(nights 7 and 8; 15 with a success), known from the loop's line. With the field alone, "7.g discovery" would be 2 of 29
(0.10). The designer's 23 of 81 counted a brief's success down its whole lineage: 6 of the 23 briefs paid only through
a follow-up (7.b, 7.d), whose success is that line's, as for every line. 2 of the 82 briefs come from discoveries of
line 7.e (open, below).

## Proof 2: night 9's six runs replayed
For each of the 184 ideas the loop tested, in its order, the run's queue rebuilt as it stood when step 7 started on it,
and `discovery_call` (the code `run_idea` calls) asked whether 7.g would have been called.

| Run | Tests | 7.g calls made | Their USD | Calls the rule skips | Their USD | Of which behind a brief's own idea | Variant (w and groups): skips | Its USD |
|---|---|---|---|---|---|---|---|---|
| night9_chopagishort_run | 27 | 27 | 16.74 | 23 | 14.76 | 0 | 23 | 14.76 |
| night9_chopdeep_run | 35 | 35 | 17.36 | 7 | 3.24 | 3 | 30 | 14.98 |
| night9_chopmonth_run | 35 | 35 | 16.11 | 13 | 5.88 | 2 | 30 | 13.90 |
| night9_chopstretch_run | 31 | 31 | 14.33 | 2 | 0.95 | 0 | 29 | 13.51 |
| night9_fallcalmfade_run | 28 | 28 | 12.87 | 0 | 0.00 | 0 | 20 | 9.24 |
| night9_fallcalmwide_run | 28 | 28 | 12.96 | 7 | 3.18 | 1 | 24 | 11.28 |
| all | 184 | 184 | 90.37 | 52 | 28.00 | 6 | 156 | 77.68 |

Calls kept by the rule: 132, of which with nothing waiting: 1. 7.g calls whose helper failed: 1 (counted as made).

The path check: for each of night 9's 11 profitable strategies (confirmed, profitable enough), the 7.g calls it
descends from (the discovery its brief came from, an on-theme idea of 7.g on its line), and whether one was skipped:

| Run | Strategy | 7.g calls on its path (the tested idea read) | Rule | Variant |
|---|---|---|---|---|
| night9_chopdeep_run | 074-01.g1.d1 | 074-01, 072-01 | all called | skipped: 072-01 |
| night9_chopdeep_run | 074-01.b1.b1.b1.b1.d1.d1 | 072-01 | all called | skipped: 072-01 |
| night9_chopdeep_run | 074-01.b1.b1.b1.b1.d1.d2 | 072-01 | all called | skipped: 072-01 |
| night9_chopdeep_run | 074-01.b1.b1.b1.b1.d1.g1 | 074-01.b1.b1.b1.b1.d1, 072-01 | all called | skipped: 074-01.b1.b1.b1.b1.d1, 072-01 |
| night9_chopdeep_run | 074-01.b1.b1.b1.b1.g1.e1 | 074-01.b1.b1.b1.b1, 072-01 | all called | skipped: 072-01 |
| night9_fallcalmfade_run | 074-01.b1.d2 | 070-01 | all called | all called |
| night9_fallcalmfade_run | 074-01.b1.d1.d1 | 070-01 | all called | all called |
| night9_fallcalmfade_run | 074-01.b1.g1 | 074-01.b1, 070-01 | all called | skipped: 074-01.b1 |
| night9_fallcalmfade_run | 070-01.b1.b1.b1 | - | all called | all called |
| night9_fallcalmfade_run | 074-01.b1.d3.d1 | 070-01 | all called | all called |
| night9_fallcalmfade_run | 074-01.b1.d3.d2.d1 | 070-01 | all called | all called |

Profitable strategies with a skipped 7.g call on their path: the rule 0 of 11; the variant 6 of 11.

The skipped calls had written 25 discoveries (10 became briefs) and 47 on-theme ideas; none of them led to a profitable
strategy.

**How exact the replay is.**
- The order and the times: the loop's lines and `run_idea`'s journal (the decision time: the start of the idea's first
  step 7 line, its journal time minus its seconds).
- The files at that time: a plan, a verdict, a check, a line's ideas dated by their journal lines; a discovery's brief
  and its ideas by the loop's line that wrote them; a register book by its `added_utc`; the loop's lines up to then (its
  failed ideas). Every named run is rebuilt, as the records read them all (the six ran side by side).
- Night 9's briefs as git had them: the designer removed, put back and removed again the `discovery:` line of starting
  briefs during the night; the version used is the last commit at or before the decision (a commit lags the working
  tree by up to a few minutes).
- Not rebuilt (today's state): the register's comparisons' contents (a later recomputation keeps its new nearest
  book), the components step's answers, the plans' wish lists.
- **Check:** at the turns the loop logged, the rebuilt queue ranked by the code that ran that night:
  at **161 of 200** turns the rebuilt queue's first idea is the one the loop chose; at
  29 it is ranked 2 to 15, and at 10 it is not a candidate in the rebuild (an idea turned again after a failure, or
  tested by the rebuild's dating). The misses cluster: 22 of 39 in fallcalmfade between 22:31 and 01:52 (when its
  briefs' `discovery:` lines were being edited), and 9 in chopstretch, where the rebuild puts 067-02.b1.g1 first and the
  loop never chose it. Likely cause, not checked turn by turn: the register was rebuilt over every book after the night
  (`db4390f`, 08:09 UTC), which changes the parents' differences w and so the groups.
- It is not a simulation: after a skipped call, the turns are those that happened; with the rule, the night would have
  taken other turns.

## Proof 3: runs of `run_idea` on seeded runs (no model call)
| Run | What | Result |
|---|---|---|
| (a) the change not in effect | night 9's 074-01.b1.g1 (fallcalmfade), seeded as `build_a4_join/run_one.sh` (plan, verdict, every line's outputs), once with this branch's `run_idea.py` and `select_next.py`, once with those of this build's base, 7b7f0e8bbd8 | **the same files**: 1118 on each side, none only on one; 438 byte-identical, 676 identical once times, shas, ids, paths and durations are masked; 4 different in allowed ways only, as build A4's proof: the order in which the parallel step 7 lines finished (`journal.jsonl`, `table.json`, `table.md`: the same 13 journal lines and the same row once sorted, times and minutes aside), the backtest's minutes, the bot's log (the order in which the coins were read). The rule is not decided: 7.g's analysis is in the run |
| (b) the rule in effect | night 9's 074-01.b1.b1.b1.b1.g1 (chopdeep, inconclusive, profitable enough), seeded without 7.g's outputs, then with them | **only 7.g's files differ.** Without 7.g's outputs, the rule is decided: `step7_7.g: not called: an idea of 7.g
would score 0.0268 = record 0.2143 (7.g discovery) / (1 + generation 7); the best waiting idea,
074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade, has priority 0.0456: it would not rank first`, no model call,
cost 0.00 USD. Against the run with 7.g's outputs seeded: 1827 files against 1834; the 7 only in the seeded run are 7.g's
(its index line, its analysis, result and exploration rounds); 649 byte-identical, 1175 identical once masked; 3 differ:
the journal's 7.g line (`not called: ...` against `skipped: its output exists`), the row's step 7 (7.b and 7.e against
7.b, 7.e and 7.g's "no ideas"), the table's text. Every bar, trade, verdict and check is the same |

## Tests
| Suite | Result |
|---|---|
| cards' tests (`VENV -m pytest -q strategy_designer_v2/steps_cards`) | **206 passed** (204 before, plus the two of this build); `topics/47_review/fold_rules_test.csv`, rewritten by the suite, restored |
| bot's tests (`cd trading-bot && VENV -m pytest -q`) | **1682 passed, 16 skipped** (75 deselected by its `pytest.ini`). Run first with 4 workers (`-n 4`): 2 failed, `test_standard_checks` of two built components, on their 30 s time limit; both pass alone (30.5 s), and the whole suite passes without workers, as the brief asks. Nothing in `trading-bot/` is changed by this build |

## What went wrong during the build (redone)
- The first replays read night 9's briefs as they are today; the designer had removed and put back the `discovery:`
  line of starting briefs during the night, so their ideas ranked differently then. Redone with git's versions (a first
  attempt with a wrong git path left the briefs out; caught and redone).
- The first proof (a) and the first exactness check took the "old" code from the local `ccr-6624e33e-aakrpv` ref,
  which was 793 commits behind this build's base. Both redone with 7b7f0e8bbd8: the results above are those.
- A seeded run was stopped by the session's 30-minute limit while restoring the checkout; the restore was finished by
  hand with the script's own steps (0 changes left).

## Open, for the designer
- **The rule is decided before the other step 7 lines of the same test run** (they run side by side): an idea they
  write after it may rank above 7.g's. Waiting for them would make step 7 sequential. Not changed.
- **Discoveries of line 7.e** (2 of the 82 briefs) count in "7.g discovery"; 7.e's calls are not under the rule.
- **The saving is 28 USD of 7.g's 90 on night 9 (31 %)**, read on the night as it happened; the money would have gone to
  other tests.
- **A starting brief written from a discovery but run as the run's theme** (night 9's 061, 064, 067, 072 once their
  `discovery:` line was removed) counts in step 2: the record follows the field and the loop's lines, as the ranking.
- **Merging with build-b2-1:** both change `select_next.py`; this build touched `records()`, `discovery_of()`, the
  record line of `rank()` and added `discovery_call()`, `briefed_discoveries()`; build-b2-1 changes the candidates.
