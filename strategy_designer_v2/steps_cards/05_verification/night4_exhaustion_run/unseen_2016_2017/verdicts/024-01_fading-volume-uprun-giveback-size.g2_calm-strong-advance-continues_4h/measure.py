import numpy as np
import pandas as pd
from scipy import stats


def _ols(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = len(x)
    if n < 3 or np.var(x) == 0:
        return None, None, n
    xm, ym = x.mean(), y.mean()
    sxx = np.sum((x - xm) ** 2)
    b = np.sum((x - xm) * (y - ym)) / sxx
    a = ym - b * xm
    resid = y - a - b * x
    s2 = np.sum(resid ** 2) / (n - 2)
    se = np.sqrt(s2 / sxx) if s2 > 0 else 0.0
    t = b / se if se > 0 else (np.inf if b > 0 else (-np.inf if b < 0 else 0.0))
    return float(b), float(t), n


def measure(bars):
    H = 18
    VOLW = 180
    raw_col = "debug_info.components.scaled_run.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            r18 = close / close.shift(H) - 1.0
            recomputed = r18 / r18.abs().rolling(VOLW, min_periods=VOLW).mean()
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "slope of next-18-bar return minus coin's mean 18-bar return, on the forecast"
    thr = "confirm: slope > 0 with t >= 2 and low-vol slope > high-vol slope; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are long bars where the 18-bar scaled return is positive, the plan's situation on its long side",
            "reading": "the situation is read as the recorded raw scaled return being above 0 with a positive forecast (recomputed from closes where the raw value is missing)",
        }

    # ---------- grid cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ret1 = pd.Series(close).pct_change()
            vol = ret1.rolling(VOLW, min_periods=VOLW).std().values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                fr = close[i + H] / close[i] - 1.0
                rows.append({"coin": coin, "window": w, "fwd": fr, "forecast": fc[i], "vol": vol[i]})
    g = pd.DataFrame(rows, columns=["coin", "window", "fwd", "forecast", "vol"])
    g = g[np.isfinite(g["fwd"])]
    coin_mean = g.groupby("coin")["fwd"].transform("mean")
    g["excess"] = g["fwd"] - coin_mean
    gm = g[np.isfinite(g["forecast"])].copy()

    slope, t, n_cases = _ols(gm["forecast"], gm["excess"])

    gv = gm[np.isfinite(gm["vol"])].copy()
    med = gv.groupby("coin")["vol"].transform("median")
    low = gv[gv["vol"] <= med]
    high = gv[gv["vol"] > med]
    s_low, _, _ = _ols(low["forecast"], low["excess"])
    s_high, _, _ = _ols(high["forecast"], high["excess"])
    diff = (s_low - s_high) if (s_low is not None and s_high is not None) else None
    sup_pass = (diff > 0) if diff is not None else None

    n_pos = int((gm["forecast"] > 0).sum())
    n_pos_low = int((low["forecast"] > 0).sum())
    n_pos_high = int((high["forecast"] > 0).sum())

    counts = {
        "grid cases with a forecast above 0": n_pos,
        "low-volatility grid cases with a forecast above 0": n_pos_low,
        "high-volatility grid cases with a forecast above 0": n_pos_high,
        "grid cases in the regression": int(n_cases),
    }

    if n_pos < 100 or n_pos_low < 30 or n_pos_high < 30 or slope is None:
        status = "not observable"
        if n_pos < 100:
            decided = f"fewer than 100 grid cases with a forecast above 0 ({n_pos})."
        else:
            decided = f"fewer than 30 grid cases with a forecast above 0 in a volatility half (low {n_pos_low}, high {n_pos_high})."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "the main slope is positive with t >= 2 and the low-volatility slope exceeds the high-volatility slope."
        else:
            status = "inconclusive"
            decided = "the main t is >= 2 but the low-volatility slope does not exceed the high-volatility slope."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "the main slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "the main slope has t between -2 and 2."

    def _f(v):
        if v is None:
            return None
        v = float(v)
        return v if np.isfinite(v) else (1e300 if v > 0 else -1e300)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": _f(slope),
            "statistic": {"name": "OLS t of the slope", "value": _f(t)} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "low-vol slope minus high-vol slope",
            "value": _f(diff),
            "passed": (bool(sup_pass) if sup_pass is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "all grid bars (positions 0, 18, 36, ... of each window with a full 18-bar forward return), forecast 0 included, enter the regressions; the coin's mean is the mean of its grid 18-bar returns over all windows; volatility is the rolling 180-bar std of 4h close returns inside each window (grid cases without 180 past returns are left out of the split), split at the coin's median over its grid cases with low = at or below the median; the minimum counts are counted on grid cases with a forecast above 0.",
    }
