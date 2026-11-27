# The search rules joined: B10, B11, B12, B2.1, B13 (2026-11-27)

Designer's session, branch `join-b` from the working branch at 3a51fe9f872; the operator's go on each line
(2026-11-27). Builds: `build-b11-b12` (`BUILD_B11_B12.md`), `build-b10` (`BUILD_B10.md`), `build-b2-1`
(`BUILD_B2_1.md`, B2.1 and B13).

## Purpose and expected outcome (written before the proof)
- **Purpose:** one working branch with the five search rules: step 5's "no effect" (B11), repairs only when close
  (B12), discoveries counted where they come from and 7.g called when its idea would be tested next (B10), a run's
  target box part of its theme (B2.1), the untested ideas naming a boxed run's box taken first (B13).
- **Expected:** a run with no box gives the same files as before, except what B11 changes by its rule (the unseen
  test's own step 5 answers: the effect check, and "no effect" where t is below 1); both test suites pass.

## What was joined
| Join | What |
|---|---|
| `build-b11-b12` (0fddd6dc755) | merged, no conflict |
| `build-b10` (1eb6d310c21) | merged, no conflict |
| `build-b2-1` (2d4fde02a58) | merged; `07_common/helper/analyse.py`: both imports kept (B11's `step5_answer`, B2.1's `target_box`) |
| `common/idea_definition.md` | "if rejected" read as "if the data shows no effect" (the leftover B11's build named) |

## Proofs
| Proof | Result |
|---|---|
| cards' tests | 224 passed (`fold_rules_test.csv` restored) |
| bot's tests | 1693 passed, 8 skipped |
| `run_idea` with no box, the working branch's code (23 code and prompt files of 3a51fe9f872 put back) against the joined code; E's 074-01.b1.g1 in a seeded run (`build_a4_join/run_one.sh`, no model call) | 1118 files on each side, none only on one: 431 byte-identical, 676 identical once times, shas, ids, paths and durations are masked, **11 different, all named**: the unseen test's step 5 files for its two periods (the effect check added; 2026's answer "no effect", t +0.019 in the idea's direction, 80 cases), its index line, its log and result, the run's table (the same), and the allowed ones (the order the parallel step 7 lines finished, one duration, the bot's log). The same 11 as B11's own proof. Both runs: confirmed (+4.26), profitable enough, holds on both periods. Output: `build_b_join/` |

## Not done
- No run with a box, with "no effect", with a skipped 7.d or 7.g call has gone through the joined code on real data
  with a model: that is the pilot (A4 part 7).
