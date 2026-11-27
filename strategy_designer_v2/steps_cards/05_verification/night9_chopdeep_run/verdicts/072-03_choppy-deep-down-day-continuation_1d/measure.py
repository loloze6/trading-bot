import numpy as np
import pandas as pd


def measure(bars):
    col_raw = "debug_info.components.depth_below_high.last_history_value"
    col_pos = "postRebalance_current_allocation"

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            raw = pd.to_numeric(df[col_raw], errors="coerce") if col_raw in df.columns \
                else pd.Series(np.nan, index=df.index)
            day_ret = close / close.shift(1) - 1.0
            # down close from the prices; on a window's first row (no previous close
            # recorded) fall back to the detector's decision
            down = day_ret < 0
            first_unknown = day_ret.isna()
            down = down.where(~first_unknown, regime == "trending")
            # choppy profile: the detector's own decision (its components are not recorded)
            choppy_ok = regime == "trending"
            depth_ok = raw.notna() & (raw <= 0)
            situation = down & choppy_ok & depth_ok
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            pos = pd.to_numeric(df[col_pos], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for i in range(len(df)):
                p = pos.iloc[i]
                r = nxt.iloc[i]
                if pd.isna(p) or p == 0 or pd.isna(r) or not np.isfinite(coin_mean[coin]):
                    continue
                ex = float(r) - coin_mean[coin]
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D") if pd.notna(ts.iloc[i]) else None,
                    "gain": float(p) * ex,
                    "excess": ex,
                    "absf": abs(float(fc.iloc[i])),
                })

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = ("confirm: mean > 0 with t >= 2 (and supporting check < 0); "
                     "reject: mean < 0 with t <= -2; at least 100 cases on 100 distinct days")
    reading = ("Cases are bars with a nonzero position after the trade and a next close in the same window; "
               "the t sums each day's deviations across coins into one piece of evidence; the deeper half is "
               "|forecast| strictly above the median, the shallower half at or below it; the choppy profile is "
               "read from the detector's regime column, the down close from the prices.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean timing gain per case", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars on a down "
                           "close in the choppy trending regime with the depth component recorded."),
            "reading": reading,
        }

    d = pd.DataFrame(rows)
    n_cases = int(len(d))
    n_days = int(d["day"].nunique()) if n_cases else 0

    mean_gain = float(d["gain"].mean()) if n_cases else None
    t_val = None
    if n_cases > 1 and n_days > 1:
        dev = d["gain"] - mean_gain
        day_sums = dev.groupby(d["day"]).sum().values
        D = len(day_sums)
        var_sum = (D / (D - 1.0)) * float(np.sum(day_sums ** 2))
        se = np.sqrt(var_sum) / n_cases
        t_val = float(mean_gain / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = float(d["absf"].median())
        deep = d.loc[d["absf"] > med, "excess"]
        shallow = d.loc[d["absf"] <= med, "excess"]
        if len(deep) > 0 and len(shallow) > 0:
            sup_val = float(deep.mean() - shallow.mean())
            sup_pass = bool(sup_val < 0)

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 100:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases on 100 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean timing gain could not be computed, so it lies in no confirm or reject range."
    elif mean_gain > 0 and t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean timing gain is above 0 with t >= 2 over enough cases and days, and the deeper-minus-shallower excess return is below 0."
    elif mean_gain < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean timing gain is below 0 with t <= -2 over at least 100 cases on at least 100 distinct days."
    elif mean_gain > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "The main measure confirms but the supporting check is 0 or above (or not computable), so the result is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean timing gain lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean timing gain per case (position x next-day excess return)",
            "value": mean_gain,
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "deeper-half minus shallower-half mean next-day excess return (split at median |forecast|)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
