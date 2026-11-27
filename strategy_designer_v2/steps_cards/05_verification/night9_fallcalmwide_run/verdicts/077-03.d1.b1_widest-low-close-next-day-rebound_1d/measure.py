import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LOC_MIN = 0.8
    WIDE_MIN = 2.0
    WIDE_TOL = 0.95   # tolerance on the recomputed width (the component's exact return definition is not recorded)
    VOL_N = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []

    for coin, wins in bars.items():
        # coin's mean daily return over all windows together (returns inside windows only)
        all_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").astype(float)
            all_rets.append((c.shift(-1) / c - 1.0).dropna())
        coin_mean = float(pd.concat(all_rets).mean()) if all_rets else np.nan

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = pd.to_numeric(df["open"], errors="coerce").astype(float)
            h = pd.to_numeric(df["high"], errors="coerce").astype(float)
            l = pd.to_numeric(df["low"], errors="coerce").astype(float)
            c = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)
            regime = df["regime"].astype(str)

            rng = (h - l)
            # CloseLocationInRange, reference "high": distance of the close below the high, as a share of the range
            loc = (h - c) / rng.replace(0, np.nan)
            # RangeInReturnStd(30): range as a return, in std of the last 30 daily returns
            ret = c.pct_change()
            sd = ret.rolling(VOL_N, min_periods=VOL_N).std(ddof=1)
            wide = (rng / c) / sd.replace(0, np.nan)

            # profile (365-bar vol percentile, 60-bar trend) cannot be rebuilt from the record's
            # windows: its decision is read from `regime` (mean_reversion = not vetoed and rules held)
            in_profile = regime.eq("mean_reversion")
            loc_ok = loc >= LOC_MIN - 1e-9
            wide_ok = (wide >= WIDE_MIN * WIDE_TOL) | wide.isna()
            situation = in_profile & loc_ok & wide_ok

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # ---------- cases for the criterion ----------
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").astype(float)
            nxt = c.shift(-1) / c - 1.0  # inside the window only
            sel = (pos > 0) & nxt.notna()
            for i in np.where(sel.values)[0]:
                case_rows.append({
                    "day": pd.Timestamp(df["timestamp"].iloc[i]).normalize(),
                    "coin": coin,
                    "excess": float(nxt.iloc[i] - coin_mean),
                    "forecast": float(fc.iloc[i]),
                })

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess next-day return on long bars (minus coin's all-window mean daily return)"
    main_thr = "confirm: mean > 0 with t >= 2 and upper-minus-lower > 0; reject: mean < 0 with t <= -2"
    reading = ("Cases are bars with postRebalance_current_allocation > 0 and a next close in the same window; "
               "the mean is over cases and the t over day sums of the excess; the median split puts forecasts "
               "above the median in the upper half and the rest in the lower; the profile is read from `regime` "
               "since its 365-bar inputs are not in the record, the low close and width are recomputed from prices.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (choppy agitated profile, close in the lower fifth, range >= 2 return stds)."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "coin", "excess", "forecast"])
    n_cases = int(len(cases))
    if n_cases > 0:
        day_sums = cases.groupby("day")["excess"].sum()
        n_days = int(len(day_sums))
        mean_val = float(cases["excess"].mean())
    else:
        day_sums = pd.Series(dtype=float)
        n_days = 0
        mean_val = None

    t_val = None
    if n_days >= 2:
        s = float(day_sums.std(ddof=1))
        if s > 0:
            t_val = float(day_sums.mean() / (s / np.sqrt(n_days)))

    # supporting check
    diff = None
    welch_t = None
    sup_pass = None
    if n_cases >= 2:
        med = float(cases["forecast"].median())
        up = cases.loc[cases["forecast"] > med, "excess"]
        lo = cases.loc[cases["forecast"] <= med, "excess"]
        if len(up) > 0 and len(lo) > 0:
            diff = float(up.mean() - lo.mean())
            sup_pass = bool(diff > 0)
            if len(up) >= 2 and len(lo) >= 2:
                tt = stats.ttest_ind(up.values, lo.values, equal_var=False)
                if np.isfinite(tt.statistic):
                    welch_t = float(tt.statistic)

    counts = {"cases": n_cases, "independent days": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases (independent days): {n_days}."
    elif t_val is None or mean_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed (zero spread over days)."
    elif mean_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess next-day return above 0 with t >= 2 and upper-minus-lower difference above 0."
        else:
            status = "inconclusive"
            decided = "A t >= 2 whose upper-minus-lower difference is not above 0 is inconclusive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess next-day return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean over day sums", "value": t_val} if t_val is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean excess return at the median forecast (Welch t "
                    + (f"{welch_t:.3f}" if welch_t is not None else "n/a") + ")",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
