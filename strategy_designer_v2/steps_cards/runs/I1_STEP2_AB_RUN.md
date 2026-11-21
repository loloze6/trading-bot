# Run brief: does "a move worth several round trips" change the ideas step 2 writes? (2026-11-20, before the run)

**Purpose (improvement I1, `topics/30_review/WORKFLOW_REVIEW.md`):** the record test (`runs/RETRO_DIAGNOSIS_RUN.md`)
showed that 0 of 91 books whose move per bet does not cover a round trip pays. Hourly briefs give mostly such ideas
(F2 of `common/findings.md`). Test whether one added line in the idea definition (`common/idea_definition.md`, which
step 2 reads) moves step 2 towards ideas that can pay, before changing anything for good.

**How:** step 2 (`02_ideation/helper/make_ideas.py`) on the two hourly briefs, 016 (grind versus jump) and 017 (funding
settlement clock), twice each: A with today's definition, B with this line added to it:

> - is large enough to pay for the trade that captures it: the move it predicts, from the close of the bar where its
>   situation shows, is several times the cost of a round trip (about 0.2 % of the value traded on today's venue). The
>   move of a few hours is usually smaller than that; a horizon long enough for the move to clear it is part of the idea.

The definition is restored after the B calls; the ideas are written to a scratch folder, not to any run. 4 model calls.

**Measures, read on the ideas' own text:** each idea's horizon (the "over the next N hours/days" it states); the share
of ideas of 4 hours or less (F2: they cannot pay); whether the ideas stay within the brief's theory.

**Expected outcomes:**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| T1. The line works | B gives clearly fewer ideas of 4 hours or less than A, on both briefs, and its ideas stay on the brief's theory | add the line to the definition (and to step 7's prompt) |
| T2. No effect | A and B give the same horizons | the definition alone does not steer step 2: the brief (step 1) or the findings register must carry it |
| T3. It distorts | B's ideas leave the brief's theory (horizons stretched by force, the claim changed) | the wording is wrong: rework it before use |

**Limits:** one call per brief and version, so differences of one or two ideas are noise; read only clear differences.

## Reading (2026-11-20, 20:25 Paris; 4 model calls, 0.23 USD; the definition restored after, checked)

The ideas are kept in `runs/i1_step2_ab/` (A: today's definition; B: with the line).
| Brief | A | B |
|---|---|---|
| 016, grind versus jump | 8 ideas, all 3-day horizons | 6 ideas, all 3-day horizons |
| 017, funding settlement clock | 6 ideas of 2 hours (and 1 on volume, 2 hours around the settlement) | 6 ideas of 4 hours |

**Outcome T2 (no real effect), with one nuance.** Brief 016 already gives 3-day ideas, A and B alike. On brief 017 the
line stretched the horizon from 2 to 4 hours and the ideas kept the brief's theory (no T3), but 4 hours stays in the
range where a move does not cover a round trip (F2). The horizon is set by **the brief's theory**: a theory about the
hours around a settlement gives ideas of a few hours, whatever the definition says.

**What it means.** The lever for "large enough to trade" is first at **step 1, the brief**: whether its theory can give
moves of several round trips (for hourly bars, horizons of a day or more, unless the move is large). The line in the
idea definition is still worth having for step 7 (whose ideas come from records, not from a brief's theory), but it is
not enough alone. Proposed, for the operator's review: step 1 reads the findings register (F1, F2) and a brief states
the horizon its theory works on, before ideas are written. Not built.
