import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.low_close_vol.last_history_value"
    POST = "debug_info.components.low_close_vol.post_pipeline_value"
    VOL_PERIOD = 20
    MIN_REG = 1000
    MIN_GROUP = 200

    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            for c in ["open", "high", "low", "close", "forecast"]:
                d[c] = pd.to_numeric(d[c], errors="coerce")
            d["raw"] = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else np.nan
            d["post"] = pd.to_numeric(d[POST], errors="coerce") if POST in d.columns else np.nan
            rng = d["high"] - d["low"]
            d["loc"] = np.where(rng > 0, (d["high"] - d["close"]) / rng, np.nan)
            # next-day return inside the window only
            d["fwd"] = d["close"].shift(-1) / d["close"] - 1.0
            # 20-day std of daily returns: from the component's raw value when it can be
            # inverted (raw = loc * vol), otherwise recomputed from prices inside the window
            ret = d["close"] / d["close"].shift(1) - 1.0
            vol_px = ret.rolling(VOL_PERIOD, min_periods=VOL_PERIOD).std()
            vol_raw = np.where((d["loc"] > 0) & d["raw"].notna(), d["raw"] / d["loc"], np.nan)
            d["vol"] = np.where(np.isfinite(vol_raw), vol_raw, vol_px)
            d["coin"] = coin
            d["window"] = w
            frames.append(d[["coin", "window", "loc", "forecast", "raw", "post", "fwd", "vol"]])

    if not frames:
        return {"status": "not observable", "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None, "counts": {},
                "decided_by": "no bars in the record", "reading": "none"}

    all_ = pd.concat(frames, ignore_index=True)

    # ---- situation check: a day that did not close at its high (loc > 0), long side
    active = all_[all_["forecast"].notna() & (all_["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = (active["loc"] > 0) & (active["forecast"] > 0)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "fewer than 90% of the active bars are long bars on days that closed below their high "
                          "(close-near-low share > 0), as the Fidelity's kept situation and long side require",
            "reading": "situation recomputed from prices as (high-close)/(high-low) > 0 with a positive forecast",
        }

    # ---- excess next-day return
    coin_mean = all_.groupby("coin")["fwd"].mean()
    all_["xs"] = all_["fwd"] - all_["coin"].map(coin_mean)

    # ---- main measure: pooled OLS of excess next-day return on post_pipeline_value
    reg = all_[all_["xs"].notna() & all_["post"].notna()]
    n_reg = len(reg)
    slope = None
    t_slope = None
    if n_reg >= 3 and reg["post"].nunique() > 1:
        lr = stats.linregress(reg["post"].values, reg["xs"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---- supporting check: lower-half closes, high vs low volatility (per-coin median split)
    coin_med = all_[all_["vol"].notna()].groupby("coin")["vol"].median()
    all_["vol_med"] = all_["coin"].map(coin_med)
    sub = all_[(all_["loc"] > 0.5) & all_["xs"].notna() & all_["vol"].notna() & all_["vol_med"].notna()]
    hi = sub.loc[sub["vol"] > sub["vol_med"], "xs"].values
    lo = sub.loc[sub["vol"] <= sub["vol_med"], "xs"].values
    n_hi, n_lo = len(hi), len(lo)
    diff = None
    t_w = None
    if n_hi >= 2 and n_lo >= 2:
        diff = float(np.mean(hi) - np.mean(lo))
        tw = stats.ttest_ind(hi, lo, equal_var=False).statistic
        t_w = float(tw) if np.isfinite(tw) else None
    sup_pass = None if t_w is None else bool(diff > 0 and t_w >= 2)

    counts = {
        "bars in the regression": int(n_reg),
        "high-volatility group": int(n_hi),
        "low-volatility group": int(n_lo),
    }

    # ---- decision
    if n_reg < MIN_REG or n_hi < MIN_GROUP or n_lo < MIN_GROUP:
        status = "not observable"
        missing = []
        if n_reg < MIN_REG:
            missing.append(f"regression bars {n_reg} < {MIN_REG}")
        if n_hi < MIN_GROUP:
            missing.append(f"high-volatility group {n_hi} < {MIN_GROUP}")
        if n_lo < MIN_GROUP:
            missing.append(f"low-volatility group {n_lo} < {MIN_GROUP}")
        decided_by = "Minimum count not reached: " + "; ".join(missing) + "."
    elif t_slope is None or t_w is None:
        status = "inconclusive"
        decided_by = "A statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and t_w >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "Confirm: the slope's t is 2 or more and the supporting check's Welch t is 2 or more."
    elif t_slope <= -2 or t_w <= -2:
        status = "rejected"
        decided_by = "Reject: the slope's t is -2 or less, or the supporting check's Welch t is -2 or less."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: neither the confirm rule (both t >= 2) nor the reject rule (either t <= -2) is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of excess next-day return on post_pipeline_value, pooled",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "slope t >= 2 confirms (with the check), slope t <= -2 rejects",
        },
        "supporting_check": {
            "name": "lower-half closes: mean excess return high-vol minus low-vol (Welch t >= 2)",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": "Every bar with a next-day return inside its window is pooled (h=1, so no overlap); the coin's mean is "
                   "its mean next-day return over all windows; 'lower half' is (high-close)/(high-low) > 0.5; the 20-day "
                   "volatility is the component's own (raw / location, else the ddof-1 std of the last 20 daily returns "
                   "within the window), split at the coin's median over all its bars (above = top half); the plan's "
                   "'inconclusive' for too few cases is reported as 'not observable' as the workflow requires.",
    }
