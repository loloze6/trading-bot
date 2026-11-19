# Topic 18: Holes of up to one day ignored

Status: closed (2026-11-19)  
Where: research: engine  
Opened: 2026-11-18 (finer bars: the gap rule blocked hourly windows)

## Question
How long a hole in the data may a backtest window carry before the window is not run?

## Seen
- Before: a window with a hole of more than 3 bars was not run: 3 days on daily bars, but 3 hours on hourly bars,
  which blocked many hourly windows (`orchestration/duration/8_finer_bars_measure.md`).
- Built: `default_gap_policy(interval)` ignores holes of up to one day, whatever the bar: 1 bar on daily bars, 6 on 4h,
  24 on 1h.

## Why it matters
A rule in bars means a different tolerance on each bar size.

## Options
| Option | Gain | Risk |
|---|---|---|
| A time-based rule: one day | the same tolerance on every bar size | an hourly window may carry a day without bars |
| Three days | fewer windows blocked | too much missing data on daily bars |
| Three bars (before) | - | blocks hourly windows for 3-hour holes |

Recommended: one day.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-18 | The rule is in time, not in bars | operator | the same tolerance whatever the bar | a number of bars |
| 2026-11-19 | One day, on every bar size | operator | three days sounded a lot, even on daily data; not only an effect within the day | three days |

## Status and next
Closed. Lives in `trading-bot/core/launcher.py`.

## Links
Commit 0821b921.
