# Topic 17: The data's bar deduced from the trading bar

Status: closed (2026-11-18)  
Where: research: step 4  
Opened: 2026-11-18 (finer bars)

## Question
Which bar size of data does a backtest read for a strategy that decides on a given bar size?

## Seen
- The strategy decides on its bar (1d, 4h, 1h). The data files exist at several bar sizes.
- Built: `data_bar()` takes the largest file bar that divides the trading bar (step 4); step 3's bar arithmetic reads
  the bar's length.

## Why it matters
A strategy's data bar must not be a per-strategy choice.

## Options
| Option | Gain | Risk |
|---|---|---|
| Deduced: the closest finer bar the files hold | one rule for every strategy | - |
| Set in each plan | flexible | a choice with no relation to the strategy |

Recommended: deduced.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-18 | The data's bar is deduced, the largest file bar dividing the trading bar | operator | the data timeframe has no relation with a strategy; only the strategy's decision timeframe has | a setting per plan |

## Status and next
Closed. Lives in step 4's helper and the launcher.

## Links
Commit 5a453bc1; `orchestration/duration/8_finer_bars_measure.md`.
