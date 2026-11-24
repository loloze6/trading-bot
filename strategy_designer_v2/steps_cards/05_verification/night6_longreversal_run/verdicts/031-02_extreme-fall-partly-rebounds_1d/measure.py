import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 30
    GRID = [0, 30, 60, 90]
    RAW_COL = "debug_info.components.fall.last_history_value"

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def parse_comp(v):
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                return np.nan
        if isinstance(v, dict):
            f = v.get("fall")
            if isinstance(f, dict):
                x = f.get("last_history_value")
                try:
                    return float(x) if x is not None else np.nan
                except Exception:
                    return np.nan
        return np.nan

    def raw_fall(df):
        if RAW_COL in df.columns:
            return pd.to_numeric(df[RAW_COL], errors="coerce")
        if "debug_info.components" in df.columns:
            return df["debug_info.components"].apply(parse_comp).astype(float)
        return pd.Series(np.nan, index=df.index)

    # ---- 1. situation check -------------------------------------------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = raw_fall(df)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw <= -1.0) & (fc > 0)
            n_agree += int(ok.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess 30-day return of in-regime grid cells",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with day-clustered t >= 2 (confirm), mean < 0 with t <= -2 (reject), over at least 30 cases"},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the 90-day return is at or below minus one usual 90-day move (recorded raw value of 'fall' <= -1), as the plan's Fidelity requires.",
            "reading": "The situation is read from the recorded raw value of the 'fall' component (the same component as the detector's), a bar with that value missing counting as not in the situation.",
        }

    # ---- 2. criterion ---------------------------------------------------------
    cases = []  # (coin, day, ret, forecast)
    coin_grid_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = to_time(df["timestamp"])
            n = len(df)
            for p in GRID:
                if p + H >= n:
                    continue
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                rets_all.append(r)
                if np.isfinite(fc[p]) and fc[p] > 0:
                    day = ts.iloc[p].floor("D")
                    cases.append((coin, day, r, float(fc[p])))
        coin_grid_rets[coin] = float(np.mean(rets_all)) if rets_all else np.nan

    rows = []
    for coin, day, r, f in cases:
        mu = coin_grid_rets.get(coin, np.nan)
        if np.isfinite(mu):
            rows.append((day, r - mu, f))
    n = len(rows)
    ex = np.array([r[1] for r in rows], dtype=float)
    fcs = np.array([r[2] for r in rows], dtype=float)
    days = [r[0] for r in rows]
    n_days = len(set(days))

    mean_ex = float(np.mean(ex)) if n > 0 else None
    t = None
    if n > 1 and n_days > 1:
        dev = pd.Series(ex - mean_ex).groupby(pd.Series(days)).sum().values
        G = len(dev)
        var = (G / (G - 1)) * np.sum(dev ** 2) / (n ** 2)
        se = np.sqrt(var)
        t = float(mean_ex / se) if se > 0 else None

    sup_val, sup_pass = None, None
    if n > 1:
        med = float(np.median(fcs))
        hi = ex[fcs > med]
        lo = ex[fcs < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"in-regime cases": n, "days": n_days, "active bars": n_active}

    if n < 30:
        status = "not observable"
        decided = f"Fewer than 30 in-regime cases ({n}), the plan's minimum count."
    elif t is None:
        status = "inconclusive"
        decided = "The clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess 30-day return above 0 with t >= 2 over at least 30 cases, and the cases above the median forecast beat those below it."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the supporting check fails: a confirm without the supporting check is inconclusive."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess 30-day return below 0 with t <= -2 over at least 30 cases: deep falls keep falling more than usual."
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean excess 30-day return of in-regime grid cells",
                         "value": mean_ex,
                         "statistic": ({"name": "t clustered by day", "value": t} if t is not None else None),
                         "threshold": "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject)"},
        "supporting_check": {"name": "mean excess return above minus below median forecast",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid cells are the rows at positions 0, 30, 60, 90 of each window with a forward 30-bar close inside the window; the coin's mean 30-day return is taken over all its grid cells in all windows; the day-clustered t sums the deviations per UTC day with a G/(G-1) correction; the median split compares cases strictly above with cases strictly below the median forecast, ties left out.",
    }
