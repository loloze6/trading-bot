import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    HEAVY_COL = "debug_info.components.heavy_up.last_history_value"
    THIN_COL = "debug_info.components.thin_up.last_history_value"

    n_active = 0
    n_agree = 0
    heavy_r, heavy_w, thin_r, thin_w = [], [], [], []
    all_next = []

    for coin, wins in bars.items():
        for wname, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)

            # Raw one-bar move from the config's component (both regimes use the same raw indicator)
            move = pd.Series(np.nan, index=df.index)
            if HEAVY_COL in df.columns:
                move = df[HEAVY_COL].astype(float)
            if THIN_COL in df.columns:
                move = move.combine_first(df[THIN_COL].astype(float))
            move = move.combine_first(close.pct_change())

            # Volume against its 20-bar mean, within the window only
            vmean = vol.rolling(20, min_periods=1).mean()
            heavy = vol >= vmean
            up = move > 0
            expected = pd.Series(0.0, index=df.index)
            expected[up & heavy] = 1.0
            expected[up & ~heavy] = -1.0

            # Situation check
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (expected != 0) & (np.sign(fc) == expected)).sum())

            # Next-bar return inside the window
            nxt = close.shift(-1) / close - 1.0
            all_next.extend(nxt.dropna().tolist())

            sel = active & up & nxt.notna()
            for i in df.index[sel]:
                w = abs(fc[i])
                if fc[i] > 0:
                    heavy_r.append(nxt[i]); heavy_w.append(w)
                else:
                    thin_r.append(nxt[i]); thin_w.append(w)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("Volume's 20-bar mean is a within-window rolling mean including the current bar (min_periods=1, since warm-up bars are absent); "
               "heavy and thin groups are the forecast-bearing up bars with long and short forecast respectively; "
               "the Welch t uses |forecast|-weighted means and weighted variances with Kish effective sample sizes; "
               "the unconditional mean is the plain mean of all next-bar returns pooled over the windows.")

    threshold = "Confirm if difference > 0 and t >= 2; reject if difference < 0 and t <= -2; else inconclusive; inconclusive if fewer than 30 up bars in either group"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "heavy-minus-thin weighted mean next-bar return",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"heavy up bars": len(heavy_r), "thin up bars": len(thin_r), "active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are up bars with long forecast on volume at/above its 20-bar mean "
                           "or short forecast on volume below it, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    def wstats(r, w):
        r = np.asarray(r, float); w = np.asarray(w, float)
        if len(r) == 0 or w.sum() <= 0:
            return None, None, None
        m = float(np.sum(w * r) / np.sum(w))
        neff = float(w.sum() ** 2 / np.sum(w ** 2))
        if neff <= 1:
            return m, None, neff
        var = float(np.sum(w * (r - m) ** 2) / np.sum(w)) * neff / (neff - 1.0)
        return m, var, neff

    mh, vh, nh = wstats(heavy_r, heavy_w)
    mt, vt, nt = wstats(thin_r, thin_w)

    diff = None
    t = None
    if mh is not None and mt is not None:
        diff = mh - mt
        if vh is not None and vt is not None:
            se2 = vh / nh + vt / nt
            if se2 > 0:
                t = float(diff / np.sqrt(se2))

    uncond = float(np.mean(all_next)) if len(all_next) else None
    sup_val = (mt - uncond) if (mt is not None and uncond is not None) else None
    sup_pass = (sup_val < 0) if sup_val is not None else None

    nh_c, nt_c = len(heavy_r), len(thin_r)
    if nh_c < 30 or nt_c < 30:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 forecast-bearing up bars in at least one group across all windows."
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic could not be computed."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm: the heavy-minus-thin difference is positive with t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: the heavy-minus-thin difference is negative with t <= -2, thin moves hold better than heavy ones."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "heavy-minus-thin |forecast|-weighted mean next-bar return",
            "value": float(diff) if diff is not None else None,
            "statistic": {"name": "Welch t", "value": float(t)} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "thin weighted mean next-bar return minus unconditional mean daily return (< 0)",
            "value": float(sup_val) if sup_val is not None else None,
            "passed": bool(sup_pass) if sup_pass is not None else None,
        },
        "counts": {"heavy up bars": int(nh_c), "thin up bars": int(nt_c)},
        "decided_by": decided,
        "reading": reading,
    }
