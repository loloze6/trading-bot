import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    REC = "debug_info.components.recency.last_history_value"

    def bars_since_high(close, lookback=20, max_bars=20):
        c = close.values.astype(float)
        n = len(c)
        rmax = pd.Series(c).rolling(lookback, min_periods=lookback).max().values
        out = np.full(n, np.nan)
        last_k = None
        for t in range(n):
            if not np.isnan(rmax[t]) and c[t] >= rmax[t]:
                last_k = t
            if np.isnan(rmax[t]):
                continue
            if last_k is None:
                # no new high seen inside the window yet; unknown if the window is still short
                if t >= lookback - 1 + max_bars:
                    out[t] = 0.0
                continue
            out[t] = float(max(max_bars - (t - last_k), 0))
        return out

    # ---------- benchmark: coin's mean 5-bar return over all windows pooled ----------
    bench = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-H) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        bench[coin] = float(np.mean(allr)) if len(allr) else np.nan

    n_active = 0
    n_agree = 0
    all_exc, all_fc = [], []
    grid_exc = []

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df[FC].astype(float) if FC in df.columns else pd.Series(np.nan, index=df.index)

            # ---------- situation, recomputed from prices ----------
            sma = close.rolling(20, min_periods=20).mean()
            slope = sma - sma.shift(5)
            dist = close - sma
            bsh = pd.Series(bars_since_high(close), index=df.index)
            if REC in df.columns:
                rec = pd.to_numeric(df[REC], errors="coerce")
                bsh = rec.where(rec.notna(), bsh)
            computable = slope.notna() & dist.notna() & bsh.notna()
            sit_calc = (slope > 0) & (dist > 0) & (bsh > 0)
            regime_tr = df["regime"].astype(str).str.lower().eq("trending") if "regime" in df.columns \
                else pd.Series(False, index=df.index)
            situation = sit_calc.where(computable, regime_tr).astype(bool)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # ---------- main measure ----------
            fwd = close.shift(-H) / close - 1.0
            exc = fwd - bench[coin]
            insit = (fc > 0) & exc.notna()
            all_exc.extend(exc[insit].tolist())
            all_fc.extend(fc[insit].tolist())
            grid = (np.arange(len(df)) % H) == 0
            gmask = insit & pd.Series(grid, index=df.index)
            grid_exc.extend(exc[gmask].tolist())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation recomputed from closes per window (SMA20 5-bar change > 0, close > SMA20, "
               "bars-since-20-day-closing-high from the recorded recency value or recomputed > 0), falling back "
               "to regime == 'trending' on early rows where it cannot be computed; benchmark is the coin's mean of "
               "all overlapping 5-bar returns across its windows; the mean excess return and its ordinary t both use "
               "the non-overlapping in-situation bars (positions 0,5,10,... of each window); the supporting slope is "
               "OLS of excess return on forecast over all in-situation bars; the 30-case minimum is treated as a "
               "minimum count giving 'not observable'.")

    main_name = "mean excess 5-bar forward return vs coin mean 5-bar return, forecast > 0"
    thr = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 30 non-overlapping cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping in-situation cases": None},
            "decided_by": ("Only {:.1%} of active bars are long bars inside the plan's situation (rising SMA20, close "
                           "above SMA20, 20-day closing high within 19 bars), below 90%.").format(agreement),
            "reading": reading,
        }

    g = np.asarray(grid_exc, dtype=float)
    n_grid = int(len(g))
    mean_g = float(np.mean(g)) if n_grid > 0 else None
    if n_grid > 1 and np.std(g, ddof=1) > 0:
        t = float(mean_g / (np.std(g, ddof=1) / np.sqrt(n_grid)))
    else:
        t = None

    sup_val, sup_pass = None, None
    x = np.asarray(all_fc, dtype=float)
    y = np.asarray(all_exc, dtype=float)
    if len(x) > 2 and np.std(x) > 0:
        sup_val = float(stats.linregress(x, y).slope)
        sup_pass = bool(sup_val > 0)

    if n_grid < 30:
        status = "not observable"
        decided = "Fewer than 30 non-overlapping in-situation cases pooled across coins and windows ({}).".format(n_grid)
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_g > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm rule met: mean excess 5-bar return is above 0 with t >= 2."
    elif mean_g < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule met: mean excess 5-bar return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: t lies between -2 and 2 (or its sign disagrees with the mean)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_g,
                         "statistic": ({"name": "t of the mean (non-overlapping)", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "OLS slope of excess 5-bar return on forecast", "value": sup_val, "passed": sup_pass},
        "counts": {"non-overlapping in-situation cases": n_grid,
                   "in-situation bars": int(len(y)),
                   "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
