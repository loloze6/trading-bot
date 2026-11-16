# select_next: validation on demo_run (2026-11-16)

**Called** by `loop` at each of its three turns on `demo_run` (`../../loop/validation/reading.md`), and by hand after.

- **The ranking follows the score**: turn 1 and 2 picked the two 7.e ideas (0.25 each; the tie went to the lower
  number), turn 3 the 7.g idea (0.22), ahead of 7.d's and 7.a's.
- **Every candidate is listed with its parts** (line, generation, record, score) in the loop's queue.
- **The records move with the results**: after turn 3, 7.g went from 1 of 1 (0.67) to 1 of 2 (0.50).
- **Same files, same ranking**: two calls on the same files gave the same output, byte for byte.
- **Duplicates**: none in this run; the rule is met by the tests (same text and same data; other data is not a duplicate).

**Seen, open for the operator**: an analysis is counted once per line and parent idea, across runs. 7.e's analysis of
the repair had already counted as a success in `validation_run`, so its success here did not move 7.e's record (2 of 2).
The card says "every analysis ... in every named run"; read strictly, the same idea read again in another run is a
second analysis. Not changed.
