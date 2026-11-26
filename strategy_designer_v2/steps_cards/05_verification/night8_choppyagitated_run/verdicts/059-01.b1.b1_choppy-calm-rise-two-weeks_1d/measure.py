import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.weekly_rise.last_history_value"
    PROFILE_LABEL = "unknown"  # the detector's default regime = no veto = choppy calm (|60d move| <= 10, vol pct <= 0.5)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            # raw weekly rise: recorded raw value, else recomputed from prices
            ret7 = close / close.shift(7) - 1.0
            dret = close.pct_change()
            vol30 = dret.rolling(30, min_periods=30).std()
            raw_px = ret7 / (vol30 * np.sqrt(7.0))
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), raw_px)
            else:
                raw = raw_px
            if "regime" in d.columns:
                reg = d["regime"].astype(str)
            else:
                reg = d["debug_info.regime"].astype(str)
            in_profile = reg == PROFILE_LABEL
            situation = in_profile & (raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "slope of 14-bar excess forward return on forecast (forecast > 0 grid cells, pooled)"
    threshold = "confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2 or mean excess t <= -2; at least 100 cells"
    reading = ("The choppy calm profile is read from the recorded regime (the detector's default 'unknown', i.e. no veto) "
               "since the detector's components are not recorded and its 365-bar lookback cannot be rebuilt in a window, "
               "the rise from the raw weekly_rise value (or its price rebuild where missing); the coin's mean 14-bar return "
               "is taken over all its grid cells in all windows, and both t's cluster cases by UTC day with a G/(G-1) correction.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cells with forecast > 0": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the choppy calm "
                           "profile after a rising week, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_rows.append((coin, ts.iloc[i].floor("D"), fc[i], r))
        if not coin_rows:
            continue
        cr = pd.DataFrame(coin_rows, columns=["coin", "day", "fc", "ret"])
        cr["excess"] = cr["ret"] - cr["ret"].mean()
        rows.append(cr)

    if rows:
        allc = pd.concat(rows, ignore_index=True)
        cells = allc[(allc["fc"] > 0) & allc["fc"].notna() & allc["excess"].notna()].copy()
    else:
        cells = pd.DataFrame(columns=["coin", "day", "fc", "ret", "excess"])

    n_cells = int(len(cells))
    n_days = int(cells["day"].nunique()) if n_cells else 0

    slope = None
    slope_t = None
    mean_ex = None
    mean_t = None
    if n_cells >= 2:
        x = cells["fc"].astype(float).values
        y = cells["excess"].astype(float).values
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        mean_ex = float(np.mean(y))
        G = n_days
        corr = G / (G - 1.0) if G > 1 else np.nan
        if sxx > 0:
            slope = float(np.sum(xc * (y - y.mean())) / sxx)
            intercept = y.mean() - slope * x.mean()
            e = y - intercept - slope * x
            sc = pd.Series(xc * e).groupby(cells["day"].values).sum().values
            var_b = corr * float(np.sum(sc ** 2)) / sxx ** 2
            if np.isfinite(var_b) and var_b > 0:
                slope_t = float(slope / np.sqrt(var_b))
        dev = pd.Series(y - mean_ex).groupby(cells["day"].values).sum().values
        var_m = corr * float(np.sum(dev ** 2)) / n_cells ** 2
        if np.isfinite(var_m) and var_m > 0:
            mean_t = float(mean_ex / np.sqrt(var_m))

    sup_pass = None if mean_ex is None else bool(mean_ex > 0)
    counts = {"grid cells with forecast > 0": n_cells, "days of those cells": n_days}

    if n_cells < 100:
        status = "not observable"
        decided = f"Only {n_cells} grid cells with forecast > 0, fewer than the plan's minimum of 100."
    elif (slope_t is not None and slope_t <= -2) or (mean_t is not None and mean_t <= -2):
        status = "rejected"
        decided = "Reject rule met: the slope's t is -2 or less, or the mean excess return has t of -2 or less (a giveback)."
    elif slope_t is not None and slope_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: the slope's t is 2 or more and the mean excess return is above 0."
    else:
        status = "inconclusive"
        decided = "Neither rule met: the slope's t is between -2 and 2, or the slope is positive with a mean excess return at or below 0."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t, clustered by day", "value": slope_t} if slope_t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 14-bar return over the same cells > 0",
            "value": mean_ex,
            "passed": sup_pass,
            "t_clustered_by_day": mean_t,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
