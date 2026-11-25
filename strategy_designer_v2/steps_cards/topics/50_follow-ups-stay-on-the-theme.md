# Topic 50: follow-ups stay on their brief's theme

Status: built 2026-11-24 (option A); proof below  
Where: research: common (`theme.md`), step 7 (lines 7.b, 7.c, 7.e, 7.g; `analyse.py`), step 1, `loop`, `run_brief`  
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
| Lines 7.b, 7.c (inconclusive, rejected) | Their ideas stay on the theme: the theme's situation or a narrower case of it; when none is worth testing, "no ideas: the theme's effect is not in the data". Line 7.a unchanged: it already proposes only the tested idea on other data | they answer the brief's question |
| Line 7.d (repairs) | Unchanged: a repair already keeps the confirmed idea (2026-11-22) | |
| Lines 7.e and 7.g (what the book earns from; patterns) | Their ideas off the theme are discoveries: written as a new theme, which step 1 turns into a brief (its own number and family); on the theme, they stay follow-ups | a discovery is tested on its own theory, not counted as the old brief's |
| Step 1 | Writes a brief from a discovery (the finding, its numbers, the backtest it came from); a source whose only theory is already a brief answers `already-indexed` | the discovery's theme gets its first ideas like any brief, once |
| `loop` (with `run_brief`'s steps 1 and 2) | Before each turn, every new discovery of the run becomes a brief and its first ideas; one line each in `loop.jsonl`; steps 1 and 2 count in the run's spend | discoveries enter the search without the operator |
| `select_next` | A brief from a discovery ranks its ideas as follow-ups of the idea the discovery was found in (changed 2026-11-25, next steps 1n; at the build: group 1, as any brief) | a theme's own ideas run before the patterns found on the way; P9 weighs them |
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
| 2026-11-25 | A discovery's brief ranks its ideas as follow-ups (select_next, `discovery:` field); lines 7.e and 7.g are given the profile map (1q, option b) | the operator ("1n yes, 1q option b"), after night 7 | night 7: discovery briefs took 107 of 117 ideas tested, 0 of 4 themes answered; 31 of 51 confirmed books one effect | a morning review of discoveries (the operator: no manual step); no brief from a discovery far from the theme (1q a: loses finds such as night 6's Saturday carry) |
| 2026-11-24 | Option A, built | the operator ("go for that"), on the designer's recommendation | every theme answered; discoveries kept under their own theory | B: loses discoveries such as the weekday carry; C: themes stay unanswered |
| 2026-11-24 | An idea on the theme may change the effect's side (what the market does instead in the theme's situation), not only for a question brief | the designer, at the build | line 7.c's "what the market does instead" keeps the brief's situation and answers its question | side changes for question briefs only: 7.c's main proposal would be off the theme |
| 2026-11-24 | Step 1, given a source whose theory is already a brief and which states no other, writes no brief and names the existing one | the designer, from the proof | the same pattern found in several backtests becomes one brief; step 1's rule "write another theory" made it invent one the source did not show | one brief per discovery: duplicates, and invented variants |

## Proof (2026-11-24; about 4.0 USD)
Lines 7.b and 7.g rerun, unchanged inputs, on the 4 first ideas of night 6 whose analyses had ideas from both lines
(indecision 031-01, long reversal 031-03, streak 031-01, yearly low 031-01; step 4 rerun first, as the bars are not
kept: same window counts). Read against `common/theme.md`:

| Line | Night 6 | With topic 50 |
|---|---|---|
| 7.b | 6 ideas: 4 on the theme, 2 off (a wide day without the flat close; a 20-day return instead of a 2-3-month move) | 6 ideas, all on the theme; 2 name a profile ("in a rising market", "in a calm market": the streak's continuation, topic 49) |
| 7.g | 6 follow-ups, all off the theme (next-day rebounds, volume drift, momentum, the Saturday carry) | 0 follow-ups; 5 discoveries; on indecision "no ideas", the theme's situation looked at and nothing beyond chance |

- **The discoveries:** 3 of the 5 are the next-day rebound after a sharp fall (found in 2 backtests), the portfolio's own
  effect; the others are momentum in a calm market and short-term momentum.
- **Step 1 on discoveries** (a copy of the briefs list, `01_brief/topic50_proof_run/`): calm-market momentum gives brief
  032; the sharp-fall rebound gives brief 033; the same rebound from the other backtest first gave an invented variant
  (a fall closing at its low), then, with the rule fixed, `already-indexed: 033`; its narrower version in a falling,
  agitated market gives brief 034 (a close theory: another market). Each source line names the backtest and line.
- Tests: the loop turns each discovery into a brief once, logs it, and stops on a refused call without losing it.

## Status and next
Built. Next: the next night runs with it; its reading counts, per brief, the answer (real, not real, open) and the
discoveries turned into briefs.

## Links
`common/theme.md`; `common/idea_created_from.md` (a repair of a confirmed idea); topic 47 (1d-12, 1d-13); topic 45
(the 7.d rule); `runs/NIGHT6_RUN.md`; `orchestration/select_next/` (P9).
