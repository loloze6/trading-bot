import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RAW_COL = "debug_info.components.rise.last_history_value"

    def _f(x):
        try:
            v = float(x)
        except Exception:
            return np.nan
        return v

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            raw = (pd.to_numeric(df[RAW_COL], errors="coerce").to_numpy(dtype=float)
                   if RAW_COL in df.columns else np.full(len(df), np.nan))
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for i in range(n):
                if fc[i] == 0 or not np.isfinite(fc[i]):
                    continue
                n_active += 1
                # the rise: raw vol-scaled one-day return > 0; recomputed from prices where not recorded
                if np.isfinite(raw[i]):
                    rise_pos = raw[i] > 0
                elif i >= 1 and np.isfinite(close[i]) and np.isfinite(close[i - 1]) and close[i - 1] > 0:
                    rise_pos = close[i] / close[i - 1] - 1 > 0
                else:
                    rise_pos = False
                # the side: sign of the 90-bar return, from prices where 90 past bars exist in the window
                if i >= 90 and np.isfinite(close[i]) and np.isfinite(close[i - 90]) and close[i - 90] > 0:
                    side = 1 if close[i] / close[i - 90] - 1 >= 0 else -1
                else:
                    side = 1 if regime[i] == "trending" else (-1 if regime[i] == "mean_reversion" else 0)
                if rise_pos and side != 0 and np.sign(fc[i]) == side:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 5-day excess return, long cases minus short cases"
    main_thr = "confirm: difference > 0 with Welch t >= 2 and supporting check passes; reject: difference < 0 with Welch t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are up days (positive vol-scaled one-day return) with the forecast "
                          "long when the 90-bar return is >= 0 and short when it is < 0.",
            "reading": "The 90-bar return is recomputed from closes where 90 prior bars exist in the window, otherwise taken from the recorded regime.",
        }

    # ---------- 2. criterion ----------
    # normal 5-day drift per coin: non-overlapping grid of all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (side, excess, |forecast|)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            # bets
            bet = np.zeros(n, dtype=bool)
            s = 0
            ref = 0.0
            for i in range(n):
                side = int(np.sign(fc[i]))
                if side == 0:
                    s = 0
                    ref = 0.0
                    continue
                if side != s:
                    s = side
                    ref = 0.0
                mag = abs(fc[i])
                if mag - ref >= BAND:
                    bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            # once per 5-bar grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                cases.append((int(np.sign(fc[i])), (b / a - 1) - drift[coin], abs(fc[i])))

    longs = np.array([c[1] for c in cases if c[0] > 0], dtype=float)
    shorts = np.array([c[1] for c in cases if c[0] < 0], dtype=float)
    counts = {"long cases": int(len(longs)), "short cases": int(len(shorts))}

    diff = float(longs.mean() - shorts.mean()) if len(longs) and len(shorts) else None
    tval = None
    if len(longs) >= 2 and len(shorts) >= 2:
        t = stats.ttest_ind(longs, shorts, equal_var=False).statistic
        tval = float(t) if np.isfinite(t) else None

    # supporting check
    sup_val = None
    sup_pass = None
    if cases:
        mags = np.array([c[2] for c in cases], dtype=float)
        med = float(np.median(mags))
        def gap(sel):
            l = [c[1] for c, k in zip(cases, sel) if k and c[0] > 0]
            sh = [c[1] for c, k in zip(cases, sel) if k and c[0] < 0]
            if not l or not sh:
                return None
            return float(np.mean(l) - np.mean(sh))
        g_hi = gap(mags > med)
        g_lo = gap(mags <= med)
        if g_hi is not None and g_lo is not None:
            sup_val = g_hi - g_lo
            sup_pass = bool(g_hi > g_lo)
        else:
            sup_pass = False
    supporting = {"name": "larger-|forecast|-half gap minus smaller-half gap", "value": sup_val, "passed": sup_pass}

    main = {"name": main_name, "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": main_thr}
    reading = ("Cases are the first bet (forecast rise of >= 2 points on its side) in each 5-bar grid cell, grouped long/short by "
               "the bet's forecast sign; the larger half is |forecast| above the median, the smaller half at or below it; "
               "fewer than 30 cases in a group is treated as not observable.")

    if len(longs) < MIN_CASES or len(shorts) < MIN_CASES:
        status = "not observable"
        decided = "Minimum count not reached: either group has fewer than 30 cases."
    elif tval is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif diff > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The difference is positive with Welch t >= 2 and the larger-half gap exceeds the smaller-half gap."
    elif diff < 0 and tval <= -2:
        status = "rejected"
        decided = "The difference is negative with Welch t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Welch t >= 2 but the larger-half gap does not exceed the smaller-half gap."
    else:
        status = "inconclusive"
        decided = "The Welch t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
