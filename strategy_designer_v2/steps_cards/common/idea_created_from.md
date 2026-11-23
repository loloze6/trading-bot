What an idea is created from, and how its id shows it (operator, 2026-11-16). Every idea is created from exactly one
thing, and its id carries the whole track back to its brief.

- **Created from a brief** (step 2): the id is the brief's number, the idea's number in that brief, and a short name:
  `002-01_sma-golden-cross-upward-drift` is idea 01 of brief 002. Its file says `brief: 002_...`.
- **Created from another idea** (step 7): one line read that idea's backtest and wrote it. The id is the other idea's
  **lineage code**, then a dot, the line's letter, the idea's number, and its own short name:
  `002-01.d1_golden-cross-with-momentum` is idea 1 that line 7.d wrote from idea `002-01`. Its file says
  `source-idea:` (the full id of the idea it was created from), `line:` and `backtest:`.
- **Lineage code:** the brief's idea number (`002-01`), then one `.<letter><number>` per generation: `002-01.d1.b2`.
  It is the track back to the brief, without the ancestors' short names (operator, 2026-11-23, topic 46: with every
  ancestor's name, an id passed the 255-byte limit of a file name at generation 5 to 6 and the idea was lost). The
  ancestors' names are in their own files, reached through `source-idea:`.
- **The number:** a line numbers its ideas after those it already wrote from the same idea in the run (an idea tested on
  two bar sizes is analysed twice by the same line), so that a lineage code names one idea in a run.
- **Ids written before 2026-11-23** carry every ancestor's short name
  (`002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum`). They stay as they are and are read through
  the same lineage code (`common/lib.py`: `idea_code`).

The track follows by reading the id from left to right:

| Id (short names left out) | Created from | Line | Generation |
|---|---|---|---|
| `001-01` | brief 001 | | 0 |
| `001-01.a1` | idea `001-01` | 7.a | 1 |
| `001-01.a1.c1` | idea `001-01.a1` | 7.c | 2 |

- **An analysis:** one line reading the backtest of one idea. Its ideas share the same start and the same letter:
  `001-01.a1.c1` and `001-01.a1.c2` are two ideas of the same analysis (line 7.c on idea `001-01.a1`); `001-01.a1.e1`
  is another analysis of the same idea (line 7.e). The same line reading the same idea in another run is another
  analysis: it writes other ideas (operator, 2026-11-16).
- **Ideas written together:** the ideas of one analysis.
- **Generation:** the number of analyses between the idea and its brief: the number of `.<letter><number>` steps in
  its lineage code (0 for an idea created from a brief).

**A repair of a confirmed idea** (operator, 2026-11-22; `topics/45_why-the-research-finds-only-long-momentum.md`): an
idea line 7.d writes from an idea step 5 confirmed and whose book step 6 found not profitable enough. The effect is real,
so its book is the effect traded the wrong way, and the repair trades the same effect another way:
- it keeps the confirmed idea's situation and its signal, in the idea's own words;
- it changes only how the book uses them: when to be out of the market, the exit or the holding, the size, the side
  (the side that loses left out), a stronger case of the same situation or a longer horizon, or a condition that comes
  from the idea's own theory or from what its book's falls showed;
- an added condition is not an effect of its own: if the condition alone could make the book pay, it is a separate idea,
  not a repair.
- a real idea is closed ("no ideas") only when the effect itself cannot be traded in any version of it (its situation,
  strength, horizon, side): a weak case is a reason to look for a stronger one.
The repair's book is compared with its parent's (`orchestration/ideas_similarities_check/`): how much of it the parent
explains, and how much the nearest paying book explains, show whether it kept the idea or drifted to another effect.
