import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.ret3d.last_history_value"
    POS = "postRebalance_current_allocation"
    SIT_HOURS = {10, 11, 12}  # bars whose next bar starts at 11:00, 12:00, 13:00 UTC

    def prep(df):
        df = df.copy().reset_index(drop=True)
        ts = pd.to_datetime(df["timestamp"], utc=True)
        df["_ts"] = ts
        df["_hour"] = ts.dt.hour
        df["_minute"] = ts.dt.minute
        close = df["close"].astype(float)
        df["_close"] = close
        df["_r1"] = close.shift(-1) / close - 1.0
        df["_r3"] = close.shift(-3) / close - 1.0
        df["_ret72"] = close / close.shift(72) - 1.0
        return df

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            prepared[coin][w] = d
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), d["_ret72"])
            else:
                raw = d["_ret72"]
            in_sit = d["_hour"].isin(SIT_HOURS) & (d["_minute"] == 0)
            expected = -np.sign(raw)
            ok = in_sit & raw.notna() & (expected != 0) & (np.sign(fc) == expected)
            n_active += int(active.sum())
            n_agree += int((active & ok).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed_sit = bool(agreement is not None and agreement >= 0.90)

    main_name = "t of slope of 10:00-bar excess 3h return on forecast (pooled)"
    threshold = "t >= 2 confirms (with >= 500 cases and supporting check), t <= -2 rejects (with >= 500 cases)"
    reading = ("Situation bars are those stamped 10:00, 11:00, 12:00 UTC (next bar starts 11-13) with expected side "
               "minus the sign of the 72-bar return; close[t+3] is taken positionally inside the window; the coin's "
               "mean 3-bar return uses the non-overlapping grid 0,3,6,... of each window pooled over windows; the "
               "supporting check uses the positions after the 10:00, 11:00 and 12:00 bars' trades, held over the "
               "11:00-13:00 bars, against the coin's mean hourly return over all windows.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"daily cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are 10:00-12:00 UTC bars with the "
                           "sign opposite to the 72-bar return, which the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- main measure ----------
    xs, ys = [], []
    gains = []
    for coin, wins in prepared.items():
        # coin mean 3-bar return (non-overlapping grid) and mean hourly return, over all windows
        r3_all, r1_all = [], []
        for w, d in wins.items():
            grid = d["_r3"].iloc[0::3]
            r3_all.append(grid.dropna().values)
            r1_all.append(d["_r1"].dropna().values)
        r3_all = np.concatenate(r3_all) if r3_all else np.array([])
        r1_all = np.concatenate(r1_all) if r1_all else np.array([])
        if len(r3_all) == 0 or len(r1_all) == 0:
            continue
        mu3 = float(np.mean(r3_all))
        mu1 = float(np.mean(r1_all))
        for w, d in wins.items():
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            sel = (d["_hour"] == 10) & (d["_minute"] == 0)
            sub = pd.DataFrame({"f": fc[sel], "y": d["_r3"][sel] - mu3}).dropna()
            xs.append(sub["f"].values)
            ys.append(sub["y"].values)
            # supporting check
            pos = pd.to_numeric(d[POS], errors="coerce") if POS in d.columns else pd.Series(np.nan, index=d.index)
            sel2 = d["_hour"].isin(SIT_HOURS) & (d["_minute"] == 0)
            g = (pos[sel2] * (d["_r1"][sel2] - mu1)).dropna()
            gains.append(g.values)

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_cases = int(len(x))
    g = np.concatenate(gains) if gains else np.array([])

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_gain = float(np.mean(g)) if len(g) > 0 else None
    sup_passed = None if mean_gain is None else bool(mean_gain > 0)

    if n_cases < 500:
        status = "not observable"
        decided = f"The plan's minimum of 500 daily cases is not reached ({n_cases} cases)."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more with at least 500 cases and the supporting check passes."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 500 cases."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 with at least 500 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean before-cost excess gain of position over 11:00-13:00 bars",
            "value": mean_gain,
            "passed": sup_passed,
        },
        "counts": {"daily cases": n_cases, "supporting check bars": int(len(g))},
        "decided_by": decided,
        "reading": reading,
    }
