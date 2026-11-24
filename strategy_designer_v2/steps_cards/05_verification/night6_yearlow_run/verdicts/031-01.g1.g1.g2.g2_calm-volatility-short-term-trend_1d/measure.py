import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    MIN_CALM = 300
    MIN_NONCALM = 300
    CALM = "trending"
    MOM_COL = "debug_info.components.mom14.last_history_value"

    def ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        n = len(x)
        if n < 3 or np.var(x) == 0:
            return np.nan, np.nan, n
        xm = x - x.mean()
        b = np.sum(xm * (y - y.mean())) / np.sum(xm ** 2)
        a = y.mean() - b * x.mean()
        resid = y - a - b * x
        s2 = np.sum(resid ** 2) / (n - 2)
        se = np.sqrt(s2 / np.sum(xm ** 2))
        return b, se, n

    def standardise(raw, window=60, min_periods=20):
        absr = raw.abs()
        # mean of |past values|, bar t left out
        m = absr.shift(1).rolling(window, min_periods=min_periods).mean()
        out = raw * 10.0 / m
        out = out.where(m > 0, 0.0)
        out = out.where(m.notna(), 0.0)
        out = out.where(raw.notna())
        return out.clip(-20, 20)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    calm_rows = []
    noncalm_rows = []

    for coin, wins in bars.items():
        coin_grid = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            regime = df["regime"].astype(str)
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            r14 = close / close.shift(14) - 1.0
            if MOM_COL in df.columns:
                raw = pd.to_numeric(df[MOM_COL], errors="coerce")
                raw = raw.where(raw.notna(), r14)
            else:
                raw = r14

            active = fc.notna() & (fc != 0)
            in_sit = regime == CALM
            right_side = np.sign(fc) == np.sign(raw)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & right_side & raw.notna()).sum())

            # grid
            fwd = close.shift(-H) / close - 1.0
            std14 = standardise(r14)
            idx = np.arange(0, len(df), H)
            g = pd.DataFrame({
                "fwd": fwd.iloc[idx].values,
                "fc": fc.iloc[idx].values,
                "std14": std14.iloc[idx].values,
                "calm": in_sit.iloc[idx].values,
            })
            g["coin"] = coin
            coin_grid.append(g)

        if not coin_grid:
            continue
        cg = pd.concat(coin_grid, ignore_index=True)
        mean_ret = cg["fwd"].dropna().mean()
        cg["y"] = cg["fwd"] - mean_ret
        c = cg[cg["calm"]][["fc", "y"]].dropna()
        nc = cg[~cg["calm"]][["std14", "y"]].dropna()
        calm_rows.append(c)
        noncalm_rows.append(nc)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Calm bars are those whose recorded regime is 'trending' (the detector's vr<1 decision, its component not "
               "being recorded) and the expected side is the sign of the raw 14-day return; the grid is positions 0,2,4,... "
               "of each window, the coin's mean 2-day return is the mean over all its windows' grid returns, slopes are "
               "pooled OLS with intercept over all coins, the non-calm standardised 14-day return is rebuilt from in-window "
               "closes (missing early bars dropped), the slope-difference t is (b1-b2)/sqrt(se1^2+se2^2), and the plan's "
               "'fewer than 300 cases' minimums are reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active forecast bars are calm-regime bars whose forecast sign matches the "
                           "sign of the 14-day return, as the Fidelity's situation and outcome require."),
            "reading": reading,
        }

    C = pd.concat(calm_rows, ignore_index=True) if calm_rows else pd.DataFrame(columns=["fc", "y"])
    N = pd.concat(noncalm_rows, ignore_index=True) if noncalm_rows else pd.DataFrame(columns=["std14", "y"])

    b1, se1, n1 = ols(C["fc"].values, C["y"].values)
    b2, se2, n2 = ols(N["std14"].values, N["y"].values)
    t1 = b1 / se1 if np.isfinite(b1) and se1 > 0 else np.nan
    diff = b1 - b2 if np.isfinite(b1) and np.isfinite(b2) else np.nan
    sed = np.sqrt(se1 ** 2 + se2 ** 2) if np.isfinite(se1) and np.isfinite(se2) else np.nan
    t_diff = diff / sed if np.isfinite(diff) and sed > 0 else np.nan

    check_pass = None
    if np.isfinite(t_diff):
        check_pass = bool(diff > 0 and t_diff >= 2)

    def f(v):
        return float(v) if v is not None and np.isfinite(v) else None

    if n1 < MIN_CALM:
        status = "not observable"
        decided = f"Only {n1} calm grid cases, below the plan's minimum of {MIN_CALM}."
    elif n2 < MIN_NONCALM:
        status = "not observable"
        decided = f"Only {n2} non-calm grid cases for the check, below the plan's minimum of {MIN_NONCALM}."
    elif (np.isfinite(t1) and t1 <= -2) or (np.isfinite(t_diff) and t_diff <= -2):
        status = "rejected"
        decided = ("Reject rule: the calm slope has t <= -2, or the calm minus non-calm slope difference has t <= -2, "
                   "with at least 300 calm cases.")
    elif np.isfinite(t1) and t1 >= 2 and check_pass:
        status = "confirmed"
        decided = ("Confirm rule: the calm slope has t >= 2, the calm minus non-calm slope difference is positive with "
                   "t >= 2, and there are at least 300 calm cases.")
    else:
        status = "inconclusive"
        decided = ("Inconclusive rule: neither the confirm nor the reject rule is met (calm slope |t| < 2, or a positive "
                   "calm slope whose difference from the non-calm slope has t between -2 and 2).")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "calm-regime slope of demeaned 2-day forward return on the forecast",
            "value": f(b1),
            "statistic": {"name": "OLS slope t", "value": f(t1)},
            "threshold": "confirm if t >= 2 (with the check passing and >= 300 calm cases); reject if t <= -2",
        },
        "supporting_check": {
            "name": "calm minus non-calm slope difference (t >= 2, positive)",
            "value": f(diff),
            "passed": check_pass,
        },
        "counts": {
            "calm grid cases": int(n1),
            "non-calm grid cases": int(n2),
            "calm minus non-calm difference t": f(t_diff) if f(t_diff) is not None else 0.0,
        } if False else {
            "calm grid cases": int(n1),
            "non-calm grid cases": int(n2),
        },
        "decided_by": decided,
        "reading": reading,
    }
