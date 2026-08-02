# Engineering roadmap

One line per epic. **This is the only mandatory read for an agent starting cold.**
Rules are in `PROCESS.md`; detail is in each `E-0XX/EPIC.md`.

Research hypotheses do not appear here — they go through the campaign's
preregistration and verdict machinery. See `PROCESS.md` § "What is and is not an
epic".

| Ref | Title | State | Next step |
|---|---|---|---|
| [E-001](E-001/EPIC.md) | Establish the engineering operational process | in-progress | S2 — audit the five overlapping trackers (664 lines) |
| [E-002](E-002/EPIC.md) | Land the parked `strategy-research/` restructure | planned | S1 — replay the mapping onto master |
| [E-003](E-003/EPIC.md) | Make the holdout seal gate enforceable in every clone | new | Investigate `tools/hooks/` and `core.hooksPath` |
| [E-004](E-004/EPIC.md) | Settle the shared record taxonomy with the fork | new | Needs a joint decision, not a dispatch |
| [E-005](E-005/EPIC.md) | Verify master on macOS and Linux | new | Dorian to run both suites on `c4feaf56` |
| [E-006](E-006/EPIC.md) | Stop shipping a committed Windows venv | new | Agree with Dorian before `git rm -r --cached venv/` |

## State legend

`new` → identified · `planned` → stories written · `in-progress` → dispatched ·
`parked` → blocked, unblock condition recorded · `done` → SHA + verification ·
`killed` → abandoned with evidence

`parked` is never a synonym for `done`. See `PROCESS.md`.
