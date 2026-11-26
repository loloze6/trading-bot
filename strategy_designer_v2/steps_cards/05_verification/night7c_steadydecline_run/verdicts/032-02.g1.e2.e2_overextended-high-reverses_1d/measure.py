import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    P = 28
    FC = "forecast"
    PP = "debug_info.components.runup.post_pipeline_value"

    # ---------- 1. situation check: close at its 28-day closing high (bar t included), short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            full_max = close.rolling(P, min_periods=P).max()
            exp_max = close.rolling(P, min_periods=1).max()
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            for i in range(len(df)):
                if fc.iloc[i] == 0 or np.isnan(close.iloc[i]):
                    continue
                n_active += 1
                c = close.iloc[i]
                if not np.isnan(full_max.iloc[i]):
                    at_high = c >= full_max.iloc[i] - 1e-12 * abs(c)
                else:
                    # fewer than 28 bars in the window: a close below an earlier close of the window
                    # is surely not at the 28-day high; otherwise the detector's own decision settles it
                    if c < exp_max.iloc[i] - 1e-12 * abs(c):
                        at_high = False
                    else:
                        at_high = regime.iloc[i] == "trending"
                if at_high and fc.iloc[i] < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of the slope of next-5-bar excess return on abs(post_pipeline_value of runup), trending grid bars"
    thr = "confirm if slope t <= -2 with supporting check passing; reject if slope t >= +2; at least 30 independent cases"
    reading = ("Situation computed from closes as close >= rolling 28-bar max close of the window (bar t included), "
               "using the detector's regime only for the first 27 bars of a window where 28 closes are not available; "
               "cases are regime=='trending' bars at grid positions 0,5,10,... of each window with t+5 inside the window, "
               "strength = abs(post_pipeline_value) including zeros from the clip, drift = coin's mean non-overlapping "
               "5-bar return over all its windows, slope t from pooled OLS across coins and windows; "
               "below 30 cases is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars at the 28-day closing high"
                           if n_active > 0 else "The record has no bar with a non-zero forecast, so the short bets at "
                           "28-day closing highs the plan describes are absent"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean non-overlapping 5-bar return over all windows
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rs.append(r)
        drift[coin] = float(np.mean(rs)) if rs else np.nan

    xs, ys = [], []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            pp = (pd.to_numeric(df[PP], errors="coerce").to_numpy()
                  if PP in df.columns else np.full(len(df), np.nan))
            for i in range(0, len(close) - H, H):
                if reg[i] != "trending":
                    continue
                r = close[i + H] / close[i] - 1.0
                s = pp[i]
                if not (np.isfinite(r) and np.isfinite(s)):
                    continue
                xs.append(abs(s))
                ys.append(r - d)

    n = len(xs)
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    counts = {"independent cases": int(n)}

    slope = None
    t = None
    if n >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t = float(lr.slope / lr.stderr)

    sup_val = float(np.mean(-ys)) if n > 0 else None
    sup_pass = (sup_val is not None and sup_val > 0) if n > 0 else None

    stat = {"name": "OLS slope t", "value": t} if t is not None else None
    main = {"name": main_name, "value": t, "statistic": stat, "threshold": thr}
    sup = {"name": "mean excess 5-bar return in the short direction > 0", "value": sup_val, "passed": sup_pass}

    if n < 30:
        status = "not observable"
        decided = f"Only {n} independent cases, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (no variation in strength), so it is not <= -2 nor >= +2."
    elif t <= -2 and sup_pass:
        status = "confirmed"
        decided = "The slope t is <= -2 and the mean short-direction excess return is above 0 (confirm rule)."
    elif t >= 2:
        status = "rejected"
        decided = "The slope t is >= +2 (reject rule)."
    elif t <= -2:
        status = "inconclusive"
        decided = "The slope t is <= -2 but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
