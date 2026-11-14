# Common: definitions shared by several steps

One definition, one file: a step that needs it reads it here, so the steps cannot drift apart (operator, 2026-11-14).

| File | What | Read by |
|---|---|---|
| `idea_definition.md` | what an idea is | step 2, step 7 |
| `measures.md` | how the workflow measures (returns counted once, holding, the book, Sharpe, Calmar, t-statistics) | steps 3, 5, 7; step 6's code computes the book the same way |
