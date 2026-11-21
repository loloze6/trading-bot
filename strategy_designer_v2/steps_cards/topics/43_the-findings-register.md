# Topic 43: the findings register (common/findings.md)

Status: closed (2026-11-21: switched off and deleted)  
Where: research: shared definitions, step 7  
Opened: 2026-11-21, the operator: "its design was underthought and might be worth a look on several points".

## Question
Should the steps read a register of what earlier runs measured, and if so, how is it written and kept true?

## Seen (2026-11-21)
- 11 entries (F1 to F11), written by hand by the designer session from run readings on 2026-11-20; no rule or step
  wrote them, and the operator approved step 7 reading the register, not each entry.
- No entry stated its setup systematically (bar size, coins, period, engine and costs): F2 was about hourly ideas
  only; F1 (a buy plus a sell costs 0.21 to 0.23 %) was outdated by the measured costs (topic 38). Read by step 7 on
  any idea, an entry could steer it outside its setup.
- No business definition of an entry: what qualifies as a finding, which setup it covers, when it expires.
- The step 7 A/B test (`runs/STEP7_SIZE_AB_RUN.md`): versions B and B′ both read it, so the tested result (B pays more)
  does not rest on it.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-21 | Switched off (step 7 no longer reads it) and the file deleted (git keeps it) | the operator ("switch it off and delete finding list") | who writes it, how it separates run setups, what an entry is: not designed | keeping it read by step 7 until a review |

## Status and next
Closed. If a register of what runs measured is wanted again, it starts from these questions: who writes an entry, the
setup each entry covers (bar, coins, period, engine), the business definition of an entry, and when it expires.
Proposed F12 (under a day an idea's move is below its cost) is dropped with it; its evidence stays in the run readings.

## Links
`runs/STEP7_SIZE_AB_RUN.md`, `runs/RETRO_DIAGNOSIS_RUN.md`, `30_review/WORKFLOW_REVIEW.md` (I2), `07_common/card.md`.
