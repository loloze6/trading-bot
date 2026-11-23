# Topic 47: why most real effects give a book that does not pay, and why paying books hold less on unseen dates

Status: open (measured 2026-11-23; for the operator's decision on which step to develop)  
Where: research: step 3 (how a book is built), step 6 (the Calmar bar), steps 1-2 (effect size), steps 5-6 and
`select_next` (how many tries of one effect)  
Opened: 2026-11-23, by the operator ("go on 1, 2, 3"), after the night-5 reading (`runs/RETEST_RUN.md`,
`runs/NIGHT5_PATHS.md`).

## Question
The workflow finds real effects (step 5 confirms two in three) but few of them pay (step 6), and paying books hold
less on unseen dates: which step owns each loss?

## Seen
**1. The Calmar gate** (`47_review/calmar_gate.py`, `calmar_gate.csv`; the 81 books step 5 confirmed in the five
night-5 runs, from their committed chart files; Calmar recomputed here equals step 6's to 3e-05).
- 72 of the 81 do not pay; **all 72 fail Calmar** (bar 0.75), 42 on Calmar alone.
- Holding the same coins on the same days: Calmar 0.16 (median), below 0.75 for all 81. The books that do not pay
  reach 0.40 (median); the 9 that pay, 0.85.
- The 72 fall into three groups, by where their deepest fall comes from:

| Group | Books | What it is | Seen in |
|---|---|---|---|
| A. The trade does not pay its cost | 25 | mean return per trade after costs at or below 0 (round trip 0.19 %) | settlement 15, absorption 6 |
| B. The book falls with the market | 41 | earns its cost per trade, but over its deepest fall holding the same coins fell more than 20 % | all runs; the deepest falls mostly in 2022 |
| C. Other | 6 | short or both-sided books caught in a market rise, or small falls | weekend, learned |

- Paying books against the others (medians): in a position on 23 % of the days against 67 %; 1,272 trades against
  5,267; 1.43 % per trade after costs against 0.24 %; deepest fall 12 % against 35 %; the same yearly return (10 %).
  A book that pays trades its effect rarely and strongly; one that does not is in the market most days, with an edge
  per trade close to its cost, and lives through the market's crashes.
- Step 6 chains the windows in fold order (2022-23, then 2018-21, then 2024-25), not in date order. Chained by date,
  Calmar's verdict changes for 3 of 81 books (1 fail to pass, 2 pass to fail): not the cause.
- 4 of the 81 books are exact copies of another (same Calmar, return and trades): a 7.d repair whose added condition
  changed nothing, a test spent for nothing.

**2. Search luck** (`47_review/search_luck.py`, `search_luck.csv`; the 59 ideas with an unseen test, all runs). The
share of the effect kept on unseen dates is the unseen statistic over what the in-sample effect would give on a period
that long (a statistic grows with the square root of the length).

| Ideas | 2016-17: n, holds, effect kept | 2026: n, holds, effect kept | In-sample t (median) |
|---|---|---|---|
| Generation 0-2 | 36, 92 %, 1.19 | 17, 82 %, 1.19 | 3.38 |
| Generation 3-4 | 21, 71 %, 0.44 | 14, 79 %, 0.63 | 3.77 |
| 0-4 ideas of its branch tested before it | 39, 85 %, 1.00 | 19, 84 %, 0.88 | |
| 5 or more tested before it | 9, 78 %, 0.77 | 6, 67 %, 0.39 | |

- The deeper a book (the more tries before it), the higher its in-sample statistic and the less of it is left on
  unseen dates: the pattern of a selection that keeps luck. Small samples (generation 5+: 2 ideas), and deeper ideas
  are also later nights' non-momentum ideas: the type of idea and the depth are mixed.

## Why it matters
Developing a step without knowing which one owns the loss spends builds where the loss is not.

## Options
| Option | Gain | Risk |
|---|---|---|
| Step 3: a book built for the effect: in a position only when the signal is strong (few, large trades), and not exposed to the market's direction (B: 41 books) | the largest group; what the 9 paying books already do | a new way to build books: a card, a design, a proof |
| Steps 1-2 (and 5): the effect's size per trade against the round trip measured before a book is built (A: 25 books) | stops spending tests on effects too small to trade | none if it is a measure, not a prompt sentence (the operator's caution on cost in prompts) |
| Step 6: the Calmar bar (0.75; holding gives 0.16) | a business choice, not a defect: the 9 paying books reach it | lowering it lets books through that fall with the market |
| Steps 5-6 and `select_next`: a stricter bar for a book found after many tries of its effect, and a branch that keeps failing the same check is left | fewer lucky books; tests spread over more effects | the size of the correction is to be designed |

Recommended: step 3 first (the largest group, and the mechanism the paying books show), with the effect size per trade
measured beside it (A); the search correction next.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|

## Status and next
For the operator: which step to develop first. Then a card for it (its business objective, its definitions), a plan
with gain, effort and risk, and its proof.
