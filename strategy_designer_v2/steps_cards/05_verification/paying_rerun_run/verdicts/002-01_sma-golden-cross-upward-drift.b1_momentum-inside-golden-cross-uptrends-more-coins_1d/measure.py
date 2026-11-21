import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_CASES = 100
    RAW = "debug_info.components.mom20.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns or "regime" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fill missing raw momentum with the 20-bar return recomputed inside the window
            recomputed = close / close.shift(20) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            trail_mean = raw.shift(1).rolling(60, min_periods=20).mean()
            demeaned = raw - trail_mean
            trending = df["regime"].astype(str) == "trending"
            active = fc.notna() & (fc != 0)
            sf = np.sign(fc)
            side_ok = (sf == np.sign(raw)) | (sf == np.sign(demeaned))
            n_active += int(active.sum())
            n_agree += int((active & trending & side_ok.fillna(False)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    reading = ("Situation read on the `regime` column (SMA50>SMA200 = `trending`), and an active bar is on the "
               "expected side when its forecast sign matches the 20-day return or that return minus its trailing "
               "60-value mean (the standardisation may demean); the regression is OLS with intercept on all "
               "trending grid bars, the coin's mean 10-bar return is taken over the non-overlapping grid bars of "
               "all its windows, and thirds are the lowest and highest floor(n/3) cases sorted by forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of excess 10-bar return on forecast (trending grid bars)",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of active bars are trending (SMA50 above SMA200) bars with a forecast "
                           "sign that follows the 20-day momentum, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "ret": c1 / c0 - 1.0, "fc": fc[p],
                             "trending": reg[p] == "trending"})
    allg = pd.DataFrame(rows, columns=["coin", "ret", "fc", "trending"])
    if len(allg):
        coin_mean = allg.groupby("coin")["ret"].mean()
        allg["excess"] = allg["ret"] - allg["coin"].map(coin_mean)
    else:
        allg["excess"] = []
    cases = allg[allg["trending"].astype(bool)].dropna(subset=["fc", "excess"])
    n_cases = int(len(cases))

    main = {"name": "slope of excess 10-bar return on forecast (trending grid bars)",
            "value": None, "statistic": None,
            "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"}
    sup = {"name": "mean excess return top third minus bottom third of forecasts", "value": None, "passed": None}
    counts = {"independent trending cases": n_cases}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": sup,
            "counts": counts,
            "decided_by": f"Only {n_cases} independent trending cases, below the plan's minimum of {MIN_CASES}.",
            "reading": reading,
        }

    x = cases["fc"].values.astype(float)
    y = cases["excess"].values.astype(float)
    slope = t = None
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    main["value"] = slope
    main["statistic"] = {"name": "OLS slope t", "value": t} if t is not None else None

    order = np.argsort(x, kind="mergesort")
    k = n_cases // 3
    if k > 0:
        diff = float(y[order[-k:]].mean() - y[order[:k]].mean())
        sup["value"] = diff
        sup["passed"] = bool(diff > 0)
    counts["cases per third"] = int(k)

    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the forecast), so the result is inconclusive."
    elif slope > 0 and t >= 2:
        if sup["passed"]:
            status = "confirmed"
            decided = "The slope is above 0 with t >= 2 and the top-minus-bottom-third excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is above 0 with t >= 2 but the supporting top-minus-bottom-third check fails."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
