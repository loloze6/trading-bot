import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    comp = "debug_info.components.low_close_wide_day"
    raw_col = comp + ".last_history_value"
    post_col = comp + ".post_pipeline_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            close = df["close"].astype(float)
            # Recompute from prices where possible: base = mean range of bars t-20..t-1.
            rng = high - low
            base = rng.shift(1).rolling(20, min_periods=20).mean()
            recomputed = (high - close) / base.replace(0, np.nan)
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            # Situation: close sits below the high (positive raw value), expected side long.
            situ = (raw > 0) & (fc > 0)
            n_agree += int((situ & active).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_situ = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of excess next-day return on post_pipeline_value"
    main_thr = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2"
    sup_name = "mean excess next-day return, top fifth of forecasts minus other bars (Welch t)"

    if not passed_situ:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have the close below the high (positive raw value) with a long forecast, so the config does not do what the plan's situation and side say.",
            "reading": "Situation taken as a positive raw value (high minus close over the prior 20-day mean range), side long, raw recomputed from prices where not recorded.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            x = pd.to_numeric(df[post_col], errors="coerce") if post_col in df.columns else pd.Series(np.nan, index=df.index)
            d = pd.DataFrame({"ret": nxt, "x": x})
            d["coin"] = coin
            coin_rows.append(d)
        if coin_rows:
            cd = pd.concat(coin_rows, ignore_index=True)
            mu = cd["ret"].dropna().mean()  # coin mean over all its windows
            cd["ex"] = cd["ret"] - mu
            rows.append(cd)

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["ret", "x", "ex", "coin"])
    data = data.dropna(subset=["ex", "x"])
    n = int(len(data))

    if n > 0:
        q80 = data["x"].quantile(0.8)
        top = data["x"] >= q80
    else:
        top = pd.Series([], dtype=bool)
    n_top = int(top.sum())
    counts = {"bars with a next-day return": n, "bars in the top fifth": n_top}

    slope = None
    t_slope = None
    if n >= 3 and data["x"].var() > 0:
        res = stats.linregress(data["x"].values, data["ex"].values)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    diff = None
    t_w = None
    if n_top >= 2 and (n - n_top) >= 2:
        a = data.loc[top, "ex"].values
        b = data.loc[~top, "ex"].values
        diff = float(a.mean() - b.mean())
        tw = stats.ttest_ind(a, b, equal_var=False).statistic
        t_w = float(tw) if np.isfinite(tw) else None

    sup_passed = None if t_w is None else bool(diff > 0 and t_w >= 2)

    main = {
        "name": main_name,
        "value": slope,
        "statistic": None if t_slope is None else {"name": "OLS t of slope", "value": t_slope},
        "threshold": main_thr,
    }
    sup = {"name": sup_name, "value": diff, "passed": sup_passed}
    if t_w is not None:
        sup["name"] = sup_name + f" [Welch t = {t_w:.3f}]"

    reading = ("Top fifth taken as pooled bars with post_pipeline_value at or above its pooled 80th percentile; "
               "each coin's mean daily return is the mean of its next-bar returns over all its windows; "
               "the supporting check passes when the top-fifth mean is larger with Welch t >= 2, as the confirm rule needs.")

    if n < 1000 or n_top < 200:
        status = "not observable"
        decided = f"Minimum counts not reached: {n} bars with a next-day return (need 1000) and {n_top} in the top fifth (need 200)."
    elif t_slope is None or t_w is None:
        status = "inconclusive"
        decided = "The slope or Welch t could not be computed, so neither confirm nor reject is met."
    elif slope > 0 and t_slope >= 2 and diff > 0 and t_w >= 2:
        status = "confirmed"
        decided = "Slope positive with t >= 2 and top-fifth mean excess return larger with Welch t >= 2 (confirm rule)."
    elif slope < 0 and t_slope <= -2 and diff < 0 and t_w <= -2:
        status = "rejected"
        decided = "Slope negative with t <= -2 and top-fifth mean excess return smaller with Welch t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "Neither the confirm nor the reject rule is met (slope |t| < 2, or main measure and check disagree)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
