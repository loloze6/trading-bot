import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.stretch_below.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            # raw stretch: recorded value, else recomputed sign from prices (close vs its 20-bar SMA)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            sma = close.rolling(20, min_periods=20).mean()
            vol = close.pct_change().rolling(20, min_periods=20).std()
            recomputed = (close - sma) / (close * vol)
            raw = raw.where(raw.notna(), recomputed)
            regime = d["regime"].astype(str)
            agitated = regime != "chop"
            below = raw < 0
            active = fc != 0
            agree = active & agitated & below & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the agitated "
                           "profile (regime not chop) with the close below its 20-day average (raw stretch < 0)."),
            "reading": "Agitated profile read as regime not 'chop'; below the average read as the raw stretch value < 0.",
        }

    # ---------- 2. criterion ----------
    # coin's mean 10-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f > 0:
                    rows.append((coin, ts.iloc[i].normalize(), float(f), r))
        coin_mean[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "r"])
    if len(cases):
        cases["ex"] = cases["r"] - cases["coin"].map(coin_mean)
        cases = cases.dropna(subset=["ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    reading = ("Agitated profile read as regime not 'chop' and below the average as raw stretch < 0; cases are grid "
               "bars (positions 0,10,20,... per window) with forecast > 0 and a 10-bar return inside the window; the t "
               "is the weighted mean over a day-clustered standard error (each day's weighted deviations summed); deep "
               "half = forecast strictly above the cases' median, shallow = the rest, compared on unweighted mean excess; "
               "the plan's minimum counts not reached give 'not observable'.")
    mm_name = "forecast-weighted mean excess 10-bar return"
    thr = "confirm: > 0 with t >= 2 and deep-minus-shallow > 0; reject: < 0 with t <= -2"

    if n_cases < 100 or n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 100 cases on at least 30 distinct days is not reached.",
            "reading": reading,
        }

    f = cases["f"].values
    ex = cases["ex"].values
    wsum = f.sum()
    m = float((f * ex).sum() / wsum)
    cases["dev"] = (f / wsum) * (ex - m)
    D = cases.groupby("day")["dev"].sum().values
    G = len(D)
    var = (D ** 2).sum() * G / (G - 1) if G > 1 else np.nan
    se = float(np.sqrt(var)) if np.isfinite(var) else np.nan
    t = float(m / se) if se and np.isfinite(se) and se > 0 else 0.0

    med = float(np.median(f))
    deep = cases.loc[cases["f"] > med, "ex"]
    shallow = cases.loc[cases["f"] <= med, "ex"]
    if len(deep) and len(shallow):
        diff = float(deep.mean() - shallow.mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False

    if m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The weighted mean excess return is > 0 with t >= 2 and the deep-minus-shallow difference is > 0."
    elif m > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the deep-minus-shallow difference is <= 0, which the plan calls inconclusive."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is < 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": m,
                         "statistic": {"name": "t of the weighted mean, cases summed per day", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "deep minus shallow mean excess 10-bar return", "value": diff,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
