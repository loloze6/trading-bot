# Topic 01: Step 3: the noise from writing a test freely

Status: open  
Where: research: step 3  
Opened: 2026-11-17 and 18, from the night runs' readings

## Question
How much of an idea's verdict depends on how step 3 happened to write its test, rather than on the idea?

## Seen
- **One idea, different tests:** the same idea gets different verdicts from two plans written separately (second
  night: 013-04 t +1.99 in one run and +2.46 in another; 012-01 +2.11 and +3.26), and one judgement differs by bar size
  or between mirror ideas (a volume split "adapted" on daily bars, "replaced" on hourly ones; 003-05 against 003-06).
- **Details only a plan can settle:** how its non-overlapping samples are drawn, which test it uses, and what each case
  is ("sharp-move bars": up moves only, or every labelled bar?). Step 5's conventions cover the common cases.
- **True mismatches remain:** plans whose config does not trade the stated situation (night_013_run d2: averaging an
  always-negative and an always-positive block; second night: two more, one at 82 %).

## Why it matters
A verdict that moves with the wording of a test makes a confirmed idea less trustworthy, and a rejected one too.

## Options
| Option | Gain | Risk |
|---|---|---|
| Leave it: step 5's conventions cover the common cases | no work | the noise stays in the verdicts |
| More shared conventions for step 3 (`common/`), one at a time, each from a case a run showed | less freedom where it adds noise | each convention needs a validation of step 3 |
| Two plans per idea, compared | measures the noise directly | doubles the cost of step 3 and step 5 |

Recommended: none yet: first measure how often it changes a status (confirmed or not), not only the t.

## Decisions
None yet.

## Status and next
Opens when the operator says so.

## Links
`03_test_plan/card.md`, `05_verification/card.md`, `runs/SECOND_NIGHT_RUN.md`.
