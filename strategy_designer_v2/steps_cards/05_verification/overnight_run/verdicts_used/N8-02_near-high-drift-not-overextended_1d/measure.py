import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RH = "debug_info.components.recent_high.last_history_value"
    NH = "debug_info.components.near_high.last_history_value"
    AM = "debug_info.components.above_ma.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            if not active.any():
                continue
            if all(c in df.columns for c in (RH, NH, AM)):
                rh = pd.to_numeric(df[RH], errors="coerce")
                nh = pd.to_numeric(df[NH], errors="coerce")
                am = pd.to_numeric(df[AM], errors="coerce")
                not_veto = df["regime"].astype(str) != "chop"
                situ = (rh > 0) & (nh > 0) & (am > 0) & not_veto
                situ = situ.fillna(False)
            else:
                situ = pd.Series(False, index=df.index)
            n_agree += int((active & situ & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    reading = ("Situation read as a conjunction of the raw readings: recent high (bars-since-high > 0), close in the "
               "upper half of the 20-day range (Donchian > 0) and close above the 20-day SMA (distance > 0), on a "
               "non-vetoed bar (regime != 'chop'), long side; the coin mean 10-bar return uses all bars of all its "
               "windows (overlapping), the slope is OLS of excess return on forecast over the non-overlapping grid "
               "(positions 0,10,20,... per window) pooled over coins, vetoed bars are regime == 'chop', and the plan's "
               "minimum of 30 cases is treated as a minimum count (not observable when unmet).")

    main_name = "OLS slope of next-10-bar excess return on forecast, pooled, non-overlapping"
    thr = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"non-overlapping 10-bar cases with forecast > 0": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the high is recent, "
                           "the close is in the upper half of its range and above its 20-day average, and the bar is "
                           "not vetoed: the config's forecast is active outside the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    # coin mean 10-bar return over all windows together
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[H:] / c[:-H] - 1.0
            rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(rets)) if len(rets) else np.nan

    X, Y, VETO = [], [], []
    for coin, wins in bars.items():
        m = coin_mean.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            n = len(df)
            for i in range(0, n - H, H):
                r = c[i + H] / c[i] - 1.0
                if not (np.isfinite(r) and np.isfinite(fc[i])):
                    continue
                X.append(fc[i])
                Y.append(r - m)
                VETO.append(reg[i] == "chop")
    X = np.array(X, dtype=float)
    Y = np.array(Y, dtype=float)
    VETO = np.array(VETO, dtype=bool)

    n_pos = int((X > 0).sum())
    n_veto = int(VETO.sum())

    slope = None
    tval = None
    if len(X) >= 3 and np.var(X) > 0:
        res = stats.linregress(X, Y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    sup_val = None
    sup_pass = None
    if n_pos > 0 and n_veto > 0:
        sup_val = float(np.mean(Y[X > 0]) - np.mean(Y[VETO]))
        sup_pass = bool(sup_val > 0)

    counts = {"non-overlapping 10-bar cases with forecast > 0": n_pos,
              "non-overlapping 10-bar cases (all)": int(len(X)),
              "non-overlapping vetoed cases": n_veto}

    if n_pos < 30:
        status = "not observable"
        decided = f"Only {n_pos} non-overlapping 10-bar cases with forecast > 0, below the plan's minimum of 30."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t-statistic could not be computed, so neither confirm nor reject is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean excess 10-bar return, forecast > 0 minus vetoed bars",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
