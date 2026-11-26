import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.range_pos.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            # range position recomputed from prices (20 bars incl. today), fallback when raw not recorded
            hh = high.rolling(20, min_periods=20).max()
            ll = low.rolling(20, min_periods=20).min()
            half = (hh - ll) / 2.0
            pos_px = (close - (hh + ll) / 2.0) / half.replace(0, np.nan)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                pos = raw.where(raw.notna(), pos_px)
            else:
                pos = pos_px
            if "regime" in d.columns:
                reg = d["regime"]
            else:
                reg = d.get("debug_info.regime", pd.Series([None] * len(d)))
            reg = reg.astype(object)
            in_profile = reg.notna() & (reg.astype(str).str.lower() != "chop")
            active = fc.notna() & (fc != 0)
            agree = active & in_profile & pos.notna() & (np.sign(pos) == np.sign(fc))
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (10-bar return - coin's mean 10-bar return), per-day sums, on the 10-bar grid"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases": None, "distinct days": None},
            "decided_by": ("fewer than 90% of nonzero-forecast bars are in the rising calm profile (non-chop regime) "
                           "with the forecast's sign equal to the sign of the 20-day range position"),
            "reading": "the profile is the regime detector's non-chop regime; the side is the sign of the range position.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        cand = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    cand.append((ts.iloc[i].floor("D"), fc[i], r))
        if allr:
            m = float(np.mean(allr))
            coin_rets[coin] = m
            for day, f, r in cand:
                rows.append((day, f / 10.0 * (r - m)))

    n_cases = len(rows)
    if n_cases > 0:
        cs = pd.DataFrame(rows, columns=["day", "v"])
        daily = cs.groupby("day")["v"].sum()
        n_days = int(len(daily))
        case_mean = float(cs["v"].mean())
    else:
        daily = pd.Series(dtype=float)
        n_days = 0
        case_mean = None

    mean_val = float(daily.mean()) if n_days > 0 else None
    t_val = None
    if n_days > 1:
        sd = float(daily.std(ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_days)))

    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided_by = (f"minimum not reached: {n_cases} grid cases (need 100) on {n_days} distinct days (need 50)")
    elif t_val is None:
        status = "inconclusive"
        decided_by = "t could not be computed (zero dispersion of the daily sums), so neither confirm nor reject is met"
    elif mean_val > 0 and t_val >= 2:
        status = "confirmed"
        decided_by = "confirm rule met: the mean is positive with t >= 2"
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "reject rule met: the mean is negative with t <= -2"
    else:
        status = "inconclusive"
        decided_by = "inconclusive rule met: t lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean of per-day sums", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The profile is the non-chop regime, and the side is the sign of the range position. "
                    "Each coin's mean 10-bar return is over all its grid returns in all its windows. "
                    "The cases of one UTC day are summed into one value, and the reported mean and t are those of "
                    "these daily sums. "
                    f"The plain per-case mean is {case_mean}. "
                    "A count below the minimum gives 'not observable', as the workflow requires."),
    }
