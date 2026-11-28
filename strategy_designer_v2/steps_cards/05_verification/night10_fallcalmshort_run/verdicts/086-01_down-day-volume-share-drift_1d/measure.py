import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    XCOL = "debug_info.components.down_vol_share.last_history_value"

    def _days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            mx = s.abs().max()
            unit = "ms" if mx > 1e11 else "s"
            dt = pd.to_datetime(s, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.floor("D").dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).str.lower().values
            x = (pd.to_numeric(df[XCOL], errors="coerce").values
                 if XCOL in df.columns else np.full(len(df), np.nan))
            active = fc != 0
            in_prof = reg == "unknown"
            situ = in_prof & np.nan_to_num(x > 0, nan=False).astype(bool)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())
    if n_active > 0:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.9)
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the "
                           "falling calm profile with a down-day volume share above 0.5, as the Fidelity states."),
            "reading": "The profile is read from the recorded regime ('unknown' = falling calm, not vetoed), "
                       "since the detector's components are not recorded.",
        }

    # ---------- 2. grid cells ----------
    cells = []  # coin, day, fwd, x, forecast, in_profile
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).str.lower().values
            x = (pd.to_numeric(df[XCOL], errors="coerce").values
                 if XCOL in df.columns else np.full(len(df), np.nan))
            days = _days(df["timestamp"])
            for p in range(0, len(df), H):
                if p + H >= len(df):
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                cells.append((coin, days[p], c1 / c0 - 1.0, x[p], fc[p], reg[p] == "unknown"))
    cdf = pd.DataFrame(cells, columns=["coin", "day", "fwd", "x", "fc", "inprof"])

    if len(cdf):
        drift = cdf.groupby("coin")["fwd"].mean()
        cdf["dev"] = cdf["fwd"] - cdf["coin"].map(drift)
    else:
        cdf["dev"] = []

    prof = cdf[cdf["inprof"]] if len(cdf) else cdf
    reg_df = prof[np.isfinite(prof["x"].astype(float))] if len(prof) else prof
    n_cells = int(len(reg_df))
    short_df = prof[prof["fc"] < 0] if len(prof) else prof
    n_short = int(len(short_df))
    n_days = int(reg_df["day"].nunique()) if n_cells else 0

    # slope with day-clustered t
    slope, tstat = None, None
    if n_cells >= 3:
        xv = reg_df["x"].astype(float).values
        yv = reg_df["dev"].astype(float).values
        xm = xv - xv.mean()
        sxx = float((xm ** 2).sum())
        if sxx > 0:
            b = float((xm * (yv - yv.mean())).sum() / sxx)
            a = yv.mean() - b * xv.mean()
            e = yv - a - b * xv
            sc = pd.Series(xm * e).groupby(reg_df["day"].values).sum().values
            G = len(sc)
            if G > 1:
                var = (G / (G - 1)) * float((sc ** 2).sum()) / sxx ** 2
                slope = b
                tstat = b / np.sqrt(var) if var > 0 else None

    # supporting check
    sup_val = None
    if n_short > 0:
        sup_val = float((-short_df["dev"].astype(float)).mean())
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    counts = {"in-profile grid cells": n_cells,
              "in-profile grid cells with forecast < 0": n_short,
              "days of the in-profile grid cells": n_days}

    # ---------- 3. decision ----------
    if n_cells < 30 or n_short < 20:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_cells} in-profile grid cells (needs 30) and "
                      f"{n_short} with forecast < 0 (needs 20).")
    elif tstat is None or slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and tstat <= -2:
        if sup_pass:
            status = "confirmed"
            decided_by = "Confirm: the slope is negative with t <= -2 and the short-side mean unusual move is above 0."
        else:
            status = "inconclusive"
            decided_by = "Inconclusive: a confirming slope (t <= -2) with a failed supporting check."
    elif slope > 0 and tstat >= 2:
        status = "rejected"
        decided_by = "Reject: the slope is positive with t >= +2."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "slope of 5-bar forward return minus coin mean 5-bar return on the raw centred down-day volume share",
            "value": None if slope is None else float(slope),
            "statistic": None if tstat is None else {"name": "OLS slope t, cells of the same day clustered",
                                                     "value": float(tstat)},
            "threshold": "confirm: slope < 0 with t <= -2 (and check passes); reject: slope > 0 with t >= +2",
        },
        "supporting_check": {"name": "mean unusual 5-bar move in the short direction over grid cells with forecast < 0",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("In-profile means regime 'unknown' (the falling calm profile not vetoed, as the detector's "
                    "components are not recorded); grid cells are positions 0,5,10,... of each window with a 5-bar "
                    "return inside the window, the coin's mean is over all its grid cells in all windows, the slope is "
                    "OLS with an intercept and a day-clustered (CR1, G/(G-1)) standard error, and the plan's "
                    "'too few cells' case is reported as not observable."),
    }
