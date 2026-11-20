# Common: definitions shared by several steps

One definition, one file: a step that needs it reads it here, so the steps cannot drift apart (operator, 2026-11-14).

| File | What | Read by |
|---|---|---|
| `idea_definition.md` | what an idea is | step 2, step 7 |
| `data_available.md` | the coins and folds the workflow has data for | step 7.b (an idea on more data) |
| `backtest_record.md` | what a backtest records: its columns, their meaning, their limits | steps 3, 5, 7 |
| `lib.py` | the code shared by the helpers: the closed-book model call, atomic writes, a file's header, the idea fields step 3 reads, reading a shared definition | every step's helper |
| `idea_created_from.md` | what an idea is created from (a brief or another idea), and how its id carries the track: line, analysis, ideas written together, generation | step 7's code (it writes the ids), the orchestration |
| `forecast.md` | how a config turns its components into a forecast and a position (`standardise` scales, it does not centre; the weighted mean; centring needs an offset; the recorded raw and transformed values) | steps 3, 5 |
| `unseen_dates.md` | the dates no fold covers, the unseen periods (one windows file each) and the rule "holds" | `orchestration/unseen_test`, the operator |
| `measures.md` | how the workflow measures (returns counted once, holding, the book, Sharpe, Calmar, t-statistics) | steps 3, 5, 7; step 6's code computes the book the same way |
| `book_diagnosis.md` | **draft, topic 34:** why a book does or does not pay (big enough, opening time, closing time, holding past the bets, trend), read from a backtest's record | none yet (proposed: the observe-and-advise stage, step 7); code `book_diagnosis.py` |
| `findings.md` | **draft, I2:** what the runs have measured about what pays (short statements with their evidence and date); a finding is not a rule | step 7 (every line); proposed: steps 1, 2 |
| `idea_size.py` | the size of an idea (`measures.md`): unusual move per case, normal drift, total, strength | steps 5 and 7 (`trade_cost`: step 7) |
