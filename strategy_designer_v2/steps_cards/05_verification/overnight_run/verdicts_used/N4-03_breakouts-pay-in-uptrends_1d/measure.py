import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    COMP_IDS = ["high_up", "high_down"]

    def comp_value(df):
        # Recorded Donchian component value of whichever regime component is present on the row.
        val = pd.Series(np.nan, index=df.index, dtype=float)
        for cid in COMP_IDS:
            col = "debug_info.components.%s.last_history_value" % cid
            if col in df.columns:
                v = pd.to_numeric(df[col], errors="coerce")
                val = val.where(val.notna(), v)
        return val

    def tstat(x):
        x = np.asarray(x, dtype=float)
        n = len(x)
        if n < 2:
            return None
        sd = np.std(x, ddof=1)
        if not np.isfinite(sd) or sd == 0:
            return None
        return float(np.mean(x) / (sd / np.sqrt(n)))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            reg = df["regime"].astype(str)
            pos = comp_value(df)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            near_top = pos > 0
            long_ok = (reg == "trending") & (fc > 0)
            short_ok = (reg == "mean_reversion") & (fc < 0)
            agree = active & near_top & (long_ok | short_ok)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation taken as the recorded Donchian component value > 0 (close in the upper part of its "
               "20-day range) with side from the `regime` label (trending long, mean_reversion short) since the "
               "200-day SMA cannot be rebuilt inside the windows; holding is the coin's mean of all overlapping "
               "10-bar forward returns pooled over its windows; cases are the grid bars 0,10,20,... of each window "
               "with |forecast| >= 10; the supporting check passes when both regime sides have a positive mean.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are closes in the upper part of their 20-day "
                           "range with a long forecast in `trending` or a short one in `mean_reversion`."
                           if n_active > 0 else "No active bars in the record."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    vals, regs = [], []
    for coin, wins in bars.items():
        # holding: coin's mean 10-bar return over all its windows pooled
        all_ret = []
        frames = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            fwd = c.shift(-H) / c - 1.0
            all_ret.append(fwd.dropna().values)
            frames.append((df, fwd))
        allr = np.concatenate(all_ret) if all_ret else np.array([])
        if len(allr) == 0:
            continue
        hold = float(np.mean(allr))
        for df, fwd in frames:
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            reg = df["regime"].astype(str)
            for i in range(0, len(df), H):
                f = fc.iloc[i]
                r = fwd.iloc[i]
                if pd.isna(f) or pd.isna(r) or abs(f) < 10:
                    continue
                vals.append(float(np.sign(f) * (r - hold)))
                regs.append(reg.iloc[i])

    vals = np.array(vals, dtype=float)
    regs = np.array(regs, dtype=object)
    n_pool = int(len(vals))
    tr = vals[regs == "trending"]
    mr = vals[regs == "mean_reversion"]
    n_tr, n_mr = int(len(tr)), int(len(mr))

    mean_pool = float(np.mean(vals)) if n_pool > 0 else None
    t_pool = tstat(vals)

    tr_mean = float(np.mean(tr)) if n_tr > 0 else None
    mr_mean = float(np.mean(mr)) if n_mr > 0 else None
    t_tr = tstat(tr)
    t_mr = tstat(mr)
    sup_passed = None
    if tr_mean is not None and mr_mean is not None:
        sup_passed = bool(tr_mean > 0 and mr_mean > 0)

    counts = {"non-overlapping cases (pool)": n_pool,
              "trending cases": n_tr,
              "mean_reversion cases": n_mr}

    if n_pool < 30:
        status = "not observable"
        decided = "Fewer than 30 non-overlapping cases in the pool (%d)." % n_pool
    elif n_tr < 10 or n_mr < 10:
        status = "not observable"
        decided = "Fewer than 10 cases in a regime (trending %d, mean_reversion %d)." % (n_tr, n_mr)
    elif t_pool is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion)."
    elif mean_pool > 0 and t_pool >= 2:
        status = "confirmed"
        decided = "Pooled mean signed excess return > 0 with t >= 2 on non-overlapping cases."
    elif mean_pool < 0 and t_pool <= -2:
        status = "rejected"
        decided = "Pooled mean signed excess return < 0 with t <= -2 on non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "Pooled t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled mean signed 10-bar excess return over holding, |forecast| >= 10",
            "value": mean_pool,
            "statistic": {"name": "t of the mean", "value": t_pool} if t_pool is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "per-regime signed excess return (trending mean %s t %s; mean_reversion mean %s t %s)" % (
                tr_mean, t_tr, mr_mean, t_mr),
            "value": t_tr if t_tr is not None else None,
            "passed": sup_passed,
            "trending": {"mean": tr_mean, "sign": (None if tr_mean is None else float(np.sign(tr_mean))),
                         "t": t_tr},
            "mean_reversion": {"mean": mr_mean, "sign": (None if mr_mean is None else float(np.sign(mr_mean))),
                               "t": t_mr},
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
