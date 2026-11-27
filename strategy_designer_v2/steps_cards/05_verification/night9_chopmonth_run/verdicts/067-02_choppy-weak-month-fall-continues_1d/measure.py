import numpy as np
import pandas as pd

RAW = "debug_info.components.month_fall.last_history_value"
H = 7


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        unit = "ms" if v.abs().max() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            # recompute 30-bar return from prices where the component is not recorded
            rec = np.full(len(df), np.nan)
            if len(df) > 30:
                rec[30:] = (close[30:] / close[:-30] - 1.0) * 100.0
            raw = np.where(np.isnan(raw), rec, raw)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array(["unknown"] * len(df))
            active = f != 0
            situ = (raw < 0) & (regime == "unknown")
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars inside the choppy profile with a negative 30-day return and a short forecast, so the config does not do what the Fidelity says (or nothing is active).",
            "reading": "The situation is the 30-day return (recorded raw value, recomputed from closes when missing) below 0 on bars of the strategy's 'unknown' regime, which is the choppy profile; the expected side is short.",
        }

    # ---------- 2. criterion ----------
    vals, wts, days = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            ts = _to_dt(df["timestamp"])
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] < 0:
                    cases.append((r, abs(f[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        if not grid_rets or not cases:
            continue
        drift = float(np.mean(grid_rets))
        for r, a, d in cases:
            vals.append(-(r - drift))
            wts.append(a)
            days.append(d)

    vals = np.array(vals, dtype=float)
    wts = np.array(wts, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))

    m = None
    t = None
    if n_cases > 0 and wts.sum() > 0:
        m = float(np.sum(vals * wts) / np.sum(wts))
        dev = pd.Series(wts * (vals - m)).groupby(pd.Series(days)).sum().values
        k = len(dev)
        if k > 1:
            var = np.sum(dev ** 2) * k / (k - 1)
            se = np.sqrt(var) / np.sum(wts)
            t = float(m / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        order = np.argsort(-wts, kind="mergesort")
        half = n_cases // 2
        large = vals[order[:half]]
        small = vals[order[half:]]
        sup_val = float(np.mean(large) - np.mean(small))
        sup_pass = bool(sup_val > 0)

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} independent days with cases, fewer than the plan's minimum of 100."
    elif t is None or m is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The weighted mean short-side unusual move is above 0 with t >= 2 and the larger-half minus smaller-half difference is above 0."
    elif m > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean short-side unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "abs(forecast)-weighted mean short-side unusual 7-bar move",
            "value": m,
            "statistic": {"name": "weighted t, cases of one day summed", "value": t} if t is not None else None,
            "threshold": "confirm: above 0 with t >= 2 and supporting check passing; reject: below 0 with t <= -2; else inconclusive",
        },
        "supporting_check": {
            "name": "mean short-side unusual move, larger half of abs(forecast) minus smaller half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"independent days with cases": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": "Cases are bars at positions 0,7,14,... of each window with forecast < 0 and a close 7 bars later in the same window, the coin's mean 7-bar return is the mean over that grid in all its windows, the halves split the cases sorted by abs(forecast) with the odd middle case in the smaller half and unweighted means, and the plan's 'fewer than 100 independent days' is treated as the minimum count giving 'not observable'.",
    }
