import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 30
    MIN_DAYS = 30
    EPS = 1e-9

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.astype(float)
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ms" if mx > 1e12 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def comp_value(df, cid, field):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        out = pd.Series(np.nan, index=df.index, dtype=float)
        if "debug_info.components" in df.columns:
            for i, v in df["debug_info.components"].items():
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict) and c.get(field) is not None:
                        try:
                            out.at[i] = float(c.get(field))
                        except Exception:
                            pass
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            depth_raw = comp_value(df, "depth90", "last_history_value")
            situ = depth_raw.notna() & (depth_raw <= -1.0 + EPS)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    main_name = "mean excess 30-bar return (minus coin's normal 30-bar drift) on grid bars with forecast > 0"
    threshold = "confirm: mean > 0 with t >= 2 and slope on forecast > 0; reject: mean < 0 with t <= -2; else inconclusive; fewer than 30 cases on distinct days: not enough"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the raw scaled 90-day return (depth90) is at or below -1, as the Fidelity's adapted situation requires.",
            "reading": "Situation taken as depth90 last_history_value <= -1 with forecast > 0; bars lacking the recorded raw value count as outside the situation.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, coin, ret, forecast)
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = to_time(df["timestamp"])
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    continue
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[p]) and fc[p] > 0:
                    coin_cases.append((ts.iloc[p].normalize(), r, float(fc[p])))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for day, r, f in coin_cases:
            cases.append((day, coin, r - drift, f))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "cases on distinct days": int(n_days)}

    mean_ex = None
    t_val = None
    slope = None
    if n_cases > 0:
        ex = np.array([c[2] for c in cases], dtype=float)
        fcs = np.array([c[3] for c in cases], dtype=float)
        mean_ex = float(ex.mean())
        if n_days > 1:
            dev = pd.Series(ex - mean_ex).groupby([c[0] for c in cases]).sum().values
            var_m = (n_days / (n_days - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
            se = np.sqrt(var_m)
            t_val = float(mean_ex / se) if se > 0 else None
        if n_cases > 1 and np.var(fcs) > 0:
            fm = fcs.mean()
            slope = float(np.sum((fcs - fm) * (ex - mean_ex)) / np.sum((fcs - fm) ** 2))

    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 30 cases on distinct days (%d), the plan's minimum count." % n_days
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean excess return above 0 with t >= 2 and a positive slope of excess return on the forecast."
        else:
            status = "inconclusive"
            decided = "A confirming mean (above 0, t >= 2) whose slope on the forecast is not positive."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2: deep falls kept falling against the coin's drift."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day summed together", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of excess 30-bar return on forecast across cases", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid bars at positions 0, 30, 60, ... of each window with a full 30-bar forward return inside the window; normal drift is each coin's mean 30-bar return over all its windows' grid bars; t uses day-clustered deviations (summed per UTC day) with a D/(D-1) correction; the plan's 'fewer than 30 cases on distinct days' is applied as the minimum count giving 'not observable'.",
    }
