import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    MID = 24
    FALL_COL = "debug_info.components.fall24.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            ret72 = close / close.shift(H) - 1.0
            if FALL_COL in df.columns:
                fall24 = pd.to_numeric(df[FALL_COL], errors="coerce").reset_index(drop=True)
            else:
                fall24 = pd.Series(np.nan, index=close.index)
            fall24 = fall24.where(fall24.notna(), close / close.shift(MID) - 1.0)
            active = fc.notna() & (fc != 0) & ret72.notna() & fall24.notna()
            situ = (ret72 < 0) & (fall24 < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 72-bar change "
                           "is below 0 and the 24-bar change is a fall, as the Fidelity's situation and side require."
                           if n_active > 0 else "No active bar with computable situation values was found."),
            "reading": "Bars whose 72-bar change cannot be computed inside their window are left out of the check.",
        }

    # ---------- 2. Grid samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            n = len(close)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                r = close[t + H] / close[t] - 1.0
                r2 = close[t + H] / close[t + MID] - 1.0
                rows.append((coin, reg[t], fc[t], r, r2))
    g = pd.DataFrame(rows, columns=["coin", "regime", "forecast", "r", "r2"])
    g = g.replace([np.inf, -np.inf], np.nan)

    if len(g):
        mean_r = g.dropna(subset=["r"]).groupby("coin")["r"].mean()
        mean_r2 = g.dropna(subset=["r2"]).groupby("coin")["r2"].mean()
        g["ex"] = g["r"] - g["coin"].map(mean_r)
        g["ex2"] = g["r2"] - g["coin"].map(mean_r2)
        sub = g[(g["regime"] == "mean_reversion")].dropna(subset=["forecast", "ex", "ex2"])
    else:
        sub = pd.DataFrame(columns=["forecast", "ex", "ex2"])

    n_regime = int(len(sub))
    n_pos = int((sub["forecast"] > 0).sum()) if n_regime else 0
    counts = {"grid cases in the regime": n_regime, "grid cases with forecast > 0": n_pos}

    def ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        if len(x) < 3 or np.std(x) == 0:
            return None, None
        res = stats.linregress(x, y)
        t = res.slope / res.stderr if res.stderr and res.stderr > 0 else None
        return float(res.slope), (float(t) if t is not None else None)

    slope, tval = ols(sub["forecast"], sub["ex"]) if n_regime else (None, None)
    slope2, t2 = ols(sub["forecast"], sub["ex2"]) if n_regime else (None, None)

    sup_pass = None
    if slope is not None and slope2 is not None:
        sup_pass = bool(slope2 > 0 and slope2 >= 0.5 * slope)

    main = {
        "name": "t of the slope of 72-bar excess return on forecast (mean_reversion grid bars)",
        "value": tval,
        "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
        "threshold": "confirm if t >= 2 with supporting check passed; reject if t <= -2",
    }
    sup = {"name": "slope of 24-to-72-bar excess return on forecast, > 0 and >= half the main slope",
           "value": slope2, "passed": sup_pass}
    reading = ("Grid bars are positions 0, 72, 144... of each window with close[t+72] inside it, the regime is the "
               "recorded `regime` at the grid bar, and each excess (72-bar and 24-to-72-bar) is over that coin's "
               "mean of the same grid return across all its grid bars in all windows.")

    if n_regime < 200 or n_pos < 100:
        status = "not observable"
        decided = ("Minimum count not reached: %d grid cases in the regime (need 200) and %d with forecast > 0 "
                   "(need 100)." % (n_regime, n_pos))
    elif tval is None:
        status = "inconclusive"
        decided = "The main slope t could not be computed (no variation in the forecast)."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main slope t >= 2 and the supporting 24-to-72-bar slope is positive and at least half the main slope."
    elif tval <= -2:
        status = "rejected"
        decided = "Main slope t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Main slope t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Main slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
