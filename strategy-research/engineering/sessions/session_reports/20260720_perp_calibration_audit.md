# Dispatch J — Independent audit of commit d86f0d0 (perp cost wiring + calibration re-runs)

**Role:** Independent read-only auditor. Every claim re-derived from git, code,
and on-disk run artifacts — not from the implementer's own session reports.

## Precondition manifest

- `git log --oneline -1` → `d86f0d0 Perp cost calibration: product-aware cost
  wiring + Kraken perp block` — subject describes perp cost wiring/calibration,
  MATCH.
- `git status --porcelain` → only untracked session-report `.md` files — MATCH.
- Proceeded.

## Step 1 — PRIMARY QUESTION: the run_028 zero-trade anomaly

**Verdict: (b) reproduction mismatch — confirmed, not undeterminable.**

The differing input is the **candle interval**, not the commission rate.

Original run_028 (executed 2026-06-29, `git_sha e814b07`) and the perp re-run
(executed 2026-07-20, `git_sha 102fa8e`) both target
`protocols/escalation_solusdt_4h.json`, whose `"timeframe": "4h"` field has been
present since the file was created in commit `e814b07` itself. But their own
`manifest.json` records disagree on what was actually executed:

| | Original run_028 (2024-08 window) | Perp re-run (2024-08 window) |
|---|---|---|
| `data.timeframe` | **`"3600s"` (1h)** | **`"14400s"` (4h)** |
| `data.start` / `data.end` | 2024-08-01 / 2024-09-01 | 2024-06-27 / 2024-09-01 20:00 (warmup-extended) |
| `data.bar_count` | 768 | 402 |
| `config_sha256` | `67a51ac2...` (matches perp re-run) | `67a51ac2...` |
| `git_sha` | `e814b07` | `102fa8e` |

Same strategy config (`config_sha256` matches exactly for the two trade-bearing
windows — see reproduction-integrity note below), but a **4x different bar
resolution**. I confirmed this is not cherry-picked: `run_030`'s original run
(same arc) shows the identical defect — `data.timeframe: "3600s"` in its
original manifest vs `"14400s"` in its perp re-run manifest, despite both
targeting `protocols/escalation_avaxusdt_4h.json`.

**Root cause, independently derived:** `git show e814b07:strategy-research/tools/run_protocol.py`
has **zero** occurrences of `timeframe` or `interval_seconds` — the
protocol-timeframe-to-`interval_seconds` threading logic did not exist yet at
the commit that produced the original run_028/run_030 results. The `"4h"` field
in the protocol JSON was inert at that time; `run_backtest()` fell through to
its own default (the global-config interval, 1h). That threading logic was
added in a later commit (present by the time of Dispatch E's read, commit
`93f3d87`, and unchanged through to the perp re-run's `102fa8e`). So the
original runs silently executed at 1h despite their protocol declaring 4h, and
the perp re-run (current code) correctly executes at 4h.

**Decisive bar-level evidence** (SOLUSDT, 2024-08-24 12:00, window 2024-08):
original run's bar at this timestamp is `open=157.33 high=158.27 low=156.97
close=157.28`; the perp re-run's bar at the *same nominal timestamp* is
`open=157.33 high=159.78 low=156.97 close=159.46` — because the perp re-run's
"12:00" bar aggregates a 4-hour window while the original's is a 1-hour slice.
The current on-disk cache (`trading-bot/local_data/SOLUSDT_4h.csv`) matches the
perp re-run's bar exactly, confirming the re-run reads genuine 4h data, not a
corrupted fetch. Window 2024-09 shows the same pattern: original has bars at
00:00, 01:00, 02:00... (hourly); perp re-run has bars at 00:00, 04:00, 08:00...
(4-hourly) — for the identical calendar window.

**Reproduction-integrity note (config, ruled out as the cause):** run_028's own
*recorded* top-level `config_sha256` (`8ca06f67...`) actually only matches
windows 2024-01 through 2024-06 of the original run (all zero-trade regardless);
windows 2024-07 through 2024-11 — including both trade-bearing windows,
2024-08 and 2024-09 — were internally run under a *different* config hash,
`67a51ac2...` (a mid-run config edit within the original run_028 execution
itself, unrelated to this dispatch). The perp re-run's config_sha256 is also
`67a51ac2...`. I independently recomputed the canonical hash
(`json.dumps(cfg, sort_keys=True, separators=(",",":"))` → sha256, replicating
`run_protocol.py:_config_sha`) against the config file currently on disk and
got `67a51ac2...` — confirming the perp re-run used the *same* config as the
original run's own trade-bearing windows. Config is not the confound; interval
is.

**Conclusion:** run_028's "0 trades in every window under perp cost" cannot be
attributed to the lower fee — it is an artifact of comparing a 1h backtest
(original) to a 4h backtest (re-run). The commit's framing ("a degenerate case
for this already ~1%-activation signal") is not supported by this evidence; the
correct characterization is that the comparison itself is invalid.

**This same defect also taints run_030**, which the commit did present as a
clean before/after cost comparison (sharpe -2.61→-1.90, cost_drag_pct
128.4%→30.4%). Original run_030 ran at 1h (`data.timeframe: "3600s"`, ~310-370
trades/window); its perp re-run ran at 4h (`"14400s"`, ~96-119 trades/window,
config_sha256 `cb671e80...` matching in both). Because the timeframe changed
alongside the cost, the reported sharpe/cost_drag delta cannot be attributed to
the cost change in isolation — it is confounded by the same silent 1h→4h shift.
run_030 did not degenerate to zero trades (so it didn't visibly trip the "this
looks wrong" alarm the way run_028 did), but its comparison is equally not a
valid isolated measurement of the perp-cost effect.

## Step 2 — Rate-reached-the-engine check

Recomputed directly from `run_030`'s perp re-run `trades.json`
(2024-01 window), per-trade, entry/exit independently:

| trade | side | entry_commission / entry_notional | exit_commission / exit_notional |
|---|---|---|---|
| 1 | LONG | 0.60198521 / (38.51×31.248207) = **0.00050025** | 0.61746456 / (39.52×31.248207) = **0.00050000** |
| 2 | LONG | 0.17113607 / (38.51×8.883433) = **0.00050025** | 0.17833492 / (40.15×8.883433) = **0.00050000** |
| 3 | SHORT | 0.13987899 / (41.94×6.670434) = **0.00050000** | 0.14108351 / (42.28×6.670434) = **0.00050025** |

Implied per-event rate is 0.0005 (5bps) on both legs, both LONG and SHORT — the
new perp rate, not the old 0.001 (10bps) default. (The 0.00050025 vs 0.00050000
split reflects which price — entry or exit — the commission was computed
against, not an error.) `total_commission_percent: 0.1` (%) = 10bps round trip
= 2×5bps, consistent throughout. **CONFIRMED.**

## Step 3 — Conversion + double-charge

From `git show d86f0d0`: `_commission_rate_for_symbol` returns
`float(rate_bps) / 10000.0` — for the perp block, `5.0/10000 = 0.0005`.
Confirmed by direct read of `trading-bot/execution/portfolio_info.py`
(`CommonPortfolioDef.update_local_balance`, lines 85-200): commission is
applied exactly once per event —
`'LONG'` (open, line 115) + `'REDUCE_LONG'`/`'CLOSE'` (close, lines 133/172) = 2
events per LONG round trip;
`'SHORT'` (open, line 150) + `'REDUCE_SHORT'`/`'CLOSE'` (close, lines 158/188)
= 2 events per SHORT round trip. Symmetric, confirmed by code read (not just
citing the commit message), matching Step 2's empirical 2×5bps=10bps
observation. **CONFIRMED — no double- or half-charge.**

`cost_model.yaml`'s diff shows only additive changes: header comment expansion,
`version: "1.1"→"1.2"`, `updated_at` bump, and a new `perp:` block inserted
after `round_trip_cost_bps` and before `EXECUTION STYLE VARIANTS`. No line
within `fee_rate_bps`, `spread_estimate_bps`, `slippage_estimate_bps`,
`round_trip_cost_bps`, or `execution_style` (the spot-facing blocks) was
touched. All pre-existing provenance/rationale comments in those blocks are
byte-identical in the diff (no removed context lines). **CONFIRMED.**

## Step 4 — run_018 non-reproducibility

Checked out a separate detached worktree at `d86f0d0^` (parent, `102fa8e`) and
ran `AdvancedStrategy(config_path=.../run_018/artifacts/candidate_strategy_config.json)`
directly against the parent commit's `strategies/main_strategy.py` (the
`run_018` artifact itself isn't tracked in git — `strategy-research/runs/` is
gitignored — so I pointed the parent-commit code at the real on-disk config
file). Result: identical failure —
`ValueError: invalid strategy_config`, with the same V9 message
(`regime_detector.default_regime: 'trending' is forbidden in mode
'threshold_rules'...`). Confirms this is genuine pre-existing validator/artifact
drift, not introduced by d86f0d0. **CONFIRMED.**

## Step 5 — Suites + hygiene

- `trading-bot/` suite (`pytest -m ""`): **44 passed, 4 errors** — identical to
  the pre-existing 4 `test_regression_backtest.py` errors confirmed in Dispatch
  D's audit of 93f3d87. d86f0d0 touches no file under `trading-bot/`
  (`git show d86f0d0 --stat` confirms only `strategy-research/` files changed),
  so this is expected and unaffected.
- `strategy-research/tests/` suite (`pytest tests/`, no `-m` filter — the
  commit's own `conftest.py` change registers the `slow` marker but does not
  add a default `-m` exclusion, so slow tests run too): **318 passed**, no
  skips, no failures. `git show d86f0d0 --stat` shows only `conftest.py` (marker
  registration, no test functions) and the new
  `test_run_protocol_perp_cost_wiring.py` (8 new test functions: counted
  directly from the diff — `test_default_product_is_spot`,
  `test_perp_product_reads_perp_block`,
  `test_perp_product_falls_back_to_perp_default_not_spot_default`,
  `test_perp_product_none_when_perp_block_absent`,
  `test_perp_product_none_when_no_cost_model`,
  `test_real_cost_model_perp_block_matches_kraken_perp_taker`,
  `test_cli_cost_product_defaults_to_spot`,
  `test_perp_rate_changes_engine_output`) were added; no existing test file was
  modified. 318 (measured) − 8 (new) = 310, exactly matching the claimed
  pre-arc baseline, without needing to independently re-run the suite at the
  parent commit. No pre-existing test was removed or skipped to get green.
  **CONFIRMED.**
- `git show d86f0d0 --name-only` contains **zero** matches for `trades.json` or
  any `runs/` path (grep exit 1). **CONFIRMED not committed.**
- `git check-ignore -v strategy-research/runs/run_028/perp_recalibration_20260720/protocol_summary.json`
  → matched by `.gitignore:36:runs/`. Checked history of that rule
  (`git log --follow -- .gitignore`) — it traces back to `ac27791`
  ("Restructure repository, add strategy-research framework..."), long before
  this commit, and `git show d86f0d0` touches no line of `.gitignore`. The
  "gitignored project-wide for every prior run" description is accurate, not a
  post-hoc rationalization. **CONFIRMED.**

## Hygiene note

Running the audit's own test suites (both `pytest` invocations) left
`trading-bot/results/trades.json` modified in the working tree, exactly as
Dispatch D previously found and flagged as a pre-existing hardcoded-path side
effect of the engine (unrelated to this commit). Reverted via
`git checkout -- trading-bot/results/trades.json` to restore the precondition
tree state before filing this report.

## Verdict

| Step | Result |
|---|---|
| 1 (run_028) | **DISCREPANCY** — confirmed reproduction mismatch (1h original vs 4h re-run), not attributable to cost |
| 1 (run_030, extended) | **DISCREPANCY** — same mismatch confirmed present; its reported sharpe/cost_drag delta is equally confounded, not a clean cost-effect measurement |
| 2 (rate reached engine) | CONFIRMED |
| 3 (conversion / double-charge) | CONFIRMED |
| 4 (run_018 non-reproducibility) | CONFIRMED (genuine, pre-existing) |
| 5 (suites + hygiene) | CONFIRMED |

The code changes in d86f0d0 (the `--cost-product` flag, `_commission_rate_for_symbol`,
the additive `perp` cost_model.yaml block, and the new unit/integration tests)
are themselves sound — correctly converted, correctly non-double-charging, additive
and non-destructive to the spot block, properly gitignore-consistent, with
genuinely green test suites. But the two numeric research outputs this commit
exists to produce — the recalibrated run_028 and run_030 verdicts — are both
built on a re-run that silently changed the candle interval alongside the cost
rate, for a reason unrelated to and undisclosed by this commit (a timeframe-threading
gap that predates it). Neither number isolates the effect of the perp cost
change as claimed.

**AUDIT FAIL** — blocking issue: run_028's and run_030's perp-recalibration
numbers are both confounded by an undisclosed 1h→4h candle-interval change
between the original runs and the re-runs, and neither is ratifiable as a
measurement of the cost change's effect. The wiring code itself (Steps 2-3) and
run_018's deferral (Step 4) are sound and would pass in isolation; the
re-run's numeric outputs are not.
