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
| [E-014](E-014/EPIC.md) | Venue-parameterized cost model + calibration re-runs | planned | S1 — turn the venue fee schedule into a real parameter (today: one hardcoded `{spot,perp}` flag) and wire the unread `execution_style` block in; S3 (funding retest) now has a real data source — Dorian's PR #24 |
| [E-015](E-015/EPIC.md) | Venue/product declared at brief registration | planned | S1b — make missing venue/product a hard registration failure; S3 — enforce `research_only` at a real downstream gate (currently written, never read) |
| [E-016](E-016/EPIC.md) | Fee-reduction autopsy field | planned | S2 — wire the "yes" branch to brief registration end-to-end; S3 — resolve whether the non-blocking check should become blocking or the "MUST" should be softened |
| [E-017](E-017/EPIC.md) | Autopsy standard v1 | parked | Blocked on Phase 2's gate (`docs/CAMPAIGN_PROGRAM.md` §Phase 2) — S1 implements the 2 missing palette metrics (profit-per-forecast-bin, regime-ID correctness), S2 builds the sibling-registration hard gate from scratch |
| [E-018](E-018/EPIC.md) | Near-miss scoreboard | parked | Blocked on Phase 2's gate (`docs/CAMPAIGN_PROGRAM.md` §Phase 2) |
| [E-019](E-019/EPIC.md) | Feature matrix + leakage checks | parked | Blocked on Phase 3 complete |
| [E-020](E-020/EPIC.md) | Cut per-dispatch codebase context cost (scoped CLAUDE.md, then re-evaluate tree-sitter) | new | S1 — inventory known landmines with file:line refs across both trees |
| [E-021](E-021/EPIC.md) | Consolidate bug/ticket tracking onto GitHub; narrow Notion's role | new | S1 — joint conversation with Dorian before touching anything he relies on |
| [E-023](E-023/EPIC.md) | Enable live trading, targeting Kraken (P3/P4/P5 migrated in) | parked | Deliberately unscoped — priority is the research workflow; unpark only alongside a real live-deployment decision |
| [E-024](E-024/EPIC.md) | Mandatory live-trading safety backstop (kill switch, daily loss limit, flatten-all) | parked | Deliberately unscoped — same reasoning as E-023; per-trade sizing/stops stay in the normal strategy-validation workflow, not this epic |
| [E-025](E-025/EPIC.md) | Trial-ledger dual-writer merge protocol (mechanics) | planned | S1 (Jeremy) — `forecast_hash` mandatory emission + idempotency guard on backtest re-entry (issue #28 H3); S2 (Jeremy) — mechanical duplicate-`trial_id` refusal in `deflate_sharpe.py` |

## Done

Per amendment 2 (`PROCESS.md`): done epics never move; they stay listed here,
not archived elsewhere.

| Ref | Title | State | Closing SHA |
|---|---|---|---|
| [E-002](E-002/EPIC.md) | Land the parked `strategy-research/` restructure | done | `1787258b` amended the mapping (dropped `protocols/` and `briefs/` as contract migrations); `8f162fa6` (S3-S5, dispatch W44) landed 169 renames plus 94 repointed files — see `E-002/EPIC.md` Log. S6's independent audit was not run |
| [E-001](E-001/EPIC.md) | Establish the engineering operational process | done | `25960cac` corrected the Done-when; this file's own dispatch (W26) closes it — see `E-001/EPIC.md` Log for the verification output |
| [E-013](E-013/EPIC.md) | Split docs/ROADMAP.md — retire the name, graduate the engineering items | done | `cd20e6ec` created the six epics (S2); `cc69410f` (S3, W36) closed it but left six live citations unrepointed; this commit (S4, dispatch W37) reopened and re-closed it — see `E-013/EPIC.md` Log for the repoint and re-verification |
| [E-022](E-022/EPIC.md) | Automated "what's happening" digest, every 2 days | done | Two real firings verified (2026-08-13 p1786650635663579, 2026-08-14 p1786696390584949); moved off the session-bound workaround onto a proper fresh-session claude.ai routine (`trig_01XUckqVaSTdJ4rjPABhKZWv`) — see `E-022/EPIC.md` Log for the 3 sourcing gaps it self-flagged and what's deferred to a later pass |

## State legend

`new` → identified · `planned` → stories written · `in-progress` → dispatched ·
`parked` → blocked, unblock condition recorded · `done` → SHA + verification ·
`killed` → abandoned with evidence · `withdrawn` → not an epic after all,
continues as a card reference

`parked` is never a synonym for `done`. `withdrawn` is never a synonym for
`killed` — the work continues, just not here. See `PROCESS.md`.

**WIP limit (amendment 11): at most 2 epics may be `in-progress` at once**,
and only via an actual dispatch under the epic — a tree audit crediting
pre-existing code does not itself count. Currently 0 of 2 slots used.
