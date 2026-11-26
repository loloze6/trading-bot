import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    FC = "forecast"
    RAW = "debug_info.components.fade.last_history_value"
    REG = "regime"

    def _f(x):
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    # ---------- 1. Situation check ----------
    # Situation: the high-volatility regime (the detector's decision 'mean_reversion', i.e. vol percentile >= 0.5).
    # Expected side: a fade, so the forecast's sign is opposite to the day's return.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            day_ret = close.pct_change()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                move = raw.where(raw.notna(), day_ret)
            else:
                move = day_ret
            reg = df[REG].astype(str) if REG in df.columns else pd.Series([""] * len(df))
            active = fc != 0
            in_regime = reg == "mean_reversion"
            side_ok = np.sign(fc) == -np.sign(move)
            ok = active & in_regime & side_ok & move.notna()
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS t of the slope of excess forward 3-bar return on forecast"
    threshold = "confirm: t >= 2 with supporting check > 0; reject: t <= -2; else inconclusive"
    sup_name = "mean sign(forecast) x excess 3-bar return over the top 20% |forecast| cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _f(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on fade side": n_agree},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are high-volatility (mean_reversion) bars "
                           "with a forecast opposite to the day's return, so the config does not do what the "
                           "Fidelity's volatile-day fade describes."),
            "reading": "Situation taken as regime == 'mean_reversion' and side as -sign(day's return) from the fade raw value (or close-to-close return where not recorded).",
        }

    # ---------- 2. Criterion ----------
    grid_rets = {}   # coin -> list of all grid forward 3-bar returns (for the coin mean)
    cases = []       # (coin, forecast, fwd)
    for coin, wins in bars.items():
        grid_rets.setdefault(coin, [])
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            reg = df[REG].astype(str).values if REG in df.columns else np.array([""] * len(df))
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets[coin].append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0 and reg[i] == "mean_reversion":
                    cases.append((coin, float(f), r))

    coin_mean = {c: (np.mean(v) if len(v) else np.nan) for c, v in grid_rets.items()}
    F = np.array([c[1] for c in cases], dtype=float)
    X = np.array([c[2] - coin_mean[c[0]] for c in cases], dtype=float)
    m = np.isfinite(F) & np.isfinite(X)
    F, X = F[m], X[m]
    N = int(len(F))

    n_top = int(np.ceil(0.2 * N)) if N > 0 else 0
    sup_val = None
    if n_top > 0:
        order = np.argsort(-np.abs(F), kind="mergesort")[:n_top]
        sup_val = float(np.mean(np.sign(F[order]) * X[order]))
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    slope, t = None, None
    if N >= 3 and np.std(F) > 0:
        lr = stats.linregress(F, X)
        slope = _f(lr.slope)
        t = _f(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {"independent cases": N, "cases in top-20% group": n_top}

    if N < 100 or n_top < 20:
        status = "not observable"
        decided = ("Minimum count not reached: %d independent cases (100 needed) and %d in the top-20%% group (20 needed)."
                   % (N, n_top))
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-20% mean of sign(forecast) x excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger fade forecasts are followed by continuation."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": _f(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are grid bars (positions 0,3,6,... per window) with regime 'mean_reversion', non-zero forecast and a full "
                    "3-bar forward return in the window; the coin's mean 3-bar return is the mean over all grid bars of all its windows; "
                    "the regression is pooled across coins; the top-20% group is the ceil(20% of cases) largest |forecast|."),
    }
