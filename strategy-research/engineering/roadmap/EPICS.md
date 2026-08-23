# Engineering roadmap

One line per epic. **This is the only mandatory read for an agent starting cold.**
Rules are in `PROCESS.md`; detail is in each `E-0XX/EPIC.md`.

Research hypotheses do not appear here — they go through the campaign's
preregistration and verdict machinery. See `PROCESS.md` § "What is and is not an
epic".

## Active

| Ref | Title | State | Next step |
|---|---|---|---|
| [E-004](E-004/EPIC.md) | Settle the shared record taxonomy with the fork | new | Needs a joint decision, not a dispatch |
| [E-005](E-005/EPIC.md) | Verify master on macOS and Linux | new | Dorian to run both suites on `c4feaf56` |
| [E-006](E-006/EPIC.md) | Stop shipping a committed Windows venv | new | Agree with Dorian before `git rm -r --cached venv/` |
| [E-007](E-007/EPIC.md) | Recorder storage and host migration: deploy the daemon to culi.to | planned | **Re-scoped 2026-08-23** from a decision epic to a deployment epic — the operator made the call: deploy to `culi.to` under a real budget. S1 — characterize what a real budget covers vs the measured 360GB/yr, and confirm `culi.to`'s actual capacity (do NOT inherit the 100GB figure, pre-registered before anything was measured). Order-book depth cannot be backfilled — every day off is permanently lost sample |
| [E-008](E-008/EPIC.md) | q1_26 tick archive aggregation | new | Evaluate extending `data_manager.py:637`'s `.resample()` seam |
| [E-009](E-009/EPIC.md) | Pipeline harmonization (STAGE_CONFIGS/skill_map, sample_split) | new | S1 — merge STAGE_CONFIGS/skill_map; S3/S4 split to E-030 2026-08-21 |
| [E-010](E-010/EPIC.md) | Slippage and lot-size/min-notional model | new | S1 — implement, with the non-BTCUSDT hard-fail |
| [E-011](E-011/EPIC.md) | Shared campaign execution location (S1a: host provisioning, folded in from the Ubuntu-deployment bug card) | new | **E-003 blocker cleared 2026-08-18** — S1a done (`culi.to` live, baseline byte-identical); S1b (write-serialize `campaign_state`, retire single-writer Option A) is now the next real step, jointly with Dorian |
| [E-012](E-012/EPIC.md) | Two-bars manifest/loop defect | new | S1 — measure the delta before designing any fix |
| [E-014](E-014/EPIC.md) | Venue-parameterized cost model + calibration re-runs | planned | S1 — turn the venue fee schedule into a real parameter (today: one hardcoded `{spot,perp}` flag) and wire the unread `execution_style` block in; S3 (funding retest) now has a real data source — Dorian's PR #24 |
| [E-016](E-016/EPIC.md) | Fee-reduction autopsy field | planned | S2 — wire the "yes" branch to brief registration end-to-end; S3 — resolve whether the non-blocking check should become blocking or the "MUST" should be softened |
| [E-017](E-017/EPIC.md) | Autopsy standard v1 | parked | Blocked on Phase 2's gate (`docs/CAMPAIGN_PROGRAM.md` §Phase 2) — S1 implements the 2 missing palette metrics (profit-per-forecast-bin, regime-ID correctness), S2 builds the sibling-registration hard gate from scratch; **park reviewed 2026-08-23 and KEPT for S1** — Part 4's standing guarantee 3.4 says palette metrics are added when an autopsy needs them, never speculatively. **S2 (sibling-registration hard gate) is not a metric and inherited its park by adjacency — split it out and judge it on its own** |
| [E-018](E-018/EPIC.md) | Near-miss scoreboard | in-progress | **Unparked 2026-08-23** (park was inherited from Phase 3's position, not from this epic's inputs — it ranks 38 verdicts already on disk and needs nothing from Phase 2). **S1 dispatched 2026-08-23** — ranked table + the promotion-read firewall, built in the same story. Feedstock for E-032 |
| [E-019](E-019/EPIC.md) | Feature matrix + leakage checks | parked | Blocked on Phase 3 complete |
| [E-020](E-020/EPIC.md) | Cut per-dispatch codebase context cost (scoped CLAUDE.md, then re-evaluate tree-sitter) | new | S1 — inventory known landmines with file:line refs across both trees |
| [E-021](E-021/EPIC.md) | Consolidate bug/ticket tracking onto GitHub; narrow Notion's role | new | S1 — joint conversation with Dorian before touching anything he relies on |
| [E-023](E-023/EPIC.md) | Enable live trading, targeting Kraken (P3/P4/P5 migrated in) | parked | Deliberately unscoped — priority is the research workflow; unpark only alongside a real live-deployment decision |
| [E-024](E-024/EPIC.md) | Mandatory live-trading safety backstop (kill switch, daily loss limit, flatten-all) | parked | Deliberately unscoped — same reasoning as E-023; per-trade sizing/stops stay in the normal strategy-validation workflow, not this epic |
| [E-025](E-025/EPIC.md) | Trial-ledger dual-writer merge protocol (mechanics) | planned | S1/S2/S3 done; issue #28's H1-H4 all code-complete as of 2026-08-16 (Jeremy: H1/H3, Dorian: H2/H4); S4 mechanics verified (plain merge conflicts, keep-both is correct; merge=union not adopted — layout-contingent safety + one demonstrated silent scalar-loss mode, does NOT corrupt the file, see EPIC.md log for the correction) — only a real two-sided PR proving it end to end remains before campaigns |
| [E-026](E-026/EPIC.md) | Cross-sectional strategies: two engines, one decision | new | S1 — characterize `panel_backtester.py` (it already runs the 19-pair universe with an engine-equivalence gate, so this is a consolidation decision, not a build) |
| [E-027](E-027/EPIC.md) | Exit-cause attribution: stop labelling a switched-off strategy as a signal flip | new | S1 — characterize which of the three zero-forecast paths fired for the 5,094 recorded closes (measured: 0 of them happened with a nonzero forecast; `_infer_exit_reason` calls them all `signal_flip`) |
| [E-028](E-028/EPIC.md) | Realized allocation must reflect strategy intent, not gate state | new | Needs an operator decision, not a dispatch — S1 characterizes the three policies for "regime has no strategy"; hysteresis/dwell is already closed as `unusable_for_this_symbol_timeframe` |
| [E-029](E-029/EPIC.md) | The trade record must carry the decision, not just the outcome | new | S1 — characterize where `regime_at_exit` / forecast / allocation-pair can be sourced without changing behaviour, and resolve the 20% of trades recording `regime_at_entry: unknown`. Sequenced BEFORE E-027, and both sequenced BEHIND E-030 (2026-08-21) |
| [E-031](E-031/EPIC.md) | Queue return edge: the loop must be able to start a new line of inquiry | in-progress | **S1 dispatched 2026-08-23** — characterize-and-STOP: which seed sources can legitimately refill the queue, what each holds today, and the routing policy. S2 (schedulability block) and S3 (return edge + trial accounting) follow |
| [E-032](E-032/EPIC.md) | Proactive idea generation: propose something not already tried | new | S1 — characterize what the generating stages can see vs. what they need. **Depends on an open operator decision: unpark E-018** (near-miss scoreboard), which the campaign program names as the idea-generation stage's raw material |

## Done

Per amendment 2 (`PROCESS.md`): done epics never move; they stay listed here,
not archived elsewhere.

| Ref | Title | State | Closing SHA |
|---|---|---|---|
| [E-015](E-015/EPIC.md) | Venue/product declared at brief registration | done | S1b (`_parse_brief_frontmatter` requires venue+product, raises on either missing) closes the last open Done-when; S3's affirmative `research_only is False` holdout check (2026-08-18) already closed the real safety gap, S1b was belt-and-braces at registration time. 4 new tests, both suites green, holdout gate PASS |
| [E-030](E-030/EPIC.md) | Halt recovery + a loop-health instrument | done | S1 `3073ca7e` (taxonomy), S1.5 `994157ec`/`842a2788`, S2a `83f8f1b0` (quarantine, off by default), S3 `5053148e` (loop_health.yaml wired into quarantine-vs-escalate), S4 `3eba6ba0` (epic-level bit-identity); closed `057d301c`. S2b (retry) explicitly parked on missing evidence, not effort. Slow suite verified: trading-bot 409 passed / 2 skipped, strategy-research 884 passed |
| [E-003](E-003/EPIC.md) | Make the holdout seal gate enforceable in every clone | done | S2a `74c7397` (gate green + CI enforcement), S2b `2ea51a3` (hook made real: exec bit, lying test gate removed, `setup_hooks.sh`). Verify: `sh strategy-research/tools/holdout_date_gate.sh` → PASS, 7942 files examined; fresh-clone probes block a credential / a `.env` / a `2026-03-15` CSV and allow an ordinary commit in 1.85s |
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
pre-existing code does not itself count. Currently **2 of 2** slots used — E-031 and E-018 (both S1 dispatched 2026-08-23). At the limit: no third epic may go `in-progress` until one closes.
(E-003 closed `done` 2026-08-18; E-030 closed `done` 2026-08-23.)
