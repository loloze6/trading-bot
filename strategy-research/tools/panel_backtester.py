"""
panel_backtester.py -- RESEARCH-ONLY vectorized panel backtester.

Scope (hard): this file is NOT part of the production engine. It does not import or
modify core/backtester.py, main_strategy.py, RollingBuffer, or any live path. It exists
solely to run a cross-sectional (panel) strategy that the single-symbol production engine
cannot express (backtester.py:92,:359 load self.symbols[0] only; main_strategy.py:44's
RollingBuffer is unpartitioned; there are no netting hooks). See the ledger blocker entry.

Two responsibilities:
  1. VALIDATION GATE (validate_gate): reproduce an archived single-symbol engine run
     (P4_ts_trend / run_054, SmaTrendLongOnlyComponent L=100, daily, long-only) to prove
     this file's return/cost/Sharpe/drawdown accounting matches the trusted engine before
     any cross-sectional result is trusted.
  2. XS-MOMENTUM (run_xs): dollar-neutral cross-sectional momentum on the ratified 19-pair
     Kraken universe.

The metric functions below are ports of the production engine's OWN formulas
(trading-bot/performance/metrics.py::calculate_sharpe_ratio / calculate_max_drawdown /
_calculate_standard_metrics and reporting/run_artifact.py::build_core). They are copied so
the gate can prove byte-for-byte-equivalent accounting; if the engine's formulas change,
the gate will catch the drift.

Engine accounting reconstructed and verified against runs/run_054 trades.json:
  A long-only 0/1 allocation (forecast/10) enters a full position at close[T] when the
  signal turns on and closes it at close[T'] when it turns off. For episode i with
  portfolio value V_i at entry, entry price Pe, exit price Px, one-way rate r:
    matched_qty      = (V_i / Pe) * (1 - r)
    gross_pnl        = (Px - Pe) * matched_qty
    entry_commission = matched_qty * Pe * (r / (1 - r))      # == V_i * r
    exit_commission  = matched_qty * Px * r
    net_pnl          = gross_pnl - entry_commission - exit_commission
    impact_pct       = net_pnl / V_i * 100                   # portfolio_impact_pct
    final_pv_i       = V_i * (1 - r) * (Px / Pe)             # mark-to-market at exit close
    V_{i+1}          = V_i + net_pnl
"""

import sys
import os
import json
import math
import argparse
import statistics
from datetime import datetime, date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_SR = os.path.dirname(_HERE)
_REPO = os.path.dirname(_SR)
_LOCAL_DATA = os.path.join(_REPO, "trading-bot", "local_data")
_COST_MODEL = os.path.join(_SR, "config", "cost_model.yaml")

DEFAULT_COMMISSION_RATE = 0.001  # engine DEFAULT_COMMISSION_RATE (10 bps one-way)
INITIAL_CAPITAL = 1000.0         # engine DEFAULT_INITIAL_BALANCE


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_ohlcv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, usecols=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    for c in ("open", "high", "low", "close", "volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("timestamp").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Engine metric ports (verbatim logic from trading-bot/performance/metrics.py)
# operate on a list of trade dicts, each with:
#   exit_time (datetime), portfolio_impact_pct (float), profitable_net (bool),
#   profit_loss_absolute, net_profit_loss_absolute, total_commission,
#   initial_portfolio_value, final_portfolio_value, entry_time
# ---------------------------------------------------------------------------

def _calculate_max_drawdown(trades: list) -> float:
    if not trades:
        return 0.0
    ts = sorted(trades, key=lambda t: t["exit_time"])
    returns = pd.Series([t["portfolio_impact_pct"] / 100 for t in ts])
    equity = (1 + returns).cumprod()
    equity = pd.concat([pd.Series([1.0]), equity], ignore_index=True)
    running_max = equity.expanding().max()
    drawdown = (equity - running_max) / running_max
    return drawdown.min() * 100


def _calculate_sharpe_ratio(trades: list, risk_free_rate: float = 0.0) -> float:
    """Port of metrics.py::calculate_sharpe_ratio -- daily-bucketed, annualized sqrt(365)."""
    if len(trades) < 2:
        return 0.0
    df = pd.DataFrame({
        "exit_date": [pd.to_datetime(t["exit_time"]).date() for t in trades],
        "impact": [t["portfolio_impact_pct"] for t in trades],
    })
    daily = df.groupby("exit_date")["impact"].sum() / 100
    start_date, end_date = min(daily.index), max(daily.index)
    if start_date == end_date:
        return 0.0
    full_cal = pd.date_range(start=start_date, end=end_date).date
    daily = daily.reindex(full_cal).fillna(0.0)
    std = daily.std()
    if std == 0 or pd.isna(std):
        return 0.0
    daily_rf = risk_free_rate / 365
    return (daily - daily_rf).mean() / std * math.sqrt(365)


def core_metrics_from_trades(trades: list) -> dict:
    """Port of run_artifact.build_core + the subset of _calculate_standard_metrics it reads."""
    n = len(trades)
    if n == 0:
        return {
            "net_return_pct": 0.0, "sharpe": 0.0, "max_drawdown_pct": 0.0,
            "trade_count": 0, "win_rate": 0.0, "fees_paid": 0.0,
            "gross_pnl": 0.0, "net_pnl": 0.0,
        }
    gross_pnl = sum(t["profit_loss_absolute"] for t in trades)
    net_pnl = sum(t["net_profit_loss_absolute"] for t in trades)
    fees_paid = sum(t["total_commission"] for t in trades)
    wins = sum(1 for t in trades if t["profitable_net"])
    win_rate = wins / n * 100
    # total_return_pct: (last-by-exit final_pv - first-by-entry initial_pv) / first initial
    first = min(trades, key=lambda t: t["entry_time"])
    last = max(trades, key=lambda t: t["exit_time"])
    start_cap = first["initial_portfolio_value"]
    final_cap = last["final_portfolio_value"]
    total_return_pct = (final_cap - start_cap) / start_cap * 100
    sharpe = _calculate_sharpe_ratio(trades)
    max_dd = _calculate_max_drawdown(trades)
    return {
        "net_return_pct": round(total_return_pct, 3),
        "sharpe": round(sharpe, 3),
        "max_drawdown_pct": round(max_dd, 3),
        "trade_count": n,
        "win_rate": round(win_rate, 2),
        "fees_paid": round(fees_paid, 6),
        "gross_pnl": round(gross_pnl, 6),
        "net_pnl": round(net_pnl, 6),
    }


# ---------------------------------------------------------------------------
# Single-asset long/flat simulator (GATE) -- reproduces engine trade accounting
# ---------------------------------------------------------------------------

def sma_long_only_signal(closes: pd.Series, L: int = 100) -> pd.Series:
    """forecast_T = long if close[T-1] > SMA_L(close)[T-1]. Returns bool position series
    aligned to each bar: position held during [close_T, close_{T+1}]."""
    sma = closes.rolling(L).mean()
    cond = closes > sma            # elementwise close_t > SMA_t
    return cond.shift(1).fillna(False).astype(bool)  # signal at T uses T-1


def simulate_long_flat(df: pd.DataFrame, signal: pd.Series, score_mask: pd.Series,
                       initial_capital: float = INITIAL_CAPITAL,
                       rate: float = DEFAULT_COMMISSION_RATE) -> list:
    """Sequential long/flat simulation over the SCORED bars only (score_mask True).
    signal[i] True => want to be long during bar i. Enter at close[i] on 0->1, exit at
    close[i] on 1->0. Force-close at the last scored bar. Reproduces the engine's
    per-episode accounting exactly (see module docstring)."""
    closes = df["close"].values
    times = df["timestamp"].values
    idxs = np.where(score_mask.values)[0]
    trades = []
    V = initial_capital
    in_pos = False
    entry_i = None
    prev_sig = False  # engine starts flat; first scored bar compares against flat

    for k, i in enumerate(idxs):
        sig = bool(signal.iloc[i])
        if sig and not in_pos:
            in_pos = True
            entry_i = i
        elif (not sig) and in_pos:
            trades.append(_close_episode(df, entry_i, i, V, rate))
            V += trades[-1]["net_profit_loss_absolute"]
            in_pos = False
            entry_i = None
    # force-close at last scored bar
    if in_pos:
        last_i = idxs[-1]
        trades.append(_close_episode(df, entry_i, last_i, V, rate))
        V += trades[-1]["net_profit_loss_absolute"]
    return trades


def _close_episode(df: pd.DataFrame, entry_i: int, exit_i: int, V: float, rate: float) -> dict:
    Pe = float(df["close"].iloc[entry_i])
    Px = float(df["close"].iloc[exit_i])
    te = pd.to_datetime(df["timestamp"].iloc[entry_i])
    tx = pd.to_datetime(df["timestamp"].iloc[exit_i])
    matched = (V / Pe) * (1 - rate)
    gross = (Px - Pe) * matched
    entry_comm = matched * Pe * (rate / (1 - rate))
    exit_comm = matched * Px * rate
    net = gross - entry_comm - exit_comm
    final_pv = V * (1 - rate) * (Px / Pe)
    return {
        "entry_time": te, "exit_time": tx,
        "entry_price": Pe, "exit_price": Px,
        "matched_quantity": matched,
        "profit_loss_absolute": gross,
        "total_commission": entry_comm + exit_comm,
        "net_profit_loss_absolute": net,
        "portfolio_impact_pct": net / V * 100,
        "initial_portfolio_value": V,
        "final_portfolio_value": final_pv,
        "profitable_net": (Px / Pe - 1) * 100 - rate * 100 - (Px / Pe) * rate * 100 > 0,
    }


# ---------------------------------------------------------------------------
# GATE
# ---------------------------------------------------------------------------

# run_054 semi-annual windows (from protocols/ts_trend_daily_v1.json)
_TS_WINDOWS = [
    ("2018-04", "2018-04-01", "2018-10-01"), ("2018-10", "2018-10-01", "2019-04-01"),
    ("2019-04", "2019-04-01", "2019-10-01"), ("2019-10", "2019-10-01", "2020-04-01"),
    ("2020-04", "2020-04-01", "2020-10-01"), ("2020-10", "2020-10-01", "2021-04-01"),
    ("2021-04", "2021-04-01", "2021-10-01"), ("2021-10", "2021-10-01", "2022-04-01"),
    ("2022-04", "2022-04-01", "2022-10-01"), ("2022-10", "2022-10-01", "2023-04-01"),
    ("2023-04", "2023-04-01", "2023-10-01"), ("2023-10", "2023-10-01", "2024-04-01"),
    ("2024-04", "2024-04-01", "2024-10-01"), ("2024-10", "2024-10-01", "2025-04-01"),
    ("2025-04", "2025-04-01", "2025-10-01"),
]
_SPARSE_TRADE_FLOOR = 5  # run_protocol nulls per-window sharpe below this


def _window_gate(df: pd.DataFrame, start: str, end: str) -> dict:
    """Reproduce one window: score bars in [start,end); SMA warmup from preceding rows.
    Timestamps in bars.csv carry a +2h label offset vs the raw daily CSV; daily returns
    and SMA are invariant to a uniform label shift, so we score on the raw CSV date."""
    signal = sma_long_only_signal(df["close"], L=100)
    d = df["timestamp"].dt.normalize()
    # Engine data alignment: the production engine resamples the daily CSV with a +2h
    # origin (closed='left', label='left'), so its bar labeled D carries the raw CSV's
    # D+1 close, and the fetch/resample edge drops the final ~2 raw rows. Empirically
    # (verified on 2018-04 and 2019-04 windows against the archived bars.csv): the engine
    # scores raw CSV rows dated [start+1d, end-2d]. My signal on the raw series at row r
    # equals the engine's forecast at the bar carrying raw close[r], so scoring this raw
    # slice reproduces the engine's exact entry/exit prices.
    s = pd.Timestamp(start) + timedelta(days=1)
    e = pd.Timestamp(end) - timedelta(days=2)
    score_mask = (d >= s) & (d <= e)
    trades = simulate_long_flat(df, signal, score_mask)
    core = core_metrics_from_trades(trades)
    if core["trade_count"] < _SPARSE_TRADE_FLOOR:
        core["sharpe"] = None
    return core


def validate_gate(verbose: bool = True) -> dict:
    """Reproduce all 30 run_054 window-symbol slots; compare to recorded metrics."""
    recorded_path = os.path.join(_SR, "runs", "run_054", "protocol_summary.json")
    with open(recorded_path, encoding="utf-8") as f:
        recorded = json.load(f)["results"]

    data = {sym: load_ohlcv(os.path.join(_LOCAL_DATA, f"{sym}_1d.csv"))
            for sym in ("BTCUSDT", "ETHUSDT")}

    # pre-registered tolerances
    TOL = {
        "trade_count": ("exact", 0),
        "net_return_pct": ("pp_or_rel", (0.5, 0.02)),
        "sharpe": ("abs", 0.10),
        "max_drawdown_pct": ("abs", 0.5),
        "gross_pnl": ("rel", 0.02),
        "net_pnl": ("rel", 0.02),
        "fees_paid": ("rel", 0.02),
    }

    rows = []
    all_pass = True
    for rec in recorded:
        sym, wlabel = rec["symbol"], rec["window"]
        win = next(w for w in _TS_WINDOWS if w[0] == wlabel)
        got = _window_gate(data[sym], win[1], win[2])
        exp = rec["core"]
        for field, (kind, param) in TOL.items():
            gv, ev = got.get(field), exp.get(field)
            ok, detail = _check(kind, param, gv, ev)
            if not ok:
                all_pass = False
            rows.append({"symbol": sym, "window": wlabel, "field": field,
                         "got": gv, "expected": ev, "pass": ok, "detail": detail})
    return {"all_pass": all_pass, "rows": rows}


def _check(kind, param, gv, ev):
    if gv is None and ev is None:
        return True, "both None"
    if (gv is None) != (ev is None):
        return False, f"None mismatch got={gv} exp={ev}"
    if kind == "exact":
        return gv == ev, f"{gv} vs {ev}"
    if kind == "abs":
        return abs(gv - ev) <= param, f"|{gv}-{ev}|={abs(gv-ev):.4f}<= {param}"
    if kind == "rel":
        if ev == 0:
            return abs(gv) <= 1e-6, f"{gv} vs 0"
        return abs(gv - ev) / abs(ev) <= param, f"rel={abs(gv-ev)/abs(ev):.4f}<= {param}"
    if kind == "pp_or_rel":
        pp, rel = param
        d = abs(gv - ev)
        rok = (abs(gv - ev) / abs(ev) <= rel) if ev != 0 else (d <= pp)
        return (d <= pp) or rok, f"|Δ|={d:.4f}pp rel={ (d/abs(ev)) if ev else 0:.4f}"
    return False, "unknown"


# ---------------------------------------------------------------------------
# XS-MOMENTUM (panel) -- dollar-neutral cross-sectional momentum
# ---------------------------------------------------------------------------

# Ratified 19-pair universe (research_brief_XS_momentum.md frontmatter), Kraken base.
_XS_UNIVERSE = ["BTC", "ETH", "XRP", "SOL", "ADA", "SUI", "ZEC", "DOGE", "XMR", "LTC",
                "ONDO", "NEAR", "LINK", "TAO", "AVAX", "TRX", "AAVE", "INJ", "UNI"]
_XS_START = "2017-05-18"          # ratified effective start (n>=6 first reached)
_XS_END = "2025-12-31 23:00:00"   # archive cutoff (holdout begins 2026-01-01)


def _load_perp_cost_bps() -> float:
    """One-way perp taker fee (bps) from cost_model.yaml perp block. No re-derivation."""
    import yaml
    with open(_COST_MODEL, encoding="utf-8") as f:
        cm = yaml.safe_load(f)
    return float(cm["perp"]["fee_rate_bps"]["default"])


def _build_panel() -> pd.DataFrame:
    """Common hourly close panel: index = union of all timestamps, columns = 19 bases.
    Missing = NaN (never forward-filled)."""
    series = {}
    for base in _XS_UNIVERSE:
        df = load_ohlcv(os.path.join(_LOCAL_DATA, f"kraken_{base}USD_1h.csv"))
        s = df.set_index("timestamp")["close"]
        s = s[~s.index.duplicated(keep="last")]
        series[base] = s
    panel = pd.DataFrame(series).sort_index()
    return panel


def run_xs(lookback_L: int = 168, rebalance_every: int = 24, min_n: int = 6,
           long_short_frac: float = 1/3.0, cost_bps: float = None,
           start: str = _XS_START, end: str = _XS_END, exec_lag: int = 1,
           verbose: bool = True) -> dict:
    """Dollar-neutral cross-sectional momentum on the 19-pair Kraken panel.

    Pre-registered mechanics (each a STOP if violated):
      (a) no forward-fill into the ranking: an asset with NaN close at t OR at t-L is
          excluded from that bar's cross-section.
      (b) dollar-neutral: long leg weights sum to +1, short leg to -1.
      (c) pointwise entry, no lookahead on listing dates (NaN before listing => excluded).
      (d) rank at bar t uses data through t; the resulting target weights are applied
          starting t+1 (returns from t+1 onward), never same-bar.
    """
    if cost_bps is None:
        cost_bps = _load_perp_cost_bps()
    panel = _build_panel()
    panel = panel[(panel.index >= pd.Timestamp(start)) & (panel.index <= pd.Timestamp(end))]
    ts = panel.index
    P = panel.values                       # (T, N) closes, NaN where missing
    T, N = P.shape
    # simple 1-bar returns per asset (NaN-safe); asset return only valid when both
    # close[t] and close[t-1] present.
    R = np.full((T, N), np.nan)
    R[1:] = P[1:] / P[:-1] - 1.0
    # momentum at t: valid only when close[t] and close[t-L] both present
    MOM = np.full((T, N), np.nan)
    MOM[lookback_L:] = P[lookback_L:] / P[:-lookback_L] - 1.0

    W = np.zeros(N)                        # active weights earning returns this bar
    port_ret = np.zeros(T)                 # hourly portfolio return (net of cost)
    turnover_series = np.zeros(T)
    gross_ret = np.zeros(T)                # before cost
    n_elig_hist = []
    rebal_bars = []
    pending = {}                           # apply_at bar -> target weights

    for t in range(T):
        # 1) apply any weights scheduled to become active at the START of bar t; charge
        #    turnover here. With exec_lag=1 a rebalance decided at bar r activates at r+1,
        #    so the position is rebalanced at the open of the next bar and earns that bar's
        #    return -- a clean 1-bar (signal-to-fill) delay, no same-bar lookahead.
        if t in pending:
            W_target = pending.pop(t)
            turn = float(np.sum(np.abs(W_target - W)))
            turnover_series[t] = turn
            port_ret[t] -= turn * cost_bps / 1e4
            W = W_target

        # 2) accrue return from t-1 -> t on ACTIVE weights (mechanic d)
        if t > 0:
            r_t = R[t]
            active = ~np.isnan(r_t) & (W != 0)
            g = float(np.sum(W[active] * r_t[active]))
            gross_ret[t] += g
            port_ret[t] += g

        # 3) rebalance decision at bar t (uses MOM[t] = data through t only); target
        #    weights scheduled to activate at t+exec_lag.
        if t % rebalance_every == 0:
            mom_t = MOM[t]
            elig = np.where(~np.isnan(mom_t) & ~np.isnan(P[t]))[0]
            n = len(elig)
            n_elig_hist.append((ts[t], n))
            W_new = np.zeros(N)
            if n >= min_n:
                order = elig[np.argsort(mom_t[elig])]     # ascending
                k = max(1, int(np.floor(n * long_short_frac)))
                longs = order[-k:]
                shorts = order[:k]
                W_new[longs] = 1.0 / k                    # long leg sums to +1
                W_new[shorts] = -1.0 / k                  # short leg sums to -1
            apply_at = t + exec_lag
            if apply_at < T:
                pending[apply_at] = W_new
            rebal_bars.append(t)

    # daily bucketing for Sharpe (campaign convention: daily returns, annualize sqrt(365))
    dfp = pd.DataFrame({"ts": ts, "ret": port_ret, "gross": gross_ret})
    dfp["date"] = dfp["ts"].dt.date
    daily = dfp.groupby("date")["ret"].sum()
    daily_gross = dfp.groupby("date")["gross"].sum()

    def _sharpe(dseries):
        if len(dseries) < 2 or dseries.std() == 0:
            return 0.0
        return dseries.mean() / dseries.std() * math.sqrt(365)

    net_sharpe = _sharpe(daily)
    gross_sharpe = _sharpe(daily_gross)
    # equity + max drawdown (net), compounded daily
    eq = (1 + daily).cumprod()
    eq = pd.concat([pd.Series([1.0]), eq], ignore_index=True)
    run_max = eq.expanding().max()
    max_dd = ((eq - run_max) / run_max).min() * 100
    total_net_return = (eq.iloc[-1] - 1) * 100
    total_gross_return = ((1 + daily_gross).cumprod().iloc[-1] - 1) * 100
    ann_turnover = float(np.sum(turnover_series)) / (len(daily) / 365.0)
    total_cost_pct = float(np.sum(turnover_series) * cost_bps / 1e4) * 100

    result = {
        "spec": {"lookback_L": lookback_L, "rebalance_every": rebalance_every,
                 "min_n": min_n, "long_short_frac": long_short_frac,
                 "cost_bps_one_way": cost_bps, "start": start, "end": end,
                 "n_bars": int(T), "n_days": int(len(daily)), "n_rebalances": len(rebal_bars)},
        "net_sharpe": round(net_sharpe, 4),
        "gross_sharpe": round(gross_sharpe, 4),
        "total_net_return_pct": round(total_net_return, 3),
        "total_gross_return_pct": round(total_gross_return, 3),
        "max_drawdown_pct": round(max_dd, 3),
        "annualized_turnover_x": round(ann_turnover, 2),
        "total_cost_drag_pct_of_equity": round(total_cost_pct, 3),
        "n_eligible_min": min(n for _, n in n_elig_hist),
        "n_eligible_max": max(n for _, n in n_elig_hist),
        "first_rebalance_ts": str(ts[rebal_bars[0]]) if rebal_bars else None,
    }
    daily_df = pd.DataFrame({"date": daily.index, "net": daily.values,
                             "gross": daily_gross.reindex(daily.index).values})
    return result, n_elig_hist, daily_df


def _cross_section_curve(n_elig_hist):
    """When did the cross-section reach n>=6? (validates 2017-05-18 effective start)."""
    out = []
    seen = {}
    for tstamp, n in n_elig_hist:
        if n not in seen:
            seen[n] = tstamp
    for n in sorted(seen):
        out.append((n, str(seen[n])))
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("gate")
    px = sub.add_parser("xs")
    px.add_argument("--lookback", type=int, default=168)
    px.add_argument("--rebalance", type=int, default=24)
    px.add_argument("--min-n", type=int, default=6)
    args = parser.parse_args()
    if args.cmd == "xs":
        res, hist, daily = run_xs(lookback_L=args.lookback, rebalance_every=args.rebalance,
                                  min_n=args.min_n)
        print("=== XS-MOMENTUM (research path, Kraken perp cost) ===")
        print(json.dumps(res, indent=2))
        print("\n=== cross-section size: first date each n_eligible reached ===")
        for n, d in _cross_section_curve(hist):
            print(f"  n={n:2d}  first at {d}")

        def _sh(x):
            x = pd.Series(x).dropna()
            return round(x.mean() / x.std() * math.sqrt(365), 3) if len(x) > 1 and x.std() else 0.0
        daily["year"] = pd.to_datetime(daily["date"]).dt.year
        print("\n=== ROBUSTNESS ===")
        print("per-year net Sharpe:")
        for y, g in daily.groupby("year"):
            print(f"  {y}: net={_sh(g['net']):>7}  gross={_sh(g['gross']):>7}  "
                  f"n_days={len(g)}  cum_net={round((( 1+g['net']).prod()-1)*100,1)}%")
        post = daily[pd.to_datetime(daily["date"]) >= "2019-01-01"]
        print(f"post-2019 (larger-n): net Sharpe={_sh(post['net'])}  gross={_sh(post['gross'])}")
        post21 = daily[pd.to_datetime(daily["date"]) >= "2021-01-01"]
        print(f"post-2021 (n>=12):    net Sharpe={_sh(post21['net'])}  gross={_sh(post21['gross'])}")
        # execution-lag lookahead probe: t+1 (base) vs t+2 vs t+4
        print("\nexecution-lag lookahead probe (net Sharpe):")
        for lag in (1, 2, 4):
            r2, _, d2 = run_xs(lookback_L=args.lookback, rebalance_every=args.rebalance,
                               min_n=args.min_n, exec_lag=lag)
            print(f"  exec_lag={lag} bar(s): net={r2['net_sharpe']}  gross={r2['gross_sharpe']}  "
                  f"net_return%={r2['total_net_return_pct']}")
    elif args.cmd == "gate":
        res = validate_gate()
        fails = [r for r in res["rows"] if not r["pass"]]
        # compact side-by-side per slot
        by_slot = {}
        for r in res["rows"]:
            by_slot.setdefault((r["symbol"], r["window"]), []).append(r)
        print(f"{'symbol':8} {'window':8} {'tc':>3} {'ret%(g/e)':>18} {'sharpe(g/e)':>16} "
              f"{'dd%(g/e)':>16} {'ok'}")
        for (sym, w), rs in by_slot.items():
            d = {r["field"]: r for r in rs}
            tc = d["trade_count"]
            ret = d["net_return_pct"]; sh = d["sharpe"]; dd = d["max_drawdown_pct"]
            slot_ok = all(r["pass"] for r in rs)
            print(f"{sym:8} {w:8} {str(tc['got']):>3} "
                  f"{str(ret['got'])+'/'+str(ret['expected']):>18} "
                  f"{str(sh['got'])+'/'+str(sh['expected']):>16} "
                  f"{str(dd['got'])+'/'+str(dd['expected']):>16} {'OK' if slot_ok else 'FAIL'}")
        print()
        if fails:
            print(f"GATE FAIL: {len(fails)} field-checks failed:")
            for r in fails[:40]:
                print(f"  {r['symbol']} {r['window']} {r['field']}: "
                      f"got={r['got']} exp={r['expected']} [{r['detail']}]")
        print("\nGATE RESULT:", "PASS" if res["all_pass"] else "FAIL")
