import numpy as np
import pandas as pd

H = 6
BAND = 2.0
CL_EDGE = 0.75
MIN_DAYS = 30
LHV = "debug_info.components.low_close.last_history_value"


def _cl_prev_from_prices(df):
    h = df["high"].astype(float)
    l = df["low"].astype(float)
    c = df["close"].astype(float)
    rng = h - l
    cl = (h - c) / rng.where(rng != 0)
    return cl.shift(1)


def _bets(fc):
    # short-side bets: a rise of the short forecast (-forecast) of at least BAND from its
    # lowest level on that side since the last bet (from 0 after a flat or a change of side)
    out = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f >= 0:
            ref = 0.0
            continue
        s = -f
        if s - ref >= BAND - 1e-12:
            out[i] = True
            ref = s
        else:
            ref = min(ref, s)
    return out


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            cl = _cl_prev_from_prices(df)
            if LHV in df.columns:
                rec = pd.to_numeric(df[LHV], errors="coerce")
                cl = rec.where(rec.notna(), cl)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (cl >= CL_EDGE) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 6-bar move of short cases (short direction, coin drift removed)"
    threshold = "t >= 2 confirms (with supporting difference > 0); t <= -2 rejects; at least 30 distinct case days"
    reading = ("The situation is checked as previous-day close location (recorded raw value, else rebuilt from "
               "prices) >= 0.75 with a negative forecast, the agitated profile not being recomputable from the record; "
               "a case is the first short bet (rise of -forecast by >= 2 from its low since the last bet) in each "
               "6-bar grid cell of a window, its return taken from that bar's close over 6 bars inside the window, "
               "the drift is the coin's mean 6-bar return on the non-overlapping grid of all its windows, the t is "
               "day-clustered (deviations summed per UTC day), and the median split puts |forecast| above the "
               "median in the upper half and at or below it in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the active bars are short bars with a previous-day close "
                           f"location of 0.75 or more, below the 90 % the plan's situation requires."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df.sort_values("timestamp")["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    rows = []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = df["close"].astype(float).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            bet = _bets(fc)
            n = len(df)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] <= 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                u = -(r - drift[coin])
                rows.append({"day": ts.iloc[i].strftime("%Y-%m-%d"), "u": u, "absf": abs(fc[i])})

    cases = pd.DataFrame(rows, columns=["day", "u", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct case days": n_days, "cases": n_cases}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cases["u"] - mean_u
        ds = dev.groupby(cases["day"]).sum().to_numpy()
        var = (n_days / (n_days - 1.0)) * float(np.sum(ds ** 2)) / (n_cases ** 2)
        if var > 0:
            t_val = float(mean_u / np.sqrt(var))

    diff = None
    if n_cases >= 2:
        med = float(cases["absf"].median())
        up = cases.loc[cases["absf"] > med, "u"]
        lo = cases.loc[cases["absf"] <= med, "u"]
        if len(up) and len(lo):
            diff = float(up.mean() - lo.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t_val is None else {"name": "day-clustered t of the mean", "value": t_val},
            "threshold": threshold}
    supporting = {"name": "upper-half minus lower-half mean unusual move by |forecast| at entry",
                  "value": diff, "passed": sup_pass}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so it is not >= 2 nor <= -2."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move has t >= 2 and the upper-minus-lower |forecast| difference is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move has t <= -2: the coin rises more than its drift after low closes."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The t is >= 2 but the supporting difference is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
