import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    WIDE = 1.5
    MIN_CASES = 30
    RM = "debug_info.components.range_mult.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        for c in ["open", "high", "low", "close", "forecast"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d[RM] = pd.to_numeric(d[RM], errors="coerce") if RM in d.columns else np.nan
        return d

    data = {}
    for coin, wins in bars.items():
        data[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[coin][w] = prep(df)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in data.items():
        for w, d in wins.items():
            rng = d["high"] - d["low"]
            ratio_px = rng / rng.rolling(30, min_periods=30).mean()
            ratio = d[RM].where(d[RM].notna(), ratio_px)
            wide = ratio >= WIDE - 1e-9
            ret60 = d["close"] / d["close"].shift(60) - 1.0
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            falling = np.where(ret60.notna(), ret60 < 0, regime == "trending")
            falling = pd.Series(falling, index=d.index).astype(bool)
            f = d["forecast"].fillna(0.0)
            active = f != 0
            agree = active & wide.fillna(False) & falling & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 3-bar move per case, short direction"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 over >= 30 cases and slope < 0; reject: mean < 0 with t <= -2"
    reading_base = ("Situation = range ratio >= 1.5 (recorded range_mult, else recomputed from prices) in a falling market "
                    "(60-bar close return < 0, or regime 'trending' where 60 bars are not available in the window), short side; "
                    "a case is the first short bet (forecast falling >= 2 points below its lowest short level since the last bet) "
                    "in each 3-bar grid cell of a window, its return taken from that bet bar's close over 3 bars inside the window, "
                    "drift = per-coin mean of non-overlapping grid 3-bar returns over all windows, t clustered by UTC day, "
                    "slope = OLS of raw (unsigned) excess return on range_mult at the case bar.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars on a wide day "
                           "(range >= 1.5x its 30-day mean) in a falling market, as the Fidelity requires."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin
    drift = {}
    for coin, wins in data.items():
        rets = []
        for w, d in wins.items():
            c = d["close"].values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, short_excess, raw_excess, range_mult)
    for coin, wins in data.items():
        dr = drift[coin]
        if not np.isfinite(dr):
            continue
        for w, d in wins.items():
            f = d["forecast"].fillna(0.0).values
            c = d["close"].values
            rm = d[RM].values
            ts = d["timestamp"]
            n = len(d)
            ref = 0.0
            prev_short = False
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                if f[i] < 0:
                    s = -f[i]
                    if not prev_short:
                        ref = 0.0
                    ref = min(ref, s)
                    if s - ref >= BAND - 1e-12:
                        bet[i] = True
                        ref = s
                    prev_short = True
                else:
                    ref = 0.0
                    prev_short = False
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                ex = r - dr
                cases.append((ts.iloc[i].normalize(), -ex, ex, rm[i]))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)

    mean_val = None
    t_val = None
    if n_cases >= 1:
        v = np.array([x[1] for x in cases], dtype=float)
        mean_val = float(v.mean())
        if n_days >= 2:
            dev = v - v.mean()
            dser = pd.Series(dev, index=[x[0] for x in cases]).groupby(level=0).sum()
            G = len(dser)
            var = float((dser.values ** 2).sum()) * G / (G - 1) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_val / se) if se > 0 else None

    slope = None
    sl_x = np.array([x[3] for x in cases], dtype=float)
    sl_y = np.array([x[2] for x in cases], dtype=float)
    ok = np.isfinite(sl_x) & np.isfinite(sl_y)
    if ok.sum() >= 3 and np.ptp(sl_x[ok]) > 0:
        slope = float(stats.linregress(sl_x[ok], sl_y[ok]).slope)
    slope_passed = None if slope is None else bool(slope < 0)

    counts = {"cases (non-overlapping 3-bar cells)": int(n_cases), "days with cases": int(n_days),
              "cases in slope regression": int(ok.sum())}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30 non-overlapping 3-bar cells."
    elif t_val is not None and mean_val > 0 and t_val >= 2:
        if slope_passed:
            status = "confirmed"
            decided = "Mean unusual move in the short direction is positive with t >= 2 over at least 30 cases, and the slope on the range multiple is negative."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (positive, t >= 2) but the supporting slope is 0 or above (or not computable)."
    elif t_val is not None and mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move in the short direction is negative with t <= -2: wide days in falling markets are followed by rebounds against the drift."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (or could not be computed)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_val,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of 3-bar excess return on raw range multiple (must be < 0)",
                             "value": slope, "passed": slope_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
