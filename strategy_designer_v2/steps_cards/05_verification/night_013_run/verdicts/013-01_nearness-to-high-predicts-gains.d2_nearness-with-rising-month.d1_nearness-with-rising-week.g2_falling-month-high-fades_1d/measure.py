import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RET_PERIOD = 30
    RAW = "debug_info.components.dist_high.last_history_value"

    # ---------- 1. situation check ----------
    # Pool the raw distance values to find which way the component signs "below the high".
    raw_all = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if RAW in df.columns:
                raw_all.append(pd.to_numeric(df[RAW], errors="coerce").dropna().values)
    raw_all = np.concatenate(raw_all) if raw_all else np.array([])
    # Positive "distance below the high": if the raw value is mostly <= 0 (close/high - 1), flip it.
    flip = bool(len(raw_all) and np.nanmedian(raw_all) <= 0)

    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret30 = close / close.shift(RET_PERIOD) - 1.0
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            dbelow = -raw if flip else raw

            prev_d = None
            prev_f = None
            for i in range(len(df)):
                f = fc.iloc[i]
                d = dbelow.iloc[i]
                if f != 0:
                    n_active += 1
                    r = ret30.iloc[i]
                    if pd.notna(r):
                        in_sit = r < 0
                    else:
                        # Too few bars in the window to recompute the 30-bar change: use the detector's decision.
                        in_sit = regime.iloc[i] == "mean_reversion"
                    side_ok = True
                    if prev_d is not None and pd.notna(d) and pd.notna(prev_d):
                        dd = d - prev_d
                        dfc = f - prev_f
                        # Further below the high -> larger long (the 364-bar mean/std move slowly).
                        if dd != 0 and dfc != 0 and np.sign(dd) != np.sign(dfc):
                            side_ok = False
                    if in_sit and side_ok:
                        n_agree += 1
                if f != 0 and pd.notna(d):
                    prev_d, prev_f = d, f
                else:
                    prev_d, prev_f = None, None

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is the 30-bar close change below 0 recomputed inside each window (the detector's "
               "regime is used only on bars with fewer than 30 prior bars in the window), and the graded side is checked "
               "as the forecast rising when the bar-to-bar distance below the 364-bar high rises; the grid keeps rows "
               "with regime 'mean_reversion', each coin's mean 7-bar return is the mean of all its grid forward "
               "returns over all windows, the slope t is the OLS t of excess return on forecast, and the thirds "
               "are split by forecast rank into three equal-sized groups.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "OLS slope of excess 7-bar return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are falling-month (30-bar change < 0) bars whose forecast "
                           "grows with the distance below the 364-bar high."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "fr": c1 / c0 - 1.0, "fc": fc[i], "reg": reg[i]})

    grid = pd.DataFrame(rows, columns=["coin", "fr", "fc", "reg"])
    if len(grid):
        coin_mean = grid.groupby("coin")["fr"].mean()
        grid["ex"] = grid["fr"] - grid["coin"].map(coin_mean)
        cases = grid[(grid["reg"] == "mean_reversion")].dropna(subset=["ex", "fc"])
    else:
        cases = pd.DataFrame(columns=["coin", "fr", "fc", "reg", "ex"])
    n = int(len(cases))

    slope = None
    tval = None
    if n >= 3 and np.nanstd(cases["fc"].values) > 0:
        res = stats.linregress(cases["fc"].values.astype(float), cases["ex"].values.astype(float))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    sup_val = None
    sup_pass = None
    if n >= 3:
        ranks = cases["fc"].rank(method="first").values
        third = pd.qcut(ranks, 3, labels=False)
        ex = cases["ex"].values
        low = ex[third == 0]
        high = ex[third == 2]
        if len(low) and len(high):
            sup_val = float(np.mean(low) - np.mean(high))
            sup_pass = bool(sup_val < 0)

    main = {"name": "OLS slope of excess 7-bar return on forecast, pooled",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": "t >= 2 (with supporting check) confirms; t <= -2 rejects; at least 100 cases"}
    support = {"name": "mean excess return, nearest third minus farthest third (must be < 0)",
               "value": sup_val, "passed": sup_pass}
    counts = {"cases": n}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} independent cases, fewer than the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope t is 2 or more, the nearest-minus-farthest third difference is below 0, with at least 100 cases."
    elif tval >= 2:
        status = "inconclusive"
        decided = "A confirming slope t of 2 or more whose supporting check fails is inconclusive."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less: further below the high is followed by lower returns."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
