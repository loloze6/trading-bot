import json
import numpy as np
import pandas as pd


def _to_ts(s):
    if pd.api.types.is_numeric_dtype(s):
        v = pd.Series(s).astype(float)
        unit = "ms" if v.abs().max() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _component_raw(df, cid):
    col = "debug_info.components.%s.last_history_value" % cid
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
    out = np.full(len(df), np.nan)
    if "debug_info.components" in df.columns:
        for i, v in enumerate(df["debug_info.components"].tolist()):
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict) and isinstance(d.get(cid), dict):
                x = d[cid].get("last_history_value")
                try:
                    out[i] = float(x)
                except (TypeError, ValueError):
                    pass
    return out


def measure(bars):
    H = 5
    BAND = 2.0

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            hi = df["high"].to_numpy(dtype=float)
            lo = df["low"].to_numpy(dtype=float)
            cl = df["close"].to_numpy(dtype=float)
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            r5_px = np.full(len(df), np.nan)
            if len(df) > 5:
                r5_px[5:] = cl[5:] / cl[:-5] - 1.0
            r5_rec = _component_raw(df, "fall5")
            r5 = np.where(np.isfinite(r5_rec), r5_rec, r5_px)
            reg = df["regime"].astype(str).str.lower().to_numpy()
            profile = reg != "chop"
            situ = profile & (loc > 0.5) & (r5 < 0)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    reading = ("Profile taken from the recorded regime (not 'chop', the vetoes' result outside the choppy agitated "
               "profile) since its 365-bar volatility percentile cannot be rebuilt from the record, close location "
               "and 5-day return from prices (5-day return from fall5's raw value where recorded); a case is the first "
               "short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, reset at flat) "
               "in each 5-bar grid cell of a window, with a full 5-bar forward return in that window; drift is the mean "
               "of the coin's grid 5-bar returns over all its windows; the day-clustered t uses per-day summed "
               "deviations with a D/(D-1) correction; the larger-size half is cases with |forecast| above the median, "
               "the smaller-size half those at or below it; the plan's 'fewer than 30 cases or days' is reported as "
               "not observable.")

    main_name = "mean unusual 5-day move in the short direction vs coin drift"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the choppy "
                           "agitated profile with close location above 0.5 and a negative 5-day return."),
            "reading": reading,
        }

    # ---------- cases ----------
    rows = []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            cl = df["close"].to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = _to_ts(df["timestamp"])
            days = ts.dt.strftime("%Y-%m-%d").to_numpy()
            for p in range(0, n - H, H):
                r = cl[p + H] / cl[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # bets on the short side
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if f[i] >= 0:
                    ref = 0.0
                    continue
                s = -f[i]
                if s - ref >= BAND:
                    bet[i] = True
                    ref = s
                else:
                    ref = min(ref, s)
            for c0 in range(0, n, H):
                idx = [i for i in range(c0, min(c0 + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                r = cl[i + H] / cl[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_cases.append((r, abs(f[i]), days[i]))
        if not coin_cases or not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, a, d in coin_cases:
            rows.append({"x": -(r - drift), "absf": a, "day": d})

    cases = pd.DataFrame(rows, columns=["x", "absf", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = float(cases["x"].mean()) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["x"] - mean
        S = dev.groupby(cases["day"]).sum().to_numpy()
        D = len(S)
        var = (D / (D - 1.0)) * np.sum(S ** 2) / (n_cases ** 2)
        if var > 0:
            tval = float(mean / np.sqrt(var))

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = float(cases["absf"].median())
        big = cases.loc[cases["absf"] > med, "x"]
        small = cases.loc[cases["absf"] <= med, "x"]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": mean,
            "statistic": {"name": "day-clustered t of the mean", "value": tval} if tval is not None else None,
            "threshold": thr}
    sup = {"name": "larger-|forecast| half minus smaller half, mean unusual short move",
           "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 30 cases on at least 30 distinct days (%d cases, %d days)." % (n_cases, n_days)
    elif tval is not None and mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual short move is positive with t >= 2 and the larger-size half beats the smaller-size half."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual short move is negative with t <= -2: prices rise after these closes beyond the coin's drift."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the larger-size half does not beat the smaller-size half."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual short move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
