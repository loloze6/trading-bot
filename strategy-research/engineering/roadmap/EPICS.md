# Engineering roadmap

One line per epic. **This is the only mandatory read for an agent starting cold.**
Rules are in `PROCESS.md`; detail is in each `E-0XX/EPIC.md`.

Research hypotheses do not appear here — they go through the campaign's
preregistration and verdict machinery. See `PROCESS.md` § "What is and is not an
epic".

## Active

| Ref | Title | State | Next step |
|---|---|---|---|
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
| [E-014](E-014/EPIC.md) | Venue-parameterized cost model + calibration re-runs | in-progress | S1 — turn the venue fee schedule into a real parameter (today: one hardcoded `{spot,perp}` flag) and wire the unread `execution_style` block in; S2/S3 redo the near-miss re-runs and build the funding retest |
| [E-015](E-015/EPIC.md) | Venue/product declared at brief registration | in-progress | S1b — make missing venue/product a hard registration failure; S3 — enforce `research_only` at a real downstream gate (currently written, never read) |
| [E-016](E-016/EPIC.md) | Fee-reduction autopsy field | in-progress | S2 — wire the "yes" branch to brief registration end-to-end; S3 — resolve whether the non-blocking check should become blocking or the "MUST" should be softened |
| [E-017](E-017/EPIC.md) | Autopsy standard v1 | parked | Blocked on Phase 2's gate (`docs/CAMPAIGN_PROGRAM.md` §Phase 2) — S1 implements the 2 missing palette metrics (profit-per-forecast-bin, regime-ID correctness), S2 builds the sibling-registration hard gate from scratch |
| [E-018](E-018/EPIC.md) | Near-miss scoreboard | parked | Blocked on Phase 2's gate (`docs/CAMPAIGN_PROGRAM.md` §Phase 2) |
| [E-019](E-019/EPIC.md) | Feature matrix + leakage checks | parked | Blocked on Phase 3 complete |
| [E-020](E-020/EPIC.md) | Cut per-dispatch codebase context cost (scoped CLAUDE.md, then re-evaluate tree-sitter) | new | S1 — inventory known landmines with file:line refs across both trees |
| [E-021](E-021/EPIC.md) | Consolidate bug/ticket tracking onto GitHub; narrow Notion's role | new | S1 — joint conversation with Dorian before touching anything he relies on |
| [E-022](E-022/EPIC.md) | Automated "what's happening" digest, every 2 days | new | S1 — write the digest logic (6 sections, simple v1) |

## Done

Per amendment 2 (`PROCESS.md`): done epics never move; they stay listed here,
not archived elsewhere.

| Ref | Title | State | Closing SHA |
|---|---|---|---|
| [E-002](E-002/EPIC.md) | Land the parked `strategy-research/` restructure | done | `1787258b` amended the mapping (dropped `protocols/` and `briefs/` as contract migrations); `8f162fa6` (S3-S5, dispatch W44) landed 169 renames plus 94 repointed files — see `E-002/EPIC.md` Log. S6's independent audit was not run |
| [E-001](E-001/EPIC.md) | Establish the engineering operational process | done | `25960cac` corrected the Done-when; this file's own dispatch (W26) closes it — see `E-001/EPIC.md` Log for the verification output |
| [E-013](E-013/EPIC.md) | Split docs/ROADMAP.md — retire the name, graduate the engineering items | done | `cd20e6ec` created the six epics (S2); `cc69410f` (S3, W36) closed it but left six live citations unrepointed; this commit (S4, dispatch W37) reopened and re-closed it — see `E-013/EPIC.md` Log for the repoint and re-verification |

## State legend

`new` → identified · `planned` → stories written · `in-progress` → dispatched ·
`parked` → blocked, unblock condition recorded · `done` → SHA + verification ·
`killed` → abandoned with evidence · `withdrawn` → not an epic after all,
continues as a card reference

`parked` is never a synonym for `done`. `withdrawn` is never a synonym for
`killed` — the work continues, just not here. See `PROCESS.md`.
