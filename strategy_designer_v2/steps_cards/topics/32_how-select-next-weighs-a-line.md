# Topic 32: How select_next weighs a step 7 line

Status: open (parked)  
Where: research: select_next  
Opened: 2026-11-19 (operator: "not convinced about this way to decide")

## Question
Is a line's record (how often its past analyses led to a profitable book) a sound way to decide which idea is tested
next?

## Seen
- record = (analyses that paid + 1) / (analyses + 2), over every analysis of the line with a tested idea, in every run;
  score = record / (1 + the idea's generation) (`orchestration/select_next/card.md`; a success is a profitable book
  since 2026-11-19, topic 30).
- 2026-11-19: 7.b 4 of 12 (0.357), 7.d 3 of 10 (0.333): one success apart, a near tie that decides the order.
- **Inherited successes:** 3 of 7.b's 4 paying analyses re-tested, on more coins, an idea that already paid (golden
  cross, nearness to high): the record credits the parent more than the line's own judgement.
- **Untested analyses do not count:** 7.d's 39 hourly analyses have no tested idea, so its record rests on 10 daily
  analyses only.
- **The generation penalty** puts 7.d's hourly ideas that read 7.g's ideas (generation 2) at rank 36 and beyond.

## Why it matters
The order decides which ideas are ever tested; with near ties and inherited credit, it may follow noise.

## Options
To set when the topic is opened.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Parked; first check whether the analyst can find profitability (d_line_1h_run) | operator | the objective first | - |

## Status and next
Parked. Reopen after d_line_1h_run's reading.

## Links
Topic 30; `orchestration/select_next/card.md`; `runs/D_LINE_1H_RUN.md`.
