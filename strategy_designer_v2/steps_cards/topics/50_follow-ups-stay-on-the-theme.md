# Topic 50: follow-ups stay on their brief's theme

Status: open (designed 2026-11-24; waits for the operator's go)  
Where: research: common (`theme.md`), step 7 (lines 7.a, 7.b, 7.c, 7.e, 7.g), step 1, `select_next`  
Opened: 2026-11-24, the operator ("we performed a change recently to keep ideas on the same theme: wasn't it supposed to
do what we try to solve?"); next steps 1j.

## Question
How does the search answer a brief's theory, real or not, instead of drifting to effects the portfolio already holds?

## Seen
- **The first ideas rarely hold** (topic 47, 1d-12): 13 of 140 ideas written from a brief are confirmed (9 %); night 6:
  0 of 16. Their effect is not in the data (median t 0.32; 41 % the other way).
- **The follow-ups leave the theme at once** (topic 47, 1d-13): on night 6 the first follow-ups came from line 7.b (14,
  2 confirmed) and line 7.g (8, 5 confirmed); 6 of 7 confirmed first follow-ups re-found the portfolio's effects (the
  next-day rebound after a fall, trend continuation). The four themes were never answered.
- **The rule "keep the idea" covers line 7.d only** (2026-11-22): it runs on a confirmed idea whose book does not pay;
  on night 6 no first idea was confirmed, so it never ran.
- **Line 7.g's discoveries can be new:** one of night 6's two new portfolio candidates ("a week's gain carries into
  Saturday") came from line 7.g, off its theme (the yearly low).

## Why it matters
Without it, a brief's theory is never answered, and the search spends its budget re-finding the same two effects under
other briefs' names.

## The terms (business definitions: `common/theme.md`)
A brief's theme; its situation and its effect; an idea on the theme; an idea off the theme; a theme found real; a theme
found not real; a discovery.

## What changes, step by step (the design)
| Where | Change | Why |
|---|---|---|
| `common/theme.md` | The definitions above | one meaning for "on the theme", read by every line |
| Lines 7.a, 7.b, 7.c (not observable, inconclusive, rejected) | Their ideas stay on the theme: the theme's situation or a narrower case of it; when none is worth testing, "no ideas: the theme's effect is not in the data" | they answer the brief's question |
| Line 7.d (repairs) | Unchanged: a repair already keeps the confirmed idea (2026-11-22) | |
| Lines 7.e and 7.g (what the book earns from; patterns) | Their ideas off the theme are discoveries: written as a new theme, which step 1 turns into a brief (its own number and family); on the theme, they stay follow-ups | a discovery is tested on its own theory, not counted as the old brief's |
| Step 1 | Writes a brief from a discovery (the finding, its numbers, the backtest it came from) | the discovery's theme gets its first ideas like any brief |
| `select_next` | A brief from a discovery is a brief: its first ideas come in group 1; P9 still pushes copies of held books down | one rule for every brief |
| The run's reading | Each brief ends with its answer: real, not real, or open (budget ended) | the brief's question is answered and recorded |

## Options
| Option | Gain | Risk |
|---|---|---|
| A. Lines 7.a, 7.b, 7.c stay on the theme; 7.e and 7.g's off-theme findings become new briefs | every theme answered; discoveries kept and tested fairly; P9 handles copies | more briefs to run; a discovery brief is chosen after looking at the data (the direction check on folds A and D covers that) |
| B. Every line stays on the theme, discoveries dropped | simplest; themes answered | loses findings like the weekday carry (one of two new candidates of night 6) |
| C. No change; P9 alone pushes copies down | no build | themes still unanswered; follow-ups still leave them |

Recommended: A. It answers every theme and keeps what 7.g finds, under its own name.

## Proof plan (before the merge)
- Lines 7.b and 7.g rerun on 4 fixed backtests of night 6 (the four briefs' first ideas): 7.b's ideas stay on the theme,
  or it answers "no ideas: not in the data"; 7.g's off-theme findings are written as discoveries (a new theme), not as
  follow-ups.
- Step 1 writes one brief from one discovery.
- Cost: about 3 to 5 USD of model calls.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|

## Status and next
Designed; the operator's go on option A, then the build and its proof; together with topic 49.

## Links
`common/theme.md`; `common/idea_created_from.md` (a repair of a confirmed idea); topic 47 (1d-12, 1d-13); topic 45
(the 7.d rule); `runs/NIGHT6_RUN.md`; `orchestration/select_next/` (P9).
