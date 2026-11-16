import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field="last_history_value"):
    """Raw value of a strategy component, from a flattened column or a nested debug dict column."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(v):
            try:
                if isinstance(v, dict):
                    c = v.get(comp_id)
                    if isinstance(c, dict):
                        x = c.get(field)
                        return float(x) if x is not None else np.nan
            except Exception:
                pass
            return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    H = 20

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            dist = _component_series(df, "dist")
            ret20 = _component_series(df, "ret20")
            active = f.notna() & (f != 0)
            situ = dist.notna() & ret20.notna() & (dist >= 0) & (ret20 > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close is at "
                           "or above its SMA200 (dist >= 0) and the 20-day return is above 0, as the plan's situation requires."
                           if n_active > 0 else "The record has no bar with a non-zero forecast to check against the plan's situation."),
            "reading": "Situation recomputed from the recorded raw values of dist (>= 0) and ret20 (> 0); a missing value counts as outside the situation.",
        }

    # ---------- 2. non-overlapping grid ----------
    rows = []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
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
    grid = pd.DataFrame(rows, columns=["coin", "fwd", "forecast"])

    if len(grid):
        coin_mean = grid.groupby("coin")["fwd"].mean()
        grid["excess"] = grid["fwd"] - grid["coin"].map(coin_mean)
        act = grid[(grid["forecast"] > 0) & grid["forecast"].notna() & grid["excess"].notna()]
    else:
        act = grid
    n_cases = int(len(act))
    counts = {"active non-overlapping cases": n_cases}

    reading = ("Coin's mean 20-bar return taken over all non-overlapping grid cases of all its windows; slope t is the OLS "
               "t of excess return on forecast; the forecast-weighted mean's t is the ordinary t of the mean of forecast x excess; "
               "fewer than 30 active cases is reported as not observable.")

    main_name = "OLS slope of excess 20-bar return on forecast (active non-overlapping cases)"
    main_thr = "slope t >= 2 confirms (with supporting check), slope t <= -2 rejects"
    sup_name = "forecast-weighted mean excess 20-bar return > 0"

    if n_cases < 30:
        slope = t_slope = wmean = None
        if n_cases >= 3 and act["forecast"].nunique() > 1:
            lr = stats.linregress(act["forecast"].values, act["excess"].values)
            slope = float(lr.slope)
            t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else None
        if n_cases > 0 and act["forecast"].sum() > 0:
            wmean = float((act["excess"] * act["forecast"]).sum() / act["forecast"].sum())
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": slope,
                             "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
                             "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": wmean, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} active non-overlapping cases, fewer than the plan's minimum of 30.",
            "reading": reading,
        }

    x = act["forecast"].values.astype(float)
    y = act["excess"].values.astype(float)
    if np.unique(x).size > 1:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else (np.inf * np.sign(lr.slope) if lr.slope != 0 else 0.0)
    else:
        slope, t_slope = float("nan"), float("nan")

    wmean = float((x * y).sum() / x.sum())
    z = x * y
    sd = z.std(ddof=1)
    t_w = float(z.mean() / (sd / np.sqrt(len(z)))) if sd > 0 else 0.0
    sup_pass = bool(wmean > 0)

    t_ok = np.isfinite(t_slope)
    if (t_ok and t_slope <= -2) or t_w <= -2:
        status = "rejected"
        if t_ok and t_slope <= -2:
            decided = f"Reject: slope t = {t_slope:.2f} <= -2."
        else:
            decided = f"Reject: forecast-weighted mean excess return t = {t_w:.2f} <= -2."
    elif t_ok and t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = f"Confirm: slope t = {t_slope:.2f} >= 2 and the forecast-weighted mean excess return ({wmean:.4f}) is above 0."
    else:
        status = "inconclusive"
        if t_ok and t_slope >= 2:
            decided = f"Inconclusive: slope t = {t_slope:.2f} >= 2 but the supporting check fails (weighted mean {wmean:.4f} <= 0)."
        else:
            decided = (f"Inconclusive: slope t = {t_slope:.2f} and weighted-mean t = {t_w:.2f} meet neither the confirm "
                       f"nor the reject rule.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": float(t_slope)},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
