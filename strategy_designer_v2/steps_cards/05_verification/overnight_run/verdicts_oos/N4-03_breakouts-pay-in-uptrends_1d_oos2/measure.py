import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    HU = "debug_info.components.high_up.last_history_value"
    HD = "debug_info.components.high_down.last_history_value"

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
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.Series(np.nan, index=df.index)
            if HU in df.columns:
                raw = raw.fillna(pd.to_numeric(df[HU], errors="coerce"))
            if HD in df.columns:
                raw = raw.fillna(pd.to_numeric(df[HD], errors="coerce"))
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            active = fc.notna() & (fc != 0)
            for i in df.index[active]:
                n_active += 1
                r = raw.loc[i]
                if not np.isfinite(r) or r <= 0:
                    continue
                g = reg.loc[i]
                f = fc.loc[i]
                if (g == "trending" and f > 0) or (g == "mean_reversion" and f < 0):
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "pooled mean of sign(forecast) x (10-bar forward return - coin holding mean) on |forecast|>=10, non-overlapping"
    thr = "confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2; else inconclusive; needs >= 30 cases pooled and >= 10 per regime"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have the close in the upper half of its 20-day range with a long side in the trending (close >= 200-SMA) regime and a short side in the mean_reversion regime.",
            "reading": "The situation was checked as the raw Donchian position > 0 (upper half of the 20-day range) with the side taken from the recorded regime label, since the 200-SMA cannot be recomputed without warm-up bars.",
        }

    # ---------- 2. criterion ----------
    # holding: coin's mean 10-bar forward return over all bars of all its windows pooled
    holding = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > H:
                r = c[H:] / c[:-H] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        holding[coin] = float(np.mean(rets)) if len(rets) else np.nan

    pooled, trend, mr = [], [], []
    for coin, wins in bars.items():
        hold = holding.get(coin, np.nan)
        if not np.isfinite(hold):
            continue
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                f = fc[p]
                if not np.isfinite(f) or abs(f) < 10:
                    continue
                if not (np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0):
                    continue
                ex = c[p + H] / c[p] - 1.0 - hold
                val = float(np.sign(f) * ex)
                pooled.append(val)
                if reg[p] == "trending":
                    trend.append(val)
                elif reg[p] == "mean_reversion":
                    mr.append(val)

    n_pool, n_tr, n_mr = len(pooled), len(trend), len(mr)
    mean_pool = float(np.mean(pooled)) if n_pool else None
    t_pool = tstat(pooled)
    mean_tr = float(np.mean(trend)) if n_tr else None
    t_tr = tstat(trend)
    mean_mr = float(np.mean(mr)) if n_mr else None
    t_mr = tstat(mr)

    sup_val = None
    if t_tr is not None and t_mr is not None:
        sup_val = float(min(t_tr, t_mr))
    sup_passed = None
    if mean_tr is not None and mean_mr is not None:
        sup_passed = bool(mean_tr > 0 and mean_mr > 0)
    sup_name = ("per-regime signed excess return: trending mean=%s t=%s; mean_reversion mean=%s t=%s; value = smaller t"
                % (None if mean_tr is None else round(mean_tr, 6), None if t_tr is None else round(t_tr, 3),
                   None if mean_mr is None else round(mean_mr, 6), None if t_mr is None else round(t_mr, 3)))

    counts = {"non-overlapping cases": int(n_pool),
              "trending cases": int(n_tr),
              "mean_reversion cases": int(n_mr)}

    if n_pool < 30:
        status = "not observable"
        decided = "Fewer than 30 non-overlapping cases in the pool."
    elif n_tr < 10 or n_mr < 10:
        status = "not observable"
        decided = "Fewer than 10 non-overlapping cases in at least one regime."
    elif t_pool is not None and mean_pool > 0 and t_pool >= 2:
        status = "confirmed"
        decided = "The pooled mean signed excess return is > 0 with t >= 2 on non-overlapping cases."
    elif t_pool is not None and mean_pool < 0 and t_pool <= -2:
        status = "rejected"
        decided = "The pooled mean signed excess return is < 0 with t <= -2 on non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "The pooled t lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_pool,
                         "statistic": None if t_pool is None else {"name": "t of the mean", "value": t_pool},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": "Holding is each coin's mean of all overlapping 10-bar forward returns across its windows. Cases are the window-grid bars 0, 10, 20, ... with |forecast| >= 10 and a full 10-bar return inside the window, split by the recorded regime label. The supporting check passes when both regimes have a positive mean and is not part of the decision.",
    }
