# RUNBOOK.md command audit (night work round 4)

Scope: every command line, code block and inline command in `strategy-research/docs/RUNBOOK.md`,
checked against the committed code. RC = `strategy-research/workflow/run_campaign.py`,
RP = `strategy-research/workflow/run_phase1_research.py`; other paths are relative to
`strategy-research/` unless prefixed `TB/` (trading-bot/) or `repo/`. RUNBOOK line numbers are
for the file AFTER the fixes below (one line was added at line 16, so every line from 17 on is
the old number + 1). Nothing was run except `--help` of the `gh` CLI and the tests listed at the
end.

## Verdicts

| RUNBOOK line | Command | Verdict | Evidence |
|---|---|---|---|
| 16-17 | "Shell: bash ... No PowerShell syntax used here" | FIXED | Line 559 (run viewer) is PowerShell (`& $env:TBOT_PYTHON ...`); the claim now names that one exception. The PowerShell form is kept as written. |
| 20 | `../venv/Scripts/python.exe` (interpreter) | UNCHECKABLE | Windows venv at the repo root on the operator's machine; repo/.gitignore:13 ignores `venv/`, so there is none in this checkout. Consistent with the hook's own note at tools/hooks/pre-commit:19. |
| 22 | `PYTHONUTF8=1` / `setup_run.py` emoji prints | OK | workflow/setup_run.py exists; RC:100-103 also guards stdout itself. |
| 30 | `cd trading-bot/strategy-research` | OK | RC:5977-5981 refuses to run unless CWD is `strategy-research/` (ROOT, RC:105). The `trading-bot/` prefix assumes the clone folder is called `trading-bot` (it is here). |
| 40 | `sh strategy-research/tools/setup_hooks.sh` (from repo root) | OK | tools/setup_hooks.sh:15, 26-30 (cds to the git toplevel itself), 77 sets `core.hooksPath` to `strategy-research/tools/hooks`. Effect (secret scan + holdout gate) matches tools/hooks/pre-commit:32-52, 60-93. |
| 51 | `sh strategy-research/tools/setup_hooks.sh --check` | OK | tools/setup_hooks.sh:39-58: changes nothing, reports status, exits non-zero when not wired. Only `--check` is accepted (positional `$1`). |
| 46 | `git pull` (updates the gates) | OK | Follows from the relative `core.hooksPath` (tools/setup_hooks.sh:74-77). |
| 90 | `gh pr list --state open --limit 20` | OK | `gh pr list --help`: `-s, --state {open\|closed\|merged\|all}`, `-L, --limit int`. External tool. |
| 91 | `gh issue list --state open --limit 30` | OK | `gh issue list --help`: `-s, --state {open\|closed\|all}`, `-L, --limit int`. External tool. |
| 139 | `run_campaign.py --dry-run` | OK (note) | RC:5935 (`store_true`), dispatched at RC:5993 to `dry_run_verify` (RC:5837); sandbox run id `run_dryrun_verify` (RC:5869), removed in `finally` with its generated protocol (RC:5918-5922); never takes the campaign lock. Note 1: it does append `[DRY RUN]` lines to `campaign_record/campaign_log.md` (`_log`, RC:2816-2822), so "zero footprint" (heading) means zero footprint on state, not on the log. Note 2 (line 142): on an all-terminal queue it logs "nothing to verify" and returns WITHOUT `=== DRY RUN PASSED ===` (RC:5845-5853), exit 0. Not changed: the paragraph's explicit list (campaign_state, queue, runs numbering) is correct. |
| 187-202 | 1a-bis check-all-four `python -c` snippet | OK | `camp._parse_brief_frontmatter` RC:669; brief `evaluation.pass_rule` -> `pre_registration.pass_rule` as in RC:808-819; `orch._lint_pass_rule_total_mapping(pre)` returns `(violations, warnings)` RP:11311, 11324; `orch._lint_machine_constraints_protocol_selection(constraints, pass_rule)` RP:10908; `orch._compute_protocol_content_hash(path)` RP:10895-10905 (drops `protocol_version`/`protocol_content_hash`, as the text says). |
| 208 | `run_campaign.py` (no flags, continuous) | OK | RC:6016-6028: takes the campaign lock, then `run_forever(once=False)` (RC:5787-5791) loops until `process_once` returns False. |
| 213 | "`XS_momentum` stays `blocked_on_P2`" | WRONG-NOT-FIXED | Queue state, not a command: committed config/campaign_queue.yaml:259-261 has `XS_momentum` `status: done`. Either way it is never picked up; left for the lead (the operator's live queue may differ). |
| 218-220 | `PYTHONUTF8=1 nohup ... run_campaign.py > campaign_stdout.log 2>&1 &` / `echo $! > campaign.pid` | OK | Same entry point as line 208; shell only. Section is marked blocked (prose). |
| 257 | `run_campaign.py --once` | OK | RC:5937; `run_forever(once=True)` = exactly one `process_once()` (RC:5787-5791), which calls `_run_after_preflight` once (RC:4651) -> one `orch.run_loop` (RC:4463/4465). "NOT one pipeline stage" correct. |
| 264 | "`--step` mode does not exist yet" | OK | No `--step` in RC argparse (RC:5932-5975). |
| 296-318 | target flag-set YAML block | OK | Every key (`exclusion_digest_input` ... `score_provenance`, `operator_approval`, `halt_policy.quarantine_enabled`) is declared in committed config/campaign_config.yaml (one match each). Values are a target set, not the committed defaults (the section says so). |
| 363-364 | `tools/decide_next.py:1494`, `:2343-2344`, `workflow/run_campaign.py:5443` (fixed brief key lists) | FIXED | The cited lines had drifted. The key lists `("strategy_domain", "market_universe", "timeframe", "venue", "product")` are now at tools/decide_next.py:1537-1538 (`composition_brief`, def 1515), tools/decide_next.py:2664-2665 (`candidate_brief`, def 2646) and RC:5707-5708 (`refold_brief`, def 5691). None includes `scope` (claim still true). |
| 380, 393 | `run_tool_worker` passes `--legacy-verdict-retired`; `tools/run_protocol.py` refuses a missing/empty/partial promotion block before any backtest (exit 3) | OK | RP:1745-1752 (flag added only when promotion is retired), RP:1813; tools/run_protocol.py:2365 (flag), 2472-2487 (refusal via `_refuse_before_any_backtest`, 2014-2019), `EXIT_NO_DATA_TOUCHED = 3` tools/protocol_refusal.py:8. |
| 396-397 | "A by-hand `--holdout` run ... must pass `--legacy-verdict-retired` too" | OK | tools/run_protocol.py:2487 (refusal text says the same). |
| 426-427 | `run_campaign.py register --brief <path> --priority 1 --notes "..."` | OK | Subcommand RC:5953-5962: `--brief` (required, Path), `--priority` (required, int), `--notes` (required); dispatched RC:5983-5984. Effect: with `decide_next` on, the entry gets `brief_status: open` (`_register_from_cli` RC:5615-5626); entry `status: ready` by default (`register_hypothesis` RC:955-958). Not lock-gated (RC:6012-6015 comment). |
| 516 | `kill -0 "$(cat campaign.pid)" ... RUNNING / STOPPED` | OK | Shell only. |
| 522-528 | queue-state `python -c` snippet | OK | config/campaign_queue.yaml top-level `queue:` (line 3), entries carry `id`, `status`, `run_ids`, `outcome`; same loader shape as `_load_queue` RC:173-175. |
| 533 | `tail -n 20 campaign_log.md` | FIXED | The log is `campaign_record/campaign_log.md` (RC:107, `CAMPAIGN_LOG_PATH`); no `campaign_log.md` exists at `strategy-research/`. Now `tail -n 20 campaign_record/campaign_log.md`. |
| 539 | `cat campaign_summary.md` | FIXED | The summary is `campaign_record/campaign_summary.md` (RC:108, written RC:3150). Now `cat campaign_record/campaign_summary.md`. |
| 550 | `cat "runs/<run_id>/pipeline_state.yaml"` | OK | Run state file, written by `update_state` RP:609. |
| 559 | `& $env:TBOT_PYTHON tools/run_viewer/server.py --runs runs --port 8765` (+ `--host 0.0.0.0`) | OK | tools/run_viewer/server.py:229-235: `--runs` (default `runs`), `--host` (default `127.0.0.1`), `--port` (int, default 8765). `TBOT_PYTHON` is defined by strategy-research/CLAUDE.md:64-66. PowerShell form kept. |
| 587 | `kill -0 "$(cat campaign.pid)"` reports STOPPED after a halt | OK | A halt makes `process_once` return False, ending `run_forever` (RC:5787-5791) and the process. |
| 604, 852-859 | `--resume` refuses while the run is `paused_for_human`/`failed`; skips parked entries; flips the entry to `in_progress`; `data_block_hitl` calls `resume_pipeline()`; then falls through into the loop | OK | RC:5939; `resume_paused_entry` RC:2197-2375: parked skipped 2208-2217, still-stuck refusal 2350-2358 (also `pending_stage: human_pause`), `in_progress` 2371 (2328 for `data_block_hitl`), `resume_pipeline` 2332; on success main falls through to the lock and `run_forever(once=args.once)` (RC:6010-6026), so `--resume --once` limits it to one step. Note (code, not doc): `--resume` writes the queue BEFORE the campaign lock is taken (RC:6010-6012 vs 6021). |
| 621 | `docs/00_closing_state.md` section 7 | WRONG-NOT-FIXED | No such path. The only tracked copy is engineering/improvements/done/design_and_docs/00_closing_state.md, which has sections 1-6 only and does not mention run_045/run_046; git history holds other copies (strategy-research/00_closing_state.md, docs/plan/00_closing_state.md). Target ambiguous, left for the lead. |
| 619, 1130 | `run_campaign.py::evaluate_wishlist_predicate()` / `evaluate_and_persist_wishlist_predicate()` | OK | RC:1326, RC:1380. |
| 654 | `tests/test_wishlist_predicate.py` | OK | Exists. |
| 683 | `python workflow/run_campaign.py refold --run <run_id> --fold <A\|B\|C\|D>`, then `--once` | OK | Subcommand RC:5963-5970: `--run` (required), `--fold` (required, `choices=research_folds.ALL_FOLDS` = A, B, C, D, tools/research_folds.py:61-67), `--priority` (int, default 0); RC:5986-5987 -> `_refold_from_cli` RC:5763-5784 writes `briefs/refold_<run>_fold_<X>.md` and registers it ready. Precondition the row does not repeat: `_refold_flag_refusal` RC:5680 (REFOLD_HELP: needs `exact_config_1b` + `config_direct_authoring` on, `variant_loop` off). |
| 684, 715 | `tools/run_protocol.py <config> <protocol> --holdout --i-understand --hypothesis-id <hypothesis_id>` (715: plus `--legacy-verdict-retired`) | OK | tools/run_protocol.py:2348-2352 (two positionals, `--holdout`, `--i-understand`, `--hypothesis-id`), 2365. `--holdout` and `--i-understand` must come together (2435-2439); `--hypothesis-id` is required with `--holdout` and refused without it (2190-2193, 2461-2462); refused if already in `holdout_consumed_by` (2182-2189); range taken from the policy's `holdout_range`, a disagreeing protocol block refused before any fetch (2068-2080). |
| 689-692 etc. | `--resume` / `--unpark` / `resume_pipeline` clear `stage_exception`, `protocol_promotion_unratified`, `launch_exception` | OK | `_clear_run_halt_flags` RC:2378-2389 called from `--resume` (2327, 2370) and `--unpark` (2457); `_stale_run_halt_flags` RP:19587. |
| 693 | `tools/stamp_protocol.py` (for `protocol_ref_content_hash`) | OK | tools/stamp_protocol.py:60-66: positional `protocol_path`, optional `--version`; prints the hash for `machine_constraints.protocol_ref_content_hash`. |
| 701-704 | `tools/anti_adjacency_gate.py`, `tools/novelty.py`, `tools/variant_coin.py` `resolve_variant`, TB `tools/validate_config.py`, `tools/forecast_rules.py` (cited as code) | OK | All exist (validate_config.py is TB/tools/validate_config.py, cited by bare name). |
| 707, 735 | `python workflow/run_campaign.py register --brief <path> --priority <n> --notes "<text>"` | OK | As line 426. |
| 708, 739 | `BRIEF_MAX_CONSECUTIVE_EMPTY_R2` in `tools/decide_next.py` | OK | tools/decide_next.py:172 (`= 2`). |
| 711 | `run_campaign.py refold --run <run_id> --fold <X>` | OK | As line 683. |
| 737, 739 | `--unpark <entry_id>` / stop line `Parked, waiting for a component or data: [...] -- unpark with --unpark <id>` | OK | RC:4945 (`_parked_note`), RC:4534. |
| 738 | `tools/claim_tests.py` (cited as code) | OK | Exists; its CLI (RC-independent) listed below. |
| 767-772 | reset snippet `orch.update_state(path=..., status='active', last_error=None)` | OK | `update_state(path, **kwargs)` RP:609. |
| 797-820 | full reset snippet (state keys + every sticky flag) | OK | The 27 flags equal the set the classifiers read (`_classify_human_pause` RC:1494, `_hard_pause_reason` RC:1706; constants RP:6970, 7053-7057, tools/campaign_review_retired.py:33), minus the three run-halt flags every un-pause path clears itself (RC:2378). The priority ORDER claim was not audited. |
| 846 | `run_campaign.py --resume` | OK | See line 604 row. |
| 860-861 | "After it prints `RESUME ...`" / `Queue exhausted — no ready or in_progress entries remain.` | OK | RC:2373, RC:4534. |
| 906 | `run_campaign.py --unpark <entry_id>` | OK | RC:5941-5943 (`metavar=ENTRY_ID`), RC:5997-6000 -> `_unpark_entry` RC:2392-2470: takes the lock (2403-2408), refusals as listed (2417-2450), sets run `active` at `parked.resume_stage` (2452), entry `ready` priority kept (2458), logs `UNPARK` (2462), exits. |
| 941-942 | `run_campaign.py --relaunch <entry_id>` then `--once` | OK | RC:5948-5951, RC:6006-6008 -> `_relaunch_entry` RC:2496-2625: lock (2508-2513); refuses park, non-paused/hold, launch/flag pre-flight halts (2531), anything but `stage_exception`/`unhandled_exception` (RELAUNCHABLE_REASONS RC:2474), refinement brief, no run, lineage, split child (2563), queued cards (2571); clears `run_ids`, `ready` (2591), note, saves the queue, THEN writes `ORPHANED_README.md` (2601), logs `RELAUNCH` (2617). |
| 981-982 | `run_campaign.py retry-analyst --run <run_id>` then `--once` | OK | Subcommand RC:5971-5974 (`--run` required), RC:5989-5991 -> `_retry_analyst` RC:2699: lock (2706); refusals in `_retry_analyst_refusal` RC:2654 match lines 985-991; archive to `retry_<n>` = 1 + highest (2724), items analyst_queries/, analyst/, proposals/, decision_record.yaml (RC:2651, RP:4455); clears live analyst dirs + the two lens readings (RC:2752 -> RP:4480-4496); entry `in_progress`/`outcome: null` (2729), run `active` at `analyst`, logs `RETRY-ANALYST` (2757). |
| 1024 | log line `awaiting operator approval: <id> (run_campaign.py --approve <id>)` | OK | RC:3438. Stop-line suffix `Awaiting operator approval: [...]` RC:4933. |
| 1032 | "`register`, `--unpark` and `--resume` set `ready` as before" | FIXED | `--resume` sets the entry `in_progress` (RC:2371; 2328 for `data_block_hitl`); only a flag pre-flight halt with no run goes back to `ready` (RC:2230) and a launch exception to its prior status (RC:2246-2247). `register` sets `ready` (RC:958), `--unpark` sets `ready` (RC:2458). |
| 1038 | `run_campaign.py --approve <entry_id>` | OK | RC:5944-5947, RC:6002-6004 -> `_approve_entry` RC:2772-2811: lock (2781); refuses unless status is exactly `blocked_on_operator_approval` (RC:148, 2795); sets `ready` (2799, priority kept), regenerates summary, logs `APPROVE`, writes loop health; flag state not read (works with the flag off). "launches one run" is NOT claimed: it only sets ready and exits; the text says to relaunch (line 1045). |
| 1096 | `kill "$(cat campaign.pid)"` | OK | Shell. Lock left by a killed process is cleared as stale on next acquire (same host, dead pid; or older than 6 h): tools/campaign_lock.py:27-33, 127-151. |
| 1099 | "no special signal handling in `run_campaign.py`" | OK | No `signal` import or handler in RC. |
| 1109 | `kill -0 ... STILL RUNNING / STOPPED` | OK | Shell. |
| 1156 | `tools/fragment_patterns.py` writes `fragment_patterns.yaml` | OK | Exists (no CLI). |

Not found in RUNBOOK: any `run_phase1_research.py` invocation (it is named only as the wrapped
orchestrator), any `run_tests.py` invocation, any git command other than `git pull` (line 46),
any `.ps1` helper. RUNBOOK claims no mutual exclusion between RC flags.

### Flags: mutual exclusion and required (as coded)

- RC top-level flags (`--dry-run`, `--once`, `--resume`, `--unpark`, `--approve`, `--relaunch`)
  are NOT in a mutually exclusive group (RC:5932-5951). With several given, the first match wins
  in this order: subcommand (`register` / `refold` / `retry-analyst`, RC:5983-5991) >
  `--dry-run` (5993) > `--unpark` (5997) > `--approve` (6002) > `--relaunch` (6006); `--resume`
  (6010) then falls through to the loop and combines with `--once`. RUNBOOK never says otherwise.
- Required: `register --brief/--priority/--notes` (RC:5957-5962), `refold --run/--fold`
  (5964-5966), `retry-analyst --run` (5973). RUNBOOK always passes them.
- run_protocol.py: `--holdout` iff `--i-understand` (2435); `--hypothesis-id` required with and
  only with `--holdout` (2190-2193, 2461); `--diagnostics-only` excludes `--validation-protocol`
  (2442-2444). RUNBOOK's holdout commands respect all three.

## Fixes applied (old -> new)

1. Line 16: `No PowerShell syntax used here.` -> `No PowerShell syntax used here,` + new line 17
   `except the run-viewer line in section 2 (PowerShell, as written there).`
2. Line 363-364: `tools/decide_next.py:1494`, `:2343-2344`, `workflow/run_campaign.py:5443` ->
   `tools/decide_next.py:1537`, `:2664-2665`, `workflow/run_campaign.py:5707`.
3. Line 533: `tail -n 20 campaign_log.md` -> `tail -n 20 campaign_record/campaign_log.md`.
4. Line 539: `cat campaign_summary.md` -> `cat campaign_record/campaign_summary.md`.
5. Line 1032: `` `register`, `--unpark` and `--resume` set `ready` as before. `` ->
   `` `register` and `--unpark` set `ready`, and `--resume` sets `in_progress`, as before. ``

The standing-rules holdout pointer (lines 1116-1117) is untouched. No PowerShell form was
converted.

## Left as is (for the lead)

- Line 213: `XS_momentum` "stays `blocked_on_P2`"; committed queue has it `done`
  (config/campaign_queue.yaml:259-261).
- Line 621: `docs/00_closing_state.md` section 7 does not exist; the only tracked copy
  (engineering/improvements/done/design_and_docs/00_closing_state.md) has no section 7.
- Line 139-142: the dry run appends `[DRY RUN]` lines to the campaign log (RC:2816-2822), and on an
  all-terminal queue ends without `=== DRY RUN PASSED ===` (RC:5845-5853).
- Code notes, not doc: `--resume` modifies the queue before taking the campaign lock
  (RC:6010-6012 vs 6021); `retry-analyst`'s lock refusal prints `--retry-analyst refused`
  (RC:2710) although it is a subcommand, not a flag.
- Outside this task's files: tools/hooks/pre-commit:47 writes the sealed window's dates out
  in a comment (CLAUDE.md hard rule says refer to them only via the policy file). Not edited.

## CLI options that exist but RUNBOOK never documents

- RC `refold --priority <int>` (default 0; RC:5967-5970).
- RC: `--resume` combined with `--once` (one step after the resume; RC:6010-6026) is not stated.
- RP `run_phase1_research.py <run_id> [--resume]` (RP:20717-20718); no RP invocation in RUNBOOK.
- `workflow/setup_run.py <run_id>` (setup_run.py:132).
- tools/run_protocol.py: `--validation-protocol`, `--diagnostics-only`, `--out-dir`,
  `--cost-product {spot,perp}`, `--commission-bps`, `--exchange`, `--drop-feeds`,
  `--cost-bar-all-costs`, `--forecast-ic-horizons` (tools/run_protocol.py:2357-2424).
- tools/run_viewer/server.py `--root` (server.py:232).
- tools/stamp_protocol.py `<protocol_path> [--version]` (stamp_protocol.py:60-66): named, but its
  invocation is not shown.
- tools/claim_tests.py `--run --spec --out --cache-dir` (required), `--cache-pattern`, `--method`,
  `--calibration` (claim_tests.py:2307-2317).
- tools/anti_adjacency_gate.py `<config> <protocol> [--memory] [--kb] [--runs-dir]
  [--hypothesis-id] [--exclude-run-id] [--out]` (anti_adjacency_gate.py:454-462).
- TB tools/validate_config.py `<config.json>` (single positional via sys.argv, validate_config.py:604-608).

## Tests

Tests that read `docs/RUNBOOK.md` (grep of strategy-research/tests and trading-bot/tests; TB has
none; no test pins any string changed above), run from `strategy-research/` with
`CI=true PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -m pytest -q`:

test_e059_6c_s2a_route_retirement.py, test_e059_6c_s2b_campaign_review.py,
test_e059_6c_s2b_review_fixes.py, test_e059_6c_s2c_parked_states.py,
test_e059_6c_s2c_review_fixes.py, test_e059_6c_s2d_holdout_unlock.py, test_e059_s2b_briefs.py,
test_e059_s2b_review_fixes.py, test_e061_c2_s2c_variant_shape.py,
test_e068_4_approval_cap_warnings.py, test_holdout_research_only_gate.py,
test_profit_bars_every_backtest.py

Result: **550 passed**, 11 warnings (numpy timedelta deprecation in tools/composition.py:881), 53 s.
