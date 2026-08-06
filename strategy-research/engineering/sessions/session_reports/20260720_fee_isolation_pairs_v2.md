# Phase 1.2 / Dispatch L — Controlled fee-isolation pairs, executed

Date: 2026-07-20
Precondition check: PASSED — HEAD=6cde7ae, `git status --porcelain` showed only
untracked `strategy-research/docs/session_reports/*.md` reports.

## Step 1-3 — the flag, tests, commit

Added `--commission-bps <float>` to `strategy-research/tools/run_protocol.py`: a
new `_resolve_commission_rate(symbol, cost_model, commission_bps, product)` helper
that returns `commission_bps/10000` when set (takes precedence over
`--cost-product`), else falls through unchanged to the pre-existing
`_commission_rate_for_symbol(..., product=product)`. One log line emitted only
when the override is active. No file besides `run_protocol.py` and its test file
was touched; the engine (`trading-bot/`) was not edited.

Added `tests/test_run_protocol_commission_bps_flag.py` (10 tests: resolver
precedence/fallback, CLI parsing, an end-to-end no-flag run, and two real engine
runs at `--commission-bps 10`/`5` whose actual `trades.json` records were
independently recomputed to `commission/notional ≈ 0.001`/`0.0005`).

- `strategy-research/` suite: **328 passed** (318 + 10 new), 0 failures.
- `trading-bot/` suite: **44 passed**, same 4 pre-existing unrelated
  `test_regression_backtest.py` errors, unchanged.

Committed flag + test only: **`e3bcbb0`** (`git show --stat` confirms exactly
`strategy-research/tools/run_protocol.py` and
`strategy-research/tests/test_run_protocol_commission_bps_flag.py`, 220 insertions,
4 deletions). Read-back verified before running any pairs, so the pairs below cite
this clean commit as their code provenance.

## Step 4 — pairs executed

Four runs, `--out-dir` under each source run's own directory for clear attribution
(not committed — `strategy-research/runs/` is gitignored, same policy as every
prior run this campaign):

| Pair | Protocol | Leg | Command | Out-dir |
|---|---|---|---|---|
| run_028 | `protocols/escalation_solusdt_4h.json` | A (10bps) | `--commission-bps 10` | `runs/run_028/fee_isolation_pairs_20260720/legA_10bps` |
| run_028 | same | B (5bps) | `--commission-bps 5` | `runs/run_028/fee_isolation_pairs_20260720/legB_5bps` |
| run_030 | `protocols/escalation_avaxusdt_4h.json` | A (10bps) | `--commission-bps 10` | `runs/run_030/fee_isolation_pairs_20260720/legA_10bps` |
| run_030 | same | B (5bps) | `--commission-bps 5` | `runs/run_030/fee_isolation_pairs_20260720/legB_5bps` |

Config: `runs/run_028/artifacts/candidate_strategy_config.json` /
`runs/run_030/artifacts/candidate_strategy_config.json` (unchanged from Dispatch H,
identical within each pair by construction — both legs of a pair use the exact
same command except for `--commission-bps`).

## Step 5 — pair integrity: CONFIRMED for both pairs

| Check | run_028 legA vs legB | run_030 legA vs legB |
|---|---|---|
| `config_sha256` | `67a51ac2...` both | `cb671e80...` both — **match** |
| window set (11 windows) | identical list, both | identical list, both — **match** |
| `manifest.json` timeframe | `14400s` both | `14400s` both — **match** (this is the exact defect Dispatch K/the audit found broken in the old comparison; now controlled) |
| bar_count (2024-01 window) | 402 both | 402 both — **match** |
| trade-derived rate | **N/A — 0 trades in both legs** (see below) | legA: `entry/exit_commission / notional` = 0.001/0.001001 per trade (10bps); legB: 0.0005/0.0005 per trade (5bps) — **matches expected rate exactly, both LONG and SHORT** |

No mismatch on anything but commission in either pair — both pairs are valid.
run_028's trade-rate check is structurally vacuous (nothing to divide by zero
trades), not a failure; noted rather than glossed over.

## Step 6 — within-pair deltas

**run_028 (SOLUSDT):**

| | leg A (10bps) | leg B (5bps) |
|---|---|---|
| median_sharpe | null (all 11 windows sparse) | null (all 11 windows sparse) |
| max_abs_drawdown_pct | 0.0% | 0.0% |
| min_trade_count | 0 | 0 |
| total trades (all windows) | 0 | 0 |
| median_cost_drag_pct | undefined (no trades) | undefined (no trades) |
| verdict | refine | refine |

**Claim supported:** on `escalation_solusdt_4h.json` at the current engine, this
strategy generates **zero trades at 4h resolution regardless of fee level in the
5-10bps range** — the earlier (Dispatch H) report of "0 trades under perp cost"
was not a fee effect; it's simply what this config does at 4h, at any fee tested.
**No verdict flip** (trivially — both refine).

**run_030 (AVAXUSDT):**

| | leg A (10bps) | leg B (5bps) | Δ |
|---|---|---|---|
| median_sharpe | -2.735 | -1.900 | +0.835 |
| max_abs_drawdown_pct | 51.533% | 49.62% | -1.91pp |
| min_trade_count | 96 | 96 | **0 — identical** |
| total trades (all windows) | 1178 | 1178 | **0 — identical** |
| median_cost_drag_pct | 62.6513% | 30.386% | -32.27pp (≈halved) |
| verdict | kill | kill | — |

**Claim supported:** on `escalation_avaxusdt_4h.json` at the current engine,
halving the fee from 10→5 bps roughly halves `cost_drag_pct` (62.65%→30.39%,
consistent with cost_drag scaling near-linearly with the fee term) and improves
`median_sharpe` by +0.835 (-2.735→-1.900), but **does not flip the verdict** —
still `kill` (median_sharpe remains below the -1 threshold). **Trade count is
exactly unchanged (1178 both legs)** — with timeframe genuinely controlled, this
strategy's trade path is insensitive to fee level in this range; the earlier
(confounded) Dispatch H report's apparent trade-count sensitivity (310→96) is now
attributable entirely to the 1h→4h interval change Dispatch J's audit found, not
to the fee change.

**Historical footnote only** (not a comparison baseline, per this dispatch's
instruction): the original 1h-executed `run_028`/`run_030` (10bps, pre-threading)
recorded `run_028`: 3 total trades / median_sharpe 0.0 / cost_drag 84.29%;
`run_030`: median_sharpe -2.61 / cost_drag 128.44% / ~310-370 trades per window.
These numbers reflect a different candle resolution (1h) than either leg above
(4h) and are not comparable to the deltas in this report.

## Confirmation

Neither verdict flips in either pair. FUNDING_MR_DAILY_RETEST was not touched. No
engine code was edited this dispatch — only `run_protocol.py`'s CLI/resolver layer
and its test file (committed separately and before the pairs, per instruction).
`git status --porcelain` after the pairs shows no change beyond this report (the
four new run directories are gitignored, matching every prior run in this
campaign).
