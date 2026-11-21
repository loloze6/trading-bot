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
- Today's way: a resumable queue; after a cut, the session asks the operator before relaunching it.

## Why it matters
A night of runs loses hours when nothing relaunches the queue, and the morning reading is incomplete.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. The cloud session as today: a resumable queue, check-ins that relaunch it after a cut | works now | a cut costs the cut backtest and the wait until the check-in |
| B. The CLI on the operator's machine: the operator starts the same queue script in a terminal (for example in tmux), no two-hour limit | no cut | the machine must stay on; the session reads the results afterwards |
| C. A standard runner for queues (a card of its own under `orchestration/`), used by both | one way for every long run | to design |
| D. Spread one queue across cloud sessions, each on its own machine (4 cores each), coordinated by one session | about N times the throughput for N sessions; no result changes; the 2 h limit then cuts less | each session builds its venv; results come back on separate branches and are merged (the INDEX files merged line by line); model use and cost add up per session |

Recommended: B for long runs from tomorrow, with the queue script made a standard runner (C) when a second run needs it.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-20 | (Corrected the same day) Relaunch after a cut: the operator asked for "an automatic way" but did not say yes to relaunching without asking; the session recorded it as an OK by mistake. A task stopped at its 2 h limit is relaunched only on the operator's go | the session's correction | the harness asks not to restart a task stopped at its longest timeout without the person's go | – |
| 2026-11-20 | Test D (parallel sessions) on the books left, coordinated by the designer session; part of this improvement, not a topic of its own | the operator | more throughput now, no result change | – |
| 2026-11-21 | A task stopped by the 2-hour limit (or a restart) in the middle of a run is relaunched by the session without asking; the run resumes where it stopped | the operator ("you do not need my go to relaunch a task killed mid run") | the run was already approved; relaunching continues it | asking each time (it stopped the paying books rerun for hours) |

**2026-11-20, option D tested** (`runs/HOLD2_AND_PILOT_RUN.md`): 9 books in 3 parts, 72 minutes side by side against about
149 one after another (about 2 times faster), no result changed; the INDEX files merged row by row, no conflict.

## Status and next
2026-11-20: D tested on the corrected-rule reruns' last 9 books, in 3 parts (`runs/hold2_parts/`): this session and 2
sessions of their own. B (the CLI) stays to try on the next long run.

## Links
`runs/HOLDING_NIGHT_RUN.md`, `topics/30_review/hold_rerun.py`.
