"""E-068 slice 1 (CUL-386): the claim test engine.

Measures an idea's CLAIM on the bars a backtest already saved (`bars.csv`).
A test is one sentence built from four slots
(engineering/roadmap/E-068/DESIGN_PROPOSAL.md section 3):

    On these bars (SELECTOR), what happens next (OUTCOME) is different from
    these other bars (BASELINE), measured like this (STATISTIC).

In the campaign (flag orchestrator.claim_tests.enabled), slice 2 uses
check_spec/spec_hash and slice 3 (tools/claim_measure.py) uses effect_sizes
only: no p-value or verdict is ever computed inside a run (CUL-394). The CLI
reads bars.csv (plus read-only warm-up rows from the data cache) and writes one
YAML file; it never writes into a run directory.

PARKED (CUL-394, D-077 -- operator, delivery plan v26 cont. 2 section 9 item 1):
THE VERDICT PATH. The running pipeline has no verdict on a claim: it shows the
number only. Everything below that exists to grade a claim -- the significance
methods (the SIGNIFICANCE section below, SIGNIFICANCE_METHODS, `_graded`, `_a851a_horizon`, `fake_window` and the
null it builds), the VERDICT rule and `combine`, `run_test(calibrated=True)`,
the calibration gate (CALIBRATION_GATE, `judge_calibration_row`,
`passed_calibrations`, `calibration_for`, tools/claim_tests_calibration.py)
and the grading CLI (`grade_claim_file`, `main`) -- is kept as code and kept
tested, but no run, reader or document of the running pipeline calls it or
speaks of its verdict. The real pass/fail is unchanged: the profit bars, the
count of all attempts, and the holdout. Un-parking is a new operator decision.

Blocks (v1, 17):
  selectors   all, event, regime, regime_change, calendar, quantile
  outcomes    fwd_return, fwd_volatility, fwd_max_drawdown, trend_ends
  baselines   complement, placebo, other_selector   (rank_ic takes none)
  statistics  mean_diff, rank_ic, hit_rate, decay_curve

GATED trade-level family (E-075 PR-3, CUL-420; see the "Trade-level tests"
section below): selector `trade {where: [...]}`, outcomes trade_net_return and
post_exit_return, baseline other_trades, statistics mean_diff | hit_rate. It is
not in the lists above, check_spec / check_claim refuse it unless the caller
passes trade_tests=True, and nothing in the pipeline does yet.

Block definitions (fixed in tasks/todo.md before any code):
  fwd_return(h)        close[t+h] / close[t] - 1
  fwd_volatility(h)    sample std (ddof=1) of the h one-bar log returns in (t, t+h]; h >= 2
  fwd_max_drawdown(h)  min over (t, t+h] of close / close[t] - 1
  trend_ends(h)        1.0 if the sign of the forward h-bar return is opposite to
                       the sign of the trailing h-bar return (close[t]/close[t-h]-1),
                       0.0 if the same; undefined if either is missing or exactly 0
  mean_diff            mean outcome on the selected bars minus the baseline's mean
  rank_ic              Spearman rank correlation of the bar-t `forecast` with the
                       outcome, on the selected bars (no baseline)
  hit_rate             share of selected bars whose outcome points the claimed way
                       (> 0 for `greater`, < 0 for `less`) minus the baseline's share
  decay_curve          mean_diff at each horizon, reported as a curve with its peak

WHY THIS CANNOT LEAK (no lookahead):
  - Selectors read only bar-t fields: `forecast` and `close` at t (BAR_T_FIELDS),
    `regime` at t and t-1, and the timestamp. check_spec refuses any other field.
  - `past_return` (field, with `bars: n`) is close[t] / close[t-n] - 1: rows
    t-n .. t only, the move that ENDED at t. It is defined only where the bar
    stamped ts[t] - n*step is in the SAME window and all n bars are present
    (row distance exactly n); NaN otherwise, including the first n bars of
    every window. No warm-up rows, nothing chained across windows.
  - `trailing_vol` (E-074 slice 1, field with `bars: n`, n >= 2; GATED: not in
    BAR_T_FIELDS, accepted only by check_spec(..., extra_fields=...)) is the
    sample std (ddof=1) of the n one-bar log returns ending at t: rows
    t-n .. t only, under exactly the `past_return` rule (bar ts[t] - n*step in
    the SAME window, row distance exactly n); NaN otherwise, including the
    first n bars of every window. No warm-up rows (`Window.warm` is never read).
  - `quantile` compares x[t] with the quantile of the TRAILING `lookback` bars
    t-lookback .. t-1 of the same window -- never a whole-sample quantile.
  - Outcomes are the label (the future); they never feed a selector. They are
    matched by TIMESTAMP: t+h exists only if a bar is stamped exactly
    ts[t] + h*step in the SAME window; nothing is chained across windows.
  - Warm-up rows are read from the cache only BEFORE a window's first bar; the
    reader stops at that timestamp, so no later row is ever parsed.

OPERATOR RULES (2026-10-03, the lesson of the deleted signal prescreen, E-039):
  1. The claim test only ever runs AFTER a completed backtest, on its saved
     bars. It never gates, skips or kills a backtest.
  2. claim_status is INFORMATION ONLY. It never changes idea_status, never
     routes, never bans (D-055).
  3. No verdict without a passed calibration gate: run_test(calibrated=False)
     returns effect sizes and status `method_not_calibrated`, never a guess.
  4. Existing or standard methods first; new statistics code kept minimal.

SIGNIFICANCE (amendment 3). Retired after failing the calibration gate: a
circular shift of the signal, a block-adjusted analytic p, and a bootstrap
drawing chunks WITH replacement. Two candidates remain:
  A `a851a_episode_v1` -- the existing tools/episode_significance.py
    (A8.5.1a), unchanged. Its statistic is the pooled rank IC of forecast vs
    forward return AMONG THE EVENT BARS (claimed: > 0), not the spec's own.
  B `block_permutation_v1` -- a world with no edge rebuilt from each window's
    own bar units (log return, log high/close, log low/close): rotated by a
    random phase, cut into blocks of B bars (5 daily, 24 hourly), blocks put
    in random order WITHOUT replacement; path rebuilt from the last real close
    before the window; the signal RECOMPUTED on real warm-up + fake window with
    the variant's own component (SIGNALS: vectorized copies of update(),
    proven equal by a test); selectors, baselines and outcomes recomputed.
    One-sided p = (1 + #{fake >= real}) / (1 + N). Before grading, the signal
    recomputed on the REAL path must equal the saved forecast
    (FORECAST_TOLERANCE), else stop. Regime selectors are refused.
  The method used is the one that passed tools/claim_tests_calibration.py.
  The gate is ONE-SIDED (amendment 5): flattering (above the ceiling) fails;
  too strict (below the floor) passes, reported as "conservative".

VERDICT (amendment 3, section 3), floor met at every horizon:
  refuted       at any horizon, the opposite-direction effect is itself
                significant (p_value_opposite < alpha)
  supported     right direction and p < alpha at every horizon, sign rule met
  inconclusive  everything else (a non-significant wrong-way wobble included)
  A weak result, either way, is not stored as a fact.

FLOORS name their unit: min_events, min_windows, min_eras, min_blocks. Below
any floor, at any horizon, the result is `inconclusive`, never a pass.
min_blocks counts independent h-bar blocks of SELECTED bars; it is a true
sample size only for a dense selector (`all`). For a sparse event selector it
counts events // h, so prefer min_events there.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from collections import deque
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))           # strategy-research/tools/
_TBOT = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "trading-bot")
for _p in (_HERE, _TBOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from performance.signal_statistics import gap_aware_active_block_count  # noqa: E402
import episode_significance as _es  # noqa: E402

# A8.5.1a's own settings (kept in sync with config/campaign_config.yaml
# episode_significance by tests/test_campaign_config_sync.py).
A851A_SETTINGS = {"gap_bars": _es._DEFAULT_GAP_BARS,
                  "density_fallback_pct": _es._DEFAULT_DENSITY_FALLBACK_PCT,
                  "min_n_episodes": _es._MIN_N_EPISODES,
                  "n_resamples": _es._DEFAULT_N_RESAMPLES}

# Which blocks have been run on real backtest output (the run_065/run_066
# re-grade, E-068 slice 1). Every other block is tested on synthetic data only.
EXERCISED_ON_REAL_RUNS = frozenset({
    "selector:all", "selector:event", "outcome:fwd_return",
    "baseline:complement", "statistic:mean_diff", "statistic:rank_ic",
})

# numeric fields a selector may read. `past_return` (E-068 3b) is the move
# that ENDED at bar t: close[t] / close[t-bars] - 1, with its required `bars`.
BAR_T_FIELDS = ("forecast", "close", "past_return")
FIELDS_WITH_BARS = ("past_return",)            # fields that take (and need) `bars: n`
# E-074 slice 1 (engineering/roadmap/E-074/PHASE_A.md 1.3 item 1): bar-t fields
# that exist but are NOT in BAR_T_FIELDS, so check_spec refuses them by default
# and every flag-off message, prompt and guide is unchanged. A caller accepts
# them only by passing them as check_spec(spec, extra_fields=...); the
# exploration digest (E-074) does, and the readers' exposure is wired behind
# orchestrator.exploration_digest.enabled (E-074 slice 4). All take `bars: n`.
GATED_BAR_T_FIELDS = ("trailing_vol",)
MIN_FIELD_BARS = {"past_return": 1, "trailing_vol": 2}   # ddof=1 needs >= 2 returns
# PHASE_A table 2.1: the digest's `trailing_vol` length per timeframe.
TRAILING_VOL_BARS = {"hourly": 24, "daily": 10}
DIRECTIONS = ("greater", "less")
FLOOR_UNITS = ("min_events", "min_windows", "min_eras", "min_blocks")
CONSISTENCY_UNITS = ("window", "era")
SIGNIFICANCE_METHOD = "block_permutation_v1"          # method B (amendment 3, 4B)
A851A_METHOD = "a851a_episode_v1"                      # method A: existing A8.5.1a, unchanged
# Amendment 4: A8.5.1a with its episode gap expressed in TIME, as its own
# pre-registration states it ("48 bars @ 1h ~= 2 days"): 2 days / bar step,
# i.e. 2 bars daily, 48 bars hourly (unchanged). Every other rule unchanged.
A851A_TIMEGAP_METHOD = "a851a_episode_timegap_v1"
A851A_GAP_SECONDS = 2 * 86400
A851A_METHODS = (A851A_METHOD, A851A_TIMEGAP_METHOD)
SIGNIFICANCE_METHODS = (SIGNIFICANCE_METHOD, A851A_METHOD, A851A_TIMEGAP_METHOD)
DEFAULT_SIGNIFICANCE = {"method": SIGNIFICANCE_METHOD, "n_resamples": 1000, "seed": 20261003}
A851A_SEED = 20261003
# The calibration gate (amendment 3, section 5; ONE-SIDED since amendment 5).
# A calibration summary unlocks a verdict only if it carries exactly this gate,
# all its rows, and a scope that matches the graded variant (method, signal,
# cadence, statistic). Above the ceiling (flattering) is a fail; below the
# floor (too strict) is a pass with a "conservative" warning.
CALIBRATION_GATE = {"alpha": 0.05, "ceiling": 0.075, "floor_warning": 0.025,
                    "max_share_undefined": 0.05, "rule": "one_sided"}
CALIBRATION_ROWS = 8
CALIBRATION_HORIZONS = (1, 2, 3, 4, 5)   # every gate row must cover exactly these
CALIBRATION_N_SIMS = 400
_TF = {"daily": "1d", "hourly": "1h"}
NOT_RECOMPUTABLE_SELECTORS = ("regime", "regime_change")
PLACEBO_SEED = 20261003       # the placebo baseline's random dates (a baseline, not a p-value)
DAY = 86400
WARMUP_BARS = {"daily": 30, "hourly": 500}
BLOCK_BARS = {"daily": 5, "hourly": 24}
FORECAST_CLIP = 20.0
HOLDOUT_DIR_NAME = "holdout_sealed"
_OPS = {">=": np.greater_equal, ">": np.greater, "<=": np.less_equal,
        "<": np.less, "==": np.equal}


def _cadence(step: int) -> str:
    if step == DAY:
        return "daily"
    if step == 3600:
        return "hourly"
    raise ValueError(f"unsupported bar step {step}s (daily or hourly only)")


# ---------------------------------------------------------------------------
# Signals: vectorized copies of the components' update() (equality is tested)
# ---------------------------------------------------------------------------

def donchian_forecast(high, low, close, period: int, scaling_factor: float = 20.0):
    """DonchianBreakoutComponent.update(), every bar. NaN before ready."""
    from numpy.lib.stride_tricks import sliding_window_view
    close = np.asarray(close, dtype=float)
    out = np.full(len(close), np.nan)
    if len(close) < period:
        return out
    win = sliding_window_view(close, period)
    hi, lo = win.max(axis=1), win.min(axis=1)
    cur = close[period - 1:]
    rng_ = hi - lo
    pos = np.where(rng_ == 0, 0.5, (cur - lo) / np.where(rng_ == 0, 1.0, rng_))
    out[period - 1:] = (pos * 2.0 - 1.0) * scaling_factor
    return out


def keltner_forecast(high, low, close, ema_period: int = 20, atr_period: int = 20,
                     atr_multiplier: float = 1.5, scaling_factor: float = 20.0):
    """KeltnerBreakoutComponent.update() over the full history, every bar.
    NaN before ready (max(ema_period, atr_period) + 1 bars)."""
    import pandas as pd
    close = np.asarray(close, dtype=float)
    c = pd.Series(close)
    tr = pd.concat([pd.Series(np.asarray(high) - np.asarray(low)),
                    (pd.Series(high) - c.shift(1)).abs(),
                    (pd.Series(low) - c.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(window=atr_period).mean().to_numpy()
    ema = c.ewm(span=ema_period, adjust=False).mean().to_numpy()
    band = atr_multiplier * atr
    ok = band > 0
    osc = np.where(ok, (close - ema) / np.where(ok, band, 1.0), 0.0)
    out = np.clip(osc, -1.2, 1.2) * scaling_factor
    out[:max(ema_period, atr_period)] = np.nan
    return out


SIGNALS = {"DonchianBreakoutComponent": donchian_forecast,
           "KeltnerBreakoutComponent": keltner_forecast}
FORECAST_TOLERANCE = {"DonchianBreakoutComponent": 1e-6, "KeltnerBreakoutComponent": 0.05}


def compute_signal(signal: dict, high, low, close) -> np.ndarray:
    fn = SIGNALS[signal["class"]]
    return np.clip(fn(high, low, close, **signal["params"]), -FORECAST_CLIP, FORECAST_CLIP)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass
class Window:
    """One backtest window of one symbol, bar-ordered, timestamps unique.
    `high`/`low` default to `close`; `warm` holds real bars before the window
    (close/high/low arrays) and `signal` the component that made `forecast`;
    both are needed only to build the null."""
    symbol: str
    window: str
    ts: np.ndarray            # int64 epoch seconds, UTC, strictly increasing
    close: np.ndarray         # float
    forecast: np.ndarray      # float, NaN allowed
    regime: np.ndarray        # object (str)
    step: int                 # seconds between bars
    source: str = ""
    sha256: str = ""
    high: np.ndarray | None = None
    low: np.ndarray | None = None
    warm: dict | None = None
    signal: dict | None = None

    def __post_init__(self):
        n = len(self.ts)
        if self.high is None:
            self.high = np.asarray(self.close, dtype=float).copy()
        if self.low is None:
            self.low = np.asarray(self.close, dtype=float).copy()
        if not (len(self.close) == len(self.forecast) == len(self.regime)
                == len(self.high) == len(self.low) == n):
            raise ValueError(f"{self.label}: column lengths differ")
        if n > 1 and not np.all(np.diff(self.ts) > 0):
            raise ValueError(f"{self.label}: timestamps not strictly increasing")
        if self.step <= 0:
            raise ValueError(f"{self.label}: step must be > 0")

    @property
    def label(self) -> str:
        return f"{self.symbol}/{self.window}"

    def index_at(self, offset_steps: int) -> np.ndarray:
        """For each bar t, the row whose timestamp is ts[t] + offset_steps*step,
        or -1 if no such bar exists in this window (timestamp matching)."""
        target = self.ts + offset_steps * self.step
        idx = np.searchsorted(self.ts, target)
        ok = (idx < len(self.ts)) & (idx >= 0)
        out = np.full(len(self.ts), -1, dtype=np.int64)
        hit = np.zeros(len(self.ts), dtype=bool)
        hit[ok] = self.ts[idx[ok]] == target[ok]
        out[hit] = idx[hit]
        return out


def _parse_ts(values: list[str]) -> np.ndarray:
    import pandas as pd
    parsed = pd.to_datetime(pd.Series(values), utc=True)
    # whole seconds since the epoch, whatever time unit pandas stores (E-068
    # slice 3 review: astype("int64") // 10**9 assumed nanoseconds)
    seconds = (parsed - pd.Timestamp(0, tz="UTC")).dt.total_seconds().to_numpy()
    return np.floor(seconds).astype(np.int64)


def _float(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


def read_bars_csv(path: Path, symbol: str, window: str) -> Window:
    raw = Path(path).read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    if len(rows) < 2:
        raise ValueError(f"{path}: fewer than 2 bars")
    ts = _parse_ts([r["timestamp"] for r in rows])
    step = int(np.median(np.diff(ts)))
    close = np.array([_float(r["close"]) for r in rows])
    has_hl = "high" in rows[0] and "low" in rows[0]
    return Window(symbol=symbol, window=window, ts=ts, close=close,
                  forecast=np.array([_float(r.get("forecast")) for r in rows]),
                  regime=np.array([r.get("regime") or "" for r in rows], dtype=object),
                  step=step, source=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                  high=np.array([_float(r["high"]) for r in rows]) if has_hl else None,
                  low=np.array([_float(r["low"]) for r in rows]) if has_hl else None)


def read_warmup(cache_path: Path, first_ts: int, step: int, n_bars: int) -> dict:
    """The last `n_bars` cache rows strictly BEFORE `first_ts` (read only; the
    reader stops at the first row at or after `first_ts`, so no later row is
    parsed). They must end exactly one step before the window and be gap-free."""
    import pandas as pd
    if HOLDOUT_DIR_NAME in Path(cache_path).resolve().parts:
        raise ValueError(f"refusing to read the holdout store: {cache_path}")
    keep: deque = deque(maxlen=n_bars)
    with open(cache_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_ts, i_h, i_l, i_c = (header.index(k) for k in ("timestamp", "high", "low", "close"))
        for row in reader:
            t = int(pd.Timestamp(row[i_ts], tz="UTC").timestamp())
            if t >= first_ts:
                break
            keep.append((t, float(row[i_h]), float(row[i_l]), float(row[i_c])))
    if len(keep) < n_bars:
        raise ValueError(f"{cache_path}: only {len(keep)} warm-up rows before the window")
    arr = np.array(keep)
    ts = arr[:, 0].astype(np.int64)
    if ts[-1] != first_ts - step or not np.all(np.diff(ts) == step):
        raise ValueError(f"{cache_path}: warm-up rows are not gap-free up to the window start")
    return {"ts": ts, "high": arr[:, 1], "low": arr[:, 2], "close": arr[:, 3]}


def graded_variants(run_dir: Path) -> tuple[list[str], list[str]]:
    """(graded, not_graded) variant ids: graded = has a protocol_result.yaml."""
    root = Path(run_dir) / "artifacts" / "variants"
    graded, not_graded = [], []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        (graded if (d / "protocol_result.yaml").exists() else not_graded).append(d.name)
    return graded, not_graded


def variant_signal(run_dir: Path, vid: str) -> dict:
    """The one component that made a variant's forecast, from its own
    strategy_config.json. Refused unless it is a single component with an
    identity transform and weight 1, whose class has a vectorized copy."""
    path = Path(run_dir) / "artifacts" / "variants" / vid / "strategy_config.json"
    cfg = json.loads(path.read_text(encoding="utf-8"))
    # Refuse any setting the null would not copy (amendment 3, section 7).
    problems = []
    top_extra = set(cfg) - {"regime_detector", "strategies"}
    if top_extra:
        problems.append(f"top-level keys {sorted(top_extra)}")
    rd = cfg.get("regime_detector") or {}
    if rd.get("components") or rd.get("rules"):
        problems.append("a gated regime detector (components or rules)")
    if set(cfg.get("strategies") or {}) - {"regimes"}:
        problems.append("strategies keys other than regimes")
    regimes = (cfg.get("strategies") or {}).get("regimes") or {}
    live = [r for r in regimes.values() if r]
    if len(live) != 1:
        problems.append(f"{len(live)} non-null regimes (need exactly 1)")
    for r in live:
        if set(r) - {"components"}:
            problems.append(f"regime keys {sorted(set(r) - {'components'})}")
        for c in r.get("components") or []:
            extra = set(c) - {"id", "class", "params", "weight", "transforms"}
            if extra:
                problems.append(f"component keys {sorted(extra)}")
    if problems:
        raise ValueError(f"{path}: settings the null does not copy: " + "; ".join(problems))
    comps = [c for r in live for c in r.get("components") or []]
    if len(comps) != 1:
        raise ValueError(f"{path}: {len(comps)} components; the null needs exactly one")
    c = comps[0]
    cls = c["class"].split(".")[-1]
    if cls not in SIGNALS:
        raise ValueError(f"{path}: no vectorized copy of {cls}; add it to SIGNALS first")
    if (c.get("transforms") or [{"op": "identity"}]) != [{"op": "identity"}] \
            or float(c.get("weight", 1.0)) != 1.0:
        raise ValueError(f"{path}: transforms/weight other than identity x 1 are not supported")
    return {"class": cls, "params": dict(c["params"])}


def load_variant_bars(run_dir: Path, vid: str, cache_path_for=None) -> list[Window]:
    """Same mapping as tools/build_reports.py::load_run_sources: each
    results[].run_id of artifacts/variants/<vid>/protocol_result.yaml points to
    variants/<vid>/results/<run_id>/bars.csv. A missing file is an error.
    With `cache_path_for(symbol, cadence) -> Path`, also attaches the variant's
    signal and the real warm-up rows needed by the null."""
    import yaml
    run_dir = Path(run_dir)
    pr_path = run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml"
    with open(pr_path, encoding="utf-8") as f:
        pr = yaml.safe_load(f) or {}
    signal = variant_signal(run_dir, vid) if cache_path_for is not None else None
    windows = []
    for entry in pr.get("results") or []:
        rid = entry.get("run_id")
        if not rid:
            continue
        bars = run_dir / "variants" / vid / "results" / str(rid) / "bars.csv"
        if not bars.exists():
            raise FileNotFoundError(f"{bars} (named by {pr_path})")
        w = read_bars_csv(bars, str(entry.get("symbol")), str(entry.get("window")))
        if cache_path_for is not None:
            cad = _cadence(w.step)
            w.warm = read_warmup(cache_path_for(w.symbol, cad), int(w.ts[0]), w.step,
                                 WARMUP_BARS[cad])
            w.signal = signal
        windows.append(w)
    if not windows:
        raise ValueError(f"{pr_path}: no results with a run_id")
    return windows


# ---------------------------------------------------------------------------
# Selectors: (window, params) -> (mask, valid). Bar t only.
# ---------------------------------------------------------------------------

def sel_all(w: Window, p: dict):
    n = len(w.ts)
    return np.ones(n, dtype=bool), np.ones(n, dtype=bool)


def past_return(w: Window, n: int) -> np.ndarray:
    """close[t] / close[t-n] - 1, defined ONLY where the bar stamped exactly
    ts[t] - n*step exists in this window AND all n bars in between are present
    (row distance t - k == n). NaN elsewhere -- the first n bars of every
    window included: no warm-up rows, nothing chained across windows. Reads
    rows t-n .. t only (the past)."""
    k = w.index_at(-int(n))
    t = np.arange(len(w.ts))
    ok = (k >= 0) & (t - k == int(n))
    r = np.full(len(w.ts), np.nan)
    r[ok] = w.close[ok] / w.close[k[ok]] - 1.0
    return r


def trailing_vol(w: Window, n: int) -> np.ndarray:
    """Sample std (ddof=1) of the n one-bar log returns ending at bar t,
    log(close[i] / close[i-1]) for i = t-n+1 .. t: rows t-n .. t only (the
    past). Defined ONLY where the bar stamped exactly ts[t] - n*step exists in
    this window AND all n bars in between are present (row distance t - k ==
    n), the `past_return` rule. NaN elsewhere -- the first n bars of every
    window included: no warm-up rows (`w.warm` is never read), nothing chained
    across windows. n >= 2 (one return has no sample std)."""
    from numpy.lib.stride_tricks import sliding_window_view
    n = int(n)
    if n < MIN_FIELD_BARS["trailing_vol"]:
        raise ValueError(f"trailing_vol needs bars >= {MIN_FIELD_BARS['trailing_vol']}, got {n}")
    m = len(w.ts)
    out = np.full(m, np.nan)
    if m <= n:
        return out
    k = w.index_at(-n)
    t = np.arange(m)
    ok = (k >= 0) & (t - k == n)
    lr = np.log(w.close[1:] / w.close[:-1])          # lr[i-1] = return INTO row i
    # window j holds the returns into rows j+1 .. j+n, i.e. it ends at row j+n
    sd = np.std(sliding_window_view(lr, n), axis=1, ddof=1)
    rows = np.arange(n, m)
    keep = ok[rows]
    out[rows[keep]] = sd[keep]
    return out


_FIELD_FUNCS = {"past_return": past_return, "trailing_vol": trailing_vol}


def _field_values(w: Window, sel: dict) -> np.ndarray:
    """The bar-t numbers a selector reads (BAR_T_FIELDS, GATED_BAR_T_FIELDS)."""
    f = sel["field"]
    if f in _FIELD_FUNCS:
        return _FIELD_FUNCS[f](w, int(sel["bars"]))
    return getattr(w, f).astype(float)


def sel_event(w: Window, p: dict):
    x = _field_values(w, p)
    valid = np.isfinite(x)
    mask = np.zeros(len(x), dtype=bool)
    mask[valid] = _OPS[p["op"]](x[valid], float(p["value"]))
    return mask, valid


def _regime_values(p: dict) -> set:
    v = p.get("values", p.get("value"))
    return set(v) if isinstance(v, list) else {v}


def sel_regime(w: Window, p: dict):
    valid = np.array([bool(r) for r in w.regime], dtype=bool)
    vals = _regime_values(p)
    mask = np.array([r in vals for r in w.regime], dtype=bool) & valid
    return mask, valid


def sel_regime_change(w: Window, p: dict):
    prev = w.index_at(-1)
    valid = (prev >= 0) & np.array([bool(r) for r in w.regime], dtype=bool)
    to = p["to"]
    mask = np.zeros(len(w.ts), dtype=bool)
    for t in np.nonzero(valid)[0]:
        mask[t] = w.regime[t] == to and w.regime[prev[t]] != to
    return mask, valid


def sel_calendar(w: Window, p: dict):
    days = w.ts // DAY
    weekday = (days + 3) % 7          # 1970-01-01 was a Thursday; Monday = 0
    hour = (w.ts % DAY) // 3600
    mask = np.ones(len(w.ts), dtype=bool)
    if p.get("weekdays") is not None:
        mask &= np.isin(weekday, list(p["weekdays"]))
    if p.get("hours") is not None:
        mask &= np.isin(hour, list(p["hours"]))
    return mask, np.ones(len(w.ts), dtype=bool)


def sel_quantile(w: Window, p: dict):
    """x[t] against the quantile of the trailing `lookback` bars t-lookback..t-1
    of this window (past only). The first `lookback` bars are not selectable."""
    x = _field_values(w, p)
    L, q, top = int(p["lookback"]), float(p["q"]), p["side"] == "top"
    n = len(x)
    mask = np.zeros(n, dtype=bool)
    valid = np.zeros(n, dtype=bool)
    for t in range(L, n):
        past = x[t - L:t]
        if not np.isfinite(x[t]) or not np.all(np.isfinite(past)):
            continue
        valid[t] = True
        thr = np.quantile(past, 1.0 - q if top else q)
        mask[t] = x[t] >= thr if top else x[t] <= thr
    return mask, valid


SELECTORS = {"all": sel_all, "event": sel_event, "regime": sel_regime,
             "regime_change": sel_regime_change, "calendar": sel_calendar,
             "quantile": sel_quantile}


# ---------------------------------------------------------------------------
# Outcomes: (window, h) -> array, NaN where undefined. The future = the label.
# ---------------------------------------------------------------------------

def _path_rows(w: Window, h: int):
    """Rows t whose whole path (t, t+h] is present (timestamp-matched)."""
    j = w.index_at(h)
    ok = (j >= 0) & (j - np.arange(len(w.ts)) == h)
    return np.nonzero(ok)[0]


def out_fwd_return(w: Window, h: int):
    j = w.index_at(h)
    y = np.full(len(w.ts), np.nan)
    ok = j >= 0
    y[ok] = w.close[j[ok]] / w.close[ok] - 1.0
    return y


def out_fwd_vol(w: Window, h: int):
    y = np.full(len(w.ts), np.nan)
    lr = np.log(w.close[1:] / w.close[:-1])       # lr[i] = return from row i to i+1
    for t in _path_rows(w, h):
        y[t] = np.std(lr[t:t + h], ddof=1)
    return y


def out_fwd_mdd(w: Window, h: int):
    y = np.full(len(w.ts), np.nan)
    for t in _path_rows(w, h):
        y[t] = np.min(w.close[t + 1:t + h + 1] / w.close[t]) - 1.0
    return y


def out_trend_ends(w: Window, h: int):
    fwd = out_fwd_return(w, h)
    k = w.index_at(-h)
    past = np.full(len(w.ts), np.nan)
    ok = k >= 0
    past[ok] = w.close[ok] / w.close[k[ok]] - 1.0
    s = np.sign(fwd) * np.sign(past)
    y = np.full(len(w.ts), np.nan)
    good = np.isfinite(s) & (s != 0)
    y[good] = (s[good] < 0).astype(float)
    return y


OUTCOMES = {"fwd_return": out_fwd_return, "fwd_volatility": out_fwd_vol,
            "fwd_max_drawdown": out_fwd_mdd, "trend_ends": out_trend_ends}


# ---------------------------------------------------------------------------
# Baselines: -> reference weights (0 = not in the baseline)
# ---------------------------------------------------------------------------

def _shift_offsets(n: int, h_max: int, rng, size: int, period: int | None = None) -> np.ndarray:
    """Offsets in [h_max+1, n-h_max-1] for the placebo baseline. With `period`
    (calendar selectors), whole multiples of the period are excluded: shifting
    an hour-of-day selection by exactly 24 h gives back the same selection."""
    lo, hi = h_max + 1, n - h_max - 1
    allowed = np.arange(lo, hi + 1) if hi >= lo else np.arange(0)
    if period:
        allowed = allowed[allowed % period != 0]
    if len(allowed) == 0:
        raise ValueError(f"window of {n} bars is too short to shift by more than "
                         f"the longest horizon ({h_max}); need >= {2 * h_max + 2} bars")
    return rng.choice(allowed, size=size)


def _calendar_period(selector: dict, step: int) -> int | None:
    """Period of a calendar selection, in bars: a week if it names weekdays,
    else a day. None for every other selector."""
    if selector.get("kind") != "calendar":
        return None
    seconds = 7 * DAY if selector.get("weekdays") is not None else DAY
    return seconds // step if seconds % step == 0 else None


def base_complement(w, mask, valid, p, h_max, rng):
    return (valid & ~mask).astype(float)


def base_block_placebo(w, mask, valid, p, h_max, rng):
    """`n_draws` copies of the selection, each shifted circularly by more than
    the longest horizon: same number of bars, same clustering, other dates.
    (A reference set of bars, not a significance method.)"""
    wts = np.zeros(len(mask))
    for k in _shift_offsets(len(mask), h_max, rng, int(p.get("n_draws", 20)), p.get("_period")):
        wts += (np.roll(mask, k) & valid).astype(float)
    return wts


def base_other_selector(w, mask, valid, p, h_max, rng):
    sub = p["selector"]
    m2, v2 = SELECTORS[sub["kind"]](w, sub)
    return (m2 & v2 & valid & ~mask).astype(float)


BASELINES = {"complement": base_complement, "placebo": base_block_placebo,
             "other_selector": base_other_selector}


# ---------------------------------------------------------------------------
# Statistics: -> (raw value, claim-oriented value; > 0 supports the claim)
# ---------------------------------------------------------------------------

def rank_average(x: np.ndarray) -> np.ndarray:
    """Average ranks with ties (1-based), as signal_statistics.spearman_correlation."""
    sorter = np.argsort(x, kind="mergesort")
    inv = np.empty(len(x), dtype=np.int64)
    inv[sorter] = np.arange(len(x))
    xs = x[sorter]
    obs = np.r_[True, xs[1:] != xs[:-1]]
    dense = obs.cumsum()[inv]
    count = np.r_[np.nonzero(obs)[0], len(obs)]
    return 0.5 * (count[dense] + count[dense - 1] + 1)


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    """NaN (never a fabricated 0.0) when fewer than 3 points or a constant rank."""
    if len(x) < 3:
        return float("nan")
    rx, ry = rank_average(x), rank_average(y)
    rx, ry = rx - rx.mean(), ry - ry.mean()
    sx, sy = math.sqrt(float(rx @ rx) / len(rx)), math.sqrt(float(ry @ ry) / len(ry))
    if sx < 1e-10 or sy < 1e-10:
        return float("nan")
    return float(rx @ ry) / len(rx) / (sx * sy)


def _sign(direction: str) -> float:
    return 1.0 if direction == "greater" else -1.0


def _wmean(y, wts):
    ok = (wts > 0) & np.isfinite(y)
    s = wts[ok].sum()
    return float((wts[ok] * y[ok]).sum() / s) if s > 0 else float("nan")


def st_mean_diff(y, mask, wref, fc, direction):
    sel = mask & np.isfinite(y)
    if not sel.any():
        return float("nan"), float("nan")
    raw = float(y[sel].mean()) - _wmean(y, wref)
    return raw, raw * _sign(direction)


def st_hit_rate(y, mask, wref, fc, direction):
    sel = mask & np.isfinite(y)
    if not sel.any():
        return float("nan"), float("nan")
    hit = (y > 0) if direction == "greater" else (y < 0)
    hitf = np.where(np.isfinite(y), hit.astype(float), np.nan)
    raw = float(hitf[sel].mean()) - _wmean(hitf, wref)
    return raw, raw                      # already oriented to the claim


def st_rank_ic(y, mask, wref, fc, direction):
    sel = mask & np.isfinite(y) & np.isfinite(fc)
    raw = spearman(fc[sel], y[sel])
    return raw, raw * _sign(direction)


STATISTICS = {"mean_diff": st_mean_diff, "rank_ic": st_rank_ic,
              "hit_rate": st_hit_rate, "decay_curve": st_mean_diff}


# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TestSpec:
    __test__ = False                       # not a pytest class
    selector: dict
    outcome: dict
    baseline: dict | None
    statistic: str
    direction: str
    floor: dict
    alpha: float = 0.05
    consistency: dict | None = None
    significance: dict = field(default_factory=lambda: dict(DEFAULT_SIGNIFICANCE))

    @classmethod
    def from_dict(cls, d: dict) -> "TestSpec":
        known = {"selector", "outcome", "baseline", "statistic", "direction",
                 "floor", "alpha", "consistency", "significance"}
        unknown = set(d) - known - {"name"}
        if unknown:
            raise ValueError(f"unknown spec keys: {sorted(unknown)}")
        kw = {k: d[k] for k in known if k in d}
        if kw.get("significance") is None:
            kw.pop("significance", None)
        return cls(**kw)


def _canon(v):
    if isinstance(v, bool) or v is None or isinstance(v, str):
        return v
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, dict):
        return {str(k): _canon(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_canon(x) for x in v]
    raise TypeError(f"spec value of type {type(v).__name__} is not allowed")


def spec_hash(spec: TestSpec) -> str:
    """Identity of a test: sha256 of canonical JSON (keys sorted, numbers as
    floats, horizons sorted). Key order and 12 vs 12.0 do not change it."""
    d = asdict(spec)
    d["outcome"] = dict(d["outcome"], horizons=sorted(d["outcome"].get("horizons") or []))
    blob = json.dumps(_canon(d), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _check_selector(s, where: str, extra_fields: tuple = ()) -> list[str]:
    if not isinstance(s, dict) or s.get("kind") not in SELECTORS:
        return [f"{where}: unknown selector {s!r}; known: {sorted(SELECTORS)}"]
    # extra_fields == () (the default): exactly the pre-E-074 fields and messages
    fields = BAR_T_FIELDS + tuple(extra_fields)
    with_bars = FIELDS_WITH_BARS + tuple(extra_fields)    # every gated field takes `bars`
    k, e = s["kind"], []
    if k in NOT_RECOMPUTABLE_SELECTORS:
        e.append(f"{where}: {k} cannot be graded under {SIGNIFICANCE_METHOD} (regime labels "
                 f"cannot be recomputed on fake prices); park it as a test request")
    if k in ("event", "quantile") and s.get("field") not in fields:
        e.append(f"{where}: field {s.get('field')!r} is not a bar-t field "
                 f"(allowed: {list(fields)}); a selector may not read the future")
    if k in ("event", "quantile") and s.get("field") in with_bars:
        b, lo = s.get("bars"), MIN_FIELD_BARS[s.get("field")]
        if not isinstance(b, int) or isinstance(b, bool) or b < lo:
            what = ("the length of the past move" if s.get("field") == "past_return"
                    else "the number of one-bar returns")
            e.append(f"{where}: field {s.get('field')} needs `bars`: an int >= {lo} "
                     f"({what}, in bars of the card's timeframe)")
    elif "bars" in s:
        e.append(f"{where}: `bars` is only allowed with field {list(with_bars)}")
    if k == "event":
        if s.get("op") not in _OPS:
            e.append(f"{where}: op must be one of {list(_OPS)}")
        if not isinstance(s.get("value"), (int, float)) or isinstance(s.get("value"), bool):
            e.append(f"{where}: event value must be a number")
    if k == "quantile":
        if s.get("side") not in ("top", "bottom"):
            e.append(f"{where}: side must be top or bottom")
        q = s.get("q")
        if not isinstance(q, (int, float)) or not 0 < q <= 0.5:
            e.append(f"{where}: q must be in (0, 0.5]")
        if not isinstance(s.get("lookback"), int) or s["lookback"] < 2:
            e.append(f"{where}: lookback must be an int >= 2 (trailing bars)")
    if k == "regime" and s.get("value") is None and not s.get("values"):
        e.append(f"{where}: regime needs value or values")
    if k == "regime_change" and not s.get("to"):
        e.append(f"{where}: regime_change needs `to`")
    if k == "calendar":
        if s.get("weekdays") is None and s.get("hours") is None:
            e.append(f"{where}: calendar needs weekdays and/or hours")
        if any(d not in range(7) for d in s.get("weekdays") or []):
            e.append(f"{where}: weekdays are 0 (Monday) .. 6")
        if any(h not in range(24) for h in s.get("hours") or []):
            e.append(f"{where}: hours are 0 .. 23 (UTC)")
    return e


def check_spec(spec: TestSpec, extra_fields: tuple = (), trade_tests: bool = False) -> list[str]:
    """Static checks, before any data. Empty list = valid. `extra_fields`
    (E-074): gated bar-t fields this caller accepts on top of BAR_T_FIELDS,
    each from GATED_BAR_T_FIELDS (anything else raises); empty by default,
    so every default result is unchanged. `trade_tests` (E-075 PR-3): accept
    the gated trade-level family (selector `trade`, outcomes trade_net_return
    and post_exit_return, baseline other_trades); False by default, when a
    trade selector, outcome or baseline gets exactly the pre-PR-3 refusal."""
    extra_fields = tuple(extra_fields)
    bad = [f for f in extra_fields if f not in GATED_BAR_T_FIELDS]
    if bad:
        raise ValueError(f"extra_fields {bad} are not gated bar-t fields "
                         f"(known: {list(GATED_BAR_T_FIELDS)})")
    if trade_tests:
        is_trade = isinstance(spec.selector, dict) and spec.selector.get("kind") == TRADE_SELECTOR
        mixed = ((isinstance(spec.outcome, dict) and spec.outcome.get("kind") in TRADE_OUTCOMES)
                 or (isinstance(spec.baseline, dict)
                     and spec.baseline.get("kind") in TRADE_BASELINES))
        if is_trade:
            return _check_trade_head(spec) + _check_tail(spec)
        if mixed:
            return [f"selector: the trade outcomes {list(TRADE_OUTCOMES)} and the baseline "
                    f"{list(TRADE_BASELINES)} need a selector of kind {TRADE_SELECTOR!r}"]
    e = _check_selector(spec.selector, "selector", extra_fields)
    o = spec.outcome
    if not isinstance(o, dict) or o.get("kind") not in OUTCOMES:
        e.append(f"outcome: unknown {o!r}; known: {sorted(OUTCOMES)}")
    else:
        hs = o.get("horizons")
        if (not isinstance(hs, list) or not hs or len(set(hs)) != len(hs)
                or any(not isinstance(h, int) or isinstance(h, bool) or h < 1 for h in hs)):
            e.append("outcome: horizons must be a non-empty list of distinct ints >= 1")
        elif o["kind"] == "fwd_volatility" and min(hs) < 2:
            e.append("outcome: fwd_volatility needs horizons >= 2")
    if spec.statistic not in STATISTICS:
        e.append(f"statistic: unknown {spec.statistic!r}; known: {sorted(STATISTICS)}")
    if spec.statistic == "rank_ic":
        if spec.baseline is not None:
            e.append("baseline: rank_ic compares nothing; baseline must be null")
    elif not isinstance(spec.baseline, dict) or spec.baseline.get("kind") not in BASELINES:
        e.append(f"baseline: unknown {spec.baseline!r}; known: {sorted(BASELINES)}")
    elif spec.baseline["kind"] == "other_selector":
        e += _check_selector(spec.baseline.get("selector"), "baseline.selector", extra_fields)
    return e + _check_tail(spec)


def _check_tail(spec: TestSpec) -> list[str]:
    """The checks every test shares, whatever its selector: direction, floor,
    alpha, consistency, significance (moved verbatim out of check_spec)."""
    e: list[str] = []
    if spec.direction not in DIRECTIONS:
        e.append(f"direction must be one of {list(DIRECTIONS)}")
    if not isinstance(spec.floor, dict) or not spec.floor:
        e.append(f"floor: required, with units from {list(FLOOR_UNITS)}")
    else:
        for k, v in spec.floor.items():
            if k not in FLOOR_UNITS:
                e.append(f"floor: unknown unit {k!r}; known: {list(FLOOR_UNITS)}")
            elif not isinstance(v, int) or isinstance(v, bool) or v < 1:
                e.append(f"floor: {k} must be an int >= 1")
    if not isinstance(spec.alpha, (int, float)) or not 0 < spec.alpha < 1:
        e.append("alpha must be in (0, 1)")
    c = spec.consistency
    if c is not None and (not isinstance(c, dict) or c.get("unit") not in CONSISTENCY_UNITS
                          or not isinstance(c.get("min_same_sign"), int)
                          or c["min_same_sign"] < 1):
        e.append(f"consistency: needs unit in {list(CONSISTENCY_UNITS)} and min_same_sign >= 1")
    s = spec.significance
    if isinstance(s, dict) and set(s) == {"method"} and s["method"] in A851A_METHODS:
        pass
    elif (not isinstance(s, dict) or set(s) != {"method", "n_resamples", "seed"}
            or s.get("method") != SIGNIFICANCE_METHOD
            or not isinstance(s.get("n_resamples"), int) or s["n_resamples"] < 99
            or not isinstance(s.get("seed"), int)):
        e.append(f"significance: {{method: one of {list(A851A_METHODS)}}} or {{method: {SIGNIFICANCE_METHOD}, "
                 f"n_resamples >= 99, seed: int}} (earlier methods were retired, amendments 1-3)")
    return e


# ---------------------------------------------------------------------------
# Trade-level tests (E-075 PR-3, CUL-420): a GATED family
#
# On these TRADES (selector `trade`), what the trade returned or what the
# market did after its exit (outcome) is different from the OTHER trades
# (baseline `other_trades`), measured as mean_diff or hit_rate. A "trade" is
# one LIFO-matched lot of the run's trades.json (docs/DATA_DICTIONARY.md
# section 2): a partial reduction closes a lot, so several trades can share an
# entry bar and several can exit on one bar.
#
# Gated like E-074's GATED_BAR_T_FIELDS: check_spec / check_claim refuse all of
# it unless the caller passes trade_tests=True (nothing in the pipeline does
# yet), with exactly the pre-PR-3 refusal, so every default message, hash and
# artifact is unchanged. SELECTORS / OUTCOMES / BASELINES / STATISTICS are NOT
# extended (CLAIM_TESTS.md is pinned equal to them); the family has its own
# tables below and its guide is workflow_artifacts/skills/hypothesis-design/
# CLAIM_TESTS_TRADE.md, shown to no prompt in this PR.
#
# WHY THIS CANNOT LEAK (no lookahead):
#   - Entry-time selector fields (side, entry_hour, entry_weekday,
#     regime_at_entry, entry_forecast) read only the lot's own entry stamp, its
#     entry-bar row (bar-t, known at that close) and its side.
#   - The two exit-time DESCRIPTORS (exit_cause, holding_bars) describe what
#     the strategy did and are known only at the exit bar's close. A claim may
#     select on them; a rule built on a confirmed claim may act only on the
#     entry-time fields. exit_cause reads the lot's exit_forecast (exit bar's
#     close), the exit row's postRebalance_current_allocation (that bar's
#     fill) and whether the exit bar is the window's last bar (the window's
#     own length, not a market value).
#   - Outcomes are the label (the future). post_exit_return(h) reads the
#     exit bar's close and the close of the bar stamped exactly ts_exit +
#     h*step in the SAME window; no row later than that is read. It never
#     feeds a selector. trade_net_return is the lot's own result.
#   - Nothing is matched across windows; no warm-up rows, no data cache.
# ---------------------------------------------------------------------------

TRADE_SELECTOR = "trade"
TRADE_OUTCOMES = ("trade_net_return", "post_exit_return")
TRADE_BASELINES = ("other_trades",)
TRADE_STATISTICS = ("mean_diff", "hit_rate")
# The interim exit classifier (E-074 PHASE_A 4.2), in this order. Replaced by
# E-029's recorded decision when it exists; run_protocol's own exit_reason is
# NOT changed (CUL-417 / E-029).
EXIT_CAUSES = ("end_of_window", "flip", "to_zero", "reduction", "same_sign_flat", "unknown")
FLAT_EPS = 1e-6                    # |allocation| at or below this is flat (bars.csv has 6 decimals)
TRADE_SIDES = ("long", "short")
# the closed field list. Entry-time fields are known at the entry bar's close;
# the exit-time descriptors only at the exit bar's close.
TRADE_ENTRY_FIELDS = ("side", "entry_hour", "entry_weekday", "regime_at_entry", "entry_forecast")
TRADE_EXIT_FIELDS = ("exit_cause", "holding_bars")
TRADE_FIELDS = TRADE_EXIT_FIELDS + TRADE_ENTRY_FIELDS
_TRADE_CATEGORICAL = ("exit_cause", "side", "regime_at_entry")
_TRADE_NUMERIC = ("holding_bars", "entry_hour", "entry_weekday", "entry_forecast")
_TRADE_RANGE = {"entry_hour": (0, 23), "entry_weekday": (0, 6), "holding_bars": (0, None)}
TRADE_OPS = ("==", "!=", "in", ">=", ">", "<=", "<")
_TRADE_CAT_OPS = ("==", "!=", "in")
MAX_TRADE_CLAUSES = 4
_CMP = {">=": np.greater_equal, ">": np.greater, "<=": np.less_equal, "<": np.less,
        "==": np.equal, "!=": np.not_equal}


def classify_exit(side_sign: int, exit_forecast, post_alloc, exit_found: bool,
                  exit_is_last_bar: bool) -> str:
    """E-074 PHASE_A 4.2 for one lot. `side_sign` +1 (LONG) / -1 (SHORT);
    `exit_forecast`: the lot's exit forecast (None / NaN: unknown);
    `post_alloc`: the exit row's postRebalance_current_allocation (None / NaN:
    unknown); `exit_found`: the exit bar is a row of the window's bars.csv;
    `exit_is_last_bar`: that row is the window's LAST bar (timestamp equality,
    never the last calendar day -- run_protocol's date test labels a whole
    last day end_of_window, E-073 A5 / CUL-417).

      unknown          no exit row in bars.csv
      end_of_window    the exit bar is the window's last bar
      unknown          no exit_forecast
      flip             exit_forecast has the opposite sign to the lot's side
      to_zero          exit_forecast is exactly 0
      reduction        same sign, and the position is still open on that side
                       after the bar (a partial LIFO close by the rebalance)
      same_sign_flat   same sign, and flat after the bar (a gap large-tier
                       flatten looks like this; unexplained until E-029)
      unknown          anything else (allocation missing or on the other side)
    """
    if not exit_found:
        return "unknown"
    if exit_is_last_bar:
        return "end_of_window"
    if exit_forecast is None or not math.isfinite(float(exit_forecast)):
        return "unknown"
    s = side_sign * float(exit_forecast)
    if s < 0:
        return "flip"
    if s == 0:
        return "to_zero"
    if post_alloc is None or not math.isfinite(float(post_alloc)):
        return "unknown"
    a = side_sign * float(post_alloc)
    if a > FLAT_EPS:
        return "reduction"
    if abs(a) <= FLAT_EPS:
        return "same_sign_flat"
    return "unknown"


@dataclass
class TradeWindow:
    """One window's trades (rows of trades.json) beside its bars. Arrays are
    per trade, in trades.json order; `bars` is the window's Window."""
    bars: Window
    entry_ts: np.ndarray        # int64 epoch seconds
    exit_ts: np.ndarray
    side: np.ndarray            # object: "long" / "short"
    exit_cause: np.ndarray      # object, one of EXIT_CAUSES
    regime_at_entry: np.ndarray  # object (str; "" when absent)
    entry_forecast: np.ndarray  # float: the entry bar's forecast (bars.csv), NaN if no row
    entry_idx: np.ndarray       # int64 row in bars (-1: not found)
    exit_idx: np.ndarray
    net_return: np.ndarray      # float, a fraction (0.01 = 1%), NaN if missing
    basis: str = "net_of_fees_and_slippage"

    def __post_init__(self):
        n = len(self.entry_ts)
        if not all(len(a) == n for a in (self.exit_ts, self.side, self.exit_cause,
                                         self.regime_at_entry, self.entry_forecast,
                                         self.entry_idx, self.exit_idx, self.net_return)):
            raise ValueError(f"{self.bars.label}: trade column lengths differ")

    @property
    def symbol(self) -> str:
        return self.bars.symbol

    @property
    def window(self) -> str:
        return self.bars.window

    @property
    def label(self) -> str:
        return self.bars.label

    @property
    def step(self) -> int:
        return self.bars.step

    @property
    def ts(self) -> np.ndarray:           # the BARS' stamps (block counts)
        return self.bars.ts

    @property
    def n(self) -> int:
        return len(self.entry_ts)


def build_trade_window(bars: Window, trades: list, post_alloc: np.ndarray,
                       costs: list | None = None) -> TradeWindow:
    """Trade rows (trades.json dicts) + the window's bars -> a TradeWindow.
    `post_alloc[i]`: postRebalance_current_allocation of bars row i (NaN where
    absent). `costs`: this window's trade_diagnostics.json records, used only
    when they pair one-to-one with `trades` (same trade_id, in order) and every
    one carries gross_return_before_costs and cost_paid_all (CUL-414, flag
    --cost-bar-all-costs): then the net return is the all-costs basis, else
    trades.json's net_profit_loss_percent (after the commission; slippage is
    already inside the fill prices)."""
    n = len(trades)
    ent = _parse_ts([t["entry_time"] for t in trades]) if n else np.zeros(0, dtype=np.int64)
    ext = _parse_ts([t["exit_time"] for t in trades]) if n else np.zeros(0, dtype=np.int64)

    def rows_of(stamps):
        idx = np.searchsorted(bars.ts, stamps)
        ok = idx < len(bars.ts)
        hit = np.zeros(n, dtype=bool)
        hit[ok] = bars.ts[idx[ok]] == stamps[ok]
        return np.where(hit, idx, -1).astype(np.int64)

    ent_i, ext_i = rows_of(ent), rows_of(ext)
    side = np.empty(n, dtype=object)
    cause = np.empty(n, dtype=object)
    regime = np.empty(n, dtype=object)
    ef = np.full(n, np.nan)
    ret = np.full(n, np.nan)
    last_ts = int(bars.ts[-1])
    for i, t in enumerate(trades):
        sd = str(t.get("side", "")).upper()
        if sd not in ("LONG", "SHORT"):
            raise ValueError(f"{bars.label}: trade {t.get('trade_id')!r} has side "
                             f"{t.get('side')!r} (LONG or SHORT)")
        sign = 1 if sd == "LONG" else -1
        side[i] = sd.lower()
        regime[i] = str(t.get("entry_regime") or "")
        if ent_i[i] >= 0:
            ef[i] = bars.forecast[ent_i[i]]
        found = bool(ext_i[i] >= 0)
        cause[i] = classify_exit(sign, t.get("exit_forecast"),
                                 post_alloc[ext_i[i]] if found else None, found,
                                 found and int(ext[i]) == last_ts)
        v = t.get("net_profit_loss_percent")
        ret[i] = _float(v) / 100.0 if v is not None else np.nan
    basis = "net_of_fees_and_slippage"
    if (costs is not None and n and len(costs) == n
            and all(c.get("trade_id") == t.get("trade_id") for c, t in zip(costs, trades))
            and all(c.get("gross_return_before_costs") is not None
                    and c.get("cost_paid_all") is not None for c in costs)):
        # gross at the bar closes (%) minus fees + slippage of both legs (bps / 100 = %)
        ret = np.array([(float(c["gross_return_before_costs"]) - float(c["cost_paid_all"]) / 100.0)
                        / 100.0 for c in costs])
        basis = "all_costs"
    return TradeWindow(bars=bars, entry_ts=ent, exit_ts=ext, side=side, exit_cause=cause,
                       regime_at_entry=regime, entry_forecast=ef, entry_idx=ent_i,
                       exit_idx=ext_i, net_return=ret, basis=basis)


def _read_column(path: Path, name: str, n_rows: int) -> np.ndarray:
    rows = list(csv.DictReader(Path(path).read_bytes().decode("utf-8").splitlines()))
    if len(rows) != n_rows:
        raise ValueError(f"{path}: {len(rows)} rows, expected {n_rows}")
    return np.array([_float(r.get(name)) for r in rows])


def load_variant_trade_windows(run_dir: Path, vid: str) -> list[TradeWindow]:
    """Same window mapping as load_variant_bars (protocol_result.yaml results[]
    .run_id -> variants/<vid>/results/<run_id>/), reading each window's
    trades.json and bars.csv (and the variant's trade_diagnostics.json for the
    all-costs basis when it has it). A missing bars.csv or trades.json is an
    error, never an empty window."""
    import yaml
    run_dir = Path(run_dir)
    pr_path = run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml"
    with open(pr_path, encoding="utf-8") as f:
        pr = yaml.safe_load(f) or {}
    diag_path = run_dir / "variants" / vid / "trade_diagnostics.json"
    diag_by_window: dict = {}
    if diag_path.exists():
        for rec in (json.loads(diag_path.read_text(encoding="utf-8")).get("trades") or []):
            diag_by_window.setdefault(str(rec.get("window")), []).append(rec)
    out = []
    for entry in pr.get("results") or []:
        rid = entry.get("run_id")
        if not rid:
            continue
        rdir = run_dir / "variants" / vid / "results" / str(rid)
        for name in ("bars.csv", "trades.json"):
            if not (rdir / name).exists():
                raise FileNotFoundError(f"{rdir / name} (named by {pr_path})")
        w = read_bars_csv(rdir / "bars.csv", str(entry.get("symbol")), str(entry.get("window")))
        trades = json.loads((rdir / "trades.json").read_text(encoding="utf-8"))
        post = _read_column(rdir / "bars.csv", "postRebalance_current_allocation", len(w.ts))
        out.append(build_trade_window(w, trades, post, diag_by_window.get(w.window)))
    if not out:
        raise ValueError(f"{pr_path}: no results with a run_id")
    return out


def _trade_field(tw: TradeWindow, field_: str):
    """(values, valid) of one closed field over the window's trades."""
    n = tw.n
    if field_ == "exit_cause":
        return tw.exit_cause, np.ones(n, dtype=bool)
    if field_ == "side":
        return tw.side, np.ones(n, dtype=bool)
    if field_ == "regime_at_entry":
        return tw.regime_at_entry, np.array([bool(r) for r in tw.regime_at_entry], dtype=bool)
    if field_ == "holding_bars":
        return (tw.exit_ts - tw.entry_ts) // tw.step, np.ones(n, dtype=bool)
    if field_ == "entry_hour":
        return (tw.entry_ts % DAY) // 3600, np.ones(n, dtype=bool)
    if field_ == "entry_weekday":
        return ((tw.entry_ts // DAY) + 3) % 7, np.ones(n, dtype=bool)     # Monday = 0
    if field_ == "entry_forecast":
        return tw.entry_forecast, np.isfinite(tw.entry_forecast)
    raise ValueError(f"unknown trade field {field_!r}")


def sel_trade(tw: TradeWindow, p: dict):
    """(mask, valid) over the window's trades: every `where` clause must hold
    (AND). A trade whose field is missing is neither selected nor in the
    baseline."""
    mask = np.ones(tw.n, dtype=bool)
    valid = np.ones(tw.n, dtype=bool)
    for c in p["where"]:
        vals, ok = _trade_field(tw, c["field"])
        valid &= ok
        if c["field"] in _TRADE_CATEGORICAL:
            if c["op"] == "in":
                hit = np.array([v in c["value"] for v in vals], dtype=bool)
            else:
                eq = np.array([v == c["value"] for v in vals], dtype=bool)
                hit = eq if c["op"] == "==" else ~eq
        else:
            x = np.asarray(vals, dtype=float)
            hit = np.zeros(tw.n, dtype=bool)
            fin = ok & np.isfinite(x)
            if c["op"] == "in":
                hit[fin] = np.isin(x[fin], [float(v) for v in c["value"]])
            else:
                hit[fin] = _CMP[c["op"]](x[fin], float(c["value"]))
        mask &= hit
    return mask, valid


def trade_outcome(tw: TradeWindow, kind: str, h: int) -> np.ndarray:
    """Per-trade outcome, NaN where undefined. trade_net_return ignores h.
    post_exit_return: signed by side (positive = the market kept moving the
    trade's way), from the exit bar's close to the close of the bar stamped
    exactly ts_exit + h*step in this window; NaN when that bar does not exist
    (the window's end) or the exit bar is not a row."""
    if kind == "trade_net_return":
        return tw.net_return.copy()
    y = np.full(tw.n, np.nan)
    j_all = tw.bars.index_at(h)
    for i in range(tw.n):
        e = int(tw.exit_idx[i])
        if e < 0 or j_all[e] < 0:
            continue
        r = tw.bars.close[j_all[e]] / tw.bars.close[e] - 1.0
        y[i] = r if tw.side[i] == "long" else -r
    return y


def _check_trade_where(sel) -> list[str]:
    where = "selector"
    if not isinstance(sel, dict) or set(sel) != {"kind", "where"}:
        return [f"{where}: a trade selector is exactly {{kind: trade, where: [...]}}"]
    clauses = sel["where"]
    if (not isinstance(clauses, list) or not clauses
            or len(clauses) > MAX_TRADE_CLAUSES):
        return [f"{where}: where must be a list of 1 to {MAX_TRADE_CLAUSES} clauses "
                f"{{field, op, value}}, all of which must hold"]
    e = []
    for i, c in enumerate(clauses):
        w = f"{where}.where[{i}]"
        if not isinstance(c, dict) or set(c) != {"field", "op", "value"}:
            e.append(f"{w}: a clause is exactly {{field, op, value}}")
            continue
        f, op, v = c["field"], c["op"], c["value"]
        if f not in TRADE_FIELDS:
            e.append(f"{w}: field {f!r} is not a trade field (allowed: {list(TRADE_FIELDS)}); "
                     f"a selector may not read anything else")
            continue
        allowed_ops = _TRADE_CAT_OPS if f in _TRADE_CATEGORICAL else TRADE_OPS
        if op not in allowed_ops:
            e.append(f"{w}: op for {f} must be one of {list(allowed_ops)}")
            continue
        if op == "in" and (not isinstance(v, list) or not v or len(set(map(str, v))) != len(v)):
            e.append(f"{w}: `in` needs a non-empty list of distinct values")
            continue
        for x in (v if op == "in" else [v]):
            if f == "exit_cause" and x not in EXIT_CAUSES:
                e.append(f"{w}: exit_cause value {x!r} is not one of {list(EXIT_CAUSES)}")
            elif f == "side" and x not in TRADE_SIDES:
                e.append(f"{w}: side value {x!r} is not one of {list(TRADE_SIDES)}")
            elif f == "regime_at_entry" and (not isinstance(x, str) or not x.strip()):
                e.append(f"{w}: regime_at_entry value must be a non-empty label")
            elif f in _TRADE_NUMERIC:
                if not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x):
                    e.append(f"{w}: {f} value must be a number")
                elif f in _TRADE_RANGE:
                    lo, hi = _TRADE_RANGE[f]
                    if x < lo or (hi is not None and x > hi):
                        e.append(f"{w}: {f} must be in {lo}..{hi}, got {x!r}" if hi is not None
                                 else f"{w}: {f} must be >= {lo}, got {x!r}")
    return e


def _check_trade_head(spec: TestSpec) -> list[str]:
    """Selector / outcome / statistic / baseline checks of a trade test."""
    e = _check_trade_where(spec.selector)
    o = spec.outcome
    if not isinstance(o, dict) or o.get("kind") not in TRADE_OUTCOMES:
        e.append(f"outcome: a trade test needs one of {list(TRADE_OUTCOMES)}, got {o!r}")
    elif o["kind"] == "trade_net_return":
        if set(o) != {"kind"}:
            e.append("outcome: trade_net_return is the lot's own result: no horizons "
                     "(write {kind: trade_net_return})")
    else:
        hs = o.get("horizons")
        if set(o) - {"kind", "horizons"}:
            e.append("outcome: post_exit_return takes only `horizons`")
        elif (not isinstance(hs, list) or not hs or len(set(hs)) != len(hs)
                or any(not isinstance(h, int) or isinstance(h, bool) or h < 1 for h in hs)):
            e.append("outcome: horizons must be a non-empty list of distinct ints >= 1")
    if spec.statistic not in TRADE_STATISTICS:
        e.append(f"statistic: a trade test needs one of {list(TRADE_STATISTICS)}, "
                 f"got {spec.statistic!r}")
    if not isinstance(spec.baseline, dict) or spec.baseline != {"kind": "other_trades"}:
        e.append(f"baseline: a trade test needs {{kind: other_trades}}, got {spec.baseline!r}")
    return e


def _trade_horizons(spec: TestSpec) -> list:
    """The outcome's horizons; [0] (the trade's own life) for trade_net_return."""
    if spec.outcome["kind"] == "trade_net_return":
        return [0]
    return sorted(spec.outcome["horizons"])


def trade_effect_sizes(windows: list, spec: TestSpec, eras: list | None = None):
    """effect_sizes for the trade family: the same return shape (per-window
    prepared data, per-horizon effect sizes, horizons, rng) so claim_measure
    reads it unchanged. `windows` are TradeWindows. The pooled statistics are
    the bar statistics applied to per-trade arrays; per-window values are
    given exactly as for bar tests (the all-but-one-window rule is E-077
    PR-2's). n_events = selected trades with an outcome; n_blocks counts
    independent blocks of their entry bars (gap-aware, as for bars). Horizon 0
    is trade_net_return's: the trade's own life."""
    horizons = _trade_horizons(spec)
    stat = STATISTICS[spec.statistic]
    opposite = "less" if spec.direction == "greater" else "greater"
    per = []
    for tw in windows:
        mask, valid = sel_trade(tw, spec.selector)
        mask = mask & valid
        wref = (valid & ~mask).astype(float)
        ys = {h: trade_outcome(tw, spec.outcome["kind"], h) for h in horizons}
        era = None
        if eras is not None:
            from protocol_resolution import era_id_for_timestamp
            days = np.datetime_as_string(tw.entry_ts.astype("datetime64[s]"), unit="D")
            era = np.array([era_id_for_timestamp(str(d), eras) for d in days], dtype=object)
        per.append({"w": tw, "mask": mask, "wref": wref, "fc": np.full(tw.n, np.nan),
                    "ys": ys, "era": era})
    out_h = {}
    for h in horizons:
        y, m, wr, fc = _pooled(per, h)
        raw, oriented = stat(y, m, wr, fc, spec.direction)
        events = [p["mask"] & np.isfinite(p["ys"][h]) for p in per]
        active = []
        for ev, p in zip(events, per):
            a = np.zeros(len(p["w"].bars.ts), dtype=bool)
            rows = p["w"].entry_idx[ev]
            a[rows[rows >= 0]] = True
            active.append(a)
        per_window = {}
        for p in per:
            r, o = stat(p["ys"][h], p["mask"], p["wref"], p["fc"], spec.direction)
            per_window[p["w"].label] = {"value": _num(r), "oriented": _num(o)}
        per_era, n_eras = {}, None
        if eras is not None:
            era_all = np.concatenate([p["era"] for p in per])
            n_eras = len(set(era_all[np.concatenate(events)])) if len(era_all) else 0
            for e_id in sorted(set(era_all)):
                sub = era_all == e_id
                r, o = stat(y[sub], m[sub], wr[sub], fc[sub], spec.direction)
                per_era[e_id] = {"value": _num(r), "oriented": _num(o)}
        out_h[h] = {"value": _num(raw), "oriented": _num(oriented),
                    "oriented_opposite": _num(stat(y, m, wr, fc, opposite)[1]),
                    "p_value": None, "p_value_opposite": None,
                    "n_events": int(sum(ev.sum() for ev in events)),
                    "n_windows_with_events": int(sum(bool(ev.any()) for ev in events)),
                    "n_blocks": _blocks(active, per, max(h, 1)), "n_eras_with_events": n_eras,
                    "per_window": per_window, "per_era": per_era}
    return per, out_h, horizons, np.random.default_rng(PLACEBO_SEED)


# ---------------------------------------------------------------------------
# The null: fake windows with no edge, signal recomputed
# ---------------------------------------------------------------------------

def _full_path(w: Window, close, high, low):
    return (np.r_[w.warm["high"], high], np.r_[w.warm["low"], low],
            np.r_[w.warm["close"], close])


def forecast_check(w: Window) -> float:
    """Max |signal recomputed on the REAL path - saved forecast| over the
    window's bars. Must be within FORECAST_TOLERANCE before any grade."""
    fc = compute_signal(w.signal, *_full_path(w, w.close, w.high, w.low))[-len(w.ts):]
    ok = np.isfinite(w.forecast)
    if np.any(np.isnan(fc[ok])):
        return float("inf")
    return float(np.max(np.abs(fc[ok] - w.forecast[ok]))) if ok.any() else 0.0


def fake_window(w: Window, rng) -> Window:
    """One draw of the null (method B, amendment 3 section 4B): the window's
    own bar units, rotated by a random phase, cut into consecutive blocks of B
    bars and put in random order -- WITHOUT replacement, each unit used exactly
    once, like the real window. A path is rebuilt from the last real close
    before the window and the signal recomputed on real warm-up + fake window.
    Timestamps are kept."""
    n = len(w.ts)
    B = BLOCK_BARS[_cadence(w.step)]
    prev = np.r_[w.warm["close"][-1], w.close[:-1]]
    r = np.log(w.close / prev)
    lh, ll = np.log(w.high / w.close), np.log(w.low / w.close)
    rotated = (int(rng.integers(0, n)) + np.arange(n)) % n
    blocks = [rotated[k:k + B] for k in range(0, n, B)]
    idx = np.concatenate([blocks[i] for i in rng.permutation(len(blocks))])
    close = w.warm["close"][-1] * np.exp(np.cumsum(r[idx]))
    high, low = close * np.exp(lh[idx]), close * np.exp(ll[idx])
    fc = compute_signal(w.signal, *_full_path(w, close, high, low))[-n:]
    return replace(w, close=close, high=high, low=low, forecast=fc, source="", sha256="")


# ---------------------------------------------------------------------------
# Running a test
# ---------------------------------------------------------------------------

def _era_ids(w: Window, eras: list) -> np.ndarray:
    from protocol_resolution import era_id_for_timestamp
    days = np.datetime_as_string(w.ts.astype("datetime64[s]"), unit="D")
    return np.array([era_id_for_timestamp(str(d), eras) for d in days], dtype=object)


def _prepare(windows, spec, horizons, rng, eras=None) -> list[dict]:
    h_max = horizons[-1]
    per = []
    for w in windows:
        mask, valid = SELECTORS[spec.selector["kind"]](w, spec.selector)
        mask = mask & valid
        if spec.baseline is None:
            wref = np.zeros(len(w.ts))
        else:
            bp = dict(spec.baseline, _period=_calendar_period(spec.selector, w.step))
            wref = BASELINES[spec.baseline["kind"]](w, mask, valid, bp, h_max, rng)
        ys = {h: OUTCOMES[spec.outcome["kind"]](w, h) for h in horizons}
        per.append({"w": w, "mask": mask, "wref": wref, "fc": w.forecast, "ys": ys,
                    "era": _era_ids(w, eras) if eras is not None else None})
    return per


def _pooled(per, h):
    return (np.concatenate([p["ys"][h] for p in per]),
            np.concatenate([p["mask"] for p in per]),
            np.concatenate([p["wref"] for p in per]),
            np.concatenate([p["fc"] for p in per]))


def _blocks(active_by_window: list, per: list, h: int) -> int:
    return int(sum(
        gap_aware_active_block_count(
            [{"active": bool(a), "timestamp": int(t)} for a, t in zip(act, p["w"].ts)],
            block_size=h, expected_step=p["w"].step)
        for act, p in zip(active_by_window, per)))


def a851a_gap_bars(method: str, step: int) -> int:
    """A8.5.1a's episode gap in bars: the configured bar count (method A, as
    the pipeline passes it) or 2 days of bars (amendment 4)."""
    if method == A851A_TIMEGAP_METHOD:
        if A851A_GAP_SECONDS % step:
            raise ValueError(f"2 days is not a whole number of {step}s bars")
        return A851A_GAP_SECONDS // step
    return A851A_SETTINGS["gap_bars"]


def _a851a_horizon(per, h, method=A851A_METHOD):
    """Method A (`a851a_episode_v1`, amendment 3 section 4A): the existing
    tools/episode_significance.compute_a851a_significance, unchanged, fed the
    way tools/run_protocol._a851a_episode_significance feeds it. Its statistic
    is the pooled rank IC of forecast vs forward return AMONG THE EVENT BARS
    (not the spec's statistic). Claimed direction: IC > 0."""
    import pandas as pd
    import episode_significance as es
    from timeframe import bars_per_day
    eras = per[0]["eras_list"]
    records = []
    for p in per:
        w, y = p["w"], p["ys"][h]
        for t in range(len(w.ts)):
            if not np.isfinite(y[t]) or not np.isfinite(w.forecast[t]):
                continue
            records.append({"forecast": float(w.forecast[t]),
                            "next_return_bps": float(y[t]) * 1e4,
                            "active": bool(p["mask"][t]), "symbol": w.symbol,
                            "timestamp": pd.Timestamp(int(w.ts[t]), unit="s")})
    era_of = None
    if eras is not None:
        from protocol_resolution import era_id_for_timestamp

        def era_of(i, _r=records):
            return (_r[i]["symbol"], era_id_for_timestamp(_r[i]["timestamp"], eras))
    step = per[0]["w"].step
    cfg = A851A_SETTINGS
    res = es.compute_a851a_significance(
        records, era_of=era_of, gap_bars=a851a_gap_bars(method, step),
        density_fallback_pct=cfg["density_fallback_pct"],
        min_n_episodes=cfg["min_n_episodes"], block_size=bars_per_day(_TF[_cadence(step)]),
        n_resamples=cfg["n_resamples"], seed=A851A_SEED,
        expected_step=pd.Timedelta(step, unit="s"))
    ic, p2 = res.get("pooled_ic"), res.get("p_value")
    out = {"method_label": res.get("method"), "pooled_ic": ic, "n_episodes": res.get("n_episodes"),
           "density_pct": res.get("density_pct"), "p_value": None, "p_value_opposite": None}
    if ic is not None and p2 is not None:
        right = ic > 0
        out["p_value"] = float(p2 / 2 if right else 1 - p2 / 2)
        out["p_value_opposite"] = float(1 - p2 / 2 if right else p2 / 2)
    out["per_window"] = {}
    for p in per:
        sel = p["mask"] & np.isfinite(p["ys"][h]) & np.isfinite(p["w"].forecast)
        v = spearman(p["w"].forecast[sel], p["ys"][h][sel])
        out["per_window"][p["w"].label] = {"value": _num(v), "oriented": _num(v)}
    return out


def run_test(windows: list[Window], spec: TestSpec, eras: list | None = None,
             calibrated: bool = False) -> dict:
    """Grade one test on one variant's windows.

    Always reports effect sizes (the spec's statistic per horizon, per window
    and per era, and the sample counts). A verdict (supported | refuted |
    inconclusive) is given ONLY when `calibrated` is True, i.e. the method has
    a passed calibration gate (operator rule 3); otherwise the status is
    `method_not_calibrated` and no p-value is computed."""
    errors = check_spec(spec)
    if errors:
        raise ValueError("invalid spec: " + "; ".join(errors))
    needs_eras = "min_eras" in spec.floor or (spec.consistency or {}).get("unit") == "era"
    if needs_eras and eras is None:
        raise ValueError("this spec needs eras (min_eras or era consistency); pass eras")
    method = spec.significance["method"]
    per, out_h, horizons, base_rng = effect_sizes(windows, spec, eras)

    result = {"spec_hash": spec_hash(spec), "status": None, "reasons": [], "warnings": [],
              "statistic": spec.statistic, "direction": spec.direction,
              "significance": dict(spec.significance), "horizons": out_h}
    if spec.statistic == "decay_curve":
        vals = {h: out_h[h]["oriented"] for h in horizons if out_h[h]["oriented"] is not None}
        result["peak_horizon"] = max(vals, key=vals.get) if vals else None
    if not calibrated:
        result["status"] = "method_not_calibrated"
        result["reasons"] = [f"verdict: method not calibrated (no passed calibration gate "
                             f"for {method}); effect sizes only"]
        return result
    return _graded(result, per, out_h, horizons, base_rng, windows, spec, eras)


def effect_sizes(windows: list[Window], spec: TestSpec, eras: list | None = None):
    """The effect-size half of run_test: (per-window prepared data, per-horizon
    effect sizes, sorted horizons, the placebo rng in its post-baseline state).
    No check_spec here (the caller checks the spec; E-068 slice 3 measures
    regime-selector tests too, which check_spec refuses for a verdict), no
    p-value, no verdict. Reads only the given windows: selectors read bar t,
    outcomes are timestamp-matched inside one window."""
    if isinstance(spec.selector, dict) and spec.selector.get("kind") == TRADE_SELECTOR:
        return trade_effect_sizes(windows, spec, eras)      # E-075 PR-3: gated family
    horizons = sorted(spec.outcome["horizons"])
    base_rng = np.random.default_rng(int((spec.baseline or {}).get("seed", PLACEBO_SEED)))
    stat = STATISTICS[spec.statistic]
    opposite = "less" if spec.direction == "greater" else "greater"

    per = _prepare(windows, spec, horizons, base_rng, eras)
    out_h = {}
    for h in horizons:
        y, m, wr, fc = _pooled(per, h)
        raw, oriented = stat(y, m, wr, fc, spec.direction)
        events = [p["mask"] & np.isfinite(p["ys"][h]) for p in per]
        if spec.statistic == "rank_ic":
            events = [ev & np.isfinite(p["fc"]) for ev, p in zip(events, per)]
        per_window = {}
        for p in per:
            r, o = stat(p["ys"][h], p["mask"], p["wref"], p["fc"], spec.direction)
            per_window[p["w"].label] = {"value": _num(r), "oriented": _num(o)}
        per_era, n_eras = {}, None
        if eras is not None:
            era_all = np.concatenate([p["era"] for p in per])
            n_eras = len(set(era_all[np.concatenate(events)]))
            for e_id in sorted(set(era_all)):
                sub = era_all == e_id
                r, o = stat(y[sub], m[sub], wr[sub], fc[sub], spec.direction)
                per_era[e_id] = {"value": _num(r), "oriented": _num(o)}
        out_h[h] = {"value": _num(raw), "oriented": _num(oriented),
                    "oriented_opposite": _num(stat(y, m, wr, fc, opposite)[1]),
                    "p_value": None, "p_value_opposite": None,
                    "n_events": int(sum(ev.sum() for ev in events)),
                    "n_windows_with_events": int(sum(bool(ev.any()) for ev in events)),
                    "n_blocks": _blocks(events, per, h), "n_eras_with_events": n_eras,
                    "per_window": per_window, "per_era": per_era}
    return per, out_h, horizons, base_rng


def _graded(result, per, out_h, horizons, base_rng, windows, spec, eras) -> dict:
    """The verdict half of run_test (calibrated only): p-values, floors, verdict."""
    method = spec.significance["method"]
    stat = STATISTICS[spec.statistic]
    opposite = "less" if spec.direction == "greater" else "greater"
    # The values judged: the spec's statistic (method B) or A8.5.1a's own (method A).
    judged = {}
    if method in A851A_METHODS:
        for p in per:
            p["eras_list"] = eras
        result["verdict_statistic"] = "a851a pooled rank IC among event bars (claimed: > 0)"
        result["a851a_gap_bars"] = a851a_gap_bars(method, windows[0].step)
        for h in horizons:
            a = _a851a_horizon(per, h, method)
            out_h[h]["a851a"] = a
            judged[h] = (a["pooled_ic"], a["p_value"], a["p_value_opposite"], a["per_window"])
    else:
        result["verdict_statistic"] = f"{spec.statistic} ({spec.direction})"
        checks = {}
        for w in windows:
            if w.signal is None or w.warm is None:
                raise ValueError(f"{w.label}: the null needs the window's signal and warm-up rows")
            diff = forecast_check(w)
            checks[w.label] = diff
            if not diff <= FORECAST_TOLERANCE[w.signal["class"]]:
                raise ValueError(f"{w.label}: recomputed forecast differs from the saved one by "
                                 f"{diff:.3g} (> {FORECAST_TOLERANCE[w.signal['class']]}); "
                                 f"the null would not test the strategy that ran")
        result["forecast_check_max_abs_diff"] = checks
        rng = np.random.default_rng(spec.significance["seed"])
        n_res = spec.significance["n_resamples"]
        null = {d: {h: np.full(n_res, np.nan) for h in horizons}
                for d in (spec.direction, opposite)}
        for r in range(n_res):
            fper = _prepare([fake_window(w, rng) for w in windows], spec, horizons, base_rng)
            for h in horizons:
                pooled = _pooled(fper, h)
                o = stat(*pooled, spec.direction)[1]
                null[spec.direction][h][r] = o
                # The opposite direction is the sign flip, except for hit_rate,
                # whose hit definition itself depends on the direction.
                null[opposite][h][r] = (stat(*pooled, opposite)[1]
                                        if spec.statistic == "hit_rate" else -o)
        for h in horizons:
            for d, key, okey in ((spec.direction, "p_value", "oriented"),
                                 (opposite, "p_value_opposite", "oriented_opposite")):
                obs = out_h[h][okey]
                nd = null[d][h][np.isfinite(null[d][h])]
                if obs is not None and len(nd):
                    out_h[h][key] = float((1 + np.sum(nd >= obs)) / (1 + len(nd)))
            out_h[h]["n_null"] = int(np.isfinite(null[spec.direction][h]).sum())
            if out_h[h]["n_null"] < n_res:
                result["warnings"].append(f"h={h}: {n_res - out_h[h]['n_null']} of {n_res} fake "
                                          f"worlds gave an undefined statistic (dropped)")
            judged[h] = (out_h[h]["oriented"], out_h[h]["p_value"], out_h[h]["p_value_opposite"],
                         out_h[h]["per_window"])

    # Floors (every horizon), then the verdict (amendment 3, section 3).
    reasons = []
    floor_key = {"min_events": "n_events", "min_windows": "n_windows_with_events",
                 "min_blocks": "n_blocks", "min_eras": "n_eras_with_events"}
    for unit, need in spec.floor.items():
        for h in horizons:
            have = out_h[h][floor_key[unit]] or 0
            if have < need:
                reasons.append(f"floor {unit}={need} not met at h={h} (have {have})")
    if reasons:
        status = "inconclusive"
    else:
        wrong, weak = [], []
        for h in horizons:
            o, pv, pv_opp, pw = judged[h]
            if pv_opp is not None and pv_opp < spec.alpha:
                wrong.append(f"h={h}: significant in the opposite direction "
                             f"(p_opposite {pv_opp:.4g} < {spec.alpha})")
            elif o is None or pv is None:
                weak.append(f"h={h}: statistic or p undefined")
            elif o <= 0:
                weak.append(f"h={h}: wrong direction or zero, not significant (value {o:.6g})")
            elif pv >= spec.alpha:
                weak.append(f"h={h}: right direction, p {pv:.4g} >= {spec.alpha}")
            if spec.consistency:
                unit = spec.consistency["unit"]
                vals = (pw if unit == "window" else out_h[h]["per_era"]).values()
                same = sum(1 for v in vals if v["oriented"] is not None and v["oriented"] > 0)
                if same < spec.consistency["min_same_sign"]:
                    weak.append(f"h={h}: same sign in {same} {unit}s "
                                f"(need {spec.consistency['min_same_sign']})")
        reasons = wrong + weak
        status = "refuted" if wrong else ("inconclusive" if weak else "supported")
    result["status"], result["reasons"] = status, reasons
    return result


def _num(v):
    return None if v is None or not np.isfinite(v) else float(v)


def combine(statuses: list[str]) -> str:
    """D-014: refuted dominates inconclusive; supported only if all supported.
    No verdict at all (`method_not_calibrated`) dominates everything, and
    nothing graded is `not_graded`, never a verdict-shaped status."""
    if not statuses:
        return "not_graded"
    if "method_not_calibrated" in statuses:
        return "method_not_calibrated"
    if "refuted" in statuses:
        return "refuted"
    if "inconclusive" in statuses:
        return "inconclusive"
    return "supported"


# ---------------------------------------------------------------------------
# CLI: one claim file (several tests) on every graded variant of one run
# ---------------------------------------------------------------------------

CLAIM_FILE_KEYS = {"claim_id", "source_run", "statement", "combine", "across_variants", "tests"}


def check_claim_file(doc: dict, run_dir: Path) -> list[str]:
    """A claim file may only state the rules this tool implements: a rule it
    would silently ignore is refused instead."""
    e = []
    if not isinstance(doc, dict):
        return ["not a mapping"]
    unknown = set(doc) - CLAIM_FILE_KEYS
    if unknown:
        e.append(f"unknown keys {sorted(unknown)}")
    if doc.get("combine", "all_supported") != "all_supported":
        e.append("combine: only all_supported is implemented")
    if doc.get("across_variants", "fail_dominates") != "fail_dominates":
        e.append("across_variants: only fail_dominates is implemented")
    if doc.get("source_run") is not None and doc["source_run"] != Path(run_dir).name:
        e.append(f"source_run {doc['source_run']!r} does not match --run {Path(run_dir).name!r}")
    tests = doc.get("tests")
    if not isinstance(tests, list) or not tests:
        e.append("tests: a non-empty list is required")
    else:
        names = [t.get("name") for t in tests if isinstance(t, dict)]
        if len(names) != len(tests) or None in names or len(set(names)) != len(names):
            e.append("tests: every test needs a unique name")
    return e


def cache_resolver(cache_dir: Path, pattern: str):
    """(symbol, cadence) -> cache file; pattern fields {symbol} and {tf} (1d/1h)."""
    tf = {"daily": "1d", "hourly": "1h"}
    return lambda symbol, cadence: Path(cache_dir) / pattern.format(symbol=symbol, tf=tf[cadence])


def judge_calibration_row(row: dict, gate: dict = CALIBRATION_GATE) -> tuple[bool, list]:
    """Amendment 5: (passes, conservative horizons) for one gate row. Fails if
    any horizon has undefined p above the limit or a share of p < alpha above
    the ceiling (flattering); horizons below the floor are a warning only."""
    shares = row.get("share_p_below_0_05_of_defined") or {}
    und = row.get("share_undefined") or {}
    ok = set(shares) == set(und) == set(CALIBRATION_HORIZONS) and all(
        und[h] is not None and und[h] <= gate["max_share_undefined"]
        and shares[h] is not None and shares[h] <= gate["ceiling"] for h in shares)
    conservative = sorted(h for h, v in shares.items()
                          if v is not None and v < gate["floor_warning"])
    return ok, conservative


def passed_calibrations(paths) -> list[dict]:
    """The calibration summaries that really passed: all_pass, the exact gate,
    every row present and passing (re-judged here from its numbers, not taken
    from its flag), a scope and a code hash. Anything else is ignored
    (operator rule 3: no verdict without a passed gate). Each kept summary
    carries `conservative`: {row: horizons below the floor} (amendment 5)."""
    import yaml
    out = []
    for p in paths or []:
        doc = yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
        rows = doc.get("rows") or []
        judged = [judge_calibration_row(r) for r in rows]
        if (doc.get("all_pass") is True and doc.get("method") in SIGNIFICANCE_METHODS
                and doc.get("gate") == CALIBRATION_GATE and len(rows) == CALIBRATION_ROWS
                and len({r.get("row") for r in rows}) == CALIBRATION_ROWS
                and all(r.get("pass") is True and r.get("n_sims") == CALIBRATION_N_SIMS
                        and ok for r, (ok, _) in zip(rows, judged))
                and isinstance(doc.get("scope"), dict) and doc.get("code_sha256")):
            cons = {r["row"]: c for r, (_, c) in zip(rows, judged) if c}
            out.append(dict(doc, file=str(p), conservative=cons))
    return out


def _selector_matches(scope_selector, selector: dict) -> bool:
    """A gate's selector scope: the exact selector it simulated, or the list of
    them (one per gate side). A bare kind (`event`, what the gates written
    before slice 3 state) matches nothing: those gates only ever simulated
    `forecast` thresholds, so a kind would also unlock a `close` threshold
    the gate never ran (slice 3 review)."""
    if isinstance(scope_selector, dict):
        return scope_selector == selector
    if isinstance(scope_selector, list):
        return any(isinstance(s, dict) and s == selector for s in scope_selector)
    return False


def _n_fakes(spec: TestSpec):
    """How many fake worlds a grade of this spec draws: the spec's own
    n_resamples (method B) or A8.5.1a's fixed resample count."""
    if spec.significance.get("method") in A851A_METHODS:
        return A851A_SETTINGS["n_resamples"]
    return spec.significance.get("n_resamples")


def calibration_for(calibrations: list[dict], spec: TestSpec, windows: list[Window]):
    """The passed calibration that covers THIS test on THIS variant, or None:
    same method, same signal (class and parameters), same cadence, same
    statistic, and the spec's horizons within the gate's. A Donchian(20) daily
    gate does not unlock Donchian(14) or hourly. Two passed summaries for the
    same scope are refused: which one labels the grade must not be a choice.

    E-068 slice 3 (CUL-393): the outcome kind, the selector and the number of
    fakes must match too (a scope that does not state one matches nothing).
    The rest of the scope (baseline, alpha, layout, code hash) is CUL-394."""
    signal = windows[0].signal
    cadence = _cadence(windows[0].step)
    found = [c for c in calibrations
             if c["method"] == spec.significance["method"] and c["scope"].get("signal") == signal
             and c["scope"].get("cadence") == cadence
             and c["scope"].get("statistic") == spec.statistic
             and c["scope"].get("outcome") == spec.outcome.get("kind")
             and _selector_matches(c["scope"].get("selector"), spec.selector)
             and c["scope"].get("n_null") == _n_fakes(spec)
             and set(spec.outcome.get("horizons") or []) <= set(CALIBRATION_HORIZONS)]
    if len(found) > 1:
        raise ValueError("more than one passed calibration covers this test: "
                         + ", ".join(c["file"] for c in found))
    return found[0] if found else None


def grade_claim_file(run_dir: Path, spec_path: Path, cache_path_for, eras: list | None = None,
                     calibration_files=None, method_override: str | None = None) -> dict:
    """`method_override`: an A8.5.1a-family method named by a committed
    amendment, applied to every test without editing the pre-registered spec
    (the spec file and its sha256 stay as fixed; spec_hash records the method)."""
    import yaml
    raw = Path(spec_path).read_bytes()
    doc = yaml.safe_load(raw.decode("utf-8"))
    problems = check_claim_file(doc, Path(run_dir))
    if problems:
        raise ValueError(f"{spec_path}: " + "; ".join(problems))
    tests = [(t["name"], TestSpec.from_dict(t)) for t in doc["tests"]]
    if method_override is not None:
        if method_override not in A851A_METHODS:
            raise ValueError(f"method override must be one of {list(A851A_METHODS)}")
        tests = [(n, replace(t, significance={"method": method_override})) for n, t in tests]
    calibrations = passed_calibrations(calibration_files)
    for name, s in tests:
        errs = check_spec(s)
        if errs:
            raise ValueError(f"{name}: " + "; ".join(errs))
    if eras is None:
        from protocol_resolution import load_policy_eras
        eras = load_policy_eras()
    graded, not_graded = graded_variants(run_dir)
    variants, bars_used = {}, []
    for vid in graded:
        windows = load_variant_bars(run_dir, vid, cache_path_for)
        bars_used += [{"variant": vid, "window": w.label, "path": w.source,
                       "bars": int(len(w.ts)), "sha256": w.sha256} for w in windows]
        used = {name: calibration_for(calibrations, s, windows) for name, s in tests}
        res = {name: run_test(windows, s, eras, calibrated=used[name] is not None)
               for name, s in tests}
        for name in res:
            res[name]["calibration_file"] = used[name]["file"] if used[name] else None
            # Amendment 5: a gate passed with cells below the floor is reported
            # "conservative" next to every verdict it unlocks.
            res[name]["calibration_status"] = (
                None if used[name] is None
                else "conservative" if used[name]["conservative"] else "pass")
            res[name]["calibration_conservative_cells"] = (
                used[name]["conservative"] if used[name] else None)
        graded_here = all(used[name] is not None for name in res)
        variants[vid] = {"symbols": sorted({w.symbol for w in windows}),
                         "signal": windows[0].signal,
                         "windows": [w.label for w in windows], "tests": res,
                         "claim_status": combine([r["status"] for r in res.values()]),
                         "graded": graded_here}
    # Amendment 4 section 4: a variant without a passed gate for its signal is
    # NOT graded; it is listed, and it does not mask the graded variants.
    graded_ok = [v for v, d in variants.items() if d["graded"]]
    no_gate = [v for v, d in variants.items() if not d["graded"]]
    return {"claim_id": doc.get("claim_id"), "statement": doc.get("statement"),
            "spec_file": str(spec_path), "spec_file_sha256": hashlib.sha256(raw).hexdigest(),
            "spec_hashes": {name: spec_hash(s) for name, s in tests},
            "method_override": method_override,
            "n_tests_run": len(tests) * len(graded_ok), "run_dir": str(run_dir),
            "graded_variants": graded_ok,
            "not_graded_variants": not_graded + [f"{v} (no passed calibration for its signal)"
                                                 for v in no_gate],
            "variants": variants, "bars_used": bars_used,
            "claim_status": (combine([variants[v]["claim_status"] for v in graded_ok])
                             if graded_ok else "method_not_calibrated"),
            "calibrations_passed": [c["file"] for c in calibrations],
            "exercised_on_real_runs": sorted(EXERCISED_ON_REAL_RUNS)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="E-068 claim test engine")
    ap.add_argument("--run", required=True, type=Path)
    ap.add_argument("--spec", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--cache-dir", required=True, type=Path,
                    help="read-only data cache with the warm-up rows (never the holdout store)")
    ap.add_argument("--cache-pattern", default="kraken_{symbol}_{tf}.csv")
    ap.add_argument("--method", default=None, choices=list(A851A_METHODS),
                    help="significance method named by a committed amendment (overrides the spec)")
    ap.add_argument("--calibration", action="append", type=Path, default=[],
                    help="calibration result file(s); a verdict needs one with all_pass: true "
                         "for the spec's method")
    a = ap.parse_args(argv)
    if a.run.resolve() in a.out.resolve().parents:
        raise SystemExit("refusing to write inside the run directory")
    if HOLDOUT_DIR_NAME in Path(a.cache_dir).resolve().parts:
        raise SystemExit("refusing to read the holdout store")
    import yaml
    result = grade_claim_file(a.run, a.spec, cache_resolver(a.cache_dir, a.cache_pattern),
                              calibration_files=a.calibration, method_override=a.method)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(result, f, sort_keys=False, allow_unicode=True)
    print(f"{result['claim_id']}: {result['claim_status']} -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
