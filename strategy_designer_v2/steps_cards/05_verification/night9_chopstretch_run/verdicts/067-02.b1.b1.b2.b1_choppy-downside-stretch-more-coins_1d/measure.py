import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.stretch.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback: recompute the stretch's sign from prices inside the window
            sma = close.rolling(20, min_periods=20).mean()
            below_px = close < sma
            below = np.where(raw.notna(), raw < 0, below_px)
            choppy = df["regime"].astype(str) == "unknown"
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & choppy & pd.Series(below, index=df.index).astype(bool) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("The choppy profile is the bars whose regime is 'unknown' (the only regime with a strategy, the "
               "vetoes sending |60-bar trend| > 10 to the null 'chop'), below the average is a raw stretch < 0 "
               "(recomputed as close < 20-bar SMA where not recorded); the drift is each coin's mean 5-bar return "
               "on the window grids; the weighted mean's t pools per-day sums of weighted deviations "
               "(cluster SE with D/(D-1)); the size split puts |forecast| > median in the larger half and uses "
               "unweighted half means; the plan's minimum counts, if not met, give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are short bars in the choppy profile with the close "
                           "below its 20-day SMA, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f < 0:
                    coin_rows.append((ts.iloc[i].floor("D"), r, abs(f)))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for d, r, a in coin_rows:
            rows.append({"day": d, "x": -(r - drift), "w": a})

    cases = pd.DataFrame(rows, columns=["day", "x", "w"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    threshold = "mean > 0 with t >= 2 confirms (with size check > 0); t <= -2 rejects; else inconclusive"
    main_name = "|forecast|-weighted mean short-side 5-day excess move (minus drift), day-pooled t"

    if n_cases < 100 or n_days < 50:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean excess, larger half minus smaller half of |forecast|",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 100 grid cases on at least 50 distinct days is not reached.",
            "reading": reading,
        }

    x = cases["x"].values
    wts = cases["w"].values
    sw = wts.sum()
    m = float((x * wts).sum() / sw) if sw > 0 else float("nan")
    cases["dev"] = wts * (x - m)
    S = cases.groupby("day")["dev"].sum().values
    D = len(S)
    se = np.sqrt((S ** 2).sum() * D / (D - 1)) / sw if (D > 1 and sw > 0) else float("nan")
    t = float(m / se) if (np.isfinite(se) and se > 0) else float("nan")

    a = cases["w"].values
    med = np.median(a)
    big = cases.loc[a > med, "x"]
    small = cases.loc[a <= med, "x"]
    if len(big) > 0 and len(small) > 0:
        diff = float(big.mean() - small.mean())
        sc_pass = bool(diff > 0)
    else:
        diff = None
        sc_pass = None

    if np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = "The main measure's t is <= -2: stretched closes were followed by a rise beyond the drift."
    elif np.isfinite(t) and m > 0 and t >= 2:
        if sc_pass:
            status = "confirmed"
            decided = "The main measure's mean is above 0 with t >= 2 and the size check is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the size check is not above 0."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (or its mean is not above 0)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "t of the weighted mean, same-day cases pooled",
                                       "value": t if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess, larger half minus smaller half of |forecast|",
                             "value": diff, "passed": sc_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
