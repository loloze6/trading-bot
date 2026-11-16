# select_next: validation on demo_run (2026-11-16)

**Called** by `loop` at each of its three turns on `demo_run` (`../../loop/validation/reading.md`), and by hand after.

- **The ranking follows the score**: turn 1 and 2 picked the two 7.e ideas (0.25 each; the tie went to the lower
  number), turn 3 the 7.g idea (0.22), ahead of 7.d's and 7.a's.
- **Every candidate is listed with its parts** (line, generation, record, score) in the loop's queue.
- **The records move with the results**: after turn 3, 7.g went from 1 of 1 (0.67) to 1 of 2 (0.50).
- **Same files, same ranking**: two calls on the same files gave the same output, byte for byte.
- **Duplicates**: none in this run; the rule is met by the tests (same text and same data; other data is not a duplicate).

**Changed after the test (operator, 2026-11-16)**: an analysis was counted once per line and parent idea, across
runs, so 7.e's reading of the repair in demo_run (e1, e2, both confirmed) did not count: its reading in validation_run
(another e1, confirmed) already had. Each run's reading now counts as its own analysis: it writes other ideas, tested
on their own. Records after the change: 7.e 0.80 (3 of 3), 7.b 0.75, 7.c 0.67, 7.g 0.50, 7.d 0.50 (2 of 4), 7.a 0.25,
step 2 0.20 (0 of 3). The next turn on demo_run is unchanged (7.b first).
