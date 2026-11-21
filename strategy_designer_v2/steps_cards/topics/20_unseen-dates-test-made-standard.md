# Topic 20: The unseen-dates test made standard

Status: closed (2026-11-18)  
Where: research: orchestration  
Opened: 2026-11-18 (operator)

## Question
Does an idea that is real and pays still hold on dates the research never used?

## Seen
- `runs/UNSEEN_RUN.md`: the 12 confirmed and profitable ideas run unchanged on 2026 and 2016-17: 10 of 12 hold on
  2026, 11 of 12 on 2016-17 (outcome 1, as pre-registered). 2026 discriminates (a falling year); 2016-17 does not (a
  bull market).
- Made standard: `orchestration/unseen_test/`, called by `run_idea` for every confirmed and profitable idea. A period
  with no data reads "no data", not "does not hold" (2026-11-19).

## Why it matters
No idea should reach live trading on the evidence of the dates it was found and judged on alone.

## Options
| Option | Gain | Risk |
|---|---|---|
| Every confirmed and profitable idea, automatically, recording only | the same test for all; no step reads it | a few minutes per idea |
| By hand, when the operator asks | no build | forgotten |

Recommended: automatic, recording only.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-18 | Standard, called by run_idea; it records and decides nothing | operator | 8 of the first 12 such ideas failed step 6 on at least one unseen period, 2 did not hold at all | by hand |
| 2026-11-19 | No data reads "no data" | design session (a defect fix) | the hourly bars of 2026 were not fetched: not judged is not failed | - |

## Status and next
Closed. Lives in `orchestration/unseen_test/`.

## Links
Commits 59c8ea2f, 16476c34, 49001747; `common/unseen_dates.md`.
