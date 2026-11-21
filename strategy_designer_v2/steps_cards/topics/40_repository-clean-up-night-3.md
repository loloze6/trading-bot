# Topic 40: repository clean-up, night 3

Status: open (part done; the rest proposed)  
Where: the repository's structure (`steps_cards/`)  
Opened: 2026-11-21, the operator: "cleaning work of the repo, ensuring structure is clean and standard, files on
correct folders, card for the topic created".

## Question
Is every file in the one place named after what it is, with the same layout in every step and function?

## Seen (survey, 2026-11-21)
- Step 5's size (`common/idea_size.py`) read its definition of a bet from the book's diagnosis, a temporary discovery
  tool of topic 34 kept in `common/` (shared definitions).
- Topic folders of working files (`topics/30_review/`, `36_review/`) had no rule written for them.
- Three run folders are named `hold2_rerun` instead of `<name>_run` (in 03, 04, 05, 06 and `orchestration/unseen_test`;
  65 tracked files name them, the records' own run.md and manifests included).
- `orchestration/duration/` holds the speed work's measures, plans and proofs (topics 21 and 33): working files of
  topics, not a function (it has no card; 14 tracked files name the path).
- `07f_real_and_profitable/` has no `validation/` folder, unlike the other step 7 lines.
- Three child sessions of 2026-11-20 (hold2 parts B and C, engine speed round 2) were finished, their branches merged.

## Done (2026-11-21)
| Change | Proof |
|---|---|
| The bet's definition (`bets`, `band_of`) moved verbatim to `common/bets.py`, with its test; `idea_size.py` reads it there | the size on 3 records identical before and after; the cards' 100 tests pass, as before |
| The book's diagnosis (`book_diagnosis.py`, `.md`, its tests) moved to `topics/34_review/`; references updated | its tests pass from there; the retro scripts' paths updated |
| `topics/README.md`: a topic's working files sit in `NN_review/` next to its card | - |
| Topic 34: its results recorded as built into steps 5 and 7, the diagnosis kept as a tool | - |
| The three finished child sessions archived | their branches are in the working branch (checked) |

## Proposed, for the operator's go
| Change | Gain | Risk |
|---|---|---|
| Rename `hold2_rerun` to `hold2_rerun_run` everywhere | one naming rule for every run | 65 files, records' own paths inside; a rename touches records (git keeps the history) |
| Move `orchestration/duration/` to `topics/33_review/duration/` | `orchestration/` holds only functions with cards | 14 references to update |
| Validate line 7.f (its own `validation/`), or say in its card why it has none | the same layout in every line | one small exercise (model calls) |

Recommended: the second and the third; the first only if a tool needs the `_run` suffix (none does today).

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-21 | Clean-up done as listed above | the session, on the operator's night go | one place per thing; step 5 no longer depends on a temporary tool | renames of records: proposed only |

## Status and next
The proposed rows wait for the operator's go.

## Links
`common/README.md`, `topics/README.md`, topic 34.
