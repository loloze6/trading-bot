# Topic 41: does a paying idea add anything beyond the filter it trades under?

Status: open (proposed by night 3's checks)  
Where: research: step 6 or the unseen test (`orchestration/unseen_test`), steps 3 and 7  
Opened: 2026-11-21, the designer session, from night 3 (`runs/NIGHT3_RUN.md`, the two "Check" sections).

## Question
When an idea is confirmed and its book pays, is it the idea that pays, or the filter it trades under (most often a
positive past return: momentum, known to pay on these coins)?

## Seen
- Night 3, four paying ideas checked against the same config without the idea's own component (the filter alone, same
  coins, folds, horizon, sizing; steps 4 and 6, no model call): the idea adds 0.0 to 0.15 of Sharpe; every control pays
  on all six checks by itself. Levels run: 1.26 vs 1.18, 1.13 vs 1.13; 4h run: 1.53 vs 1.38, 1.11 vs 1.05.
- The other paying ideas of the night are momentum outright (a 5-day rise, a weekly rise, a monthly rise: step 7 A/B
  set B, the learned run), and earlier paying books are the same family (golden cross, nearness to highs, dual
  momentum; `common/findings.md`, F3, F9).
- Step 6 compares a book with holding the coin; nothing compares it with the simplest book its own filter makes.

## Why it matters
Without it, every brief can "find" momentum again under a new name, and the research counts it as a new paying family.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. A standard control for an idea confirmed and profitable whose config has a gate (a regime rule): rerun its config with the forecast from the gate's own components, report both books side by side (visibility, no gate) | says, for every paying idea, what the idea adds; code only, about 2 backtests per paying idea | a definition of "the filter alone" for every config shape (one rule: the gate's components become the forecast) |
| B. Step 7 is told the known families (findings register) and asked to say whether a paying idea is one | no backtest | a model's reading, not a measure |
| C. Nothing | - | momentum found again and again |

Recommended: A, as a function next to the unseen test (same trigger: confirmed and profitable), its card designed by
`HOW_WE_DESIGN_A_CARD.md`; then a finding for the register if the pattern holds.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|

## Status and next
Waiting for the operator's go.

## Links
`runs/NIGHT3_RUN.md`, `runs/STEP7_SIZE_AB_RUN.md`, `common/findings.md`, `orchestration/unseen_test/card.md`.
