import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    S_CROSS = np.sqrt(300.0)  # -3s + s^3/100 = 0  ->  s = sqrt(300) ~ 17.32
    TOL = 0.5                 # bars this close to the crossing may take either side
    RAW = "debug_info.components.fall_short.last_history_value"
    POST = "debug_info.components.fall_short.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            # recompute the 14-bar change from prices where the raw value is not recorded
            raw = raw.where(raw.notna(), close / close.shift(14) - 1.0)
            post = pd.to_numeric(df[POST], errors="coerce") if POST in df.columns else pd.Series(np.nan, index=df.index)
            s = (-post).clip(lower=0.0)  # size of the standardised fall, 0..20
            for i in range(len(df)):
                f = fc.iloc[i]
                if pd.isna(f) or f == 0:
                    continue
                n_active += 1
                r = raw.iloc[i]
                if pd.isna(r):
                    is_fall = (not pd.isna(post.iloc[i])) and post.iloc[i] < 0
                else:
                    is_fall = r < 0
                if not is_fall:
                    continue
                si = s.iloc[i]
                if pd.isna(si):
                    continue
                if abs(si - S_CROSS) <= TOL:
                    ok = True
                elif si < S_CROSS:
                    ok = f < 0  # moderate fall: short
                else:
                    ok = f > 0  # deepest fall: long
                if ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 7-bar return on forecast (non-overlapping grid, forecast != 0, pooled)"
    thr = "t >= +2 confirms (with positive supporting difference); t <= -2 rejects; between is inconclusive"
    sup_name = "mean excess 7-bar return at forecast > 0 minus at forecast < 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are 14-bar falls with the forecast short below s~17.3 and long above it, as the Fidelity states.",
            "reading": "Fall size s taken as minus the fall_short post-pipeline value, raw 14-bar change sign from last_history_value (prices when missing); bars within 0.5 of the crossing s=17.32 accepted on either side.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[t]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(g):
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
        s_ = g[g["fc"].notna() & (g["fc"] != 0)]
    else:
        s_ = pd.DataFrame(columns=["coin", "ret", "fc", "excess"])

    n_nz = int(len(s_))
    pos = s_[s_["fc"] > 0]["excess"]
    neg = s_[s_["fc"] < 0]["excess"]
    n_pos = int(len(pos))
    counts = {"non-zero grid points": n_nz, "grid points with forecast > 0": n_pos,
              "grid points with forecast < 0": int(len(neg))}

    slope, tval = None, None
    if n_nz >= 3 and s_["fc"].astype(float).var() > 0:
        lr = stats.linregress(s_["fc"].astype(float).values, s_["excess"].astype(float).values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    diff = float(pos.mean() - neg.mean()) if (n_pos > 0 and len(neg) > 0) else None
    sup_pass = bool(diff is not None and diff > 0)

    if n_nz < 200 or n_pos < 30:
        status = "not observable"
        decided = ("Fewer than 200 non-zero grid points." if n_nz < 200
                   else "Fewer than 30 grid points with forecast > 0.")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope has t <= -2 (reject rule)."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope has t >= +2 and the supporting difference is positive (confirm rule)."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the supporting difference is not positive (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid points at positions 0,7,14,... of each window with t+7 inside the window; the coin's mean 7-bar return is the mean over all its grid points in all windows; the minimum counts of the plan's inconclusive rule are applied as minimums (not observable).",
    }
