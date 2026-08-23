# Near-miss scoreboard (E-018 S1)

Ranked table over every tested idea in `runs/`, for the
idea-generation stage to read as raw material only. **Not a
promotion input** -- see `tests/test_near_miss_scoreboard_firewall.py`.

Ranked BY: numeric near-miss quality first (tier 0 -- FAIL
criteria with a recoverable margin, ordered by the *smallest*
magnitude miss on the run's worst-binding failed criterion --
i.e. the criterion it came closest to passing); then (tier 1)
runs with a verdict but no recoverable numeric margin, ordered
by status (refine > escalate > pivot > kill > absent); then
(tier 2) runs with no verdict file at all, by run_id. Positive
IC is used only as a tie-break within a tier, never as the
primary key.

## Denominators (MEASURED)

- Total run dirs scanned: 59
- Have a verdict_interpretation.yaml: 38 of 59
-   full_protocol schema: 36 of 59
-   prescreen_only schema: 2 of 59
- protocol_verdict recorded (non-absent, within verdict file): 36 of 59
- status recorded (non-absent, within verdict file): 33 of 59
- Numeric worst-fail margin recovered: 24 of 59
- IC recovered (any source): 7 of 59
- Cost ratio recovered (any source): 5 of 59
- Era-behaviour text recovered: 4 of 59

## Table

| rank | run_id | hypothesis_family | evidence_tier | protocol_verdict | status | failure_bucket | worst_fail_margin_frac | margin_source | root_cause_mechanism | ic | cost_ratio | era_behavior |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | run_029 | keltner_mean_reversion | full_protocol | refine | refine | regime | 0.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 2 | run_022 | mean_reversion | full_protocol | kill | pivot | regime | -0.24 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 3 | run_031 | keltner_breakout | full_protocol | refine | escalate | regime,nosignal | -0.33 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 4 | run_018 | rsi_momentum_trending | full_protocol | refine | refine | cost | -0.4667 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 5 | run_014 | rsi_mean_reversion | full_protocol | kill | pivot | cost | -0.5333 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 6 | run_059 | funding_rate_mean_reversion | full_protocol | refine | kill | other | -0.6535 | structured | already_priced_in | not_recorded | not_recorded | not_recorded |
| 7 | run_026 | keltner_regime_gating | full_protocol | refine | refine | cost | -0.7 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 8 | run_054 | sma_trend_following | full_protocol | refine | refine | other | -0.9752 | text_approx | lag_mismatch_to_regime_persistence | not_recorded | not_recorded | per_trade_expectancy_bps mean=1050.5 (t_stat=1.91, marginall... |
| 9 | run_039 | rsi_secondary_mean_reversion | full_protocol | refine | refine | regime | -0.98 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 10 | run_015 | keltner_breakout | full_protocol | refine | pivot | nosignal | -1.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 11 | run_017 | keltner_mean_reversion | full_protocol | refine | pivot | other | -1.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 12 | run_019 | rsi_momentum | full_protocol | refine | refine | other | -1.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 13 | run_020 | rsi_momentum_trending | full_protocol | refine | escalate | regime | -1.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 14 | run_024 | keltner_trend_mean_reversion | full_protocol | refine | pivot | regime | -1.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 15 | run_025 | keltner_threshold_regime | full_protocol | refine | refine | regime | -1.0 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 16 | run_028 | keltner_scoremode | full_protocol | refine | refine | regime | -1.0 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 17 | run_032 | keltner_threshold_regime | full_protocol | refine | escalate | regime,nosignal | -1.0 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 18 | run_033 | keltner_breakout | full_protocol | refine | refine | regime | -1.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 19 | run_037 | keltner_breakout | full_protocol | refine | refine | regime | -1.0 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 20 | run_016 | keltner_mean_reversion | full_protocol | refine | refine | cost | -1.1401 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 21 | run_011 | not_recorded | full_protocol | refine | not_recorded | regime | -1.2096 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 22 | run_030 | keltner_scoremode | full_protocol | refine | pivot | cost | -9.7 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 23 | run_034 | keltner_breakout | full_protocol | kill | refine | cost | -14.582 | structured | not_recorded | not_recorded | not_recorded | not_recorded |
| 24 | run_021 | keltner_mean_reversion | full_protocol | refine | pivot | nosignal | -23.6367 | text_approx | not_recorded | not_recorded | not_recorded | not_recorded |
| 25 | run_048 | fear_greed_contrarian | full_protocol | refine | refine | nosignal | not_recorded | unparseable_free_text | entry_exit_execution_gap | -0.0403 | 1.47 | ic_active_bars=-0.0403 pooled across 234 episodes (n_bars=16... |
| 26 | run_023 | keltner_mean_reversion | full_protocol | refine | refine | cost | not_recorded | unparseable_free_text | not_recorded | not_recorded | not_recorded | not_recorded |
| 27 | run_047 | funding_rate_mean_reversion | full_protocol | kill | escalate | sample | not_recorded | unparseable_free_text | no_informational_content_this_venue | 0.008435 | not_recorded | not_recorded |
| 28 | run_044 | funding_rate_mean_reversion | full_protocol | kill | escalate | nosignal | not_recorded | unparseable_free_text | lag_mismatch_to_regime_persistence | -0.008706 | not_recorded | not_recorded |
| 29 | run_035 | regime_selectivity | full_protocol | kill | escalate | nosignal | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 30 | run_053 | macd_trend_following | full_protocol | kill | escalate | other | not_recorded | unparseable_free_text | no_informational_content_this_venue | not_recorded | 0.245 | not_recorded |
| 31 | run_050 | funding_rate_mean_reversion | full_protocol | kill | pivot | other | not_recorded | unparseable_free_text | already_priced_in | 0.000822 | 0.7368 | ic_all_bars=0.000822 (ungated, pooled across 110,904 bars, 1... |
| 32 | run_043 | moving_average_crossover | full_protocol | kill | pivot | other | not_recorded | not_recorded | already_priced_in | -0.021091 | not_recorded | not_recorded |
| 33 | run_027 | keltner_mean_reversion | full_protocol | refine | pivot | regime | not_recorded | unparseable_free_text | not_recorded | not_recorded | not_recorded | not_recorded |
| 34 | run_057 | sma_trend_longonly_with_efficiency_gate | full_protocol | kill | kill | regime | not_recorded | unparseable_free_text | already_priced_in | not_recorded | not_recorded | not_recorded |
| 35 | run_042 | not_recorded | prescreen_only | not_recorded | not_recorded | other | not_recorded | not_recorded | not_recorded | 0.190476 | 3.7545 | not_recorded |
| 36 | run_041 | funding_rate_mean_reversion | prescreen_only | not_recorded | not_recorded | other | not_recorded | not_recorded | insufficient_sample_inconclusive | 0.013993 | 0.8314 | ic_active_bars=0.014 at p=0.9705 with n_eff=10 (block_size=2... |
| 37 | run_012 | not_recorded | full_protocol | refine | not_recorded | regime | not_recorded | unparseable_free_text | not_recorded | not_recorded | not_recorded | not_recorded |
| 38 | run_013 | not_recorded | full_protocol | refine | not_recorded | regime | not_recorded | unparseable_free_text | not_recorded | not_recorded | not_recorded | not_recorded |
| 39 | run_0001 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 40 | run_002 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 41 | run_003 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 42 | run_004 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 43 | run_005 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 44 | run_006 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 45 | run_007 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 46 | run_008 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 47 | run_009 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 48 | run_010 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 49 | run_036 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 50 | run_038 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 51 | run_040 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 52 | run_045 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 53 | run_046 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 54 | run_049 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 55 | run_051 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 56 | run_052 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 57 | run_055 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 58 | run_056 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
| 59 | run_058 | not_recorded | thin_no_verdict_file | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded | not_recorded |
