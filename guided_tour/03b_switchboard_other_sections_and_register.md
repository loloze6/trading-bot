# Stop 03b: The switchboard, part b: the other sections and the flag register

## Speech (verbatim)

**Stop 03 of 29, part b: the config's other sections and the flag register.** Open on the side: `campaign_config.yaml` (the top and the bottom), `feature_flag_register.yaml`, `tests/test_campaign_config_sync.py`, `tests/test_feature_flag_register.py`.

**In one sentence.**
Around the switches sit two reference lists: a few statistical settings written down for the record, and a register that says, for every switch, who owns it, whether it is on, and why.

**Why it exists.**
The settings sections were meant to gather in one place the numbers the research relies on (how long a market "episode" lasts, how correlated BTC and ETH are), so a new campaign could change them without touching code.
The register exists because switches used to stay off with no reason given. Its rule: a finished feature is on, or the register names what it waits for. A test compares it with the real switches, so it cannot quietly drift.

**What comes in, what goes out.**
- In: numbers and switch states, written by hand.
- Out: nothing the running pipeline reads. Two tests read these files and fail when they disagree with the code.
- Used by: people, to see what is live and why; and the test suite.

**What happens here, step by step.**
The five settings sections:
1. The file's own header says it plainly: the code keeps its own copies of these numbers and does not read them here. A test checks that both copies match.
2. Prescreen: the block size used to count independent bars (24 on hourly bars, 1 on daily), a significance threshold, a fallback volatility. The copies live in the engine's statistics code.
3. Episode significance: how far apart two active bars may be and still belong to one episode (48 bars), the minimum number of episodes (8), the number of resamples (2,000). The claim test (stop 09) uses the code's copies.
4. Regime detector: a plausible band for how often a "trending" label should fire, and default test dates. The copies live in the regime-detector check, which no stage reaches today.
5. Verdict interpreter: thresholds for the old AI verdict stage. The comment says the AI applied them from its own instructions, not code.
6. Symbol correlation: BTC and ETH hourly returns are 0.82 correlated, so two coins count as about 1.1 independent coins, not 2.

The register:
1. One line per switch: its name, its kind, the config key, the code that reads it, the owner, its state, what it waits for, and a free-text criterion.
2. Two kinds. Most are config switches. Two are settings of the trading engine itself, switched on by the research tool that runs the backtests, never by changing the engine's own default.
3. One engine setting is on: equity recorded at every bar, not only at each trade's exit. The other is off: charging funding payments (the fee a perpetual future pays or receives), which fails below daily bars.
4. The test checks that every real switch has a line, that no line names a removed switch, that each line's state matches the config, that every "off" line names what it waits for, and that the two engine settings stay off by default in the engine.

**What it costs and how long it takes.**
No cost: nothing here runs during a campaign.
35 register lines: 33 config switches (30 on, 3 off) and 2 engine settings (1 on, 1 off) (`feature_flag_register.yaml`, counted with a read-only script).
929 lines in the register; 1,145 in the config file.

**What is switched off or not used here.**
- No running code reads the five settings sections; only the sync test does. Verdict interpreter and symbol correlation are checked by no test either.
- A comment in the launcher names a symbol-correlation reader that no longer exists in the code.
- 25 lines marked "on" still carry a "waiting for" text from before they were switched on. Several say "on master it stays off".
- The quarantine switch is in the config but has no register line.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Config header | `campaign_config.yaml:1-12` | Says the code keeps its own constants; `test_campaign_config_sync.py` enforces parity |
| Prescreen | `campaign_config.yaml:14-43` | Block sizes, significance threshold, degenerate volatility fallback; constants kept in code listed `:37-43` |
| Episode significance | `campaign_config.yaml:45-61` | `gap_bars` 48, `density_fallback_pct` 50, `min_n_episodes` 8, `n_resamples` 2000 |
| Regime detector | `campaign_config.yaml:63-82` | Activation band 0.10-0.40, default start/end dates; code constants listed `:74-82` |
| Verdict interpreter | `campaign_config.yaml:1113-1126` | Seven thresholds "applied by the LLM agent, not code" (`:1118`) |
| Symbol correlation | `campaign_config.yaml:1128-1145` | `btc_eth_return_correlation_1h: 0.82` and the n_eff formula |
| Sync test, prescreen | `tests/test_campaign_config_sync.py:35-82` | Compares with `timeframe.bars_per_day` and `performance.signal_statistics` |
| Sync test, regime detector | `tests/test_campaign_config_sync.py:86-117` | Compares with `tools/validate_regime_detector.py` |
| Sync test, sparse threshold | `tests/test_campaign_config_sync.py:124-135` | Looks for `below_floor > 50.0` in `run_phase1_research.py` |
| Sync test, episodes | `tests/test_campaign_config_sync.py:147-153` | Compares with `tools/episode_significance.py` |
| Episode code users | `tools/claim_tests.py:153-157`; `run_phase1_research.py:11141` | Import `episode_significance` |
| Stale reader mention | `run_campaign.py:1999` | Docstring names `_load_symbol_correlation`, absent from `run_phase1_research.py` |
| Register header | `feature_flag_register.yaml:1-23` | Purpose, the two kinds, the two states |
| Register entries | `feature_flag_register.yaml:25-894` | 33 `orchestrator_config` entries |
| Off entries | `feature_flag_register.yaml:619-625`, `:752-758`, `:829-835` | Zero-trade windows, deviation gate, extra cards at 1a |
| Engine setting on | `feature_flag_register.yaml:896-912` | `bar_equity`, passed `True` by `tools/run_protocol.py` |
| Engine setting off | `feature_flag_register.yaml:914-929` | `model_funding`, blocked on E-014 |
| Register test | `tests/test_feature_flag_register.py:120-302` | Missing entry, stale entry, state match, off names a blocker, engine defaults stay False, exactly two engine params |

Remarks? Mark a remark "direct" for an answer before the next stop; say "next" to continue.

## Operator remarks (verbatim, with the guide's direct answers)

Same remarks than before - i would clean the ones legacy by deletion. In the file should sit only mechanism workflow parameter - no statistical / specific / etc...

## Inspector notes

### (1) Design and mechanism

1. The five settings sections are not configuration: the header says so (`campaign_config.yaml:7-12`), and no code reads them (grep for `cfg.get("prescreen")`, `"episode_significance"`, `get("verdict_interpreter")`, `symbol_correlation` over `workflow/` and `tools/`: no reader; the `regime_detector` hits are the strategy config's key, not this section). They are a second copy of code constants with a parity test (`test_campaign_config_sync.py:42-153`). Deleting them, as the operator proposes, changes no run; what is lost is only the one place that says why a constant has its value, which belongs beside the constant in code.
2. What is live behind them, and through which copy: `episode_significance` is live through `tools/episode_significance.py`'s constants, read by the claim tests (`claim_tests.py:157-160`, used at `:1860`, `:1890`, `:2208`) and by the conformance check every run passes (`RP:11142` reads `episode_blocked_significance_by_symbol`, written by `run_protocol.py:2845`; run_102's `protocol_result.yaml` carries it). `prescreen` names a stage deleted in E-039; its constants now sit in `trading-bot/performance/signal_statistics.py:233,240` (whether that module is called on the live path was not checked). `regime_detector` feeds `tools/validate_regime_detector.py`, run only by `_ensure_regime_detector_report` (`RP:10146-10179`), not reached today (stop 28); its `default_start`/`default_end` (`:71-72`) point the detector check at the validation period, which the folds flag refuses for every backtest (`RP:10583-10604`): a default that would collide with the guard if the helper were ever reached. `verdict_interpreter` (`:1117-1126`) belongs to the unreached stage 11. `symbol_correlation` (`:1132-1145`) has no reader at all; the one mention is a stale docstring (`RC:1999` names `_load_symbol_correlation`, absent from `RP`, grep confirms).
3. The register is a mirror of the config with prose attached. Its test enforces four mechanical facts (an entry per `orchestrator.<name>.enabled` key, no stale entry, `state` equals `enabled`, every `off_incomplete` names a `blocked_on`; `test_feature_flag_register.py:120-199`) and two engine facts (`:223-302`). It does not check `reader`, `criterion` or `blocked_on` on an "on" entry, so those texts can be false without a failure. They are: 25 of the 31 "on" entries carry a `blocked_on` written when the flag was off (counted by hand; four entries at `:798-875` have no blank line between them); `grid_evaluation` says "held off_incomplete rather than on" (`:133-134`); `operator_approval`, `nearest_build` say "On master it stays off" (`:715`, `:739`); five entries describe "c4/flag-set (runtime, uncommitted)" as if it were another branch (`:649`, `:676`, `:715`, `:739`, `:804`); `score_provenance` describes a check on reader files D-198 deleted (`:541-551`); `decide_next`'s `blocked_on` says "no run on disk has artifacts/proposals/" (`:368`). The columns the register adds beyond the config's own comments are `owner` (Jeremy on all 35) and `reader` (the function name, also listed in `RC:3709-3747`). For autonomy: nothing here is read by a run; the cost is the same as 03a, a document that teaches the flag-off pipeline as current.
4. The register's own premise ("a finished feature is on, or the register names what it waits for", header `:20-23`) is the E-041 rule the operator set; today every flag but three is on, so the rule has done its work. A register of 35 entries where 31 are "on, switched on 2026-09/10" is a changelog. The information still useful to a new joiner (which switch, on or off, what it does in one line) is 35 lines; the file is 929.
5. The two engine parameters are the only entries that touch the backtest itself: `bar_equity` on (`:896-912`, checked by the test against `run_protocol.py`'s call sites, `:202-215`), `model_funding` off and blocked on E-014 (`:914-929`). The second is a real modelling gap for the goal: every Kraken perp brief (run_100 to run_102 are all `product: perp`, stop 01) is backtested without funding payments, so a perp strategy's cost is understated by the funding leg. The register records it as "a real gap" (`:926`); stop 13 should say by how much.
6. `halt_policy.quarantine_enabled` has no register line (grep: only a mention at `:443`); the register's test scans `orchestrator.<name>.enabled` keys only (`:103-106`), so the one switch whose state most bears on continuous running (03a note 1.2) is outside the register's guarantee.

### (2) Legacy or simplifiable (leads)

1. `symbol_correlation :1128-1145`: zero readers; its measuring recipe cites parquet files and a "campaign range" that is the validation period. Delete, with the docstring at `RC:1999`.
2. `verdict_interpreter :1113-1126`: thresholds "applied by the LLM agent" of a stage not reached. Delete with stop 28's decision on the stage.
3. `regime_detector :63-82` and `tools/validate_regime_detector.py`: reached only by `_ensure_regime_detector_report` (`RP:10143-10179`), itself a stop-28 item; `tools/retune_regime_detector.py:43` also imports it. Not checked whether the sync test (`:89-117`) is the only thing keeping the tool importable.
4. `prescreen :14-43`: the section is named after a deleted stage; the constants' live use is not checked. Candidate for a rename or a move to code comments.
5. `episode_significance :45-61`: live via code constants (note 1.2). If the sections go, this one's rationale text (`:48-61`) should move to `tools/episode_significance.py`.
6. Register: the removed-flag comment block (`:79-85`, `anti_adjacency_retry`), the `blocked_on` texts on 25 "on" entries, the "c4/flag-set" texts, and the `owner` column (one value). A register reduced to name, state, one-line effect and (for off entries) blocker is the operator's "limit the wording" applied here.
7. `test_campaign_config_sync.py:124-135` checks the sparse threshold by searching the source text for `below_floor > 50.0`; `RP` reads the number from no config (03a). A test that pins a dead config key to a source-text literal.

### (3) Disagreements between the speech and the element

1. Section 4 (register) step 4 lists what the test checks, correctly, but not what it does not check (`reader`, `criterion`, `blocked_on` on "on" entries); section 6's "25 lines ... still carry a waiting-for text" is the consequence, stated without the cause. Omission.
2. "The register ... says, for every switch, who owns it": the owner is the same person on all 35 entries (`owner: Jeremy`); true, and empty.
3. Section 4 step 4 of the settings: "The copies live in the regime-detector check, which no stage reaches today" is right (`RP:10146-10179`); the speech does not say that the section's default dates fall in the validation period the folds guard refuses (note 1.2). Fact, not error.
4. Section 6 "the quarantine switch is in the config but has no register line": confirmed; the reason (the test scans `.enabled` keys only, `:103-106`) is not given.
5. Counts verified: 35 entries (33 `orchestrator_config`, 2 `engine_param`; grep), 31 `state: "on"`, 4 `off_incomplete`; 25 "on" entries with `blocked_on` (hand count); 929 register lines, 1,145 config lines. Reading-map ranges verified: `campaign_config.yaml:1-12`, `:14-43`, `:37-43`, `:45-61`, `:63-82`, `:74-82`, `:1113-1126`, `:1118`, `:1128-1145`; `test_campaign_config_sync.py:35-82`, `:86-117`, `:124-135`, `:147-153`; `claim_tests.py:153-157` (the import at `:153`, the settings dict at `:157-160`); `RP:11141` (the import inside the conformance check, `:11138-11142`); `RC:1999`; register `:1-23`, `:25-894`, `:619-625`, `:752-758`, `:829-835`, `:896-912`, `:914-929`; `test_feature_flag_register.py:120-302`.
