# 7.a exercise 3: same idea on other data, done by code (2026-11-15)

**Changes**, from what the runs showed (operator, 2026-11-15):
- the prompt proposes only the tested idea unchanged, on data where it can be observed (more coins, periods or another
  bar size; the idea's times are in real time); the "other time scale" route is removed (it changed the idea); "no
  ideas" with the cases needed against the cases available, when no data would do;
- **step 7 now receives the tested idea itself** (the fields step 3 reads: brief, data lines, Idea, Consequence);
  before, every line saw only the plan, with step 3's adaptation, and rebuilt the idea from it;
- **"same idea on other data" is a `same-idea-on:` block**: the line gives only the data; code copies the tested
  idea's Idea and Consequence and refuses data not in `common/data_available.md` (also used by 7.b's route 2).

**Inputs**: the card's two cut records (001-01 and 002-05, one window of one coin, not observable). A real case was
rebuilt with the current steps (N4-01 on NEAR, SUI, TAO, ONDO, fold D): with the current plan it reaches its minimum
count (inconclusive), so it is not an input of this line.

**Runs.** Runs 1 to 3 rewrote the idea (the plan's adapted form, a new horizon) and wrote free-text data lines; run 4,
with the tested idea in the input and the `same-idea-on:` block, gave the tested idea's own sentence on valid data.

| Proposal (run 4) | Data | Step 5 |
|---|---|---|
| 001-01: after the RSI reaches a high extreme, price falls back | 6 coins, folds A to D | observable: **rejected** (t 2.58 the other way, 595 cases) |
| 002-05: over the stretch from an up-cross to the next down-cross, price rises more | 10 coins, folds A to D | observable: inconclusive (t 0.03, 12,451 bars) |

**Validated**: on both inputs, its proposal made the idea observable.
