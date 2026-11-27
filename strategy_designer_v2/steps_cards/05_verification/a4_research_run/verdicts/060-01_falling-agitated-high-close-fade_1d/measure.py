import numpy as np
import pandas as pd


def measure(bars):
    LOC_COL = "debug_info.components.high_close.last_history_value"

    # ---------- gather per-coin data ----------
    coin_frames = {}
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["_coin"] = coin
            d["_win"] = w
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            # next-bar return inside the window only
            d["_r1"] = close.shift(-1) / close - 1.0
            # signed close location from prices: 20 x (2 x (c - l) / (h - l) - 1)
            rng = (high - low).replace(0, np.nan)
            loc_px = 20.0 * (2.0 * (close - low) / rng - 1.0)
            if LOC_COL in d.columns:
                loc_raw = pd.to_numeric(d[LOC_COL], errors="coerce")
                d["_loc"] = loc_raw.where(loc_raw.notna(), loc_px)
            else:
                d["_loc"] = loc_px
            d["_fc"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["_day"] = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            frames.append(d)
        if frames:
            coin_frames[coin] = pd.concat(frames, ignore_index=True)

    if not coin_frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-side next-day excess return", "value": None,
                             "statistic": None, "threshold": "mean > 0 with t >= 2 (confirm); mean < 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allbars = pd.concat(coin_frames.values(), ignore_index=True)

    # ---------- situation check ----------
    active = allbars[allbars["_fc"] != 0]
    n_active = len(active)
    if n_active > 0:
        in_sit = (
            (active["regime"].astype(str) == "mean_reversion")
            & (active["_loc"] >= 0)
            & (active["_fc"] < 0)
        )
        agreement = float(in_sit.mean())
    else:
        agreement = 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.90)

    reading = (
        "The falling-agitated profile is taken from the detector's recorded regime 'mean_reversion' (its profile "
        "components are not recorded and their 365-bar lookback cannot be rebuilt inside a window), the close location "
        "from the recorded raw value or the prices; the coin's mean daily return is the mean of all its in-window "
        "next-bar returns; the day-clustered t uses per-day summed deviations with a n_days/(n_days-1) correction; "
        "the supporting split puts cases with |forecast| above the median in the larger half and the rest in the smaller."
    )

    threshold_txt = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean short-side next-day excess return", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (
                "Fewer than 90% of the bars with a non-zero forecast are short bars in the falling-agitated regime "
                "with the close in the upper half of the day's range (agreement %.3f)." % agreement
            ),
            "reading": reading,
        }

    # ---------- main measure ----------
    case_list = []
    for coin, d in coin_frames.items():
        mu = d["_r1"].mean()  # mean daily return over all windows
        c = d[(d["_fc"] < 0) & d["_r1"].notna()].copy()
        if len(c) == 0 or not np.isfinite(mu):
            continue
        c["_x"] = -(c["_r1"] - mu)
        case_list.append(c[["_coin", "_day", "_fc", "_x"]])
    cases = pd.concat(case_list, ignore_index=True) if case_list else pd.DataFrame(columns=["_coin", "_day", "_fc", "_x"])

    n_cases = int(len(cases))
    n_days = int(cases["_day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    def clustered_t(x, days):
        x = np.asarray(x, dtype=float)
        n = len(x)
        if n < 2:
            return np.nan, np.nan
        m = x.mean()
        dev = pd.Series(x - m).groupby(np.asarray(days)).sum().values
        k = len(dev)
        if k < 2:
            return m, np.nan
        var = (dev ** 2).sum() * k / (k - 1) / (n ** 2)
        se = np.sqrt(var)
        return m, (m / se if se > 0 else np.nan)

    mean_x, t_x = clustered_t(cases["_x"].values, cases["_day"].values) if n_cases else (np.nan, np.nan)

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        a = cases["_fc"].abs()
        med = a.median()
        big = cases.loc[a > med, "_x"]
        small = cases.loc[a <= med, "_x"]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    mm_val = float(mean_x) if np.isfinite(mean_x) else None
    t_val = float(t_x) if np.isfinite(t_x) else None

    main = {
        "name": "mean short-side next-day excess return over the coin's mean",
        "value": mm_val,
        "statistic": {"name": "t of the mean, cases of one day summed", "value": t_val} if t_val is not None else None,
        "threshold": threshold_txt,
    }
    support = {
        "name": "mean excess of larger-|forecast| half minus smaller half",
        "value": sup_val,
        "passed": sup_pass,
    }

    # ---------- decision ----------
    if n_cases < 100 or n_days < 100:
        status = "not observable"
        decided_by = "The plan's minimum of 100 cases on 100 distinct days is not reached (%d cases, %d days)." % (n_cases, n_days)
    elif mm_val is None or t_val is None:
        status = "inconclusive"
        decided_by = "The mean or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif mm_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = "The mean short-side excess is above 0 with t >= 2 and the supporting check is above 0."
        else:
            status = "inconclusive"
            decided_by = "The main measure confirms (mean > 0, t >= 2) but the supporting check is not above 0."
    elif mm_val < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The mean short-side excess is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean short-side excess lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
