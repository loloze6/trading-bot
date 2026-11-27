import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field):
    """Read debug_info.components.<id>.<field>, flat column or nested dict column."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(v):
            if isinstance(v, dict):
                c = v.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        return float(x)
                    except (TypeError, ValueError):
                        return np.nan
            return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    rows = []
    n_active = 0
    n_agree = 0

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        coin_frames = []
        all_rets = []
        for w in sorted(wins.keys()):
            df = wins[w].copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret_next = close.shift(-1) / close - 1.0
            all_rets.append(ret_next.dropna().values)
            prev_close = close.shift(1)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            depth = _component_series(df, "depth", "last_history_value")

            up_close = np.where(prev_close.notna(), close > prev_close, depth > 0)
            situation = (regime == "mean_reversion") & (depth >= 3.0 - 1e-9) & pd.Series(up_close, index=df.index).astype(bool)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            ts = pd.to_datetime(df["timestamp"], utc=True) if "timestamp" in df.columns else pd.Series(pd.NaT, index=df.index)
            frame = pd.DataFrame({
                "coin": coin,
                "day": ts.dt.floor("D"),
                "ret_next": ret_next,
                "depth": depth,
                "case": (regime == "mean_reversion") & active,
            })
            coin_frames.append(frame)
        rets = np.concatenate(all_rets) if all_rets else np.array([])
        mu = float(np.mean(rets)) if rets.size else np.nan
        for f in coin_frames:
            f = f[f["case"]].copy()
            f["mu"] = mu
            rows.append(f)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean short-signed next-day return minus the coin's mean daily return"
    main_thr = "mean > 0 with t >= 2 to confirm; t <= -2 to reject"
    sup_name = "OLS slope of next-day return on run depth"
    reading = ("Profile and regime taken from the recorded regime (mean_reversion only arises inside the falling calm "
               "profile, whose 365-day percentile cannot be rebuilt from the record), depth from the depth component's "
               "last_history_value, cases are mean_reversion bars with nonzero forecast and a next-day close in the same "
               "window, the slope uses the raw next-day return with its ordinary OLS t, and the main t clusters cases by UTC day.")

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the nonzero-forecast bars are short forecasts on up-close days after a down run "
                           "of 3 or more usual moves in the mean_reversion (falling calm) regime."),
            "reading": reading,
        }

    cases = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["coin", "day", "ret_next", "depth", "mu"])
    cases = cases[cases["ret_next"].notna() & cases["mu"].notna()].copy()
    n_cases = int(len(cases))
    sit = {"agreement": (float(agreement) if agreement is not None else None), "passed": passed}

    if n_cases < 30:
        return {
            "status": "not observable",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"cases": n_cases},
            "decided_by": f"Only {n_cases} cases, fewer than the plan's minimum of 30.",
            "reading": reading,
        }

    x = -(cases["ret_next"].values - cases["mu"].values)
    mean = float(np.mean(x))
    cases["x"] = x
    g = cases.groupby("day")["x"].agg(["sum", "count"])
    D = len(g)
    resid = g["sum"].values - g["count"].values * mean
    if D > 1:
        se = np.sqrt(np.sum(resid ** 2) * D / (D - 1)) / n_cases
        t_main = float(mean / se) if se > 0 else float("nan")
    else:
        t_main = float("nan")

    reg = cases[cases["depth"].notna()]
    slope, t_slope = None, None
    if len(reg) >= 3 and np.ptp(reg["depth"].values) > 0:
        lr = stats.linregress(reg["depth"].values, reg["ret_next"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else float("nan")
    slope_neg = (slope is not None and slope < 0)

    if np.isfinite(t_main) and t_main <= -2:
        status = "rejected"
        decided = f"The short-signed excess next-day return has t = {t_main:.2f} <= -2 (relief days keep rising)."
    elif slope is not None and slope > 0 and t_slope is not None and np.isfinite(t_slope) and t_slope >= 2:
        status = "rejected"
        decided = f"The depth slope is positive with t = {t_slope:.2f} >= 2."
    elif mean > 0 and np.isfinite(t_main) and t_main >= 2 and slope_neg:
        status = "confirmed"
        decided = (f"Mean short-signed excess return > 0 with t = {t_main:.2f} >= 2, negative depth slope, "
                   f"and {n_cases} >= 30 cases.")
    else:
        status = "inconclusive"
        if mean > 0 and np.isfinite(t_main) and t_main >= 2:
            decided = "The main measure meets the confirm rule but the depth slope is not negative."
        else:
            decided = f"Main t = {t_main:.2f} lies between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": {"name": "t of the mean, cases pooled by day", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope,
                             "passed": (bool(slope_neg) if slope is not None else None)},
        "counts": {"cases": n_cases, "days": int(D)},
        "decided_by": decided,
        "reading": reading,
    }
