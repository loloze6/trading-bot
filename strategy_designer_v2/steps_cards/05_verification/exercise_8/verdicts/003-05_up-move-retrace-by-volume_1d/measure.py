import numpy as np
import pandas as pd


def measure(bars):
    MOVE_COLS = ["debug_info.components.heavy_up.last_history_value",
                 "debug_info.components.thin_up.last_history_value"]

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    rows = []      # (group, weight, next_ret)
    all_next = []  # unconditional next-bar returns

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            move = pd.Series(np.nan, index=df.index)
            for c in MOVE_COLS:
                if c in df.columns:
                    move = move.fillna(pd.to_numeric(df[c], errors="coerce"))
            move = move.fillna(close.pct_change())

            vmean = vol.rolling(20, min_periods=20).mean()
            nxt = close.shift(-1) / close - 1.0

            for i in range(len(df)):
                f = fc.iloc[i]
                if pd.notna(nxt.iloc[i]):
                    all_next.append(float(nxt.iloc[i]))
                if pd.isna(f) or f == 0:
                    continue
                n_active += 1
                m = move.iloc[i]
                up = pd.notna(m) and m > 0
                if up:
                    if pd.notna(vmean.iloc[i]) and pd.notna(vol.iloc[i]):
                        heavy = vol.iloc[i] >= vmean.iloc[i]
                        expected = 1 if heavy else -1
                        if np.sign(f) == expected:
                            n_agree += 1
                    else:
                        # volume mean not computable inside the window: only the up-bar condition can be checked
                        n_agree += 1
                if up and pd.notna(nxt.iloc[i]):
                    grp = "heavy" if f > 0 else "thin"
                    rows.append((grp, abs(float(f)), float(nxt.iloc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Heavy versus thin is the bar's volume at or above its 20-bar rolling mean including the bar, computed inside "
               "each window (bars without 20 bars of volume history are checked only for being up bars); in the measure, "
               "the groups are forecast-bearing up bars split by forecast sign (long = heavy, short = thin), weighted by "
               "|forecast|, and the Welch t uses weighted variances with Kish effective sample sizes; the unconditional "
               "mean is the plain mean of all next-bar returns in the windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "weighted next-bar return, heavy minus thin up bars", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are up bars with long on heavy volume and short on thin volume, "
                           "as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    def wstats(sel):
        if not sel:
            return np.nan, np.nan, 0.0
        wt = np.array([s[1] for s in sel]); r = np.array([s[2] for s in sel])
        sw = wt.sum()
        if sw <= 0:
            return np.nan, np.nan, 0.0
        mu = (wt * r).sum() / sw
        neff = sw ** 2 / (wt ** 2).sum()
        if neff <= 1:
            return mu, np.nan, neff
        var = (wt * (r - mu) ** 2).sum() / sw * neff / (neff - 1)
        return mu, var, neff

    heavy = [r for r in rows if r[0] == "heavy"]
    thin = [r for r in rows if r[0] == "thin"]
    mh, vh, nh = wstats(heavy)
    mt, vt, nt = wstats(thin)

    diff = mh - mt if (np.isfinite(mh) and np.isfinite(mt)) else np.nan
    t = np.nan
    if np.isfinite(diff) and np.isfinite(vh) and np.isfinite(vt):
        se = np.sqrt(vh / nh + vt / nt)
        if se > 0:
            t = diff / se

    uncond = float(np.mean(all_next)) if all_next else np.nan
    sup_val = mt - uncond if (np.isfinite(mt) and np.isfinite(uncond)) else np.nan
    sup_pass = None if not np.isfinite(sup_val) else bool(sup_val < 0)

    n_heavy, n_thin = len(heavy), len(thin)
    if n_heavy < 30 or n_thin < 30:
        status = "inconclusive"
        decided = "Fewer than 30 forecast-bearing up bars fall in at least one group across all windows, so the test is inconclusive."
    elif not np.isfinite(t):
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so no confirm or reject rule is met."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "The heavy-minus-thin difference is positive with t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The heavy-minus-thin difference is negative with t <= -2, so thin moves hold better than heavy ones."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, so the test is inconclusive."

    def num(x):
        return float(x) if x is not None and np.isfinite(x) else None

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "|forecast|-weighted next-bar return, heavy minus thin up bars",
            "value": num(diff),
            "statistic": {"name": "Welch t", "value": num(t)} if np.isfinite(t) else None,
            "threshold": "confirm if difference > 0 and t >= 2; reject if difference < 0 and t <= -2; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "weighted thin-up next-bar return minus unconditional mean daily return",
            "value": num(sup_val),
            "passed": sup_pass,
        },
        "counts": {"heavy_up_bars": int(n_heavy), "thin_up_bars": int(n_thin)},
        "decided_by": decided,
        "reading": reading,
    }
