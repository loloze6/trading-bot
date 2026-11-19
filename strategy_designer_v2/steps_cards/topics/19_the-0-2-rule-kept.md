# Topic 19: The 0.2 rule kept

Status: closed (2026-11-18)  
Where: engine and live  
Opened: 2026-11-18 (the live session: a position of 0.17 held 12 days)

## Question
Should the bot keep skipping allocation changes smaller than 0.2?

## Seen
- The bot skips any allocation change smaller than 0.2 (`risk_management.controls.min_allocation_change`, judged on
  forecast / 10 with a sizing block), in every backtest and live: a position below 0.2 cannot close while the forecast
  stays at 0 (live: 0.17 held 12 days).
- Measured on the 12 confirmed and profitable ideas: 9.5 % of bars hold such a position (up to 114 days in a row), of
  mean size 0.01 to 0.05, worth -1 % to +1 % of each book's gross return.

## Why it matters
Live and backtest must follow the same rule, and a rule with a side effect must be measured.

## Options
| Option | Gain | Risk |
|---|---|---|
| Keep it | backtests and live stay identical; impact minimal | small leftover positions |
| A move to flat always executes | no leftover positions | every backtest changes; shared code |

Recommended: keep it.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-18 | Kept as it is | operator | all backtests used the same rule, so the research matches live; the measured impact is minimal | a move to flat always executes |

## Status and next
Closed. If ever wanted: a move to flat always executes.

## Links
Commit 3ab7c452; topic 9.
