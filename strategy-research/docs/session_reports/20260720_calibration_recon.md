# Dispatch E (revised) — Calibration injection-path + fee-keying recon

**Role:** Read-only recon. All claims below re-derived from code and on-disk
artifacts, not from prior session reports.

## Precondition manifest

- `git log --oneline -1` → `93f3d87` — MATCH.
- `git status --porcelain` → only the untracked session-report `.md` files — MATCH.
- Proceeded.

## Step 1 — Injection path + default-shadow check (blocking)

`strategy-research/tools/run_protocol.py` calls `run_backtest()` directly (no
intermediate layer), at **exactly two call sites**:

- `run_protocol.py:984-986` (holdout mode)
- `run_protocol.py:1046-1048` (normal walk-forward mode)

Neither call site passes a `commission_rate` keyword argument:

```
rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT,
                  runs_root=_runs_root, interval_seconds=interval_seconds,
                  warmup_prefetch=True)                                    # :984
...
rd = run_backtest(args.config_path, symbol, start, end, _RESULTS_ROOT,
                  runs_root=_runs_root, interval_seconds=interval_seconds,
                  warmup_prefetch=True, holdout_start=_holdout_start)      # :1046
```

`run_protocol.py:965` does call `cost_model = _load_cost_model()` early, and that
dict is threaded into `_compute_trade_records_for_window(..., cost_model)` →
`_cost_paid_bps(trade, cost_model)` (`run_protocol.py:233-245`). But this function
runs **after** the backtest already completed, reading `trade.get("symbol")` and
looking up `cost_model["fee_rate_bps"][symbol]` purely to compute a diagnostic bps
label attached to each trade record. It never feeds back into `run_backtest()` or
anything upstream of it. I confirmed this by grepping every `cost_model` reference
in the file (7 total) — none are on a path that reaches the `run_backtest()` calls
at 984 or 1046.

Downstream, `_build_mock_stack()` (`core/launcher.py:135-176`, verified in Dispatch
D) does thread `params.commission_rate` correctly into both
`EnhancedPerformanceTracker` and `MockPortfolioInfo` — so *if* a rate reached
`run_backtest()`, it would survive to every fee-application site without dropping
at `portfolio_info.py:86/293/324` or the dead `backtester.py:43` literal (confirmed
dead in Dispatch D: `self.commission_rate` in `BacktestEngine` is assigned once,
never read).

**Verdict: NO — a caller-supplied rate does not survive end-to-end on the re-run
path, because no caller-supplied rate is ever offered.** `run_protocol.py` never
passes `commission_rate` to either call site, so both always resolve to
`DEFAULT_COMMISSION_RATE` at **`core/launcher.py:522-524`**
(`resolved_commission_rate = commission_rate if commission_rate is not None else
DEFAULT_COMMISSION_RATE`, with `commission_rate` always `None` from
`run_protocol.py`'s perspective). The drop happens before the chain even starts —
at the call site, not partway down it. `cost_model.yaml`'s `fee_rate_bps` currently
has **zero effect on any simulated fill, matched_quantity, fees_paid, sharpe, or
net_pnl** — it only decorates already-computed (default-rate) trades with a
hypothetical bps figure after the fact. A "calibration re-run" through
`run_protocol.py` today is fiction: it would silently re-run at Binance's 0.1%
regardless of what cost_model.yaml or any operator intent specifies.

## Step 2 — Fee-keying

`strategy-research/config/cost_model.yaml`'s `fee_rate_bps` (and every parallel
block: `spread_estimate_bps`, `slippage_estimate_bps`, `round_trip_cost_bps`,
`execution_style.{taker,maker}.*`) is keyed **only by symbol** (`BTCUSDT`,
`ETHUSDT`, `SOLUSDT`, `AVAXUSDT`, `BNBUSDT`, `default`). There is no product
dimension anywhere in the schema — no spot/perp key at any level. The file's own
header states it models "Binance spot, Regular/VIP0 tier" exclusively.

Both consumers read it the same way: `run_protocol.py._cost_paid_bps()`
(`cost_model.get("fee_rate_bps", {})`, keyed by `trade["symbol"]`) and
`prescreen_signal.py._round_trip_cost(symbol, cost_model)`
(`cost_model.get("round_trip_cost_bps", {})`, same keying). Neither reads a
product field because none exists to read. **It can express only one fee per
symbol, not per product.**

Product determination for the three targets — not from a "product" field (none
exists in the KB), but from the execution layer itself: I grepped
`trading-bot/execution/execution_handler.py` and `trading-bot/execution/
portfolio_info.py` for any futures/perp order path — zero matches. Both use the
standard spot `binance.client.Client` (`get_account()`, spot `create_order`
equivalents). The only futures-aware code in the repo is
`trading-bot/data/fetchers/funding_rate_fetcher.py`, which pulls Binance
perpetual-futures funding rates via CCXT purely as an **exogenous predictive
feed** — it has no execution counterpart. Conclusion: **every target this bot can
backtest or trade executes spot**, full stop, regardless of what signal it reads.

| Target | Evidence run(s) | Product (from execution-layer capability) | Correct Kraken fee |
|---|---|---|---|
| FUNDING_MR_DAILY_RETEST | run_059 | Spot BTCUSDT/ETHUSDT — funding rate is only a predictive *signal* (fetched via `funding_rate_fetcher.py`'s separate CCXT perp feed); the bot has no perp execution path to actually trade the instrument the signal is drawn from | **Kraken spot taker: 0.80%** (80 bps) |
| rsi_momentum_trending_cost_drag | run_018 | Spot (generic RSI/regime strategy, same spot-only execution stack) | **Kraken spot taker: 0.80%** (80 bps) |
| keltner_scoremode_no_edge | run_028, run_030 | Spot (same) | **Kraken spot taker: 0.80%** (80 bps) |

Source: `docs/venue_survey_20260719.md:34` — "Official page: 0.40% / 0.80% at
Level 1" (maker/taker), flagged in that same doc as conflicting with an
unresolved secondary source citing 0.25%/0.40% ("use the official page ... and
re-verify at implementation time" — not resolved as of this recon). Kraken's
**perpetual-futures** taker fee (0.0500% / 5 bps at the $0 tier, same doc) is
**not applicable to any of the three targets**, despite FUNDING_MR_DAILY_RETEST's
signal being funding-rate-derived — a naive reading of that hypothesis's mechanism
could lead someone to apply the 5bps perp rate instead of the 80bps spot rate,
understating its real cost by ~16x. This is a real trap worth flagging explicitly
to whoever calibrates it next.

## Step 3 — Re-run inputs

All four evidence runs have both required artifacts still on disk and valid:

| Run | `candidate_strategy_config.json` | Protocol file (from `protocol_result.yaml:protocol_file`) | Exists? |
|---|---|---|---|
| run_018 | `strategy-research/runs/run_018/artifacts/candidate_strategy_config.json` (valid JSON, 2055 bytes) | `strategy-research/protocols/baseline_v1.json` | Yes |
| run_028 | `strategy-research/runs/run_028/artifacts/candidate_strategy_config.json` (valid JSON, 1672 bytes) | `strategy-research/protocols/escalation_solusdt_4h.json` | Yes |
| run_030 | `strategy-research/runs/run_030/artifacts/candidate_strategy_config.json` (valid JSON, 2493 bytes) | `strategy-research/protocols/escalation_avaxusdt_4h.json` | Yes |
| run_059 | `strategy-research/runs/run_059/artifacts/candidate_strategy_config.json` (valid JSON, 855 bytes) | `strategy-research/protocols/funding_mr_daily_retest_v1.json` | Yes |

(Note: my first pass at locating protocol files filtered by run-number substring
in the filename and missed `baseline_v1.json`/`escalation_*` — the correct
protocol filenames were pulled directly from each run's own
`protocol_result.yaml:protocol_file` field, not guessed.)

**No target drops from the set.** All three (FUNDING_MR_DAILY_RETEST/run_059,
rsi_momentum_trending_cost_drag/run_018, keltner_scoremode_no_edge/run_028+030)
have both their protocol spec and strategy config present and parseable as-is.

## Step 4 — Recommendation

The minimal honest path is **(a) only — thread `commission_rate` through
`run_protocol.py`'s two `run_backtest()` call sites (:984, :1046), sourced from
`cost_model.yaml`'s existing symbol-keyed `fee_rate_bps`** — the dict is already
loaded at `run_protocol.py:965` and just needs `* 0.0001` conversion (bps → rate)
passed as the new keyword argument at both sites, using the same
`commission_rate: float = None` parameter Dispatch D already confirmed is
byte-identical-safe when omitted and correctly threads to every fee site when
set. Product-keying `(b)` is unnecessary and would model a capability the bot
doesn't have: since every target trades spot regardless of signal source, a
spot/perp split in `cost_model.yaml` has nothing on the execution side to key
against — building it now would be speculative schema growth for a future perp
trading path that doesn't exist yet. **(c)** is therefore not needed either.
One catch not solved by wiring alone: `cost_model.yaml` is currently
Binance-calibrated (7.5 bps), not Kraken's 80 bps — plumbing the parameter
through is necessary but not sufficient for a genuine Kraken-calibrated re-run;
either `cost_model.yaml` needs a Kraken-specific value/override or the re-run
needs an explicit CLI override flag on `run_protocol.py`, itself a small,
non-structural addition. None of this is structural: it's threading one
already-audited, already-safe parameter (Dispatch D) through two already-located
call sites, reading a dict that's already in scope. **Sonnet-level minimal
change is appropriate; does not warrant Opus.** Given this plumbing feeds
directly into pass/fail calibration numbers for strategy promotion, a Dispatch-D-style
read-only follow-up audit after implementation is proportionate — but that's a
process precaution, not a signal that the change itself is architecturally
complex.
