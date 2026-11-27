import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    FC = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            ret = close.pct_change()
            vol10 = ret.rolling(10, min_periods=10).std()
            vol30 = ret.rolling(30, min_periods=30).std()
            vr = vol10 / vol30
            ret60 = (close / close.shift(60) - 1.0) * 100.0
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            fall30 = df[FC].astype(float) if FC in df.columns else pd.Series([np.nan] * len(df))
            ret30_px = (close / close.shift(30) - 1.0) * 100.0
            for i in range(len(df)):
                f = fc.iloc[i]
                if f == 0:
                    continue
                n_active += 1
                # choppy profile and quickening swing: from prices; recorded regime where prices lack history
                if np.isfinite(vr.iloc[i]) and np.isfinite(ret60.iloc[i]):
                    chop_ok = abs(ret60.iloc[i]) <= 10.0
                    vr_ok = vr.iloc[i] > 1.0
                    regime_ok = chop_ok and vr_ok
                else:
                    regime_ok = regime.iloc[i] == "trending"
                r30 = fall30.iloc[i]
                if not np.isfinite(r30):
                    r30 = ret30_px.iloc[i]
                fall_ok = np.isfinite(r30) and r30 < 0
                if regime_ok and fall_ok and f < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The choppy profile (|60-bar return| <= 10 %) and the swing rule (10-bar std of daily returns over the "
               "30-bar one > 1) are recomputed from closes inside each window, using the recorded regime where the "
               "window lacks the history; the score's mean is the mean over cases while its t is the ordinary t of the "
               "per-day summed scores; the coin's mean 10-bar return is taken on the non-overlapping grid of all its "
               "windows; the larger half of the supporting check is the cases with |forecast| strictly above the median.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars in a choppy profile with "
                           "the 10-day swing above the 30-day one after a 30-day fall."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    grid_rets = {}
    cases = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H])) or close[i] <= 0:
                    continue
                r = close[i + H] / close[i] - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    cases.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    rows = []
    for coin, day, f, r in cases:
        mu = grid_rets[coin]
        if not np.isfinite(mu):
            continue
        excess_fall = -(r - mu)
        rows.append({"coin": coin, "day": day, "f": f, "excess_fall": excess_fall,
                     "score": (-f / 10.0) * excess_fall})
    cdf = pd.DataFrame(rows, columns=["coin", "day", "f", "excess_fall", "score"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_score = float(cdf["score"].mean()) if n_cases else None
    t = None
    if n_days >= 2:
        ds = cdf.groupby("day")["score"].sum()
        sd = ds.std(ddof=1)
        if sd > 0:
            t = float(ds.mean() / (sd / np.sqrt(len(ds))))

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        a = cdf["f"].abs()
        med = a.median()
        big = cdf.loc[a > med, "excess_fall"]
        small = cdf.loc[a <= med, "excess_fall"]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"distinct case days": n_days, "cases": n_cases}
    mm = {"name": "mean position-weighted excess 10-bar fall",
          "value": mean_score,
          "statistic": None if t is None else {"name": "t of the mean (cases of a day summed)", "value": t},
          "threshold": "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"}
    sc = {"name": "mean excess fall, larger |forecast| half minus smaller half", "value": sup_val, "passed": sup_pass}
    sit = {"agreement": float(agreement), "passed": True}

    if n_days < 30:
        return {"status": "not observable", "situation_check": sit, "main_measure": mm, "supporting_check": sc,
                "counts": counts,
                "decided_by": f"Only {n_days} distinct case days, below the plan's minimum of 30.",
                "reading": reading}

    if t is not None and mean_score is not None and mean_score > 0 and t >= 2:
        if sup_pass:
            status, why = "confirmed", "The mean score is above 0 with t >= 2 and the supporting check passes."
        else:
            status, why = "inconclusive", "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif t is not None and mean_score is not None and mean_score < 0 and t <= -2:
        status, why = "rejected", "The mean score is below 0 with t <= -2."
    else:
        status, why = "inconclusive", "The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {"status": status, "situation_check": sit, "main_measure": mm, "supporting_check": sc,
            "counts": counts, "decided_by": why, "reading": reading}
