import json
import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        mx = float(np.nanmax(np.abs(s.values.astype(float)))) if len(s) else 0.0
        if mx > 1e17:
            unit = "ns"
        elif mx > 1e14:
            unit = "us"
        elif mx > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _component_raw(df, cid):
    col = "debug_info.components.%s.last_history_value" % cid
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").values.astype(float)
    out = np.full(len(df), np.nan)
    if "debug_info.components" not in df.columns:
        return out
    for i, v in enumerate(df["debug_info.components"].values):
        d = v
        if isinstance(d, str):
            try:
                d = json.loads(d)
            except Exception:
                d = None
        if isinstance(d, dict):
            c = d.get(cid)
            if isinstance(c, str):
                try:
                    c = json.loads(c)
                except Exception:
                    c = None
            if isinstance(c, dict):
                x = c.get("last_history_value")
                try:
                    out[i] = float(x)
                except Exception:
                    pass
            else:
                x = d.get(cid + ".last_history_value")
                try:
                    out[i] = float(x)
                except Exception:
                    pass
    return out


def _cluster_t(values, days):
    v = np.asarray(values, dtype=float)
    n = len(v)
    if n < 2:
        return None
    m = v.mean()
    dev = pd.Series(v - m).groupby(np.asarray(days)).sum().values
    D = len(dev)
    if D < 2:
        return None
    var = (dev ** 2).sum() / (n ** 2) * (D / (D - 1.0))
    if var <= 0:
        return None
    return float(m / np.sqrt(var))


def measure(bars):
    H = 5
    CID = "quiet_fall"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            regime = df["regime"].astype(str).str.strip().str.lower().values
            raw = _component_raw(df, CID)
            ret30 = np.full(len(df), np.nan)
            if len(df) > 30:
                ret30[30:] = close[30:] / close[:-30] - 1.0
            fall = np.where(np.isnan(raw), ret30 < 0, raw < 0)
            in_profile = regime == "unknown"
            situ = in_profile & fall
            active = (~np.isnan(f)) & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    main_name = "mean of short-direction 5-bar unusual move x |forecast|/10, per case"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passing; reject: mean < 0 with t <= -2"
    reading = ("Profile membership is the recorded regime 'unknown' (the only regime with a strategy, i.e. neither veto fired) and a fall is a negative raw quiet_fall value; "
               "the case value is (drift - forward return) x (-forecast/10), i.e. the unusual move taken in the short direction as the plan's confirm rule describes; "
               "t uses per-day summed deviations; the larger |forecast| half is the top floor(n/2) cases by |forecast| (ties broken by coin then time).")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90% of the active bars are short bars inside the falling calm profile after a 30-day fall"
                           if n_active > 0 else "No active bars: the forecast is never non-zero"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, ts, day, f, fwd, drift)
    for coin in sorted(bars):
        grid_rets = []
        per_win = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] < 0:
                    per_win.append((coin, ts.iloc[i], ts.iloc[i].strftime("%Y-%m-%d"), f[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for c in per_win:
            cases.append(c + (drift,))

    n_cases = len(cases)
    days = [c[2] for c in cases]
    n_days = len(set(days))
    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "larger-|forecast| half minus smaller half, mean short-direction unusual move", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "No grid case with forecast < 0: the minimum of 100 cases on 50 distinct days is not reached",
            "reading": reading,
        }

    fs = np.array([c[3] for c in cases], dtype=float)
    fwd = np.array([c[4] for c in cases], dtype=float)
    dr = np.array([c[5] for c in cases], dtype=float)
    unusual_short = dr - fwd
    vals = unusual_short * (-fs / 10.0)
    mean_v = float(vals.mean())
    t = _cluster_t(vals, days)

    # supporting check
    order = sorted(range(n_cases), key=lambda k: (-abs(fs[k]), cases[k][0], cases[k][1]))
    k_big = n_cases // 2
    big = [order[k] for k in range(k_big)]
    small = [order[k] for k in range(k_big, n_cases)]
    if len(big) > 0 and len(small) > 0:
        diff = float(unusual_short[big].mean() - unusual_short[small].mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None
    supporting = {"name": "larger-|forecast| half minus smaller half, mean short-direction unusual move",
                  "value": diff, "passed": sup_pass}
    stat = {"name": "t of the mean, cases of one day summed", "value": t} if t is not None else None
    main = {"name": main_name, "value": mean_v, "statistic": stat, "threshold": thr}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = "The plan's minimum of at least 100 cases on at least 50 distinct days is not reached (%d cases, %d days)" % (n_cases, n_days)
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so neither the confirm nor the reject rule is met"
    elif mean_v > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean is positive with t >= 2 and the larger-|forecast| half beats the smaller half: the confirm rule"
        else:
            status = "inconclusive"
            decided = "The mean is positive with t >= 2 but the supporting check fails: inconclusive by the plan's rule"
    elif mean_v < 0 and t <= -2:
        status = "rejected"
        decided = "The mean is negative with t <= -2: the reject rule"
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2: inconclusive by the plan's rule"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
