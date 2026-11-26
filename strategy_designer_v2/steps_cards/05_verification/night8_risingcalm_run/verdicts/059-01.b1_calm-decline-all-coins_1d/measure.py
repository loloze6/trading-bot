import numpy as np
import pandas as pd

RAW = "debug_info.components.scaled_decline.last_history_value"
H = 5


def _raw_recomputed(close):
    r1 = close.pct_change()
    ret14 = close / close.shift(14) - 1.0
    sd30 = r1.rolling(30, min_periods=30).std()
    return ret14 / (sd30 * np.sqrt(14.0))


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), _raw_recomputed(close))
            calm = df["regime"].astype(str) == "unknown"
            situ = calm & (raw < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "|forecast|-weighted mean short drift-removed 5-day return"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 30 distinct days"
    reading = ("Calm market = bars whose regime is 'unknown' (not vetoed to 'chop'), the situation is calm and raw component < 0 "
               "(recomputed from closes where not recorded), side short; cases are forecast<0 bars on the 0,5,10,... grid of each window "
               "with a 5-bar return inside the window, drift is the coin's mean 5-bar return over all its grid bars, the t is the weighted "
               "mean over a day-clustered standard error (weighted deviations summed per day), and the halves split at the median |forecast| "
               "(deeper: strictly above), compared on unweighted means of the unsigned drift-removed return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "distinct days": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are calm-market bars with a negative 14-day "
                           "swing-scaled return and a short forecast (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f < 0:
                    coin_cases.append((ts.iloc[i].strftime("%Y-%m-%d"), r, abs(float(f))))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for d, r, a in coin_cases:
            rows.append((d, r - drift, a))

    cases = pd.DataFrame(rows, columns=["day", "excess", "w"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct days": n_days, "cases": n_cases}

    mean_w = None
    t = None
    if n_cases > 0 and cases["w"].sum() > 0:
        x = -cases["excess"].values  # signed short
        wt = cases["w"].values
        W = wt.sum()
        mean_w = float(np.sum(x * wt) / W)
        dev = pd.Series(wt * (x - mean_w)).groupby(cases["day"].values).sum().values
        G = len(dev)
        if G > 1:
            se = np.sqrt(np.sum(dev ** 2) * G / (G - 1)) / W
            t = float(mean_w / se) if se > 0 else None

    supp_val = None
    supp_pass = None
    if n_cases > 0:
        med = float(np.median(cases["w"].values))
        deep = cases.loc[cases["w"] > med, "excess"]
        shal = cases.loc[cases["w"] <= med, "excess"]
        if len(deep) > 0 and len(shal) > 0:
            supp_val = float(deep.mean() - shal.mean())
            supp_pass = bool(supp_val < 0)
        else:
            supp_pass = False

    if n_days < 30:
        status = "not observable"
        decided = "Cases fall on %d distinct days, fewer than the 30 a verdict needs." % n_days
    elif mean_w is None or t is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_w > 0 and t >= 2 and supp_pass:
        status = "confirmed"
        decided = "The weighted mean short excess return is positive with t >= 2 and the deeper half falls more than the shallower half."
    elif mean_w < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean short excess return is negative with t <= -2: a rebound follows calm swing-scaled declines."
    elif mean_w > 0 and t >= 2:
        status = "inconclusive"
        decided = "The t is >= 2 but the deeper half does not fall more than the shallower half."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_w,
                         "statistic": ({"name": "t of weighted mean, cases of a day grouped", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "deeper-half minus shallower-half mean drift-removed 5-day return (must be < 0)",
                             "value": supp_val, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
