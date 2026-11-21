import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    FALL1D = "debug_info.components.fall1d.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # 72-bar past return (detector component, not recorded): recompute inside the window
            r72 = close / close.shift(H) - 1.0
            # 24-bar past return: recorded raw value, else recomputed from prices
            r24_px = close / close.shift(24) - 1.0
            if FALL1D in df.columns:
                r24 = pd.to_numeric(df[FALL1D], errors="coerce").fillna(r24_px)
            else:
                r24 = r24_px
            active = fc.notna() & (fc != 0)
            usable = active & r72.notna() & r24.notna()
            situ = (r72 < 0) & (r24 < 0) & (fc > 0)
            n_active += int(usable.sum())
            n_agree += int((usable & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 72-bar return is negative and the "
                           "last 24-bar return is negative with a long forecast, as the Fidelity's situation and side require"
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation"),
            "reading": "Bars whose 72-bar past return cannot be computed inside their window are left out of the check.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            for i in range(0, n, H):
                if i + H >= n:
                    break
                fwd = close[i + H] / close[i] - 1.0
                rows.append((coin, fwd, fc[i], reg[i]))
    g = pd.DataFrame(rows, columns=["coin", "fwd", "fc", "regime"])
    g = g[np.isfinite(g["fwd"])]
    coin_mean = g.groupby("coin")["fwd"].mean()
    g["excess"] = g["fwd"] - g["coin"].map(coin_mean)

    mr = g[(g["regime"] == "mean_reversion") & g["fc"].notna() & g["excess"].notna()]
    n_mr = int(len(mr))
    n_pos = int((mr["fc"] > 0).sum())
    counts = {"grid bars in mean_reversion": n_mr, "grid bars in mean_reversion with forecast above 0": n_pos}

    slope = None
    t = None
    if n_mr >= 3 and mr["fc"].std() > 0:
        lr = stats.linregress(mr["fc"].values, mr["excess"].values)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sw = mr["fc"].sum()
    wmean = float((mr["excess"] * mr["fc"]).sum() / sw) if sw > 0 else None
    check_pass = (wmean is not None and wmean > 0)

    main = {
        "name": "pooled OLS slope of excess 72-bar forward return on forecast (mean_reversion grid bars)",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
        "threshold": "confirm if t >= 2 with the check passing; reject if t <= -2",
    }
    support = {"name": "forecast-weighted mean excess 72-bar return > 0", "value": wmean,
               "passed": check_pass if wmean is not None else None}

    reading = ("Grid at positions 0, 72, 144, ... of each window with a full 72-bar forward return inside the window; "
               "the coin's mean 72-bar return is the mean over all its grid bars across all windows and regimes; "
               "the plan's 'fewer cases is inconclusive' is reported as 'not observable' per the workflow.")

    if n_mr < 200 or n_pos < 100:
        status = "not observable"
        decided = ("Minimum count not reached: need at least 200 mean_reversion grid bars (have %d) with at least 100 "
                   "forecast above 0 (have %d)." % (n_mr, n_pos))
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
