"""E-068 slice 1 (CUL-386): the claim test engine.

Checks whether an idea's CLAIM is true on the bars a backtest already saved
(`bars.csv`). A test is one sentence built from four slots
(engineering/roadmap/E-068/DESIGN_PROPOSAL.md section 3):

    On these bars (SELECTOR), what happens next (OUTCOME) is different from
    these other bars (BASELINE), measured like this (STATISTIC).

Pure tool: nothing in the campaign calls it yet (slices 2-3 wire it), so every
run is unchanged. It reads bars.csv (plus read-only warm-up rows from the data
cache) and writes one YAML file; it never writes into a run directory.

Blocks (v1, 17):
  selectors   all, event, regime, regime_change, calendar, quantile
  outcomes    fwd_return, fwd_volatility, fwd_max_drawdown, trend_ends
  baselines   complement, placebo, other_selector   (rank_ic takes none)
  statistics  mean_diff, rank_ic, hit_rate, decay_curve

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
  - `quantile` compares x[t] with the quantile of the TRAILING `lookback` bars
    t-lookback .. t-1 of the same window -- never a whole-sample quantile.
  - Outcomes are the label (the future); they never feed a selector. They are
    matched by TIMESTAMP: t+h exists only if a bar is stamped exactly
    ts[t] + h*step in the SAME window; nothing is chained across windows.
  - Warm-up rows are read from the cache only BEFORE a window's first bar; the
    reader stops at that timestamp, so no later row is ever parsed.

SIGNIFICANCE (`bootstrap_null_v1`, amendment 2). Two earlier methods were
retired after the calibration gate: a circular shift of the signal (invalid for
price-derived signals: a backward shift pairs a bar with a signal computed from
its own future) and a block-adjusted analytic p (0.000-0.090 on no-edge prices).
  The null is a world with no edge, rebuilt from each window's own bars:
  units (log return, log high/close, log low/close) are redrawn in circular
  blocks of B bars (5 daily, 24 hourly); a path is rebuilt from the last real
  close before the window; the signal is RECOMPUTED on real warm-up + fake
  window with the variant's own component (SIGNALS: vectorized copies of
  update(), proven equal by a test); selectors, baselines and outcomes are then
  recomputed on the fake window. One-sided
      p = (1 + #{fake >= real}) / (1 + N)
  on the claim-oriented statistic. Before grading, the signal recomputed on
  the REAL path must equal the saved forecast (FORECAST_TOLERANCE), else stop.
  Regime selectors are refused: their labels cannot be recomputed.

VERDICT (amendment 1, section C), floor met at every horizon:
  refuted       wrong direction or zero at any horizon
  inconclusive  right direction but p >= alpha somewhere, window-sign rule not
                met, or a statistic undefined (or below the floor)
  supported     right direction and p < alpha at every horizon, sign rule met
  A weak but true finding must not be stored as false.

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

# Which blocks have been run on real backtest output (the run_065/run_066
# re-grade, E-068 slice 1). Every other block is tested on synthetic data only.
EXERCISED_ON_REAL_RUNS = frozenset({
    "selector:all", "selector:event", "outcome:fwd_return",
    "baseline:complement", "statistic:mean_diff", "statistic:rank_ic",
})

BAR_T_FIELDS = ("forecast", "close")          # numeric fields a selector may read
DIRECTIONS = ("greater", "less")
FLOOR_UNITS = ("min_events", "min_windows", "min_eras", "min_blocks")
CONSISTENCY_UNITS = ("window", "era")
SIGNIFICANCE_METHOD = "bootstrap_null_v1"
DEFAULT_SIGNIFICANCE = {"method": SIGNIFICANCE_METHOD, "n_resamples": 1000, "seed": 20261003}
NOT_RECOMPUTABLE_SELECTORS = ("regime", "regime_change")
PLACEBO_SEED = 20261003       # the placebo baseline's random dates (a baseline, not a p-value)
DAY = 86400
WARMUP_BARS = {"daily": 30, "hourly": 500}
BLOCK_BARS = {"daily": 5, "hourly": 24}
FORECAST_CLIP = 20.0
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
    return (parsed.astype("int64") // 10**9).to_numpy(dtype=np.int64)


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
    regimes = (cfg.get("strategies") or cfg)["regimes"]
    comps = [c for r in regimes.values() if r for c in r.get("components") or []]
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


def sel_event(w: Window, p: dict):
    x = getattr(w, p["field"]).astype(float)
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
    x = getattr(w, p["field"]).astype(float)
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


def _check_selector(s, where: str) -> list[str]:
    if not isinstance(s, dict) or s.get("kind") not in SELECTORS:
        return [f"{where}: unknown selector {s!r}; known: {sorted(SELECTORS)}"]
    k, e = s["kind"], []
    if k in NOT_RECOMPUTABLE_SELECTORS:
        e.append(f"{where}: {k} cannot be graded under {SIGNIFICANCE_METHOD} (regime labels "
                 f"cannot be recomputed on fake prices); park it as a test request")
    if k in ("event", "quantile") and s.get("field") not in BAR_T_FIELDS:
        e.append(f"{where}: field {s.get('field')!r} is not a bar-t field "
                 f"(allowed: {list(BAR_T_FIELDS)}); a selector may not read the future")
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


def check_spec(spec: TestSpec) -> list[str]:
    """Static checks, before any data. Empty list = valid."""
    e = _check_selector(spec.selector, "selector")
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
        e += _check_selector(spec.baseline.get("selector"), "baseline.selector")
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
    if (not isinstance(s, dict) or set(s) != {"method", "n_resamples", "seed"}
            or s.get("method") != SIGNIFICANCE_METHOD
            or not isinstance(s.get("n_resamples"), int) or s["n_resamples"] < 99
            or not isinstance(s.get("seed"), int)):
        e.append(f"significance: method {SIGNIFICANCE_METHOD} (earlier methods failed the "
                 f"calibration gate, amendments 1-2), n_resamples >= 99, int seed")
    return e


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
    """One draw of the null: the window's own bar units redrawn in circular
    blocks, a path rebuilt from the last real close before the window, and the
    signal recomputed on real warm-up + fake window. Timestamps are kept."""
    n = len(w.ts)
    B = BLOCK_BARS[_cadence(w.step)]
    prev = np.r_[w.warm["close"][-1], w.close[:-1]]
    r = np.log(w.close / prev)
    lh, ll = np.log(w.high / w.close), np.log(w.low / w.close)
    starts = rng.integers(0, n, size=-(-n // B))
    idx = ((starts[:, None] + np.arange(B)[None, :]) % n).ravel()[:n]
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


def run_test(windows: list[Window], spec: TestSpec, eras: list | None = None) -> dict:
    """Grade one test on one variant's windows. Returns a plain dict:
    status (supported | refuted | inconclusive), reasons, and per horizon the
    raw and claim-oriented value, one-sided p (and the opposite direction's p),
    sample counts, per-window and per-era values, and the forecast check."""
    errors = check_spec(spec)
    if errors:
        raise ValueError("invalid spec: " + "; ".join(errors))
    needs_eras = "min_eras" in spec.floor or (spec.consistency or {}).get("unit") == "era"
    if needs_eras and eras is None:
        raise ValueError("this spec needs eras (min_eras or era consistency); pass eras")
    for w in windows:
        if w.signal is None or w.warm is None:
            raise ValueError(f"{w.label}: the null needs the window's signal and warm-up rows")
    checks = {}
    for w in windows:
        diff = forecast_check(w)
        checks[w.label] = diff
        if not diff <= FORECAST_TOLERANCE[w.signal["class"]]:
            raise ValueError(f"{w.label}: recomputed forecast differs from the saved one by "
                             f"{diff:.3g} (> {FORECAST_TOLERANCE[w.signal['class']]}); "
                             f"the null would not test the strategy that ran")
    horizons = sorted(spec.outcome["horizons"])
    sig = spec.significance
    base_rng = np.random.default_rng(int((spec.baseline or {}).get("seed", PLACEBO_SEED)))
    stat = STATISTICS[spec.statistic]
    opposite = "less" if spec.direction == "greater" else "greater"

    per = _prepare(windows, spec, horizons, base_rng, eras)
    out_h, reasons = {}, []
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

    # The null: N fake worlds with no edge.
    rng = np.random.default_rng(sig["seed"])
    n_res = sig["n_resamples"]
    null = {d: {h: np.full(n_res, np.nan) for h in horizons} for d in (spec.direction, opposite)}
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
            reasons.append(f"warning h={h}: {n_res - out_h[h]['n_null']} of {n_res} "
                           f"fake worlds gave an undefined statistic (dropped)")
    warnings = list(reasons)
    reasons = []

    # Floors (every horizon), then the verdict (amendment 1, section C).
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
            o, pv = out_h[h]["oriented"], out_h[h]["p_value"]
            if o is None or pv is None:
                weak.append(f"h={h}: statistic undefined")
            elif o <= 0:
                wrong.append(f"h={h}: wrong direction or zero (oriented {o:.6g})")
            elif pv >= spec.alpha:
                weak.append(f"h={h}: right direction, p {pv:.4g} >= {spec.alpha}")
            if spec.consistency:
                unit = spec.consistency["unit"]
                vals = out_h[h]["per_window" if unit == "window" else "per_era"].values()
                same = sum(1 for v in vals if v["oriented"] is not None and v["oriented"] > 0)
                if same < spec.consistency["min_same_sign"]:
                    weak.append(f"h={h}: same sign in {same} {unit}s "
                                f"(need {spec.consistency['min_same_sign']})")
        reasons = wrong + weak
        status = "refuted" if wrong else ("inconclusive" if weak else "supported")

    result = {"spec_hash": spec_hash(spec), "status": status, "reasons": reasons,
              "warnings": warnings, "statistic": spec.statistic,
              "direction": spec.direction, "significance": dict(sig),
              "forecast_check_max_abs_diff": checks, "horizons": out_h}
    if spec.statistic == "decay_curve":
        vals = {h: out_h[h]["oriented"] for h in horizons if out_h[h]["oriented"] is not None}
        result["peak_horizon"] = max(vals, key=vals.get) if vals else None
    return result


def _num(v):
    return None if v is None or not np.isfinite(v) else float(v)


def combine(statuses: list[str]) -> str:
    """D-014: refuted dominates inconclusive; supported only if all supported."""
    if not statuses:
        return "inconclusive"
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


def grade_claim_file(run_dir: Path, spec_path: Path, cache_path_for, eras: list | None = None) -> dict:
    import yaml
    raw = Path(spec_path).read_bytes()
    doc = yaml.safe_load(raw.decode("utf-8"))
    problems = check_claim_file(doc, Path(run_dir))
    if problems:
        raise ValueError(f"{spec_path}: " + "; ".join(problems))
    tests = [(t["name"], TestSpec.from_dict(t)) for t in doc["tests"]]
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
        res = {name: run_test(windows, s, eras) for name, s in tests}
        variants[vid] = {"symbols": sorted({w.symbol for w in windows}),
                         "signal": windows[0].signal,
                         "windows": [w.label for w in windows], "tests": res,
                         "claim_status": combine([r["status"] for r in res.values()])}
    return {"claim_id": doc.get("claim_id"), "statement": doc.get("statement"),
            "spec_file": str(spec_path), "spec_file_sha256": hashlib.sha256(raw).hexdigest(),
            "spec_hashes": {name: spec_hash(s) for name, s in tests},
            "n_tests_run": len(tests), "run_dir": str(run_dir),
            "graded_variants": graded, "not_graded_variants": not_graded,
            "variants": variants, "bars_used": bars_used,
            "claim_status": combine([v["claim_status"] for v in variants.values()]),
            "exercised_on_real_runs": sorted(EXERCISED_ON_REAL_RUNS)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="E-068 claim test engine")
    ap.add_argument("--run", required=True, type=Path)
    ap.add_argument("--spec", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--cache-dir", required=True, type=Path,
                    help="read-only data cache with the warm-up rows (never the holdout store)")
    ap.add_argument("--cache-pattern", default="kraken_{symbol}_{tf}.csv")
    a = ap.parse_args(argv)
    if a.run.resolve() in a.out.resolve().parents:
        raise SystemExit("refusing to write inside the run directory")
    if "holdout_sealed" in Path(a.cache_dir).resolve().parts:
        raise SystemExit("refusing to read the holdout store")
    import yaml
    result = grade_claim_file(a.run, a.spec, cache_resolver(a.cache_dir, a.cache_pattern))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(result, f, sort_keys=False, allow_unicode=True)
    print(f"{result['claim_id']}: {result['claim_status']} -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
