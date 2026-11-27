# Step 5's answers (B11, operator 2026-11-27)

Step 5 asks: is this idea real? It gives one of five answers. In plain words:

| Answer | What it means | Which line reads it |
|---|---|---|
| **confirmed** | the market does what the idea says, by the plan's confirm rule | 7.d (when the book does not pay), 7.g |
| **inconclusive** (unclear) | a sign of the effect, not enough proof: more cases or a clearer test may confirm it | 7.b, 7.g |
| **no effect** | enough cases, and the effect is near zero or points the other way: the data shows it absent | 7.c, 7.g |
| **not observable** | fewer cases than the plan's minimum: the data could not show the idea | 7.a, 7.g |
| **mismatch** | the test does not do what its plan says: no answer on the idea | step 3 again |

## No effect, the rule
An answer is **no effect** when:
- the plan's reject rule is met (the old answer "rejected": t at most -2 against the idea); or
- the plan's criterion gives inconclusive, **and** the measure counts at least **30 cases** (the confirmation's minimum),
  **and** the main measure's t, **counted in the idea's direction**, is **below 1**.

- **The idea's direction** is the side of the plan's confirm rule: the sign of the first t threshold in its "Confirm:"
  line (`t ≥ 2`: the idea's t is the t as measured; `t ≤ -2`: the t with its sign turned). Why: a plan whose idea is a
  falling slope confirms on t ≤ -2; its t of -1.8 is a sign of the effect, not its absence.
- **The cases** are the measure's own count of cases (the smallest count whose name says "case", else the smallest
  count), as the direction check reads them (`explore_and_check.md`).
- An inconclusive answer without a t, or whose plan states no t threshold, stays inconclusive: absence is not shown.
- Why t below 1 (nights 7 to 9, `topics/47_review/night9_review.txt`): the follow-ups of an unclear test with t below 1:
  72 tested, 10 confirmed (14 %), 2 profitable; with t from 1 to 2: 56, 17 (30 %), 7.

The rule is applied by step 5's code (`05_verification/helper/make_verdict.py`), after the plan's criterion and the
direction check, never by the model: the model applies the plan's own three rules (confirm, reject, inconclusive).

## Old records
Records written before this rule keep their words. A reader reads an old **"rejected"** as **"no effect"**
(`lib.py`, `step5_answer`). Old "inconclusive" answers are not re-read: they stay as recorded.
