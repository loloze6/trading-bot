# Topic 37: long runs without the two-hour limit

Status: open (parked)  
Where: research: how runs are launched (the cloud session, the CLI)  
Opened: 2026-11-20, the operator: "can we increase the two-hour limit, or have an automatic way? You are here now, but
what about fully CLI tomorrow? To be parked."

## Question
How do runs that last several hours (hourly backtests, 15 to 45 minutes each) go on without someone relaunching them?

## Seen
- 2026-11-20: in this cloud session a background task is stopped after 2 hours, and a container restart stops it too.
  During the holding night, set 2 was cut at 06:42 (21 of 21 needed 4 more ideas the next morning) and once by a
  restart at 04:40.
- The rerun scripts resume: a finished step is skipped and a cut backtest is restarted (`topics/30_review/hold_rerun.py`).
  A queue script chains several lists the same way.
- Today's way: a scheduled check-in relaunches the queue after a cut (the operator's OK, 2026-11-20).

## Why it matters
A night of runs loses hours when nothing relaunches the queue, and the morning reading is incomplete.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. The cloud session as today: a resumable queue, check-ins that relaunch it after a cut | works now | a cut costs the cut backtest and the wait until the check-in |
| B. The CLI on the operator's machine: the operator starts the same queue script in a terminal (for example in tmux), no two-hour limit | no cut | the machine must stay on; the session reads the results afterwards |
| C. A standard runner for queues (a card of its own under `orchestration/`), used by both | one way for every long run | to design |

Recommended: B for long runs from tomorrow, with the queue script made a standard runner (C) when a second run needs it.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-20 | Relaunch after a cut is allowed without asking each time | the operator | runs resume; asking costs hours | – |

## Status and next
Parked by the operator. Next: try B on the next long run.

## Links
`runs/HOLDING_NIGHT_RUN.md`, `topics/30_review/hold_rerun.py`.
