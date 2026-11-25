import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    VOL_P = 30
    ER_P = 30
    RAW = "debug_info.components.chop_rev.last_history_value"
    PPV = "debug_info.components.chop_rev.post_pipeline_value"

    def ols_cluster(x, y, groups):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        n = len(x)
        if n < 3:
            return None, None
        X = np.column_stack([np.ones(n), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) < 2:
            return None, None
        XtX_inv = np.linalg.inv(XtX)
        beta = XtX_inv @ (X.T @ y)
        u = y - X @ beta
        g = pd.Series(groups).astype(str).values
        meat = np.zeros((2, 2))
        uniq = pd.unique(g)
        for gg in uniq:
            m = g == gg
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        G = len(uniq)
        if G < 2:
            return float(beta[1]), None
        V = XtX_inv @ meat @ XtX_inv * (G / (G - 1.0))
        se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
        t = float(beta[1] / se) if np.isfinite(se) and se > 0 else None
        return float(beta[1]), t

    def ols_slope(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        if len(x) < 3 or np.var(x) == 0:
            return None
        xm = x - x.mean()
        return float((xm * (y - y.mean())).sum() / (xm ** 2).sum())

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            ret7 = close / close.shift(H) - 1.0
            exp_side = -np.sign(ret7)
            # where the 7-day move is not computable inside the recorded window, use the raw component's sign
            exp_side = exp_side.where(ret7.notna(), np.sign(raw))
            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw != 0) & exp_side.notna() & (exp_side != 0)
            agree = active & situation & (np.sign(fc) == exp_side)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are long after a 7-day fall or short after a 7-day rise with a nonzero choppiness-weighted scaled move, as the Fidelity's situation and outcome require.",
            "reading": "Expected side is minus the sign of the 7-bar close return within the window, or the raw component's sign on the first 7 recorded bars.",
        }

    # ---------- 2. grid cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ppv = pd.to_numeric(df[PPV], errors="coerce").values if PPV in df.columns else np.full(n, np.nan)
            dret = np.full(n, np.nan)
            dret[1:] = close[1:] / close[:-1] - 1.0
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                fwd = close[t + H] / close[t] - 1.0
                chop = np.nan
                scaled = np.nan
                if t >= VOL_P and t >= ER_P and t >= H:
                    r = dret[t - VOL_P + 1:t + 1]
                    sd = np.std(r, ddof=1)
                    path = np.abs(np.diff(close[t - ER_P:t + 1])).sum()
                    if path > 0:
                        er = abs(close[t] - close[t - ER_P]) / path
                        chop = 1.0 - er
                    if sd > 0:
                        scaled = (close[t] / close[t - H] - 1.0) / (sd * np.sqrt(H))
                rows.append({
                    "coin": coin, "window": w, "day": ts.iloc[t].strftime("%Y-%m-%d"),
                    "fwd": fwd, "fc": fc[t], "ppv": ppv[t], "chop": chop, "scaled": scaled,
                })
    g = pd.DataFrame(rows)
    if len(g) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": "pooled slope of next-7-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"grid cases with a nonzero forecast": 0, "distinct days": 0},
            "decided_by": "No grid cases: the minimum of 200 grid cases with a nonzero forecast over 100 distinct days is not reached.",
            "reading": "none",
        }
    drift = g.groupby("coin")["fwd"].mean()
    g["excess"] = g["fwd"] - g["coin"].map(drift)

    nz = g[g["fc"].notna() & (g["fc"] != 0)]
    n_cases = int(len(nz))
    n_days = int(nz["day"].nunique())

    m = g[g["ppv"].notna() & g["excess"].notna()]
    slope, tstat = ols_cluster(m["ppv"].values, m["excess"].values, m["day"].values)

    # supporting check
    s = g[g["chop"].notna() & g["scaled"].notna() & g["excess"].notna()].copy()
    diff = None
    if len(s) >= 6:
        med = s["chop"].median()
        up = s[s["chop"] > med]
        lo = s[s["chop"] <= med]
        su = ols_slope(-up["scaled"].values, up["excess"].values)
        sl = ols_slope(-lo["scaled"].values, lo["excess"].values)
        if su is not None and sl is not None:
            diff = float(su - sl)
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"grid cases with a nonzero forecast": n_cases, "distinct days": n_days,
              "regression cases": int(len(m)), "regression days": int(m["day"].nunique()),
              "supporting cases": int(len(s))}

    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} grid cases with a nonzero forecast (need 200) over {n_days} distinct days (need 100)."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Main slope positive with t >= 2 and the supporting difference (upper minus lower half of 1 - ER) above 0."
        else:
            status = "inconclusive"
            decided = "Main slope positive with t >= 2 but the supporting difference is not above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "Main slope negative with t <= -2: the 7-day move continues rather than reverses."
    else:
        status = "inconclusive"
        decided = "The main slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled slope of next-7-bar excess return on forecast (post_pipeline_value)",
            "value": slope,
            "statistic": {"name": "slope t, day-clustered", "value": tstat} if tstat is not None else None,
            "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "slope on minus scaled 7-day move, upper minus lower half of 1 - ER(30)",
            "value": diff, "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The regression uses every grid bar (positions 0, 7, 14, ... of each window with a full 7-bar forward return inside it) with a recorded post_pipeline_value, and its t uses day-clustered standard errors (G/(G-1) correction) so same-day cases count as one piece of evidence. The drift is each coin's mean grid return over all windows. The halves split at the pooled median of 1 - ER(30), median included in the lower half. 1 - ER and the 30-day std (ddof 1) are computed from closes inside the window only, so grid bars before bar 30 are left out of the supporting check.",
    }
