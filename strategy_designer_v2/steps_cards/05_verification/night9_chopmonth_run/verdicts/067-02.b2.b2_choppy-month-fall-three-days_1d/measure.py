import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # raw 30-bar return in percent: recorded value, else recomputed from prices
            raw_px = (close / close.shift(30) - 1.0) * 100.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").where(lambda s: s.notna(), raw_px)
            else:
                raw = raw_px
            # choppy profile: 60-bar return within [-10, 10] %, from prices where computable,
            # else the detector's decision (regime 'unknown' = not vetoed to 'chop')
            tr60 = (close / close.shift(60) - 1.0) * 100.0
            reg_choppy = df["regime"].astype(str) == "unknown"
            choppy = pd.Series(np.where(tr60.notna(), (tr60 >= -10) & (tr60 <= 10), reg_choppy),
                               index=df.index).astype(bool)
            active = fc.notna() & (fc != 0)
            situ = choppy & raw.notna() & (raw < 0)
            ok = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the choppy profile "
                           "(60-day return within +/-10%) with the close under its close of 30 days earlier."),
            "reading": "Choppy profile taken as the config's 60-bar return within +/-10% from prices, the regime column where 60 bars are not available.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    rows.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), float(fc[i]), float(r)))
        coin_grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "forecast", "ret"])
    if len(cases):
        cases["mean"] = cases["coin"].map(coin_grid_rets)
        cases = cases[cases["mean"].notna()]
        cases["excess"] = cases["ret"] - cases["mean"]
        cases["gain"] = (-cases["forecast"] / 10.0) * (-cases["excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    mm_name = "mean of (-forecast/10) x negated excess 3-bar return"
    thr = "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"
    reading = ("The deepest third is the n//3 cases with the most negative forecast and the shallowest the n//3 nearest 0; "
               "the coin's mean 3-bar return is over all its grid bars in all windows; the t sums each day's deviations "
               "from the mean (clustered standard error with G/(G-1) correction); fewer than the minimum cases is 'not observable'.")

    if n_cases < 100 or n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": mm_name, "value": float(cases["gain"].mean()) if n_cases else None,
                             "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of at least 100 grid cases on at least 30 distinct days is not reached.",
            "reading": reading,
        }

    g = cases["gain"].values
    m = float(g.mean())
    dev = cases.assign(d=g - m).groupby("day")["d"].sum().values
    G = len(dev)
    se = np.sqrt(np.sum(dev ** 2) * G / (G - 1)) / n_cases if G > 1 else np.nan
    t = float(m / se) if se and np.isfinite(se) and se > 0 else 0.0

    srt = cases.sort_values("forecast", kind="mergesort").reset_index(drop=True)
    k = n_cases // 3
    deep = srt.iloc[:k]["excess"].mean()
    shallow = srt.iloc[n_cases - k:]["excess"].mean()
    sup_val = float(deep - shallow) if k > 0 else None
    sup_pass = bool(sup_val is not None and sup_val < 0)

    if m > 0 and t >= 2 and sup_pass:
        status, dec = "confirmed", "The main measure is above 0 with t >= 2 and the supporting check passes."
    elif m < 0 and t <= -2:
        status, dec = "rejected", "The main measure is below 0 with t <= -2."
    elif m > 0 and t >= 2:
        status, dec = "inconclusive", "The main measure confirms but the supporting check fails, which the plan calls inconclusive."
    else:
        status, dec = "inconclusive", "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": m,
                         "statistic": {"name": "t of the mean, cases of one day summed", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "mean excess 3-bar return, deepest third minus shallowest third",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": dec,
        "reading": reading,
    }
