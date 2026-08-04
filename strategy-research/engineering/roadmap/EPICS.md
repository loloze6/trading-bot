# Engineering roadmap

One line per epic. **This is the only mandatory read for an agent starting cold.**
Rules are in `PROCESS.md`; detail is in each `E-0XX/EPIC.md`.

Research hypotheses do not appear here — they go through the campaign's
preregistration and verdict machinery. See `PROCESS.md` § "What is and is not an
epic".

## Active

| Ref | Title | State | Next step |
|---|---|---|---|
| [E-002](E-002/EPIC.md) | Land the parked `strategy-research/` restructure | planned | S2a — coordination gate with Dorian (in-flight Mac-fork test fixes) before S3's replay |
| [E-003](E-003/EPIC.md) | Make the holdout seal gate enforceable in every clone | new | Investigate `tools/hooks/` and `core.hooksPath` |
| [E-004](E-004/EPIC.md) | Settle the shared record taxonomy with the fork | new | Needs a joint decision, not a dispatch |
| [E-005](E-005/EPIC.md) | Verify master on macOS and Linux | new | Dorian to run both suites on `c4feaf56` |
| [E-006](E-006/EPIC.md) | Stop shipping a committed Windows venv | new | Agree with Dorian before `git rm -r --cached venv/` |
| [E-007](E-007/EPIC.md) | Recorder storage and host migration | parked | Operator decision on the R3 storage budget |
| [E-008](E-008/EPIC.md) | q1_26 tick archive aggregation | new | Evaluate extending `data_manager.py:637`'s `.resample()` seam |
| [E-009](E-009/EPIC.md) | Pipeline harmonization (STAGE_CONFIGS/skill_map, sample_split, protocol auto-run, auto-repair) | new | S1 — merge STAGE_CONFIGS/skill_map |
| [E-010](E-010/EPIC.md) | Slippage and lot-size/min-notional model | new | S1 — implement, with the non-BTCUSDT hard-fail |
| [E-011](E-011/EPIC.md) | Shared campaign execution location | new | blocked behind E-003 — do not start before it |
| [E-012](E-012/EPIC.md) | Two-bars manifest/loop defect | new | S1 — measure the delta before designing any fix |

## Done

Per amendment 2 (`PROCESS.md`): done epics never move; they stay listed here,
not archived elsewhere.

| Ref | Title | State | Closing SHA |
|---|---|---|---|
| [E-001](E-001/EPIC.md) | Establish the engineering operational process | done | `25960cac` corrected the Done-when; this file's own dispatch (W26) closes it — see `E-001/EPIC.md` Log for the verification output |

## State legend

`new` → identified · `planned` → stories written · `in-progress` → dispatched ·
`parked` → blocked, unblock condition recorded · `done` → SHA + verification ·
`killed` → abandoned with evidence · `withdrawn` → not an epic after all,
continues as a card reference

`parked` is never a synonym for `done`. `withdrawn` is never a synonym for
`killed` — the work continues, just not here. See `PROCESS.md`.
