import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMPS = ["mom", "rev", "high", "vol"]
    THRESH = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 independent cases"
    MAIN_NAME = "mean of (forecast/10) x (5-day return minus coin's normal 5-day drift), pooled"

    def col(df, cid, kind):
        name = "debug_info.components.%s.%s" % (cid, kind)
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            post = pd.concat([col(df, c, "post_pipeline_value") for c in COMPS], axis=1)
            raw = pd.concat([col(df, c, "last_history_value") for c in COMPS], axis=1)
            post.columns = COMPS
            raw.columns = COMPS
            # rebuilt composite: equal-weight mean of the standardised components (weights all 1.0)
            comp = post.mean(axis=1, skipna=False)
            # standardise only scales: each component's sign after it must be its raw sign
            sign_ok = ((np.sign(post) == np.sign(raw)) | (post == 0) | (raw == 0)).all(axis=1)
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                n_active += 1
                c = comp.iloc[i]
                if pd.notna(c) and c != 0 and bool(sign_ok.iloc[i]) and np.sign(c) == np.sign(fc.iloc[i]):
                    n_agree += 1

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": MAIN_NAME, "value": None, "statistic": None, "threshold": THRESH},
            "supporting_check": None,
            "counts": {"non-overlapping cases with a non-zero forecast": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 300 non-overlapping cases is not reached.",
            "reading": "The situation is the bars where the equal-weight mean of the components' standardised values "
                       "(sign-consistent with their raw w_k x z_k values) is non-zero, its side being that mean's sign.",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": MAIN_NAME, "value": None, "statistic": None, "threshold": THRESH},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90 % of active bars have a forecast whose sign is that of the equal-weight "
                          "composite of the four w_k x z_k components the Fidelity describes.",
            "reading": "The situation is the bars where the equal-weight mean of the components' standardised values "
                       "(sign-consistent with their raw w_k x z_k values) is non-zero, its side being that mean's sign.",
        }

    # ---------- 2. criterion ----------
    vals = []
    for coin, wins in bars.items():
        cells = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                    cells.append((close[t + H] / close[t] - 1.0, fc[t]))
        if not cells:
            continue
        rets = np.array([c[0] for c in cells])
        fcs = np.array([c[1] for c in cells], dtype=float)
        drift = rets.mean()
        m = np.isfinite(fcs) & (fcs != 0)
        vals.extend(list((fcs[m] / 10.0) * (rets[m] - drift)))

    vals = np.array(vals, dtype=float)
    n = int(len(vals))
    mean = float(vals.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = vals.std(ddof=1)
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    if n < 300:
        status = "not observable"
        decided = "Fewer than 300 non-overlapping cases with a non-zero forecast (%d)." % n
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean forecast-weighted excess 5-day return is positive with t >= 2 on at least 300 cases."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean forecast-weighted excess 5-day return is negative with t <= -2 on at least 300 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean lies between -2 and 2 on at least 300 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": MAIN_NAME,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": THRESH,
        },
        "supporting_check": None,
        "counts": {"non-overlapping cases with a non-zero forecast": n},
        "decided_by": decided,
        "reading": "Cases are the bars at positions 0, 5, 10, ... of each window with a full 5-bar return inside the "
                   "window and a non-zero forecast; the normal drift is each coin's mean 5-day return over all its "
                   "grid cells in all windows; the situation is the sign of the equal-weight mean of the components' "
                   "standardised values, checked sign-consistent with their raw values.",
    }
