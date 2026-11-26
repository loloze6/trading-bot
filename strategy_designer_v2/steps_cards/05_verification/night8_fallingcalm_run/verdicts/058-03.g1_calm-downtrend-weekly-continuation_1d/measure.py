import numpy as np
import pandas as pd


def _to_dt(s):
    if pd.api.types.is_numeric_dtype(s):
        v = pd.to_numeric(s, errors="coerce")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True, errors="coerce")


def measure(bars):
    H = 5
    RET_COL = "debug_info.components.ret5.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            ret_price = close / close.shift(H) - 1.0
            if RET_COL in d.columns:
                ret5 = pd.to_numeric(d[RET_COL], errors="coerce")
                ret5 = ret5.where(ret5.notna(), ret_price)
            else:
                ret5 = ret_price
            regime = d["regime"].astype(str)
            active = fc.notna() & (fc != 0)
            in_profile = regime == "unknown"
            side_ok = np.sign(fc) == np.sign(ret5)
            ok = active & in_profile & ret5.notna() & side_ok
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (next 5-bar return - coin drift), day-clustered"
    threshold = "confirm: mean > 0 with t >= 2 over >= 50 distinct days; reject: mean < 0 with t <= -2 over >= 50 distinct days"
    reading = ("Profile taken from the recorded regime ('unknown' = falling calm, both vetoes off), side = sign of the 5-day return "
               "(ret5 raw value, else recomputed from closes); drift = coin's mean next-5-bar return over all windows' grid bars; "
               "day-clustered t uses per-day summed deviations with a G/(G-1) correction; fewer than 50 distinct days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct days": 0},
            "decided_by": ("Fewer than 90% of active bars are in the falling calm profile with the forecast's sign equal to "
                           "the sign of the past 5-day return (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    grid_rows = []  # coin, ts, fc, fwd
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = _to_dt(d["timestamp"])
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((coin, ts.iloc[i], fc[i], c1 / c0 - 1.0))
    g = pd.DataFrame(grid_rows, columns=["coin", "ts", "fc", "fwd"])
    if len(g) == 0:
        g = pd.DataFrame(columns=["coin", "ts", "fc", "fwd"])
    drift = g.groupby("coin")["fwd"].mean() if len(g) else pd.Series(dtype=float)
    cases = g[g["fc"].notna() & (g["fc"] != 0)].copy()
    if len(cases):
        cases["x"] = cases["fc"] / 10.0 * (cases["fwd"] - cases["coin"].map(drift))
        cases = cases[cases["x"].notna() & cases["ts"].notna()]
        cases["day"] = cases["ts"].dt.floor("D")
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = None
    tval = None
    if n_cases > 0:
        x = cases["x"].values.astype(float)
        m = float(np.mean(x))
        mean = m
        dev = pd.Series(x - m, index=cases.index).groupby(cases["day"]).sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            tval = float(m / se) if se > 0 else None

    counts = {"distinct days": n_days, "cases": n_cases}
    stat = {"name": "t of the mean, cases of one day together", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": mean, "statistic": stat, "threshold": threshold}

    if n_days < 50:
        status = "not observable"
        decided = "Fewer than 50 distinct days of cases (%d), the plan's minimum count." % n_days
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2:
        status = "confirmed"
        decided = "The mean signed excess return is above 0 with t of 2 or more over at least 50 distinct days."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean is below 0 with t of -2 or less over at least 50 distinct days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan rules inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
