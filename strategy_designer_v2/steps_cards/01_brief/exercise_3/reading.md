# Exercise 3: the brief index, on opus

Three calls, opus only, the exercise 2 prompt with three changes (`helper_system_prompt.md`): the index rule, a 120-word limit, an `index-line:` output; and the testability line removed. The index of three briefs (`inputs/briefs_index.md`) is pasted at the top of each request. Cost: 0.143 USD.

| request | expected | got | cost |
|---|---|---|---|
| no theme | a theory not in the index | "large coins lead small coins": new, 121 words (one over the limit), index line of 17 words | 0.023 |
| RSI theme | already-in-index, line 002 | already-in-index, line 002 | 0.017 |
| TradingView page | already-in-index, line 003 | already-in-index, line 003 | 0.103 |

The index works on all three. The new brief breaks the length limit by one word; a code count would catch it. Otherwise it meets every criterion: one theory, a reason marked as the helper's own, what would prove it wrong, no results, empty header (nothing stated).

Limits: one call per request. The index holds three lines; a long index is not tested. With a source whose main theory is taken, the helper stops; it does not write the source's next theory. That follows the rule as written.
