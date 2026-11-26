# Topic 52: decide-next as an agent step that reads why each idea exists

Status: parked (the operator, 2026-11-25)  
Where: research: `select_next` (decide-next), step 2 and the step 7 lines (a new field in each idea)  
Opened: 2026-11-25, the operator ("park another ideas design for decide-next: an agent step that would consider new
fields of each analyst and brief idea around why having this idea").

## Question
Would the next idea be better chosen by an agent that reads, for each candidate, why it exists, than by today's score?

## Seen
- **Today's decide-next is code** (`orchestration/select_next/card.md`): three groups (a brief's own ideas; follow-ups of
  confirmed ideas unlike the held books; the others), and inside a group one score: the record of the line that wrote
  the idea / (1 + its generation), times P9's weight. It never reads an idea's text.
- **What the score cannot see** (night 7, `runs/NIGHT7_RUN.md`): 31 of 51 confirmed books were one effect (the next-day
  rebound), ranked like new ideas; the score does not know an idea repeats a held one until it is tested and compared.
  1n (a discovery ranks as a follow-up) and 1q (lines 7.e and 7.g see the profile map) fixed two causes by rule, on
  2026-11-25.
- **What the ideas say today:** an idea has its `Idea:` and `Consequence:` lines, a `profile:` line, and, from a step 7
  line, the findings it rests on (`rests on: F2, F5`); no line says why it is worth testing next.

## The idea (the operator's)
Each idea written by step 2 or a step 7 line carries new fields on why it exists, for example: what it would add to
the portfolio (a profile or a side the profile map lacks, an effect not held), what it answers (the brief's theme, or
a discovery), how sure its finding is. Decide-next becomes an agent step: it reads the candidates with those fields,
the profile map and the held books, and picks the next idea with a reason, written in `loop.jsonl`.

## Options (to weigh when it is opened)
| Option | Gain | Risk |
|---|---|---|
| A. An agent decides, reading the new fields | judges what the score cannot (a repeat of a held effect, a theme left unanswered, a profile not covered) | a model call per turn (cost); a choice that is not reproducible; the fields themselves written by models that favour their own ideas |
| B. The new fields, read by code (for example "adds a profile the map lacks" as a weight in the score) | reproducible, no cost per turn | the fields must be standard enough for code; less judgement |
| C. Today's rules (groups, score, P9, 1n) | no build | what night 7 showed may come back in other forms |

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-25 | Parked | the operator | an idea for later; 1n and 1q first | |

## Status and next
Parked. To open after a night run on 1n and 1q: if repeats of held effects or unanswered themes remain, they are the
evidence for it.

## Links
`orchestration/select_next/card.md`; topic 32 (how select_next weighs a line); topic 50 (1n, 1q); `common/market_profile.md`
(the profile map); `runs/NIGHT7_RUN.md`.
