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
| [E-014](E-014/EPIC.md) | Venue-parameterized cost model + calibration re-runs | new | Blocked behind E-010 — parameterize the cost model by venue fee schedule, then run the 3 calibration re-runs |
| [E-015](E-015/EPIC.md) | Venue/product declared at brief registration | new | S1 — add venue + product as required fields to brief registration; auto-flag non-tradable products research-only |
| [E-016](E-016/EPIC.md) | Fee-reduction autopsy field | parked | Blocked on E-010 (fee/slippage attribution) and E-017 (autopsy standard/cost decomposition) |
| [E-017](E-017/EPIC.md) | Autopsy standard v1 | parked | Blocked on Phase 2's gate (`docs/CAMPAIGN_PROGRAM.md` §Phase 2) |
| [E-018](E-018/EPIC.md) | Near-miss scoreboard | parked | Blocked on Phase 2's gate (`docs/CAMPAIGN_PROGRAM.md` §Phase 2) |
| [E-019](E-019/EPIC.md) | Feature matrix + leakage checks | parked | Blocked on Phase 3 complete |

## Done

Per amendment 2 (`PROCESS.md`): done epics never move; they stay listed here,
not archived elsewhere.

| Ref | Title | State | Closing SHA |
|---|---|---|---|
| [E-001](E-001/EPIC.md) | Establish the engineering operational process | done | `25960cac` corrected the Done-when; this file's own dispatch (W26) closes it — see `E-001/EPIC.md` Log for the verification output |
| [E-013](E-013/EPIC.md) | Split docs/ROADMAP.md — retire the name, graduate the engineering items | done | `cd20e6ec` created the six epics (S2); `cc69410f` (S3, W36) closed it but left six live citations unrepointed; this commit (S4, dispatch W37) reopened and re-closed it — see `E-013/EPIC.md` Log for the repoint and re-verification |

## State legend

`new` → identified · `planned` → stories written · `in-progress` → dispatched ·
`parked` → blocked, unblock condition recorded · `done` → SHA + verification ·
`killed` → abandoned with evidence · `withdrawn` → not an epic after all,
continues as a card reference

`parked` is never a synonym for `done`. `withdrawn` is never a synonym for
`killed` — the work continues, just not here. See `PROCESS.md`.
