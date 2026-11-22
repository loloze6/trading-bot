import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    D30 = "debug_info.components.depth30.last_history_value"

    def prep(df):
        df = df.sort_values("timestamp").reset_index(drop=True).copy()
        c = df["close"].astype(float)
        r1 = c.pct_change()
        vol = r1.rolling(20, min_periods=20).std()
        df["_rise"] = r1 / vol.replace(0, np.nan)
        df["_r90"] = c / c.shift(90) - 1.0
        df["_fwd"] = c.shift(-H) / c - 1.0
        df["_fc"] = pd.to_numeric(df[FC], errors="coerce") if FC in df.columns else np.nan
        df["_d30"] = pd.to_numeric(df[D30], errors="coerce") if D30 in df.columns else np.nan
        return df

    data = {}
    for coin, wins in bars.items():
        data[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[coin][w] = prep(df)

    # ---------- 1. situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in data.items():
        for w, df in wins.items():
            act = df["_fc"].fillna(0) != 0
            for i in np.where(act.values)[0]:
                n_active += 1
                row = df.iloc[i]
                side_ok = row["_fc"] < 0
                d = row["_d30"]
                depth_ok = (not np.isfinite(d)) or (d < 0)
                rise, r90 = row["_rise"], row["_r90"]
                if np.isfinite(rise) and np.isfinite(r90):
                    sit = (rise >= 2.0) and (r90 < 0.0)
                else:
                    sit = str(row.get("regime", "")) == "mean_reversion"
                if sit and side_ok and depth_ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "Welch t of 5-day return, rising-coin rises (A) minus forecast-negative bars (B)"
    thr = "confirm if t >= 2 with supporting slope > 0; reject if t <= -2; at least 30 cases per group"
    reading = ("Situation recomputed from prices (1-day return over the std of the last 20 daily returns including the bar, "
               "90-day close-to-close return inside the window), falling back to the recorded regime where the 90-day history "
               "is not inside the window; group B is the grid bars with forecast < 0; the supporting y is -(5-day return - "
               "coin's mean non-overlapping 5-day return over all windows); a group under 30 cases is 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a 1-day rise of at least "
                           "2 usual moves and a negative 90-day return (and a negative 30-day depth), as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    A, B_ret, B_x, B_coin = [], [], [], []
    drift = {}
    for coin, wins in data.items():
        allr = []
        for w, df in wins.items():
            g = df.iloc[0::H]
            g = g[g["_fwd"].notna()]
            allr.extend(g["_fwd"].tolist())
            a = g[(g["_rise"] >= 2.0) & (g["_r90"] > 0.0)]
            A.extend(a["_fwd"].tolist())
            b = g[g["_fc"] < 0]
            B_ret.extend(b["_fwd"].tolist())
            B_x.extend(b["_fc"].abs().tolist())
            B_coin.extend([coin] * len(b))
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    A = np.array(A, float)
    B = np.array(B_ret, float)
    nA, nB = int(len(A)), int(len(B))
    counts = {"group A (rise bars with positive 90-day return)": nA,
              "group B (bars with negative forecast)": nB}

    diff = float(A.mean() - B.mean()) if nA > 0 and nB > 0 else None
    t = None
    if nA >= 2 and nB >= 2:
        tt = stats.ttest_ind(A, B, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    slope = None
    if nB >= 3:
        y = -(B - np.array([drift[c] for c in B_coin], float))
        x = np.array(B_x, float)
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() >= 3 and np.ptp(x[m]) > 0:
            slope = float(stats.linregress(x[m], y[m]).slope)
    sup_pass = None if slope is None else bool(slope > 0)

    if nA < 30 or nB < 30:
        status = "not observable"
        decided = f"A group has fewer than 30 cases (A: {nA}, B: {nB}), the plan's minimum."
    elif t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed."
    elif t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main t is 2 or more and the supporting slope is above 0."
        else:
            status = "inconclusive"
            decided = "The main t is 2 or more but the supporting slope is at or below 0 (or not computable)."
    elif t <= -2:
        status = "rejected"
        decided = "The main t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": None if t is None else {"name": "Welch t", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "slope of short-signed 5-day return minus drift on |forecast|, group B",
                             "value": slope, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
