import numpy as np
import pandas as pd


def measure(bars):
    RISE_COL = "debug_info.components.rise.last_history_value"
    BAND = 2.0
    TOL = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0
            std30 = ret1.rolling(30, min_periods=30).std()
            recomputed = ret1 / std30
            if RISE_COL in df.columns:
                rise = pd.to_numeric(df[RISE_COL], errors="coerce")
                rise = rise.where(rise.notna(), recomputed)
            else:
                rise = recomputed
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = f != 0
            n_active += int(active.sum())
            ok = active & (rise > 0) & (rise <= 1.0 + TOL) & (f < 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean next-day unusual move in the short direction",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"distinct days with cases": None},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short bars with a one-day "
                           "volatility-scaled rise above 0 and at most 1, as the plan's situation requires"
                           if n_active > 0 else "the record has no bar with a non-zero forecast"),
            "reading": "situation checked on the rise condition (0 < scaled rise <= 1) and short side; the profile "
                       "components are not recorded and were not rebuilt",
        }

    # ---------- 2. criterion ----------
    rows = []  # (day, unusual_short, |forecast|)
    for coin, wins in bars.items():
        # coin's normal daily drift over all windows
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).iloc[:-1]
            all_r.append(r.dropna())
        if not all_r:
            continue
        allr = pd.concat(all_r)
        if len(allr) == 0:
            continue
        drift = float(allr.mean())

        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").values
            ref = 0.0
            prev_side = 0
            for i in range(len(df)):
                fi = f[i]
                side = 1 if fi > 0 else (-1 if fi < 0 else 0)
                is_bet = False
                if side == -1:
                    mag = -fi
                    if prev_side != -1:
                        ref = 0.0
                    if mag - ref >= BAND - TOL:
                        is_bet = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    ref = 0.0
                prev_side = side
                if is_bet and i + 1 < len(df):
                    if np.isfinite(c[i]) and np.isfinite(c[i + 1]) and c[i] != 0:
                        r = c[i + 1] / c[i] - 1.0
                        rows.append((days[i], -(r - drift), abs(fi)))

    n_cases = len(rows)
    if n_cases > 0:
        cases = pd.DataFrame(rows, columns=["day", "u", "size"])
        n_days = int(cases["day"].nunique())
    else:
        cases = None
        n_days = 0

    mean_u = None
    t_val = None
    slope = None
    if n_cases > 0:
        mean_u = float(cases["u"].mean())
        dev = cases["u"] - mean_u
        per_day = dev.groupby(cases["day"]).sum()
        G = len(per_day)
        if G > 1:
            se = np.sqrt(G / (G - 1.0) * float((per_day ** 2).sum())) / n_cases
            t_val = float(mean_u / se) if se > 0 else None
        if n_cases >= 2 and cases["size"].nunique() > 1:
            slope = float(np.polyfit(cases["size"].values, cases["u"].values, 1)[0])

    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"only {n_days} distinct days with cases, below the plan's minimum of 30"
    elif t_val is None:
        status = "inconclusive"
        decided = "the t of the mean unusual move could not be computed"
    elif mean_u > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "the mean unusual move is positive with t >= 2 and the slope on forecast size is above 0"
        else:
            status = "inconclusive"
            decided = "a confirming t (>= 2) but the slope on forecast size is at or below 0"
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "the mean unusual move is negative with t <= -2: the coins rise more than their drift after these up days"
    else:
        status = "inconclusive"
        decided = "the t of the mean unusual move is between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean next-day unusual move in the short direction",
                         "value": mean_u,
                         "statistic": None if t_val is None else {"name": "t of the mean, cases of one day summed", "value": t_val},
                         "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"},
        "supporting_check": {"name": "OLS slope of the short unusual move on |forecast|",
                             "value": slope, "passed": slope_pass},
        "counts": {"distinct days with cases": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": ("a case is a short bet as the workflow defines it (a rise of the short forecast of at least 2 points "
                    "from its lowest level since the last bet, every bar being a 1-bar grid cell), forecast size is "
                    "|forecast|, the day-clustered standard error uses a G/(G-1) correction, the 30-day minimum maps to "
                    "'not observable', and the situation check uses the rise condition and short side only since the "
                    "profile components are not recorded"),
    }
