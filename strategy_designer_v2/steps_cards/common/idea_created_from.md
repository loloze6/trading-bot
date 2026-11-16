What an idea is created from, and how its id shows it (operator, 2026-11-16). Every idea is created from exactly one
thing, and its id carries the whole track back to its brief.

- **Created from a brief** (step 2): the id is the brief's number, the idea's number in that brief, and a short name:
  `002-01_sma-golden-cross-upward-drift` is idea 01 of brief 002. Its file says `brief: 002_...`.
- **Created from another idea** (step 7): one line read that idea's backtest and wrote it. The id is the other idea's
  id, then a dot, the line's letter, the idea's number in that analysis, and a short name:
  `002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum` is idea 1 that line 7.d wrote from idea `002-01`.
  Its file says `source-idea:` (the idea it was created from), `line:` and `backtest:`.

The track follows by reading the id from left to right:

| Id (short names left out) | Created from | Line | Generation |
|---|---|---|---|
| `001-01` | brief 001 | | 0 |
| `001-01.a1` | idea `001-01` | 7.a | 1 |
| `001-01.a1.c1` | idea `001-01.a1` | 7.c | 2 |

- **An analysis:** one line reading the backtest of one idea. Its ideas share the same start and the same letter:
  `001-01.a1.c1` and `001-01.a1.c2` are two ideas of the same analysis (line 7.c on idea `001-01.a1`); `001-01.a1.e1`
  is another analysis of the same idea (line 7.e).
- **Ideas written together:** the ideas of one analysis.
- **Generation:** the number of analyses between the idea and its brief: the number of `.<letter><number>_` parts in
  its id (0 for an idea created from a brief).
