# Common: definitions shared by several steps

One definition, one file: a step that needs it reads it here, so the steps cannot drift apart (operator, 2026-11-14).

| File | What | Read by |
|---|---|---|
| `idea_definition.md` | what an idea is (its market profile included) | step 2, step 7 |
| `data_available.md` | the coins and folds the workflow has data for | step 7.b (an idea on more data) |
| `backtest_record.md` | what a backtest records: its columns, their meaning, their limits | steps 3, 5, 7 |
| `lib.py` | the code shared by the helpers: the closed-book model call, atomic writes, a file's header, the idea fields step 3 reads, reading a shared definition and pasting it where a prompt names it (`{{NAME}}`); the market profiles' names and conditions; a helper started by another helper ends when that one ends (no orphan writing after a stop); the exploration and check folds and their windows in a record (`explore_and_check.md`) | every step's helper |
| `idea_created_from.md` | what an idea is created from (a brief or another idea), and how its id carries the track: line, analysis, ideas written together, generation | step 7's code (it writes the ids), the orchestration |
| `forecast.md` | how a config turns its components into a forecast and a position (`standardise` scales, it does not centre; the weighted mean; centring needs an offset; the recorded raw and transformed values); the holding period (7); the gap rule, what a book does when bars are missing (8) | steps 3, 5 |
| `explore_and_check.md` | exploring and checking on different years: step 7 explores folds B and C, step 5 checks a confirm's direction on folds A and D, and when the check is not judged | step 5, step 7 |
| `market_profile.md` | the kind of market a coin is in (trend over 60 days, agitation over 30 days): the six profiles, an idea's profile (its trend, its agitation or both), a profile specialist, a strategy's home, the profile map; how step 3's code builds a profile (topic 49) | steps 1, 2, 3, 7; step 3's code |
| `theme.md` | a brief's theme (situation and effect), an idea on or off the theme, a theme found real or not real, a discovery (topic 50) | lines 7.b, 7.c, 7.e, 7.g; `orchestration/loop` (a discovery becomes a brief) |
| `unseen_dates.md` | the dates no fold covers, the unseen periods (one windows file each) and the rule "holds" | `orchestration/unseen_test`, the operator |
| `measures.md` | how the workflow measures (returns counted once, holding, the book, Sharpe, Calmar, t-statistics) | steps 3, 5, 7; step 6's code computes the book the same way |
| `bets.py` | where an idea makes a bet on a record (the holding period's rule) and the band it trades with | `idea_size.py` (step 5); the book's diagnosis (`../topics/34_review/book_diagnosis.md`, a discovery tool of topic 34, not a step) |
| `idea_size.py` | the size of an idea (`measures.md`): unusual move per case, normal drift, total, strength | step 5 (step 7 reads its `size.json`) |
| `engine_changes.md` | the engine changes that can change a backtest's results, one dated line each (old runs stay as recorded) | anyone reading an older record; the readings of reruns |
