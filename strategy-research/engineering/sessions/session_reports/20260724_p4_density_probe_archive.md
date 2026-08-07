# P4 density probe against the raw daily archive (READ-ONLY)

**Dispatch:** R2b — supersedes blocked Step 4 of `20260723_p4_density_probe.md`
**Date:** 2026-07-24
**Scope:** entry COUNTS only. **No return, P&L, Sharpe, expectancy, drawdown, or cost
figure was computed.** No backtest was run. Nothing was ingested. One file written
(this one). No git commit.

---

## Step 1 — Precondition manifest

`git log --oneline -1` (verbatim):

```
19fa1b9 Arc close-out: refresh NEXT_SESSION.md + SESSION_LOG for C7-EXT/XS-park arc
```

`git status --porcelain` (verbatim):

```
?? strategy-research/docs/session_reports/20260723_p4_density_probe.md
?? strategy-research/docs/session_reports/20260723_p4_panel_recon.md
```

Matches the manifest exactly: HEAD as specified, two untracked files under
`strategy-research/docs/session_reports/`, no tracked file modified. **Preconditions
hold — proceeded.**

---

## Step 2 — Rule and frame recovered from committed artifacts

### PARENT (ungated) rule — `SmaTrendLongOnlyComponent`

Source: `trading-bot/strategies/strategy_components.py:910-978`

| Element | Value | Provenance |
|---|---|---|
| Entry condition | transition of `is_long` from False→True, where `is_long = close[T-1] > SMA(100)[T-1]` | `strategy_components.py:962-964` |
| Exit condition | `is_long` False (cross-down); output returns to 0 | `strategy_components.py:966`; gated-class docstring `:1017-1019` ("Exit is the unchanged parent rule") |
| `lookback_L` | 100 | `strategy_components.py:944` `int(params.get("lookback_L", 100))`; brief `research_brief_P4_ts_trend.md:30` `lookback_L: 100d  # literature-conventional; NOT swept`; refinement brief `P4_ts_trend_r1_er_gate.yaml:77` `lookback_L: 100           # SMA(100)` |
| `scaling_factor` | 10.0 | `strategy_components.py:945`; `P4_ts_trend_r1_er_gate.yaml:78` |
| Lag convention | one-bar lag: signal at bar T uses bar T-1's fully-formed close and SMA | `strategy_components.py:959-964` |
| Direction constraint | long-only, never negative (`raw_value ∈ {0.0, 10.0}`) | `strategy_components.py:912-913`, `:966` |
| Bar interval | 1d | `protocols/ts_trend_daily_v1.json:17` `"timeframe": "1d"`; `P4_ts_trend_r1_er_gate.yaml:76` `timeframe: 1d` |
| Component warmup | `required_periods = lookback_L + 1 = 101` | `strategy_components.py:977-978` |
| Engine warmup prefetch | `2 * strategy.required_bars = 202` bars before window start | `trading-bot/core/launcher.py:562` `prefetch_bars = 2 * strategy.required_bars`; `run_protocol.py:1072,1136` pass `warmup_prefetch=True` unconditionally |

Warmup-state detail replicated exactly: `_prior_signal` initialises to `False`
(`strategy_components.py:1061-1065`) and is only assigned on ready bars
(`:1123`, after the `is_ready()` early return at `:1069-1071`). So the first ready bar
with `is_long == True` counts as a transition. This is the committed behaviour, not an
approximation.

### Window set

Source: `strategy-research/protocols/ts_trend_daily_v1.json:18-124`

15 non-overlapping semi-annual windows, `[start, end)`:

```
2018-04: 2018-04-01 → 2018-10-01      2021-10: 2021-10-01 → 2022-04-01
2018-10: 2018-10-01 → 2019-04-01      2022-04: 2022-04-01 → 2022-10-01
2019-04: 2019-04-01 → 2019-10-01      2022-10: 2022-10-01 → 2023-04-01
2019-10: 2019-10-01 → 2020-04-01      2023-04: 2023-04-01 → 2023-10-01
2020-04: 2020-04-01 → 2020-10-01      2023-10: 2023-10-01 → 2024-04-01
2020-10: 2020-10-01 → 2021-04-01      2024-04: 2024-04-01 → 2024-10-01
2021-04: 2021-04-01 → 2021-10-01      2024-10: 2024-10-01 → 2025-04-01
                                      2025-04: 2025-04-01 → 2025-10-01
```

Count = 15, confirmed against `P4_ts_trend_r1_er_gate.yaml:90-95` ("15 explicit
semi-annual windows per symbol (\"2018-04\" .. \"2025-04\")").
Holdout: `ts_trend_daily_v1.json:125-128` `"start": "2026-01-01"`.

### GATED variant — additional parameters only

Source: `trading-bot/strategies/strategy_components.py:986-1131`

| Element | Value | Provenance |
|---|---|---|
| Indicator | Kaufman Efficiency Ratio, **raw / unsmoothed** | `P4_ts_trend_r1_er_gate.yaml:48-49`; `strategy_components.py:1021-1023` |
| Formula | `ER_t(n) = abs(close_t - close_{t-n}) / sum_{i=t-n+1..t} abs(close_i - close_{i-1})` | `P4_ts_trend_r1_er_gate.yaml:49` |
| `er_period` | 20 | `strategy_components.py:1055`; `P4_ts_trend_r1_er_gate.yaml:50` `lookback_n: 20            # primary; a-priori, convention-based` |
| `gate_threshold` | 0.30, `>=` passes | `strategy_components.py:1056`; `P4_ts_trend_r1_er_gate.yaml:51` `threshold: 0.30           # a-priori, convention-based; >= passes` |
| Application | **entry-only latch**, checked exactly once on the cross-up bar; no deferred entry, no re-check, no in-position re-gating | `strategy_components.py:1090-1104`; `P4_ts_trend_r1_er_gate.yaml:58-62` |
| ER window | `close_vals[-(er_period+2):-1]` → the 21 closes ending at bar T-1 (same one-bar lag as the SMA) | `strategy_components.py:1084-1088` |
| Exit | unchanged parent rule | `strategy_components.py:1017-1019` |
| Frozen | `frozen: true  # no retune, no sweep, no post-hoc threshold moves` | `P4_ts_trend_r1_er_gate.yaml:69` |

**No parameter was left to judgment. Premise P2 holds.**

---

## Step 3 — Universe and archive schema

### Schema, inferred from the files themselves

`master_q4/*_1440.csv` files have **no header row** and **7 columns**. Inferred by two
independent means:

1. Direct inspection — first line of `XBTUSD_1440.csv` is
   `1381017600,122.0,122.0,122.0,122.0,0.1,1`, i.e. data, not column names; 7 fields.
2. In-archive corroboration — the same directory contains
   `master_q4/BTCUSD_Daily_OHLC.csv`, which **does** carry a header and whose data rows
   are the same series:

   ```
   timestamp,open,high,low,close,volume,trades
   1381017600,122.0,122.0,122.0,122.0,0.1,1
   ```

   That header names exactly the 7 columns, in order, for byte-identical leading rows.
   (`BTCUSD_Daily_OHLC.csv` has 3,728 lines vs `XBTUSD_1440.csv`'s 4,457 — it is a
   truncated older export of the same series, used here only as schema evidence, never
   as a data source.)

`timestamp` is **unix seconds, UTC**, at 86400s spacing (verified: modal step = 86400).

### Premise P1 — PARTIAL FAILURE, resolved by ticker alias (flagged, not hidden)

19 Kraken pairs are present in the price cache as `kraken_<SYM>_1h.csv`. Of these,
**17 have a directly-named `<SYM>_1440.csv` in master_q4. Two do not:**

- `BTCUSD_1440.csv` — **does not exist**
- `DOGEUSD_1440.csv` — **does not exist**

Both are Kraken *native ticker* renames, not absent assets. I mapped them via alias and
am flagging it explicitly so the director can exclude them:

| Cache symbol | Archive file used | Evidence for the alias |
|---|---|---|
| `BTCUSD` | `XBTUSD_1440.csv` | (a) XBT is Kraken's native code for bitcoin; (b) **in-archive**: `BTCUSD_Daily_OHLC.csv`, in this same directory, carries the `XBTUSD_1440.csv` series under the name "BTCUSD"; (c) `kraken_BTCUSD_1h.csv`'s first bar is `2013-10-06 21:00, close 122.0` and `XBTUSD_1440.csv`'s first bar is `1381017600 (2013-10-06), close 122.0` |
| `DOGEUSD` | `XDGUSD_1440.csv` | (a) XDG is Kraken's native code for dogecoin; (b) `kraken_DOGEUSD_1h.csv`'s first bar is `2019-12-19 18:00, close 0.026` and `XDGUSD_1440.csv`'s series starts `2019-12-19` |

**Director's call:** if you want the strict literal reading of P1 (these two are
"missing", drop them), the Step-5 numbers change only marginally for the full universe
— but the BTC/ETH control collapses to ETH alone. Every table below labels these two
rows, so either reading is recoverable without a rerun.

### Universe, spans, and holdout boundary

All series truncated to `date < 2026-01-01` before any computation (holdout guard).
"nonstd steps" = count of consecutive-timestamp gaps ≠ 86400s.

| Cache symbol | Archive file | Map | Bars | First bar | Last bar | nonstd steps |
|---|---|---|---|---|---|---|
| AAVEUSD | AAVEUSD_1440.csv | direct | 1843 | 2020-12-15 | 2025-12-31 | 0 |
| ADAUSD  | ADAUSD_1440.csv  | direct | 2652 | 2018-09-28 | 2025-12-31 | 0 |
| AVAXUSD | AVAXUSD_1440.csv | direct | 1472 | 2021-12-21 | 2025-12-31 | 0 |
| BTCUSD  | XBTUSD_1440.csv  | **alias** | 4457 | 2013-10-06 | 2025-12-31 | 12 |
| DOGEUSD | XDGUSD_1440.csv  | **alias** | 2205 | 2019-12-19 | 2025-12-31 | 0 |
| ETHUSD  | ETHUSD_1440.csv  | direct | 3794 | 2015-08-07 | 2025-12-31 | 5 |
| INJUSD  | INJUSD_1440.csv  | direct | 1605 | 2021-08-10 | 2025-12-31 | 0 |
| LINKUSD | LINKUSD_1440.csv | direct | 2290 | 2019-09-25 | 2025-12-31 | 0 |
| LTCUSD  | LTCUSD_1440.csv  | direct | 4265 | 2013-10-24 | 2025-12-31 | 88 |
| NEARUSD | NEARUSD_1440.csv | direct | 1295 | 2022-06-16 | 2025-12-31 | 0 |
| ONDOUSD | ONDOUSD_1440.csv | direct |  630 | 2024-04-11 | 2025-12-31 | 0 |
| SOLUSD  | SOLUSD_1440.csv  | direct | 1659 | 2021-06-17 | 2025-12-31 | 0 |
| SUIUSD  | SUIUSD_1440.csv  | direct |  974 | 2023-05-03 | 2025-12-31 | 0 |
| TAOUSD  | TAOUSD_1440.csv  | direct |  549 | 2024-07-01 | 2025-12-31 | 0 |
| TRXUSD  | TRXUSD_1440.csv  | direct | 2128 | 2020-03-05 | 2025-12-31 | 0 |
| UNIUSD  | UNIUSD_1440.csv  | direct | 1904 | 2020-10-15 | 2025-12-31 | 0 |
| XMRUSD  | XMRUSD_1440.csv  | direct | 3285 | 2017-01-02 | 2025-12-31 | 1 |
| XRPUSD  | XRPUSD_1440.csv  | direct | 3147 | 2017-05-18 | 2025-12-31 | 2 |
| ZECUSD  | ZECUSD_1440.csv  | direct | 3350 | 2016-10-29 | 2025-12-31 | 1 |

**Archive end date = 2025-12-31** (max last bar across all 19 files; uniform across all
of them). This is *before* the protocol's holdout start of 2026-01-01
(`ts_trend_daily_v1.json:126`), and before the last scored window's end of 2025-10-01,
so no holdout bar was loaded, counted, or reported. The explicit
`date < 2026-01-01` filter in the code below is belt-and-braces on top of that.

**Data-continuity caveat (not a blocker, but load-bearing for interpretation):** LTCUSD
has 88 non-standard steps and BTCUSD 12. The SMA(100) is computed over the *bar
sequence as loaded*, exactly as the engine feeds it, so across a gap the 100-bar window
spans more than 100 calendar days. This is the same behaviour a real run would exhibit
on this data; it is noted, not corrected.

---

## Step 4 — Entry counts

### Slot categories (three, never merged)

- **evaluable** — symbol has ≥202 bars strictly before window start (the engine's actual
  prefetch requirement, `launcher.py:562`) AND ≥1 bar inside the window.
- **insufficient-history** — otherwise. **Distinct from zero-entries and never summed
  with it.**
- Within evaluable slots, a count of **0** is a genuine zero-entries result.

### Headline

```
total window-symbol slots        285   (19 symbols x 15 windows)
evaluable                        178
insufficient-history             107
control (BTCUSD, ETHUSD) evaluable  30 / 30
```

Total entries across evaluable slots: **parent 799, gated 209** (gate rejects 74% of
parent entries).

### Entry-count distribution over the 178 evaluable slots

| entries | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **parent** slots | 3 | 22 | 25 | 19 | 29 | 28 | 9 | 15 | 11 | 9 | 4 | 3 | 1 |
| **gated** slots | 58 | 64 | 34 | 15 | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

The three genuine zero-entry parent slots: AVAXUSD/2023-04, ETHUSD/2019-04,
LTCUSD/2019-04.

### Per symbol (evaluable slots only)

`n` = evaluable slots; `par`/`gat` = total entries; `p≥1`,`p≥5`,`g≥1`,`g≥5` = slots
clearing each floor.

| Symbol | n | par | gat | p≥1 | p≥5 | g≥1 | g≥5 |
|---|---|---|---|---|---|---|---|
| AAVEUSD | 8 | 37 | 14 | 8 | 3 | 6 | 0 |
| ADAUSD | 12 | 40 | 11 | 12 | 3 | 9 | 0 |
| AVAXUSD | 6 | 15 | 2 | 5 | 1 | 1 | 0 |
| BTCUSD *(alias)* | 15 | 54 | 17 | 15 | 6 | 9 | 0 |
| DOGEUSD *(alias)* | 10 | 39 | 12 | 10 | 3 | 8 | 0 |
| ETHUSD | 15 | 53 | 18 | 14 | 7 | 10 | 1 |
| INJUSD | 7 | 37 | 5 | 7 | 4 | 4 | 0 |
| LINKUSD | 10 | 54 | 15 | 10 | 5 | 8 | 0 |
| LTCUSD | 15 | 67 | 15 | 14 | 7 | 11 | 0 |
| NEARUSD | 5 | 24 | 3 | 5 | 2 | 3 | 0 |
| ONDOUSD | 1 | 9 | 0 | 1 | 1 | 0 | 0 |
| SOLUSD | 7 | 42 | 10 | 7 | 4 | 6 | 0 |
| SUIUSD | 3 | 15 | 1 | 3 | 2 | 1 | 0 |
| TAOUSD | 1 | 7 | 1 | 1 | 1 | 1 | 0 |
| TRXUSD | 10 | 35 | 8 | 10 | 3 | 5 | 0 |
| UNIUSD | 8 | 39 | 11 | 8 | 4 | 6 | 0 |
| XMRUSD | 15 | 94 | 19 | 15 | 11 | 9 | 0 |
| XRPUSD | 15 | 83 | 22 | 15 | 7 | 11 | 1 |
| ZECUSD | 15 | 55 | 25 | 15 | 6 | 12 | 1 |

### Per window (evaluable slots only)

| Window | n eval | insuff. | par | p≥1 | p≥5 | g≥1 | g≥5 |
|---|---|---|---|---|---|---|---|
| 2018-04 | 6 | 13 | 22 | 6 | 3 | 5 | 1 |
| 2018-10 | 6 | 13 | 14 | 6 | 1 | 5 | 0 |
| 2019-04 | 6 | 13 | 10 | 4 | 0 | 2 | 0 |
| 2019-10 | 7 | 12 | 22 | 7 | 2 | 7 | 0 |
| 2020-04 | 7 | 12 | 36 | 7 | 3 | 4 | 0 |
| 2020-10 | 10 | 9 | 34 | 10 | 4 | 5 | 0 |
| 2021-04 | 10 | 9 | 32 | 10 | 3 | 10 | 0 |
| 2021-10 | 12 | 7 | 50 | 12 | 3 | 9 | 0 |
| 2022-04 | 14 | 5 | 83 | 14 | 9 | 9 | 0 |
| 2022-10 | 15 | 4 | 81 | 15 | 8 | 14 | 1 |
| 2023-04 | 16 | 3 | 77 | 15 | 7 | 10 | 0 |
| 2023-10 | 16 | 3 | 56 | 16 | 5 | 11 | 0 |
| 2024-04 | 17 | 2 | 91 | 17 | 10 | 11 | 1 |
| 2024-10 | 17 | 2 | 77 | 17 | 8 | 4 | 0 |
| 2025-04 | 19 | 0 | 114 | 19 | 14 | 14 | 0 |

### Warmup sensitivity

Primary uses the engine's 202-bar prefetch. Repeating with the bare component
requirement (101 bars) moves 10 slots from insufficient-history to evaluable and does
**not** change any conclusion:

| warmup | evaluable | f1-parent | f1-gated | f5-parent | f5-gated |
|---|---|---|---|---|---|
| 202 (engine, primary) | 178 | 175/178 | 120/178 | 80/178 | **3/178** |
| 101 (component only) | 188 | 185/188 | 127/188 | 84/188 | **3/188** |

Control slots (30/30 evaluable) and all four control figures are identical under both.

### Exact code executed (rerunnable verbatim)

Run from repo root `C:\Users\alauz\Documents\Projects\trading-bot`, piped to `python`
via stdin (no script file was written to disk):

```python
import os, json
import numpy as np, pandas as pd

ARCH="trading-bot/local_data/Kraken_batch/master_q4"; CACHE="trading-bot/local_data"
L=100; ER_N=20; ER_THR=0.30
REQUIRED_BARS=L+1              # component get_required_periods()
PREFETCH=2*REQUIRED_BARS       # launcher.py:562  prefetch_bars = 2 * strategy.required_bars
HOLDOUT_START=pd.Timestamp("2026-01-01")

WIN=[(w["label"],pd.Timestamp(w["test"]["start"]),pd.Timestamp(w["test"]["end"]))
     for w in json.load(open("strategy-research/protocols/ts_trend_daily_v1.json"))["windows"]]

cache=sorted(f[len("kraken_"):-len("_1h.csv")] for f in os.listdir(CACHE)
             if f.startswith("kraken_") and f.endswith("_1h.csv"))
ALIAS={"BTCUSD":"XBTUSD","DOGEUSD":"XDGUSD"}
COLS=["timestamp","open","high","low","close","volume","trades"]

def load(s):
    p=f"{ARCH}/{s}_1440.csv"
    if not os.path.exists(p) and s in ALIAS: p=f"{ARCH}/{ALIAS[s]}_1440.csv"
    if not os.path.exists(p): return None
    d=pd.read_csv(p,header=None,names=COLS).drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)
    d["date"]=pd.to_datetime(d["timestamp"],unit="s",utc=True).dt.tz_localize(None)
    return d[d["date"]<HOLDOUT_START].reset_index(drop=True)   # HOLDOUT guard

def entries(c):
    """Replicate SmaTrendLongOnly / GatedSmaTrendLongOnly transition logic bar-by-bar."""
    n=len(c); sma=pd.Series(c).rolling(L).mean().values
    e_par=np.zeros(n,bool); e_gat=np.zeros(n,bool); prior=False
    for i in range(REQUIRED_BARS-1, n):                      # first bar where len(data)>=101
        is_long = c[i-1] > sma[i-1]                          # one-bar lag
        if is_long and not prior:
            e_par[i]=True
            w=c[i-ER_N-1:i]                                  # close_vals[-(er_period+2):-1]
            path=np.abs(np.diff(w)).sum()
            er = abs(w[-1]-w[0])/path if path!=0 else 0.0
            if er>=ER_THR: e_gat[i]=True
        prior=is_long
    return e_par,e_gat

rows=[]
for s in cache:
    d=load(s)
    if d is None:
        print("NO ARCHIVE COUNTERPART:",s); continue
    ep,eg=entries(d["close"].values)
    for lab,st,en in WIN:
        pre=int((d["date"]<st).sum()); inw=((d["date"]>=st)&(d["date"]<en)).values
        if pre<PREFETCH or inw.sum()==0:
            rows.append(dict(sym=s,win=lab,status="insufficient_history",parent=None,gated=None))
        else:
            rows.append(dict(sym=s,win=lab,status="evaluable",
                             parent=int(ep[inw].sum()),gated=int(eg[inw].sum())))
df=pd.DataFrame(rows)
ev=df[df["status"]=="evaluable"]; ctl=ev[ev["sym"].isin(["BTCUSD","ETHUSD"])]
print(f"total slots={len(df)}  evaluable={len(ev)}  insufficient_history={len(df)-len(ev)}")
print(f"control(BTCUSD,ETHUSD) evaluable={len(ctl)}/30")
for floor in (1,5):
    for rule in ("parent","gated"):
        print(f"floor>={floor} {rule:6s} FULL {int((ev[rule]>=floor).sum())}/{len(ev)}"
              f"   CONTROL {int((ctl[rule]>=floor).sum())}/{len(ctl)}")
print("totals: parent",int(ev["parent"].sum()),"gated",int(ev["gated"].sum()))
```

Verbatim output:

```
total slots=285  evaluable=178  insufficient_history=107
control(BTCUSD,ETHUSD) evaluable=30/30
floor>=1 parent FULL 175/178   CONTROL 29/30
floor>=1 gated  FULL 120/178   CONTROL 19/30
floor>=5 parent FULL 80/178   CONTROL 13/30
floor>=5 gated  FULL 3/178   CONTROL 1/30
totals: parent 799 gated 209
```

---

## Step 5 — Floor-clearing result

### The two conflicting floors (both reported, neither chosen)

**Floor A = 1.** `strategy-research/protocols/ts_trend_daily_v1.json:132`:

```
    "min_trade_count_gte": 1,
```

Its own rationale, `ts_trend_daily_v1.json:11`: *"Revised to 1 (at least one completed
round-trip required for a window to count as evaluable), matching the LOWER end of the
brief a-priori expectation (10-25 transitions / 15 windows =~ 0.7-1.7/window). This is a
pre-registered floor, not tuned to the shakedown observed values."*

**Floor B = 5.** `strategy-research/config/campaign_config.yaml:120`:

```
  trade_floor_per_window: 5      # per-window "sparse" threshold (A3.4 gate)
```

Floor B is the one actually applied to this hypothesis in the campaign record —
`config/campaign_queue.yaml:18` and `campaign_knowledge_base.yaml:944` both report the
archived P4 gated run as *"29/30 window-symbols below the A3.4 five-trade floor."*

These two are in direct conflict for the same per-window quantity. **Choosing between
them is the director's call; this probe reports both.**

### The four combinations

Denominator is **evaluable slots only**; insufficient-history slots are excluded, not
counted as failures.

| Rule | Floor | FULL UNIVERSE (19 sym) | CONTROL (BTCUSD, ETHUSD) |
|---|---|---|---|
| PARENT | ≥1 | **175 / 178** (98.3%) | **29 / 30** (96.7%) |
| GATED  | ≥1 | **120 / 178** (67.4%) | **19 / 30** (63.3%) |
| PARENT | ≥5 | **80 / 178** (44.9%) | **13 / 30** (43.3%) |
| GATED  | ≥5 | **3 / 178** (1.7%) | **1 / 30** (3.3%) |

### Control-vs-archive correspondence

The gated/floor-5 control gives 1/30 clearing, i.e. **29/30 below the five-trade
floor** — numerically identical to the archived run's recorded
`29/30 window-symbols below the A3.4 five-trade floor`
(`campaign_queue.yaml:18`, `campaign_knowledge_base.yaml:944`).

**Do not over-read this.** It is a correspondence on a *different venue and a different
quote asset* (Kraken BTCUSD/ETHUSD spot here; the archived run was Binance
BTCUSDT/ETHUSDT). It is a sanity check that this probe's rule reimplementation is
behaving like the committed component, and it weakens the possibility that the archived
sparsity was a Binance-data artifact. It is **not** a reproduction of that run, and the
"like-for-like control" label should be read with that instrument mismatch attached.

---

## Step 6 — What this establishes and what it does not

### Does breadth lift density above each candidate floor?

**Under Floor A (≥1): yes for the parent, and it was never really in question.**
175/178 evaluable slots clear it. The parent rule fires 1–13 times per window-symbol,
median ~4. Even the gated variant clears Floor A in 120/178 slots. Breadth is not what
achieves this — single-symbol BTC/ETH already clears 29/30. Floor A is simply a very
low bar.

**Under Floor B (≥5): NO. Breadth does not rescue this, and for the gated variant it is
not close.**

- Parent: 80/178 = 44.9% of evaluable slots. Going from 2 symbols to 19 moved the rate
  from 43.3% to 44.9% — a 1.6-point change. **Breadth added slots, not density.**
- Gated: **3/178 = 1.7%**. Across nineteen symbols and fifteen windows, exactly three
  window-symbol slots produce five or more gated entries — and they share no symbol and
  no window:

  | Slot | parent entries | gated entries |
  |---|---|---|
  | ETHUSD / 2022-10 | 5 | 5 |
  | XRPUSD / 2018-04 | 5 | 5 |
  | ZECUSD / 2024-04 | 10 | 6 |

  The maximum gated count in any evaluable slot in the entire panel is **6**. Two of the
  three qualify only because the gate happened to reject nothing at all in that slot.

This is the answer to the question the probe was dispatched to settle, stated plainly:
**breadth does not clear the five-trade floor for the gated variant.** The gate removes
74% of parent entries (799 → 209), and no amount of adding symbols compensates, because
the sparsity is not a small-universe artifact — it is a property of how rarely the
conjunction (SMA cross-up AND ER(20) ≥ 0.30) occurs per symbol-half-year. Nineteen
symbols reproduce the two-symbol rate almost exactly.

### Where does residual sparsity concentrate?

**It is spread, not concentrated — which is the more damaging finding.** If sparsity had
localised in a few illiquid symbols or a few dead windows, dropping them would be a
legitimate fix. It does not:

- **By symbol:** `g≥5` is zero for 16 of 19 symbols, including the two deepest-history
  majors (BTCUSD 0/15, LTCUSD 0/15, XMRUSD 0/15). The three symbols with any qualifying
  slot have exactly one each. There is no subset of symbols to keep.
- **By window:** `g≥5` is 0 in 12 of 15 windows and 1 in the other three. Windows with
  strong parent density (2025-04: 114 parent entries, 14/19 slots at p≥5) still produce
  **zero** gated slots at ≥5. There is no era to restrict to.
- **Parent sparsity is milder and does have structure** — XMRUSD (11/15 at p≥5) and
  ETHUSD/LTCUSD/XRPUSD (7/15) carry it, while AVAXUSD (1/6) and ADAUSD (3/12) are thin,
  and the early windows (2018-10, 2019-04) are thinnest. But even the best symbol clears
  Floor B in only 11 of 15 windows.

**Insufficient-history is a separate, large problem for breadth.** 107 of 285 slots
(37.5%) are insufficient-history, overwhelmingly in the early windows: 13 of 19 symbols
are unevaluable in each of 2018-04, 2018-10, and 2019-04, versus 0 in 2025-04. So the
breadth this archive provides is heavily back-loaded — the extra symbols contribute
mostly to the recent half of the panel, where they are most correlated with each other
and add the least independent information. Correlation-adjusted breadth (which the
parent brief `research_brief_P4_ts_trend.md:41` requires) would discount these further;
that adjustment was **not** computed here.

### What this does NOT establish

- **Entry counts are not evidence of edge.** Nothing here says whether P4, gated or
  ungated, makes or loses money. A rule that fires often can be worthless and a rule
  that fires rarely can be excellent. This probe only measures whether enough events
  exist to *evaluate* the question at the campaign's stated per-window floor.
- **No performance statistic of any kind was computed.** No return, P&L, Sharpe,
  expectancy, drawdown, cost, win rate, or IC. The hypothesis remains unregistered on
  this data and this probe has not contaminated a future pre-registration.
- These counts are **entry transitions**, not completed round-trips. Floor A's own
  wording is "at least one completed round-trip"; an entry near a window's right edge
  may not close inside it. Completed-round-trip counts would be **≤** these figures, so
  every floor-clearing number above is an **upper bound**. This makes the negative
  finding stronger, not weaker.
- This is Kraken spot USD data. The archived P4 runs were Binance USDT. Cross-venue
  agreement on the control is reassuring but is not a like-for-like replication.
- The BTCUSD/DOGEUSD ticker aliases (Step 3) are my mapping decision, flagged for
  override. Excluding both leaves 17 symbols and removes BTC from the control.

### Bottom line

The parent rule has adequate density under Floor A and marginal density under Floor B
(45% of slots). **The gated variant does not have enough entries to be evaluated at a
five-trade-per-window floor on any universe available here — 3 qualifying slots out of
178 — and adding seventeen symbols to the original two did not change that rate.** If
Floor B is the governing floor, breadth is not the unblock for P4_ts_trend_r1_er_gate.
If Floor A governs, the gated variant is evaluable in 120/178 slots and the density
question is not the blocker.

---

## Compliance record

- Files written: **1** — this file. No other path was written, including no temp or
  scratch file (all computation was piped to `python` via stdin and held in memory).
- No git commit. No edit to the knowledge base, campaign queue, protocols, tools, briefs,
  or the price cache. Nothing ingested. Archive read in place, read-only.
- No bar dated ≥ 2026-01-01 loaded, counted, or reported; archive's own end is
  2025-12-31.
- No return, P&L, Sharpe, expectancy, drawdown, or cost figure computed or reported.
