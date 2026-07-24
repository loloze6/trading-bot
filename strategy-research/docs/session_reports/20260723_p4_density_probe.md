# P4 daily-trend entry-density probe — HALTED AT STEP 4 (premise P3 does not hold)

**Agent:** read-only diagnosis agent, Claude Opus 4.8
**Date executed:** 2026-07-24
**Repo:** `C:\Users\alauz\Documents\Projects\trading-bot`
**Mode:** READ-ONLY. Exactly one file written (this one). No git commit. No KB/queue/protocol/tool edit.

**Outcome in one line:** Steps 1–3 completed and are reported in full below. **Step 4 triggered the
dispatch's STOP condition: premise P3 is false as found — there is no daily-bar cached price data for
any Kraken pair.** Steps 5, 6 and 7 were therefore not performed. **No entry counts were computed.**
No return, P&L, Sharpe, expectancy, drawdown, or cost figure was computed or is reported anywhere in
this document.

---

## Step 1 — Precondition manifest: **PASS**

Command executed (single PowerShell invocation):

```
$ git status --porcelain
(no output)
$ git log --oneline -1
19fa1b9 Arc close-out: refresh NEXT_SESSION.md + SESSION_LOG for C7-EXT/XS-park arc
```

Both actual values reproduced verbatim above. Working tree empty; HEAD matches the required commit
line exactly, character for character. No STOP condition. The tree was re-observed at the end of the
task via the same `git status --porcelain` check implied by the read-only mode — no concurrent change
was observed under me.

---

## Step 2 — Strategy rule recovered from committed artifacts: **PASS (P1 holds)**

Both the parent rule and the gated variant are fully pinned by committed artifacts. **No parameter
was left to my judgment.**

### 2a. Which artifact defines which

| Rule | Defining artifact | Component class |
|---|---|---|
| **PARENT** (ungated) | `strategy-research/runs/run_054/artifacts/candidate_strategy_config.json` | `SmaTrendLongOnlyComponent` |
| **GATED** variant | `strategy-research/runs/run_057/artifacts/backtest_spec.yaml` (= `.../run_057/artifacts/candidate_strategy_config.json`, byte-identical config block) | `GatedSmaTrendLongOnlyComponent` |

The gate itself is additionally pinned, independently of the config, in
`strategy-research/runs/run_057/artifacts/pre_registration.yaml`.

Both configs are consumed against the same protocol file
`strategy-research/protocols/ts_trend_daily_v1.json`, pinned for run_057 by
`runs/run_057/artifacts/pre_registration.yaml:8` (`window_set_protocol: protocols/ts_trend_daily_v1.json`)
and confirmed at `runs/run_057/artifacts/run_context.yaml:2` (`protocol: ts_trend_daily_v1.json`).

### 2b. PARENT rule — numeric parameters (verbatim)

`strategy-research/runs/run_054/artifacts/candidate_strategy_config.json`, key path
`strategies.regimes.unknown.components[0]`, lines 15–19:

```json
            "class": "strategies.strategy_components.SmaTrendLongOnlyComponent",
            "params": {
              "lookback_L": 100,
              "scaling_factor": 10.0
            },
```

Warmup, `strategies.warmup`, line 9: `"warmup": 50`.

### 2c. PARENT rule — entry / exit / direction (verbatim)

Implementation: `trading-bot/strategies/strategy_components.py:910–978`.

Direction constraint — `strategy_components.py:912–914` (class docstring):

> `Canonical time-series momentum: long (full allocation) when close > SMA(L),`
> `flat otherwise. Long-only (no shorts) -- this component NEVER outputs a`
> `negative raw_value.`

Entry / exit condition — `strategy_components.py:956–966`:

```python
        close = data['close']
        sma = close.rolling(self.lookback_L).mean()

        # One-bar lag (see class docstring "ENGINE LIMITATION") -- use the
        # PRIOR bar's fully-formed close/SMA, not the current bar's, so the
        # signal a bar acts on was already determined before that bar started.
        prior_close = float(close.iloc[-2])
        prior_sma   = float(sma.iloc[-2])
        is_long     = prior_close > prior_sma

        self._raw_value = self.scaling_factor if is_long else 0.0
```

So: **entry** = the bar on which `close[T-1] > SMA(100)[T-1]` first becomes true after being false
(a cross-up, evaluated on the one-bar-lagged prior bar); **exit** = the bar on which it becomes false
(cross-down). There is no stop, no time stop, no target — exit is signal-flip only.

Warmup / required history — `strategy_components.py:977–978`:

```python
    def get_required_periods(self) -> int:
        return self.lookback_L + 1   # +1 for the one-bar lag (bar T-1 must be fully formed)
```

= **101 daily bars** minimum for the component itself. The protocol file records a materially larger
*engine* readiness requirement — `protocols/ts_trend_daily_v1.json:10`:

> `SmaTrendLongOnlyComponent needs 101 days of warmup (engine readiness actually needs ~2x that, ~200 bars, due to the strategy_engine history-deque-fill mechanic -- see trading-bot/core/launcher.py run_backtest docstring)`

### 2d. Bar interval (verbatim)

`strategy-research/protocols/ts_trend_daily_v1.json:17`, key path `timeframe`:

```json
  "timeframe": "1d",
```

### 2e. Execution convention (verbatim, applies to both rules)

`strategy_components.py:919–930` (parent) and `strategy-research/runs/run_057/artifacts/backtest_spec.yaml:30`:

> `"Execution: next-day open after signal change. Engine caveat: this backtester fills at bar close, not next-bar open -- see strategies/strategy_components.py::SmaTrendLongOnlyComponent's docstring for the one-bar-lag approximation actually used; not identical to true next-open execution."`

### 2f. GATED variant — the added entry gate (verbatim)

`strategy-research/runs/run_057/artifacts/pre_registration.yaml:15–19`, key path
`machine_constraints.gate_definition`:

```yaml
  gate_definition:
    indicator: kaufman_efficiency_ratio
    lookback_n: 20
    threshold: 0.3
    frozen: true
```

`strategy-research/runs/run_057/artifacts/backtest_spec.yaml:14–19`, key path
`config.strategies.regimes.unknown.components[0]`:

```yaml
            class: strategies.strategy_components.GatedSmaTrendLongOnlyComponent
            params:
              lookback_L: 100
              scaling_factor: 10.0
              er_period: 20
              gate_threshold: 0.3
```

Semantics, verbatim from `backtest_spec.yaml:27–29` (`config_rationale`):

> `"Entry-only LATCH gate (not a regime gate): GatedSmaTrendLongOnlyComponent checks ER(20)>=0.30 EXACTLY ONCE, on the bar the SMA(100) signal transitions off->on (a fresh cross-up). If the gate passes, the position latches in and is held at scaling_factor for every subsequent bar the signal remains on, REGARDLESS of ER -- in-position ER changes have no effect, no re-check, no early exit."`
>
> `"No deferred entry: if the gate check on the transition bar fails, the entry is skipped ENTIRELY for that episode -- there is no re-check on a later bar while the signal stays on; re-entry requires a fresh off-then-on transition (a real cross-down followed by a real cross-up)."`
>
> `"Exit is the unchanged parent rule: the bar the SMA(100) signal goes off (cross-down), the latch clears and output returns to 0 -- identical to SmaTrendLongOnlyComponent's own exit behavior."`

ER basis, verbatim from `strategy_components.py:1020–1026`:

> `ER BASIS: Kaufman ER_t(er_period) = abs(close_t - close_{t-n}) / sum(abs(close_i - close_i-1)), computed RAW (no smoothing -- unlike EfficiencyRatioRegimeComponent's EWM-smoothed regime-detector version; the brief's gate_definition specifies the unsmoothed formula), over a window ending at the SAME prior bar (T-1) the SMA comparison uses -- identical one-bar lag, no lookahead, no cross-contamination between the two indicators' effective "as-of" bar.`

Gate evaluation, `strategy_components.py:1090–1104`:

```python
        if is_long_signal and not self._prior_signal:
            # Transition bar (signal off -> on): the ONLY point the gate is
            # ever evaluated. No deferred entry, no re-check on later bars.
            if prior_er >= self.gate_threshold:
                self._in_position = True
                entered_this_bar = True
            else:
                self._in_position = False
                gate_rejected_this_bar = True
        elif not is_long_signal:
            # Signal-off bar (cross-down, or signal never triggered): flat,
            # latch cleared -- unchanged parent exit rule.
            self._in_position = False
```

Gated warmup, `strategy_components.py:1128–1131`:

```python
    def get_required_periods(self) -> int:
        # SMA needs lookback_L+1 (one-bar lag); ER needs er_period+2 (er_period+1
        # closes ending at the SAME prior bar, one-bar lag) -- take the binding one.
        return max(self.lookback_L + 1, self.er_period + 2)
```

= `max(101, 22)` = **101 daily bars** — the gate does not widen the warmup.

**Delta between parent and gated variant: exactly one entry gate, `ER(20) >= 0.30`, checked once per
episode on the cross-up bar. Exit rule, direction constraint, lookback, scaling factor, interval and
execution convention are all identical.**

---

## Step 3 — Evaluation frame recovered: **PASS (P2 holds)**

### 3a. Window definition and count

Source: `strategy-research/protocols/ts_trend_daily_v1.json`, key path `windows` (lines 18–124).

- **15 windows**, non-overlapping, **semi-annual (182-day)**, each a bare `test` block with
  `start` / `end`; no train split.
- First window `2018-04` = `2018-04-01 → 2018-10-01` (lines 20–24); last window `2025-04` =
  `2025-04-01 → 2025-10-01` (lines 118–122). Boundaries step by exactly 6 calendar months, every
  window's `end` equal to the next window's `start`.

Full boundary list, verbatim from lines 18–124:

| # | label | test.start | test.end |
|---|---|---|---|
| 1 | 2018-04 | 2018-04-01 | 2018-10-01 |
| 2 | 2018-10 | 2018-10-01 | 2019-04-01 |
| 3 | 2019-04 | 2019-04-01 | 2019-10-01 |
| 4 | 2019-10 | 2019-10-01 | 2020-04-01 |
| 5 | 2020-04 | 2020-04-01 | 2020-10-01 |
| 6 | 2020-10 | 2020-10-01 | 2021-04-01 |
| 7 | 2021-04 | 2021-04-01 | 2021-10-01 |
| 8 | 2021-10 | 2021-10-01 | 2022-04-01 |
| 9 | 2022-04 | 2022-04-01 | 2022-10-01 |
| 10 | 2022-10 | 2022-10-01 | 2023-04-01 |
| 11 | 2023-04 | 2023-04-01 | 2023-10-01 |
| 12 | 2023-10 | 2023-10-01 | 2024-04-01 |
| 13 | 2024-04 | 2024-04-01 | 2024-10-01 |
| 14 | 2024-10 | 2024-10-01 | 2025-04-01 |
| 15 | 2025-04 | 2025-04-01 | 2025-10-01 |

Why semi-annual and why the 2018-04-01 start, verbatim from `ts_trend_daily_v1.json:10`
(key path `pre_registration._note_windows`):

> `2026-07-08 revision: original design used monthly (~30-day) windows copied from the 1h baseline_v2.json convention. That is structurally incompatible with this signal: SmaTrendLongOnlyComponent needs 101 days of warmup (engine readiness actually needs ~2x that, ~200 bars, due to the strategy_engine history-deque-fill mechanic -- see trading-bot/core/launcher.py run_backtest docstring), so every monthly window showed zero trades regardless of true signal quality (verified via a zero-trade repro run, 2026-07-07, which leaked no information about the signal itself -- see brief addendum). Redesigned to semi-annual (182-day) non-overlapping windows: the shakedown showed ~6.4 opens/symbol/year, giving ~3.2 expected trades/window -- comfortably clears a quarterly (91-day, ~1.6 expected) floor with real margin while giving 2x the walk-forward sample count of annual windows. First window starts 2018-04-01 (not 2018-01-01): Binance BTCUSDT/ETHUSDT true history starts 2017-08-17 (confirmed via live fetch, backfill extended in local_data/*_1d.csv), and the required_bars-based warmup prefetch (up to 2x required_bars=202 days before window_start) needs window_start >= ~2018-03-07 to stay within available history; 2018-04-01 gives a 25-day safety margin.`

### 3b. Symbols evaluated

`strategy-research/protocols/ts_trend_daily_v1.json:13–16`, key path `symbols`:

```json
  "symbols": [
    "BTCUSDT",
    "ETHUSDT"
  ],
```

**2 symbols × 15 windows = 30 window-symbol slots.** Corroborated by
`strategy-research/runs/run_054/artifacts/protocol_result.yaml`, which enumerates exactly 30
`results:` entries (BTCUSDT `2018-04` at line 5 through ETHUSDT `2025-04` at line 875) and a
`per_symbol_summary` (line 905) containing exactly `BTCUSDT` and `ETHUSDT`.

### 3c. The A3.4 floor (quoted from the artifact that defines it, not from the dispatch)

**Defining artifact:** `strategy-research/skills/verdict-interpreter/SKILL.md:581–589`. Verbatim:

> `## A3.4 — Sparse-trader Sharpe gate (mandatory)`
>
> `Before applying any Sharpe-based diagnostic rule, compute:`
>   `` `below_floor_pct = fraction of windows with trade_count < 5` ``
>
> `If `below_floor_pct > 0.50` (more than half the windows are sparse):`
> `- Suspend all `median_sharpe`-based rules.`
> `- Use `per_trade_expectancy_bps` (from `hypothesis_verdict.diagnostics`) as the primary`
>   `performance statistic.`

**The A3.4 floor is `trade_count >= 5` per window-symbol slot.** A slot with fewer than 5 is "sparse".

Machine-readable mirror, `strategy-research/config/campaign_config.yaml:120`, key path
`verdict_interpreter.trade_floor_per_window`:

```yaml
  trade_floor_per_window: 5      # per-window "sparse" threshold (A3.4 gate)
```

**Ambiguity flagged, not resolved by me:** the protocol file carries a *different*, lower,
separately-named per-window minimum — `ts_trend_daily_v1.json:132`, key path
`promotion.min_trade_count_gte`:

```json
    "min_trade_count_gte": 1,
```

pre-registered at that value by `ts_trend_daily_v1.json:11` (`pre_registration._note_min_trade_count`),
verbatim in relevant part:

> `Revised to 1 (at least one completed round-trip required for a window to count as evaluable), matching the LOWER end of the brief a-priori expectation (10-25 transitions / 15 windows =~ 0.7-1.7/window). This is a pre-registered floor, not tuned to the shakedown observed values.`

These are two distinct gates with two distinct names. The dispatch asked specifically for the **A3.4**
floor, which is **5** (SKILL.md:584). The protocol's `min_trade_count_gte: 1` is the promotion
evaluability gate, not A3.4. Had Steps 5–7 run, table (c) would have been computed against **5**, with
a `>= 1` column reported alongside as a secondary reference — I record this here so the choice is
auditable rather than silent.

---

## Step 4 — Daily-bar universe from the cache: **STOP — premise P3 is FALSE**

### The premise as written

> `P3. Daily-bar cached price data exists for the Kraken pairs ingested in Phase 2 Track A.`

### What the cache actually contains

**Cache path:** `C:\Users\alauz\Documents\Projects\trading-bot\trading-bot\local_data\` (flat
namespace; this is the directory `CcxtFetcher`/`BaseFetcher` read and write, keyed by `cache_key()`
per `trading-bot/data/fetchers/ccxt_fetcher.py:117`).

Commands executed:

```
$ Get-ChildItem $d -Filter "*_1d.csv" -File | Select-Object -ExpandProperty Name
BTCUSDT_1d.csv
ETHUSDT_1d.csv

$ (Get-ChildItem $d -Filter "kraken_*" -File | Measure-Object).Count
19

$ Get-ChildItem $d -Filter "kraken_*" -File | Where-Object { $_.Name -notmatch '_1h\.csv$' } | Select-Object -ExpandProperty Name
(no output)
```

**Result, stated plainly:**

- There are exactly **two** daily-bar files in the cache: `BTCUSDT_1d.csv` and `ETHUSDT_1d.csv`. Both
  are Binance, USDT-quoted — **precisely and only the two symbols run_057 already evaluated.**
- There are **19** Kraken cache files. **Every one of them is `_1h`.** The filter for any Kraken cache
  file not ending in `_1h.csv` returned nothing.

The 19 ingested Kraken pairs, all 1-hour only:
`AAVEUSD, ADAUSD, AVAXUSD, BTCUSD, DOGEUSD, ETHUSD, INJUSD, LINKUSD, LTCUSD, NEARUSD, ONDOUSD,
SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD, XMRUSD, XRPUSD, ZECUSD`.

**Therefore: the daily-bar universe available in the cache has breadth 2 — the exact same two symbols
run_057 ran on. There is no breadth to test at the daily interval. P3 does not hold, and the probe's
whole premise (that breadth might lift per-window entry density above the floor) cannot be exercised
from the cache as it stands.**

### The near-miss artifact I did NOT substitute

The raw Kraken bulk archive at
`C:\Users\alauz\Documents\Projects\trading-bot\trading-bot\local_data\Kraken_batch\master_q4\`
**does** contain 1440-minute (= daily) CSVs, e.g. `XBTUSD_1440.csv`. Spot-read of seven of them
(direct `Get-Content` of first/last line, unix seconds decoded to UTC date):

| Archive file | rows | first bar | last bar |
|---|---|---|---|
| `XBTUSD_1440.csv` | 4457 | 2013-10-06 | 2025-12-31 |
| `ETHUSD_1440.csv` | 3794 | 2015-08-07 | 2025-12-31 |
| `SOLUSD_1440.csv` | 1659 | 2021-06-17 | 2025-12-31 |
| `ADAUSD_1440.csv` | 2652 | 2018-09-28 | 2025-12-31 |
| `LINKUSD_1440.csv` | 2290 | 2019-09-25 | 2025-12-31 |
| `XRPUSD_1440.csv` | 3147 | 2017-05-18 | 2025-12-31 |
| `LTCUSD_1440.csv` | 4265 | 2013-10-24 | 2025-12-31 |

This is a **raw bulk download, not cached price data**: it is not in the cache namespace, is not
keyed by `cache_key()`, has no header row, carries unix-seconds timestamps rather than the cache's
`timestamp` string column, and is not reachable by any loader in the repo. Per the dispatch's
explicit instruction — *"do not fabricate the missing piece, do not substitute a similar artifact,
do not gather more information first"* — **I did not ingest, convert, resample, or read these files
into a counting run.** I report their existence because it is the single most decision-relevant fact
for whoever authorizes the next step, not as a substitute for the missing premise.

Two further facts already on record confirm this is a real gap and not a lookup error on my part:

- `strategy-research/docs/session_reports/20260722_kraken_ingest_audit.md:365–366` — `data_manager.py:768`
  hardcodes `exchange="binance"`, so **"No backtest can currently reach any of the five ingested
  Kraken cache files."** Even the 1h Kraken cache is unreachable by the engine today.
- The same audit, Target E table (lines 297–303), records every ingested Kraken pair terminating at
  `2025-12-31 23:00`.

### Holdout boundary

**Archive end date = 2025-12-31**, established from the cache/archive itself: every Kraken daily
archive file read in the table above terminates on `2025-12-31`, and the audit's independently
recomputed 1h continuity table (`20260722_kraken_ingest_audit.md:297–303`) reports the same terminal
bar `2025-12-31 23:00` for all five pilot pairs.

The 2026 holdout is `2026-01-01 → 2026-06-30` per `strategy-research/protocols/ts_trend_daily_v1.json:125–128`
(key path `holdout`). **No bar dated after 2025-12-31 was loaded, counted, or examined at any point in
this task.** The last window in the Step 3 window set ends `2025-10-01`, comfortably inside the
boundary, so no window-level truncation would have been required even had Steps 5–7 run.

---

## Steps 5, 6, 7 — NOT PERFORMED

Halted per the dispatch's STOP rule at Step 4. Specifically:

- **Step 5 (entry counts):** not computed. No code was executed against price data. No parent-rule
  count, no gated-variant count, no insufficient-history classification.
- **Step 6 (three density tables + like-for-like control):** not produced. **The two side-by-side
  floor-clearing counts the dispatch asked for do not exist and are not reported.** Note that the
  "full universe" and the "restricted to symbols run_057 evaluated" arms would in any case have been
  *identical sets* — `{BTCUSDT, ETHUSDT}` — making the like-for-like control degenerate. That
  degeneracy is itself the finding.
- **Step 7 (interpretation):** the specific question *"does breadth lift density above the floor?"*
  is unanswerable from the cache as it stands, because **there is no breadth at the daily interval to
  lift it with.** This is a negative result about the data, not about the signal.

---

## What this establishes, and what it does not

**Establishes:**

1. The P4 daily-trend rule is fully and unambiguously recoverable from committed artifacts, in both
   its parent (run_054, `SmaTrendLongOnlyComponent`, SMA(100) long/flat, one-bar lag) and gated
   (run_057, `GatedSmaTrendLongOnlyComponent`, + entry-only `ER(20) >= 0.30` latch) forms. P1 holds.
   Anyone can reconstruct either rule from the quotes in Step 2 without a judgment call.
2. The evaluation frame is fully recoverable: 15 non-overlapping semi-annual windows,
   2018-04-01 → 2025-10-01, on `{BTCUSDT, ETHUSDT}` = 30 window-symbol slots. P2 holds.
3. The A3.4 floor is **5 trades per window-symbol slot** (`verdict-interpreter/SKILL.md:584`), which
   is a *different and stricter* gate than the protocol's `promotion.min_trade_count_gte: 1`
   (`ts_trend_daily_v1.json:132`). Anyone reasoning about "the floor" for this strategy needs to say
   which of the two they mean.
4. **The blocking fact:** the daily-bar cache contains exactly two symbols, and they are the two
   already evaluated. The 19-pair Kraken breadth ingestion (Phase 2 Track A and its scale-up) is
   **1-hour only**. The daily-interval breadth this probe was designed to measure does not exist in
   the cache.

**Does not establish:**

- **Nothing whatsoever about entry density.** No entry was counted, for either rule, on any symbol,
  in any window.
- **Nothing about edge.** Even had the counts been produced, **entry counts are not evidence of
  edge** — a rule that fires often can be worthless and a rule that fires rarely can be sound.
  Density is a statistical-power precondition for evaluating a hypothesis, not a property of the
  hypothesis.
- **No performance statistic of any kind was computed in the course of this task** — no return, P&L,
  Sharpe, expectancy, drawdown, or cost figure. No backtest was run. The hypothesis under study
  remains unregistered and uncontaminated by any performance observation made here.
  (`runs/run_054/artifacts/protocol_result.yaml` was opened in Step 3 solely to confirm the 30-slot
  window×symbol enumeration; its performance fields were not extracted, carried forward, or used in
  any reasoning above.)

---

## Decision needed from the operator

The probe cannot proceed without one of the following, none of which I am authorized to do:

1. **Ingest the Kraken `*_1440.csv` daily bars into the cache** (a write to `local_data/`, plus
   whatever the ingest tool requires) — makes the intended breadth measurable at the daily interval;
   or
2. **Re-scope the probe to the 1h interval**, which contradicts `ts_trend_daily_v1.json:17`
   (`"timeframe": "1d"`) and the entire warmup/window rationale at line 10 — this would be a
   different hypothesis, not the registered one; or
3. **Abandon the breadth arm** and record that P4_ts_trend's daily-bar density cannot be improved by
   the currently-ingested universe.

Additionally, per `20260722_kraken_ingest_audit.md:365–366`, even option 1 does not by itself make
the data reachable: `data_manager.py:768` hardcodes `exchange="binance"` and would need
parameterizing before any engine run could read a `kraken_*` cache key.

**No remediation was attempted. No file outside this report was written.**
