import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    DIST = "debug_info.components.dist20.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime with a strategy; the vetoes send everything else to "chop"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if DIST in df.columns:
                dist = pd.to_numeric(df[DIST], errors="coerce")
            else:
                dist = pd.Series(np.nan, index=df.index)
            in_profile = df["regime"].astype(str) == PROFILE_REGIME
            situation = in_profile & dist.notna() & (dist > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    main_name = "OLS slope of 10-bar forward excess return on raw dist20, in-profile grid bars, pooled"
    threshold = "slope t >= 2 confirms (with positive supporting excess), t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are rising-calm bars with the close above its 20-day SMA and a positive (long) forecast.",
            "reading": "The rising-calm profile is read as the bars whose regime is 'unknown' (not vetoed to 'chop'), the situation as those bars with a raw dist20 above 0, the expected side long.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if DIST in df.columns:
                dist = pd.to_numeric(df[DIST], errors="coerce").to_numpy(dtype=float)
            else:
                dist = np.full(len(df), np.nan)
            reg = df["regime"].astype(str).to_numpy()
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({
                    "coin": coin, "ret": c1 / c0 - 1.0, "dist": dist[i],
                    "fc": fc[i], "prof": reg[i] == PROFILE_REGIME,
                })

    g = pd.DataFrame(rows, columns=["coin", "ret", "dist", "fc", "prof"])
    if len(g):
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
    else:
        g["excess"] = []

    ip = g[g["prof"].astype(bool) & g["dist"].notna() & g["excess"].notna()] if len(g) else g
    n_ip = int(len(ip))

    slope = None
    t = None
    if n_ip >= 3 and np.nanstd(ip["dist"].to_numpy(dtype=float)) > 0:
        lr = stats.linregress(ip["dist"].to_numpy(dtype=float), ip["excess"].to_numpy(dtype=float))
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    pos = g[(g["fc"] > 0) & g["excess"].notna()] if len(g) else g
    n_pos = int(len(pos))
    sup_val = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {
        "in-profile grid cases": n_ip,
        "grid bars with forecast > 0": n_pos,
    }

    if n_ip < 30:
        status = "not observable"
        decided = f"Only {n_ip} in-profile grid cases, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the distance), so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the supporting check's mean excess return is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check's mean excess return is not above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: a larger distance above the average is followed by a smaller rise."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean 10-bar excess return on grid bars with forecast > 0",
            "value": sup_val,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "In-profile means regime 'unknown' with a recorded raw dist20; the coin's mean 10-bar return is the mean over all its windows' non-overlapping grid returns (positions 0, 10, 20, ... from each window's first row); the plan's 'fewer than 30 in-profile grid cases' minimum is reported as 'not observable' as the workflow requires.",
    }
