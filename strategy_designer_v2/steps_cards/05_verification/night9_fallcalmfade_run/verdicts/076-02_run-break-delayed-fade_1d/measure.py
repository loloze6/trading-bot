import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.run_len.last_history_value"
    H = 3

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            return pd.to_datetime(s, unit="ms", utc=True)
        return pd.to_datetime(s, utc=True)

    def run_break_count(close, max_bars=30):
        c = np.asarray(close, dtype=float)
        n = len(c)
        out = np.full(n, np.nan)
        down = np.zeros(n, dtype=bool)
        down[1:] = c[1:] < c[:-1]
        run = 0
        for t in range(n):
            if t == 0:
                run = 0
                continue
            if c[t] > c[t - 1]:
                out[t] = float(min(run, max_bars))
                run = 0
            else:
                out[t] = 0.0
                run = run + 1 if down[t] else 0
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            price_cnt = run_break_count(df["close"].values)
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").values
            else:
                lhv = np.full(len(df), np.nan)
            cnt = np.where(np.isnan(lhv), price_cnt, lhv)
            situ = np.nan_to_num(cnt, nan=0.0) >= 1
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None) and (agreement >= 0.9)
    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are run-break bars "
                          "(an up close ending at least one down day) with a short forecast, as the Fidelity requires.",
            "reading": "none",
        }

    # ---------- coin mean 2-day return over all windows (non-overlapping) ----------
    coin_mean2 = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - 2, 2):
                if np.isfinite(c[i]) and np.isfinite(c[i + 2]) and c[i] != 0:
                    rets.append(c[i + 2] / c[i] - 1.0)
        coin_mean2[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    recs = []
    for coin, wins in bars.items():
        m2 = coin_mean2[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = to_time(df["timestamp"])
            lhv = (pd.to_numeric(df[LHV], errors="coerce").values
                   if LHV in df.columns else np.full(n, np.nan))
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if fc[i] < 0]
                if not idx:
                    continue
                t = idx[0]
                if t + 3 >= n:
                    continue
                if not (np.isfinite(c[t + 1]) and np.isfinite(c[t + 3]) and c[t + 1] != 0):
                    continue
                if not np.isfinite(m2):
                    continue
                r2 = c[t + 3] / c[t + 1] - 1.0
                ex = -(r2) - (-m2)
                recs.append({
                    "coin": coin, "day": ts.iloc[t].strftime("%Y-%m-%d"),
                    "x": ex, "w": abs(fc[t]), "run": lhv[t],
                })

    cases = pd.DataFrame(recs, columns=["coin", "day", "x", "w", "run"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    # weighted mean, t clustered by day
    wmean = None
    t_mean = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = cases["w"].sum()
        wmean = float((cases["x"] * cases["w"]).sum() / W)
        dev = cases["w"] * (cases["x"] - wmean)
        per_day = dev.groupby(cases["day"]).sum()
        D = len(per_day)
        if D > 1:
            var = (per_day ** 2).sum() * D / (D - 1) / W ** 2
            se = np.sqrt(var)
            t_mean = float(wmean / se) if se > 0 else None

    # slope on run length (OLS)
    slope = None
    t_slope = None
    sub = cases.dropna(subset=["x", "run"])
    if len(sub) > 2 and sub["run"].nunique() > 1:
        lr = stats.linregress(sub["run"].values.astype(float), sub["x"].values.astype(float))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    slope_pass = (slope is not None and t_slope is not None and slope > 0 and t_slope >= 2)

    counts = {"cases": n_cases, "distinct case days": n_days}

    if n_cases < 300 or n_days < 200:
        status = "not observable"
        decided_by = (f"The plan's minimum counts are not reached: {n_cases} cases (minimum 300) "
                      f"and {n_days} distinct case days (minimum 200).")
    elif (t_mean is not None and t_mean <= -2) or (t_slope is not None and t_slope <= -2):
        status = "rejected"
        decided_by = "Reject rule met: the weighted mean excess short return has t <= -2, or the slope on run length has t <= -2."
    elif (wmean is not None and t_mean is not None and wmean > 0 and t_mean >= 2):
        if slope_pass:
            status = "confirmed"
            decided_by = "Confirm rule met: the weighted mean excess short return is above 0 with t >= 2 and the slope on run length is positive with t >= 2."
        else:
            status = "inconclusive"
            decided_by = "The weighted mean excess short return meets the confirm rule but the slope check fails, so the result is inconclusive."
    else:
        status = "inconclusive"
        decided_by = "Neither the confirm rule nor the reject rule is met (inconclusive rule: any other result)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": bool(passed) if agreement is not None else None},
        "main_measure": {
            "name": "abs(forecast)-weighted mean excess short return, close t+1 to t+3",
            "value": wmean,
            "statistic": ({"name": "t of the weighted mean, cases of one day taken together", "value": t_mean}
                          if t_mean is not None else None),
            "threshold": "confirm: above 0 with t >= 2 (and slope check passes); reject: t <= -2",
        },
        "supporting_check": {
            "name": "OLS slope of excess short return on run length (t)",
            "value": t_slope,
            "passed": (bool(slope_pass) if t_slope is not None else None),
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("A case is the first bar with a negative forecast in each 3-bar grid cell (positions 0,3,6,... of each "
                    "window) with close[t+3] inside the window; the coin's mean 2-day return uses non-overlapping 2-bar "
                    "returns pooled over all its windows; the weighted mean's t clusters weighted deviations by UTC day "
                    "with a D/(D-1) correction; the slope's t is the ordinary unweighted OLS t; and the plan's "
                    "'fewer than 300 cases or 200 days' rule is reported as 'not observable'."),
    }
