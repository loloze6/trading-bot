import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.up_shock.last_history_value"
    POST = "debug_info.components.up_shock.post_pipeline_value"
    H = 5

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback where the raw value is not recorded: sign of the one-day return
            ret1 = pd.to_numeric(df["close"], errors="coerce").pct_change()
            raw = raw.where(raw.notna(), ret1)
            active = fc.notna() & (fc != 0)
            situation = raw > 0          # a one-day rise
            expected = fc > 0            # rise -> long
            n_active += int(active.sum())
            n_agree += int((active & situation & expected).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of OLS slope of excess 5-bar forward return on up_shock post_pipeline_value (non-overlapping grid)"
    threshold = "confirm if slope t >= 2 and supporting check passes; reject if slope t <= -2; otherwise inconclusive"
    sup_name = "mean excess 5-bar return on grid bars with forecast >= 10 is above 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are one-day rises (positive raw volatility-scaled return) with a long forecast, as the plan's situation requires.",
            "reading": "The situation is a positive raw up_shock value (a one-day rise), expected side long; missing raw values fall back to the sign of the one-day close return.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            post = pd.to_numeric(df[POST], errors="coerce").values if POST in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, post[i]))
    g = pd.DataFrame(rows, columns=["coin", "window", "fwd", "fc"])
    if len(g):
        g["coin_mean"] = g.groupby("coin")["fwd"].transform("mean")
        g["excess"] = g["fwd"] - g["coin_mean"]
    else:
        g["excess"] = []
    s = g.dropna(subset=["excess", "fc"])

    n_pos = int((s["fc"] > 0).sum())
    n_ge10 = int((s["fc"] >= 10).sum())
    counts = {
        "grid cases with forecast above 0": n_pos,
        "grid cases with forecast of 10 or more": n_ge10,
        "grid cases in regression": int(len(s)),
    }

    slope = None
    t = None
    if len(s) >= 3 and s["fc"].nunique() > 1:
        lr = stats.linregress(s["fc"].values, s["excess"].values)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sub = s.loc[s["fc"] >= 10, "excess"]
    sup_val = float(sub.mean()) if len(sub) else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if n_pos < 150 or n_ge10 < 50:
        status = "not observable"
        missing = []
        if n_pos < 150:
            missing.append(f"grid cases with forecast above 0 = {n_pos} < 150")
        if n_ge10 < 50:
            missing.append(f"grid cases with forecast of 10 or more = {n_ge10} < 50")
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t is 2 or more and the mean excess return on grid bars with forecast >= 10 is above 0 (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "The coin's mean 5-bar return is the mean of its grid forward returns pooled over all its windows, the regression is one pooled OLS over all coins' grid bars with the slope t = slope / its standard error, grid bars without a full 5-bar forward return inside the window are dropped, and the plan's 'fewer cases' rule is reported as not observable per the workflow.",
    }
