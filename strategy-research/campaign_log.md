# Campaign log

Append-only. One line per stage transition (launch / stage / continue / done / halt / resume),
written by `workflow/run_campaign.py`. Do not hand-edit — see `campaign_summary.md` for the
regenerated scoreboard and `RUNBOOK.md` for how to read/act on this file.

- 2026-07-06T13:55:25Z [DRY RUN] === DRY RUN: verifying queue -> launch -> pause wiring (no LLM spend) ===
- 2026-07-06T13:55:25Z [DRY RUN] queue: selected entry 'P4_ts_trend' (status=ready, brief=briefs/research_brief_P4_ts_trend.md)
- 2026-07-06T13:55:25Z [DRY RUN] brief frontmatter parsed OK: strategy_domain=trend_following, market_universe=['BTCUSDT', 'ETHUSDT']
- 2026-07-06T13:55:56Z [DRY RUN] === DRY RUN: verifying queue -> launch -> pause wiring (no LLM spend) ===
- 2026-07-06T13:55:56Z [DRY RUN] queue: selected entry 'P4_ts_trend' (status=ready, brief=briefs/research_brief_P4_ts_trend.md)
- 2026-07-06T13:55:56Z [DRY RUN] brief frontmatter parsed OK: strategy_domain=trend_following, market_universe=['BTCUSDT', 'ETHUSDT']
- 2026-07-06T13:55:56Z [DRY RUN] setup_run + brief materialization OK: runs\run_dryrun_verify\artifacts\research_brief.yaml written, pre_registration.yaml written
- 2026-07-06T13:55:56Z [DRY RUN] terminal-state classification OK: pending_stage=completed_rejected -> no pause, queue would advance
- 2026-07-06T13:55:56Z [DRY RUN] hard-pause classification OK: detected reason='no_signal_artifact'
- 2026-07-06T13:55:56Z [DRY RUN] wishlist-trigger classification OK: detected family='daily_timeframe_er_overlay'
- 2026-07-06T13:55:56Z [DRY RUN] cleanup complete — no real run_ids, campaign_state.yaml, or campaign_queue.yaml were touched.
- 2026-07-06T13:55:56Z [DRY RUN] === DRY RUN PASSED ===
- 2026-07-06T13:58:56Z === REAL CAMPAIGN LAUNCH (P4_ts_trend) ===
- 2026-07-06T13:59:13Z LAUNCH P4_ts_trend -> run_053 (brief=briefs/research_brief_P4_ts_trend.md)
- 2026-07-06T14:06:14Z STAGE  P4_ts_trend / run_053: pending_stage=validation status=failed (no scored artifacts yet)
- 2026-07-06T14:06:15Z HALT — unhandled_exception: 'NoneType' object has no attribute 'strip'. Campaign stopped on P4_ts_trend / run_053. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-06T14:17:02Z RESUME P4_ts_trend / run_053: resolution confirmed for 'unhandled_exception', resuming queue processing.
- 2026-07-06T14:18:14Z STAGE  P4_ts_trend / run_053: pending_stage=backtest_specification status=paused_for_human (no scored artifacts yet)
- 2026-07-06T14:18:15Z HALT — component_gap. Campaign stopped on P4_ts_trend / run_053. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-06T16:06:42Z === RESUME after component_gap fix (MacdHistogramCrossoverComponent) ===
- 2026-07-06T16:06:57Z RESUME P4_ts_trend / run_053: resolution confirmed for 'component_gap', resuming queue processing.
- 2026-07-06T16:20:31Z STAGE  P4_ts_trend / run_053: pending_stage=completed_reframed status=active (ic=-0.050271, cost_ratio=0.2452, prescreen_route=kill_no_ic, backtest_verdict=kill, verdict_status=escalate)
- 2026-07-06T16:20:31Z CONTINUE P4_ts_trend lineage run_053 -> run_054 (completed_reframed)
- 2026-07-06T16:24:45Z STAGE  P4_ts_trend / run_054: pending_stage=hypothesis_generation status=failed (no scored artifacts yet)
- 2026-07-06T16:24:46Z HALT — unhandled_exception: Missing files: ['runs\\run_054\\artifacts\\hypothesis_card.yaml']. Campaign stopped on P4_ts_trend / run_054. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-06T18:23:26Z === RESUME after discarding invalid run_054 (KB-reactivation gate re-derivation) ===
- 2026-07-06T18:23:41Z STAGE  P4_ts_trend / run_053: pending_stage=human_pause status=active (ic=-0.050271, cost_ratio=0.2452, prescreen_route=kill_no_ic, backtest_verdict=kill, verdict_status=escalate)
- 2026-07-06T18:23:42Z HALT — kb_reactivation_violation. Campaign stopped on P4_ts_trend / run_053. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-06T18:34:57Z [DRY RUN] === DRY RUN: verifying queue -> launch -> pause wiring (no LLM spend) ===
- 2026-07-07T13:26:00Z RESUME P4_ts_trend / run_053: resolution confirmed for 'kb_reactivation_violation', resuming queue processing.
- 2026-07-07T13:26:01Z STAGE  P4_ts_trend / run_053: pending_stage=human_pause status=active (ic=-0.050271, cost_ratio=0.2452, prescreen_route=kill_no_ic, backtest_verdict=kill, verdict_status=escalate)
- 2026-07-07T13:26:01Z HALT — kb_reactivation_violation. Campaign stopped on P4_ts_trend / run_053. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-07T13:27:30Z RESUME P4_ts_trend / run_053: resolution confirmed for 'kb_reactivation_violation', resuming queue processing.
- 2026-07-07T13:27:31Z STAGE  P4_ts_trend / run_053: pending_stage=completed_reframed status=active (ic=-0.050271, cost_ratio=0.2452, prescreen_route=kill_no_ic, backtest_verdict=kill, verdict_status=escalate)
- 2026-07-07T13:27:31Z CONTINUE P4_ts_trend lineage run_053 -> run_054 (completed_reframed)
- 2026-07-07T13:35:51Z STAGE  P4_ts_trend / run_054: pending_stage=human_pause status=active (prescreen_route=no_signal_artifact)
- 2026-07-07T13:35:52Z HALT — no_signal_artifact. Campaign stopped on P4_ts_trend / run_054. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-07T13:57:45Z RESUME P4_ts_trend / run_054: resolution confirmed for 'no_signal_artifact', resuming queue processing.
- 2026-07-07T13:58:06Z STAGE  P4_ts_trend / run_054: pending_stage=protocol_execution status=failed (cost_ratio=4.3151, prescreen_route=proceed_to_backtest)
- 2026-07-07T13:58:06Z HALT — unhandled_exception: run_protocol.py failed:
C:\Users\alauz\Documents\Projects\trading-bot\trading-bot\core\backtester.py:234: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the futur. Campaign stopped on P4_ts_trend / run_054. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-09T12:49:14Z RESUME P4_ts_trend / run_054: resolution confirmed for 'unhandled_exception', resuming queue processing.
- 2026-07-09T13:02:22Z STAGE  P4_ts_trend / run_054: pending_stage=completed_refined status=active (cost_ratio=4.3151, prescreen_route=proceed_to_backtest, backtest_verdict=refine, median_sharpe=-1.66, verdict_status=pivot)
- 2026-07-09T13:02:23Z DONE P4_ts_trend (run_054) -> completed_refined
- 2026-07-09T13:02:23Z Queue exhausted — no ready or in_progress entries remain.
- 2026-07-09T13:53:35Z STAGE  P4_ts_trend / run_054: pending_stage=human_pause status=active (cost_ratio=4.3151, prescreen_route=proceed_to_backtest, backtest_verdict=refine, median_sharpe=-1.66, verdict_status=refine)
- 2026-07-09T13:53:37Z HALT — no_signal_artifact. Campaign stopped on P4_ts_trend / run_054. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-09T14:48:26Z STAGE  P4_ts_trend / run_054: pending_stage=human_pause status=active (cost_ratio=4.3151, prescreen_route=proceed_to_backtest, backtest_verdict=refine, median_sharpe=-1.66, verdict_status=refine)
- 2026-07-09T14:48:27Z HALT — component_execution_error. Campaign stopped on P4_ts_trend / run_054. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-09T16:56:16Z STAGE  P4_ts_trend / run_054: pending_stage=campaign_review status=failed (cost_ratio=4.3151, prescreen_route=proceed_to_backtest, backtest_verdict=refine, median_sharpe=-1.66, verdict_status=pivot)
- 2026-07-09T16:56:17Z HALT — unhandled_exception: Claude Code returned an error result: success. Campaign stopped on P4_ts_trend / run_054. See RUNBOOK.md 'Resume after a pause'.
- 2026-07-09T18:11:46Z RESUME P4_ts_trend / run_054: resolution confirmed for 'unhandled_exception', resuming queue processing.
- 2026-07-09T18:13:38Z STAGE  P4_ts_trend / run_054: pending_stage=completed_refined status=active (cost_ratio=4.3151, prescreen_route=proceed_to_backtest, backtest_verdict=refine, median_sharpe=-1.66, verdict_status=pivot)
- 2026-07-09T18:13:38Z DONE P4_ts_trend (run_054) -> completed_refined
- 2026-07-09T18:13:38Z Queue exhausted — no ready or in_progress entries remain.
- 2026-07-10T16:30:20Z [DRY RUN] === DRY RUN: verifying queue -> launch -> pause wiring (no LLM spend) ===
- 2026-07-10T16:30:20Z [DRY RUN] queue: selected entry 'P4_ts_trend' (status=in_progress, brief=briefs/P4_ts_trend_r1_er_gate.yaml)
- 2026-07-10T17:17:57Z [DRY RUN] === DRY RUN: verifying queue -> launch -> pause wiring (no LLM spend) ===
- 2026-07-10T17:17:57Z [DRY RUN] queue: selected entry 'P4_ts_trend' (status=in_progress, brief=briefs/P4_ts_trend_r1_er_gate.yaml)
- 2026-07-12T16:15:48Z STAGE  P4_ts_trend / run_057: pending_stage=completed_rejected status=rejected (cost_ratio=1.3626, prescreen_route=kill_no_ic, backtest_verdict=refine, median_sharpe=-0.686, verdict_status=kill)
- 2026-07-12T16:15:48Z DONE P4_ts_trend (run_057) -> kill_er_gate_mechanism_falsified
