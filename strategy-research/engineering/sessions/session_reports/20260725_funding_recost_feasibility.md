# Funding Re-Cost Feasibility Recon — FUNDING_MR_DAILY_RETEST (read-only)

Date: 2026-07-25. Scope: what stands between the ratified off-by-default funding-accrual
mechanism (b542bb2) and a properly-gated re-cost adjudication of the
FUNDING_MR_DAILY_RETEST family. No run, no code change, no verdict, no registration.
This file is the only write performed by this dispatch.

Provenance convention: every factual claim below cites either the command that produced
it or a `file:line`. Line numbers are as-of HEAD b542bb2.

---

## MANIFEST

`git log --oneline -1` →
```
b542bb2 additive off-by-default funding-accrual mechanism per the 2026-07-24 design spec; flag off = byte-identical prior behavior; no protocol registered and no re-cost run yet.
```
`git status --porcelain` → (empty output)

Both MATCH the stated precondition. Proceeded.

---

## STEP 2 — VENUE / FEED PROVENANCE

### What the mechanism would actually load

`trading-bot/data/feed_registry.py:60` —
`path = os.path.join(data_dir, f"{symbol}_funding_8h.csv")`.
Filename pattern: `{symbol}_funding_8h.csv`; directory: whatever `data_dir` the caller
passes. **No production caller exists** (see Step 5 / gap G2), so `data_dir` is not
resolved anywhere outside `trading-bot/tests/test_funding_accrual.py`. The only on-disk
set matching that pattern is `trading-bot/local_data/`.

Semantics: `f_daily[day] = SUM of that day's settlements`, days with no settlement absent
from the dict, no imputation for partial days (`feed_registry.py:36-39`, `:63-71`).

### Inventory A — `trading-bot/local_data/*_funding_8h.csv`

`ls trading-bot/local_data/` → 4 files: `BTCUSDT_`, `ETHUSDT_`, `SOLUSDT_`,
`AVAXUSDT_funding_8h.csv`.

- Naming: `{SYMBOL}_funding_8h.csv`. Symbol convention: Binance USDT-quoted perp
  (`BTCUSDT`), no venue prefix.
- Schema (`head -2 trading-bot/local_data/BTCUSDT_funding_8h.csv`):
  `timestamp,funding_rate,mark_price` / `2019-09-10 08:00:00.000,0.0001,`
  (`mark_price` empty throughout the sampled rows).
- Venue, determinable from the fetcher: `FundingRateFetcher.__init__` defaults
  `exchange_id: str = "binance"` (`trading-bot/data/fetchers/funding_rate_fetcher.py:69`),
  with `options {"defaultType": "future"}` (`:92`) and
  `cache_key → f"{symbol}_funding_8h"` (`:106-108`). Cadence constant
  `_FUNDING_INTERVAL_SECONDS = 8 * 3600` (`:48`), docstring "published every 8 hours on
  Binance (00:00, 08:00, 16:00 UTC)" (`:7`).
  **Venue = Binance perpetual futures, 8h settlement.**
- Corroborated by `strategy-research/config/campaign_data_policy.yaml:26-27`:
  "funding_rate BTCUSDT : 2019-09-10 -> present (Binance perp inception)".

### Inventory B — `trading-bot/local_data/Kraken_funding_rates/`

`ls trading-bot/local_data/Kraken_funding_rates/` → `__MACOSX`, `exports` only.
`ls .../exports/ | wc -l` → **480 files**.

- Naming: `PF_<BASE>USD.csv`, plus `PI_` and `PV_` prefixed variants
  (e.g. `PF_XBTUSD.csv`, `PI_XBTUSD.csv`, `PV_XRPXBT.csv`). Symbol convention is
  Kraken-futures tradeable IDs: **`XBT` not `BTC`, USD not USDT**. There is no
  `PF_BTCUSD.csv` (`head PF_BTCUSD.csv` → "No such file or directory").
- Schema (`head -3 .../PF_XBTUSD.csv`):
  `timestamp,tradeable,absolute_rate,relative_rate` /
  `2022-03-22 16:00:00,PF_XBTUSD,0.858943191939791995,0.000020164637711864`.
- Cadence, measured (pandas `timestamp.diff().value_counts()` on `PF_XBTUSD.csv`):
  **29,279 × 1h gaps**, 1,145 × 4h, 5 × 2h, 1 × 3h. Predominantly **1-hourly** — matching
  the EEA 1h funding interval recorded at
  `strategy-research/config/cost_model.yaml:148-149`.
- Coverage: first `2022-03-22 16:00:00`, last `2026-02-01 00:00:00`, 30,431 data rows
  (same for `PF_ETHUSD.csv`).
- Venue provenance: **no provenance record on disk.** The directory contains only
  `__MACOSX` and `exports` — no README, manifest, or fetch log. No fetcher in
  `trading-bot/data/fetchers/` (`base_fetcher.py`, `ccxt_fetcher.py`,
  `fear_greed_fetcher.py`, `funding_rate_fetcher.py`) emits this column schema. Venue is
  inferable only from the `tradeable` column values (`PF_XBTUSD` = Kraken Futures
  multi-collateral perp naming) and the directory name.

**`build_daily_funding_series` cannot read Inventory B at all** — four independent
mismatches: filename pattern (`PF_XBTUSD.csv` vs required `{symbol}_funding_8h.csv`),
symbol convention (`XBT`/USD vs `BTCUSDT`), column name (`relative_rate` vs the required
`funding_rate`, `feed_registry.py:63`), and cadence semantics (1h vs 8h).

### VENUE ANSWER — explicit

**NO. The series the mechanism would load does NOT originate from the venue this family
is declared and costed at.** There is a three-way divergence:

| Item | Venue | Citation |
|---|---|---|
| Series the mechanism loads | Binance perp, 8h | `feed_registry.py:60`, `funding_rate_fetcher.py:69,:48` |
| Family's declared go-forward execution venue | Kraken perpetual futures, 1h funding | `campaign_knowledge_base.yaml`, `funding_mr_daily_retest_killed` → `venue_live_tradability` ("perp is ... the campaign's go-forward product for this family, not spot") |
| Family's actual costing basis in run_059 | Binance **spot** taker, 17.0/17.5 bps | `cost_model.yaml:71-77`, `:103-109`; `run_protocol.py:990` (`--cost-product` default `"spot"`); KB root cause "assumed round-trip costs (17.0-17.5 bps)" |

The tree already declares this gap open rather than closed:
- `cost_model.yaml:183` — `venue_note: in_sample_proxy_binance_8h_live_venue_kraken_perp_1h`,
  and `:181-182` "Binance-vs-Kraken funding basis is an open calibration question
  (design §6 Q1)".
- `cost_model.yaml:152-157` — the perp fee block **explicitly EXCLUDES**
  FUNDING_MR_DAILY_RETEST from being costed with it.
- `cost_model.yaml:173` — `modeled: false`.

**What closing it would require (NOT closed here, no action taken):** either (a) an
operator ruling that the Binance-8h series is admissible as a proxy for a *gating* verdict
on a Kraken-perp-declared family, recorded in the re-cost's own registration; or (b) a
Kraken-native path — symbol map (`PF_XBTUSD` ↔ `BTCUSDT`), column map
(`relative_rate` → `funding_rate`), 1h→daily aggregation, a provenance record for the
export archive, and a resolution of the fee-basis conflict (the perp block is currently
forbidden for this family and the spot block is the wrong product). Option (b) additionally
cannot reach the pass-gated window: the Kraken exports start 2022-03-22, the window starts
2019-12-01.

---

## STEP 3 — COVERAGE vs PROTOCOL WINDOW

### Declared

`strategy-research/protocols/funding_mr_daily_retest_v1.json`:
- symbols `["BTCUSDT","ETHUSDT"]` (`:2-5`); timeframe `"1d"` (`:6`).
- 49 monthly windows, labels `2019-12` … `2023-12`, spanning `2019-12-01` →
  `2024-01-01` exclusive (`:7-351`).
- holdout `2026-01-01` → `2026-06-30` (`:352-355`).

`strategy-research/briefs/FUNDING_MR_DAILY_RETEST.md`: pass-gated window
`["2019-12-01","2023-12-31"]`, `n_windows: 49` (`:153-160`); 2024-01-01→2025-12-31 is
diagnostic-only and never gates (`:161-178`); holdout untouched (`:189-195`).

### Actual coverage of the required files

Measured this recon (pandas over `trading-bot/local_data/{SYMBOL}_funding_8h.csv`,
read-only):

| File | first | last | data rows |
|---|---|---|---|
| `BTCUSDT_funding_8h.csv` | 2019-09-10 08:00:00 | 2026-07-05 08:00:00 | 7,468 |
| `ETHUSDT_funding_8h.csv` | 2019-11-27 08:00:00 | 2026-07-05 08:00:00 | 7,234 |

Day-level coverage inside the pass-gated window (2019-12-01 … 2023-12-31, 1,492 calendar
days):

| Symbol | settlements | days expected | days present | **days missing** |
|---|---|---|---|---|
| BTCUSDT | 4,474 | 1,492 | 1,492 | **0** |
| ETHUSDT | 4,474 | 1,492 | 1,492 | **0** |

Holdout window (2026-01-01 … 2026-06-30, 181 days): 542 settlements, 181/181 days present,
both symbols. (Reported as a coverage fact only — see Step 6(d) for the freeze.)

**Gap in days: zero, for both symbols, over the full protocol window.** Partial days
(<3 settlements): BTCUSDT `2022-06-06` (2), `2023-05-06` (2); ETHUSDT `2020-10-25` (2),
`2022-08-23` (2). Holdout partial day: `2026-01-27` (2), both symbols.

### Would a gap silently produce zero accrual?

**Yes — silently, with no error, at three distinct sites:**
1. `feed_registry.py:61-62` — a missing CSV is skipped by `continue`; the symbol is simply
   absent from the returned dict.
2. `trading-bot/core/trading_bot.py:151-156` (`_funding_rate_for_bar`) — returns `None`
   when there is no series for the symbol or no settlement dated to that day.
3. `trading-bot/core/trading_bot.py:204` — `if f_bar is not None:` guards the
   `apply_funding` call; a `None` skips the accrual entirely. No log line, no warning, no
   raise.

A partial day additionally sums only the settlements that exist ("no imputation of a
missing settlement", `feed_registry.py:37-39`), understating that day's accrual silently.

Consequence: **flag-on with a wrong `data_dir`, a wrong symbol convention, or an absent
CSV is behaviorally indistinguishable from flag-off.** Not triggered by the Binance series
on this protocol (0 missing days, measured above), but entirely unguarded. See gap G6.

---

## STEP 4 — REPLAYABILITY OF THE ARCHIVED RUN

### The prior report

`strategy-research/docs/session_reports/20260720_run059_replay_feasibility.md`, baselined
at `HEAD=618d548` (`:4`). Its subject is a Kraken **fee** re-calibration. Its conclusion
(`:76-88`): a standalone post-hoc replay over `trades.json` is **not** sufficient, because
`matched_quantity` at every trade is sized off a portfolio value that already embeds the
prior commission's cumulative effect — multiplicative path-dependence, not a separable fee
total. Its remediation was to thread a `commission_rate` argument through `run_backtest`.

### Verified against the current tree

**Its core conclusion holds a fortiori for a funding re-cost, and for the same reason.**
`apply_funding` mutates `USDT.free` directly (`portfolio_info.py:245`); that balance feeds
`_calculate_total_portfolio_value` (`portfolio_info.py:253+`, called at
`trading_bot.py:207`), which sizes every subsequent order. Funding is therefore path-
dependent identically to commission — no post-hoc arithmetic pass over `trades.json` can
produce it.

**One element of the prior report is stale in the favorable direction:** its recommended
remediation has since shipped — `run_backtest(..., commission_rate: float = None, ...)`
(`trading-bot/core/launcher.py:481-484`), plus `--cost-product` (`run_protocol.py:990`) and
`--commission-bps` (`:999`). The fee-parameterization blocker it described is closed. It
says nothing about funding, and nothing it says about run_059's config or timeframe is
contradicted by the tree.

### C12 — inert protocol-declared timeframe: **DOES NOT APPLY to run_059**

Current tree threads it: `run_protocol.py:1029-1030` —
`protocol_timeframe = protocol.get("timeframe", "1h")`;
`interval_seconds = parse_interval_seconds(protocol_timeframe) if protocol_timeframe != "1h" else None`
— passed at `:1071` (holdout path) and `:1135` (window path). The protocol declares
`"timeframe": "1d"` (`funding_mr_daily_retest_v1.json:6`).

Confirmed empirically from run_059's own recorded output
(`strategy-research/runs/run_059/protocol_summary.json`): the `2019-12` BTCUSDT window
reports `per_regime.unknown.bar_count: 30` — a 31-day month executed at ~30 bars is daily,
not 1h (~744) — and `core.sharpe_annualization: "sqrt(365) for daily Sharpe (crypto, 365
days/year)"`. **The declared timeframe threaded through; run_059 is not a C12 instance.**

### C13 — archived config failing current V9 validation: **DOES NOT APPLY to run_059**

`strategy-research/runs/run_059/artifacts/candidate_strategy_config.json` has
`regime_detector.default_regime: "unknown"`, `components: []`, `rules: []` — the canonical
fully-ungated pattern. The V9 check requires `rules_nonempty` **and**
`default_regime in ("trending","mean_reversion","chop")`
(`trading-bot/tools/validate_config.py:217-221`); the fully-ungated case is explicitly
exempted (`:205-214`). C13's failure mode (`default_regime: 'trending'` in run_018) is
absent.

Static rule-by-rule check against every rule in `validate_config.py`
(sites from `grep -n "VIOLATION V"`): **V1** both top-level keys present, regime values are
object-or-null; **V2** vacuous (no vetoes, no rules, no detector components); **V3** op
`"identity"` is in `TRANSFORM_OPS_REGISTRY` (`trading-bot/strategies/registry.py:52`);
**V4/V5** single history op, no scalar/history ordering conflict; **V6** no-op — the config
declares no `lookback` key and the check returns early when absent (`:139-141`); **V7** all
four regime names and `default_regime: "unknown"` are valid; **V8** component weight 1.0,
regime total 1.0 > 0; **V9** exempt (above); **V10** `strategies.regimes.unknown` is
non-null. The component dotted path
`strategies.strategy_components.FundingRateMeanReversionComponent` resolves
(`trading-bot/strategies/strategy_components.py:675`).

**Provenance honesty:** this is a static read of the validator's rules against the archived
config. `validate_config.py` was **not executed** (read-only recon), so this is not an
execution result.

### Verdict for Step 4

By static inspection run_059's config is executable by today's engine as-is, and the
protocol-declared `1d` timeframe does thread through today. No disagreement between the
prior report and the current tree was found; the only drift is the closed fee-
parameterization remediation noted above.

---

## STEP 5 — ENABLEMENT PATH

### Launch paths that reach this family

1. `strategy-research/workflow/run_campaign.py` → `workflow/stages.yaml:88-89`
   (`protocol_execution`, `tool: tools/run_protocol.py`) → `run_protocol.py:1070` / `:1134`
   → `core/launcher.run_backtest` → `BacktestEngine(...)` at `launcher.py:578-594`.
2. `tools/run_protocol.py` invoked directly — same downstream.
3. `core/launcher.py` interactive CLI `BacktestEngine` sites (`:267`, `:325`, `:428`) —
   generic/parameter-sweep paths, not this family's pinned-protocol route.
4. `trading-bot/main.py simulate` → `Launcher` (`main.py:6`, `:38`) — hardcoded dates, not
   protocol-driven.
5. `core/launcher.py:215` `TradingBot(...)` — the LIVE path, not a backtest.

### Can any of them set both opt-ins? **NO.**

`grep -rn "model_funding|funding_daily|apply_funding"` across the repo returns assignments
at exactly two places: the defaults `self.model_funding = False` /
`self.funding_daily = None` (`trading_bot.py:86-87`), and
`trading-bot/tests/test_funding_accrual.py:277-278`, `:333-334`. **No launcher, runner,
orchestrator, config file, or CLI flag sets either.**

- `run_backtest`'s full signature (`launcher.py:481-484`) is
  `(config_path, symbol, start, end, results_root, runs_root, interval_seconds,
  warmup_prefetch, holdout_start, commission_rate, trades_log_file)` — no funding
  parameter. The `BacktestEngine(...)` construction at `launcher.py:578-594` passes no
  funding argument.
- `run_protocol.py`'s argparse (`:982-999`) exposes `config_path`, `protocol_path`,
  `--holdout`, `--i-understand`, `--validation-protocol`, `--out-dir`, `--cost-product`,
  `--commission-bps` — no funding flag.
- `build_daily_funding_series` has **zero production call sites**: defined at
  `feed_registry.py:30`, absent from `FEED_REGISTRY` (`:20-27`) — so
  `engine.load_data(..., extra_feeds=FEED_REGISTRY)` (`launcher.py:596`) never builds it —
  and called only from `tests/test_funding_accrual.py:28,126,141,155`.

**The blocker is wiring, not math.** For the record only (analysis, not authorship), the
settings would have to occur at: `launcher.py:481-484` (signature),
`launcher.py:578-594` (two attribute assignments on the constructed engine) and the
`:596` area (series build, needs a `data_dir`), plus `run_protocol.py:982-999` (flag) and
`:1070-1073` / `:1134-1137` (pass-through).

### Mock or live path — does the accrual land?

**Mock. The accrual would land in the valuation.**
`run_backtest` builds its stack via `launcher._build_mock_stack(...)` (`launcher.py:552`),
which constructs `MockPortfolioInfo` (`launcher.py:163`). `MockPortfolioInfo`
(`portfolio_info.py:366-392`) defines only `__init__` and inherits
`CommonPortfolioDef.get_account_balance` (`:330-331`), whose body is
`return self.local_balance` — **by reference**. The hook captures `balances` at
`trading_bot.py:193`, calls `apply_funding` at `:205` (which mutates
`self.local_balance['USDT']['free']`, `portfolio_info.py:245`), then values that same
object at `:207`. The mutation is visible to `_calculate_total_portfolio_value` and to the
recorded bar-level `total_portfolio_value` series.

The live `PortfolioInfo.get_account_balance` (`:352-364`) builds a **fresh** dict from
`client.get_account()` and never reads `local_balance`, so on the live path the mutation
would not reach the valuation. The re-cost does not traverse that path (it is
`launcher.py:215`'s `TradingBot`). Flagged as latent, not ordered fixed — gap G9.

### Flag-off vs flag-on comparison end-to-end

**Not reachable today by any existing entry point**, for the same reason: no launcher can
set `model_funding`. The only flag-off/flag-on equivalence evidence in the tree is
`tests/test_funding_accrual.py:266-320` (`_run_two_flat_bars`), a two-bar in-process stub
driving `TradingBot` directly — it produces no run directory, no `metrics.json`, no
`protocol_summary.json`, and therefore nothing a pass rule could be evaluated against.

---

## STEP 6 — WHAT A PRE-REGISTERED PASS RULE WOULD NEED

*(Analysis only. No pass_rule authored, no protocol registered.)*

### (a) Existing terminal outcome and the basis it was killed on

`strategy-research/campaign_knowledge_base.yaml`, entry `funding_mr_daily_retest_killed`
(`hypothesis_id: FUNDING_MR_DAILY_RETEST`, `evidence_runs: [run_059]`):
`outcome: completed_rejected`, `verdict_status: gated`, `exhausted: true`,
`reactivation_condition: null`.

Basis — the B11 total mapping's FAIL-a branch, from
`runs/run_059/artifacts/pass_rule_evaluation.yaml` (evaluated 2026-07-18T16:01:02Z):
- (a) median_sharpe > 0.8 → BTCUSDT **−0.296**, ETHUSDT **−0.979** → FAIL
- (b) max_abs_drawdown_pct < 30 → BTCUSDT **34.922**, ETHUSDT **49.606** → FAIL
- (c) zero_trade_slot_pct ≤ 50 → 0.0 / 0.0 → PASS
→ `hypothesis_verdict: kill`, `lineage_routing: terminate`.

Root cause (post-fix `verdict_interpretation.yaml`, quoted in the KB entry):
`mechanism_failure: already_priced_in`, confidence high; `per_trade_expectancy_bps` mean
**−38.47** (t=−1.509, n=699), `median_gross_pnl` −41.71, `win_rate_net` 41.77%,
`median_forecast_return_corr` 0.047 — against assumed round-trip costs of 17.0–17.5 bps.

Two scope facts from the same entry: `exhausted_basis` closes the **daily** branch only —
the 4h branch of the parent `funding_rate_continuous_mean_reversion_expanded_auto`
reactivation_condition is DEFERRED, not ruled out; and `venue_live_tradability` records
that this family's verdicts "stand on their FEE-ONLY evidentiary basis and should not be
read as having incorporated a realistic funding P&L."

### (b) SIGN of the effect — **TAILWIND** (derived)

**Position sign convention.** `strategy_components.py:729`:
`signal = -np.sign(funding_rate) * self.scaling_factor` (`scaling_factor: 10.0` in
run_059's config), clipped to ±20 at `:730`. Forecast→allocation is sign-preserving
(positive forecast → long). So:
- `f > 0` → forecast −10 → **SHORT** → `position_sign = −1`
- `f < 0` → forecast +10 → **LONG** → `position_sign = +1`

The position held *into* bar D was set at bar D−1 from `f_{D−1}` — the hook charges the
position as it stands *before* that bar's rebalance (`trading_bot.py:195-205`). So
`position_sign(D) = −sign(f_{D−1})`.

**Accrual formula.** `portfolio_info.py:241`:
`funding_cash_flow = -position_sign * notional * f_bar`.

**Substitution:**
```
cash_flow(D) = −(−sign(f_{D−1})) · N · f_D  =  +sign(f_{D−1}) · N · f_D

sign(f_D) == sign(f_{D−1})  →  cash_flow = +N·|f_D|  >  0   CREDIT
sign flipped                →  cash_flow = −N·|f_D|  <  0   DEBIT
```

The strategy is short exactly when longs pay and long exactly when shorts pay — it sits on
the **receiving** side by construction, on every day the funding sign has not flipped since
the prior bar.

**Frequency of the credit case.** The brief's own measured flip counts
(`FUNDING_MR_DAILY_RETEST.md:240-244`, honesty note i): over the 49-month pass-gated window
BTCUSDT **228** flips, ETHUSDT **220** flips. Against 1,492 days (measured this recon,
Step 3) that is ~84.7% / ~85.3% non-flip days.

**Answer: honest funding accrual is a HEADWIND only on ~15% of position-days and a TAILWIND
on ~85% — net, a systematic CREDIT to this family.** This is the funding-carry side of its
own thesis, exactly as `cost_model.yaml:152-157` and the KB's `venue_live_tradability` note
assert.

**Therefore re-costing CAN move the verdict; it does not merely deepen the existing kill.**
That makes a re-cost a genuine re-adjudication which must be pre-registered *before* the
run. Magnitude is **not** derived here — the sign alone does not establish whether the
credit is large enough to lift criterion (a) from −0.296/−0.979 to > 0.8, or criterion (b)
from 34.922/49.606 to < 30. Establishing that requires the run.

### (c) Fields a B11-compliant pass rule must carry

Requirement source: `strategy-research/PIPELINE_IMPROVEMENTS_20260712_v4.md:576-590`
(entry **B11**, "Pass rules must specify the complete verdict mapping — no underspecified
delegation", P0), reinforced by **C7** (`:594-610`).

B11's stated fix and acceptance:
- A **total mapping**: for every outcome (PASS / FAIL-a / FAIL-b / … /
  sparse-inconclusive) the **exact verdict enum AND routing value**.
- Discretion granted only by the explicit opt-in phrase "routing at stage discretion" —
  no "verdict routing decides" delegation.
- Mid-run pre-commitments written **into** the pass-rule artifact with an audit trail,
  never into sidecars.
- Acceptance: brief lint rejects any pass rule containing a FAIL branch without an explicit
  verdict+routing pair, at materialization.

C7 adds that criteria must be machine-checkable structured entries (field name, comparator,
metric basis) evaluated by code against computed bar-level statistics — **prose criteria
are banned from the decision path**.

Concretely, per the shape the existing precedent already uses
(`FUNDING_MR_DAILY_RETEST.md:309-364`): each criterion needs `id`, `metric`,
`metric_basis`, `comparator`, `per_symbol_threshold`, `null_handling`, `source`; and
`outcomes` needs one entry per branch carrying `branch`, `hypothesis_verdict`,
`lineage_routing`.

One field the original did **not** need and a re-cost's rule would: the lineage is
currently terminated (`exhausted: true`, `reactivation_condition: null`, KB). A re-cost
pass rule must state on what authority it re-opens a terminated lineage, and what its own
PASS branch routes to. That is a registration decision — **not supplied here.**

### (d) Holdout constraint

Registry: `strategy-research/config/campaign_data_policy.yaml`
- `:18` — `holdout_range: ["2026-01-01", "2026-06-30"]`; `:8-9` — FROZEN, "no stage, tool,
  prescreen, or diagnostic may read candles inside this range except the (future)
  holdout_evaluation stage." Era `era_2026_holdout`, same range, `:62-65`.
- `:151-168` (added by **c6ed564**, `git show c6ed564`) — `kraken_q1_2026_holdout`:
  `source_dir: local_data/holdout_sealed/2026_H1/kraken_q1_2026/`, `era: era_2026_holdout`,
  `span: ["2026-01-01", "2026-03-31"]`, `sealed: true`, `single_use: true`,
  `status: sealed_holdout_not_reachable`. Present on disk (`ls -R
  trading-bot/local_data/holdout_sealed/` → per-pair CSVs at 1/5/15/60/240/720/1440-minute
  granularities).
- `:192` — `holdout_consumed_by: []`. FUNDING_MR_DAILY_RETEST has **not** spent its single
  holdout evaluation. `:199` — `holdout_failure_is_terminal: true`.

**Date ranges a re-cost run may NOT touch:**
- **2026-01-01 → 2026-06-30** — the frozen `holdout_range`, all symbols, all feeds.
- **2026-01-01 → 2026-03-31** — additionally **sealed, single-use** as the Kraken Q1-2026
  tranche (c6ed564).

Permitted (subject to registration): the 49 pass-gated months **2019-12-01 → 2023-12-31**,
and the diagnostic-only, never-gating **2024-01-01 → 2025-12-31**
(`campaign_data_policy.yaml:12-16`; brief `era_conditioning`).

**Note on enforcement:** the freeze is policy-enforced, not data-enforced, for funding. The
Binance CSVs physically extend through the holdout (both to 2026-07-05; 181/181 holdout
days present, measured Step 3) and `build_daily_funding_series` applies **no window bound
of its own** — it reads the whole CSV (`feed_registry.py:63-71`). Bounding depends entirely
on the protocol's `windows` array.

---

## GAPS

### BLOCKING for a gated re-cost run

- **G1 — No launcher can set either opt-in.**
  `grep -rn "model_funding|funding_daily"` → assignments only at `trading_bot.py:86-87`
  (defaults) and `tests/test_funding_accrual.py:277-278,333-334`. `run_backtest`'s
  signature (`launcher.py:481-484`) has no funding parameter; the engine construction
  (`launcher.py:578-594`) passes none; `run_protocol.py`'s argparse (`:982-999`) has no
  funding flag.

- **G2 — `build_daily_funding_series` has no production call site.**
  Defined `feed_registry.py:30`; absent from `FEED_REGISTRY` (`:20-27`) so
  `load_data(extra_feeds=FEED_REGISTRY)` (`launcher.py:596`) never builds it; only test
  callers (`tests/test_funding_accrual.py:28,126,141,155`). The series can never be
  populated by a run — the second of the two required opt-ins is unreachable.

- **G3 — Venue mismatch, unresolved by anything in the tree.**
  Series = Binance perp 8h (`funding_rate_fetcher.py:69`, `feed_registry.py:60`); family's
  declared execution venue = Kraken perp 1h (KB `funding_mr_daily_retest_killed` →
  `venue_live_tradability`); run_059's costing basis = Binance spot taker
  (`cost_model.yaml:71-77`, `run_protocol.py:990`). `cost_model.yaml:152-157` forbids
  costing this family with the perp block; `cost_model.yaml:181-183` self-declares the
  basis question OPEN. Minimum to clear: an operator ruling, not a code change.

- **G4 — No pre-registered pass rule for a re-cost exists, and the lineage is terminated.**
  KB `exhausted: true`, `reactivation_condition: null`. Step 6(b) establishes the accrual is
  a tailwind, so a re-cost can flip the verdict — B11
  (`PIPELINE_IMPROVEMENTS_20260712_v4.md:576-590`) requires the total verdict+routing
  mapping to exist *before* the run.

- **G5 — No end-to-end flag-off/flag-on comparison is reachable.**
  Only existing evidence is the two-bar in-process stub
  `tests/test_funding_accrual.py:266-320`, which emits no run artifacts. Follows from G1.

### NON-BLOCKING

- **G6 — Silent-zero accrual is unguarded.** `feed_registry.py:61-62` (missing CSV
  skipped), `trading_bot.py:151-156` (`None` per missing day), `trading_bot.py:204`
  (silent skip). Flag-on with a wrong `data_dir` or symbol convention is byte-identical to
  flag-off, with no error. Not triggered by the Binance series on this protocol (0 missing
  days over 1,492, measured Step 3) — but would become BLOCKING under G3's Kraken option.

- **G7 — Kraken funding archive is structurally unloadable and carries no provenance
  record.** `PF_XBTUSD.csv` vs required `BTCUSDT_funding_8h.csv`;
  `timestamp,tradeable,absolute_rate,relative_rate` vs required `timestamp,funding_rate`;
  cadence predominantly 1h (29,279 1h gaps vs 1,145 4h, `PF_XBTUSD`, measured this recon);
  coverage starts 2022-03-22, so it cannot reach the window's 2019-12 start. No emitting
  fetcher in `trading-bot/data/fetchers/`; no README/manifest under
  `local_data/Kraken_funding_rates/` (`ls -a` → `__MACOSX`, `exports` only).

- **G8 — Four partial funding days inside the pass-gated window** (BTC 2022-06-06,
  2023-05-06; ETH 2020-10-25, 2022-08-23 — 2 of 3 settlements each) sum without imputation
  (`feed_registry.py:37-39`), understating those days' accrual. 4 of 1,492 days; documented
  behavior.

- **G9 — Live-path accrual would no-op.** `PortfolioInfo.get_account_balance`
  (`portfolio_info.py:352-364`) returns a fresh API-built dict; `apply_funding` mutates
  `self.local_balance`, which the live valuation never reads. Not on the re-cost path
  (mock only, `launcher.py:163`), latent for live.

- **G10 — The series builder applies no window bound.** `feed_registry.py:63-71` reads the
  whole CSV, and the Binance CSVs extend to 2026-07-05, i.e. through the frozen holdout.
  Bounding depends entirely on the protocol's `windows` array. A guard is a design
  question, not a defect observed in a run.

---

*No fixes applied, no files created beyond this report, nothing committed.*
