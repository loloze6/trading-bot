import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    MIN_CASES = 30
    COMP = "decline"

    def _comp_value(df, comp_id, field):
        flat = f"debug_info.components.{comp_id}.{field}"
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            col = df["debug_info.components"].tolist()
            for i, v in enumerate(col):
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(comp_id)
                    if isinstance(c, str):
                        try:
                            c = json.loads(c)
                        except Exception:
                            c = None
                    if isinstance(c, dict):
                        try:
                            x = c.get(field)
                            out[i] = float(x) if x is not None else np.nan
                        except Exception:
                            out[i] = np.nan
        return out

    def _r30_closes(close):
        n = len(close)
        r = np.full(n, np.nan)
        if n > 30:
            r[30:] = close[30:] / close[:-30] - 1.0
        return r

    # ---------- prepare windows ----------
    prepared = []
    drift_rets = {}
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True) if "timestamp" in df.columns else df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            r30_rec = _comp_value(df, COMP, "last_history_value")
            r30_cl = _r30_closes(close)
            prepared.append((coin, w, close, fc, regime, r30_rec, r30_cl))
            dr = close[1:] / close[:-1] - 1.0
            drift_rets.setdefault(coin, []).append(dr[np.isfinite(dr)])

    drift = {}
    for coin, lst in drift_rets.items():
        allr = np.concatenate(lst) if lst else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, w, close, fc, regime, r30_rec, r30_cl in prepared:
        active = np.isfinite(fc) & (fc != 0)
        r30 = np.where(np.isfinite(r30_rec), r30_rec, r30_cl)
        sit = (regime == "mean_reversion") & np.isfinite(r30) & (r30 < 0)
        ok = active & sit & (fc < 0)
        n_active += int(active.sum())
        n_agree += int(ok.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9) if n_active > 0 else True

    main_name = "t of the mean excess fall of the short over 10 days, cut at the first day the 30-day return is >= 0, minus the coin's daily drift"
    threshold = "confirm: mean > 0 with t >= 2 and deeper-minus-shallower > 0; reject: mean < 0 with t <= -2; at least 30 cases"
    reading = ("The situation is taken as regime == 'mean_reversion' (the detector's recorded decision on the break, the >=3 touch count and the falling month, whose components are not recorded) "
               "plus a negative 30-day return (recorded 'decline' raw value, else recomputed from closes) with a short forecast; "
               "a case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet) in each 10-bar grid cell of a window with all 10 following bars in the window; "
               "the stop day's return is included, the 30-day return on each day is recomputed from the window's closes (falling back to the recorded value when 30 past bars are not in the window, and not stopping when neither exists); "
               "drift is the coin's mean daily return over all its windows times the days counted; "
               "the depth split uses the recorded 30-day return on the signal bar, deeper = strictly below the median.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": (f"Only {agreement:.1%} of the active bars are short bars in the plan's situation "
                           "(fresh break of a swing-high level with >=3 turns while the 30-day return is negative), below 90 %."),
            "reading": reading,
        }

    # ---------- cases ----------
    excess = []
    depth = []
    for coin, w, close, fc, regime, r30_rec, r30_cl in prepared:
        n = len(close)
        mu = drift.get(coin, np.nan)
        ref = 0.0
        bet = np.zeros(n, dtype=bool)
        for i in range(n):
            f = fc[i]
            if not np.isfinite(f) or f >= 0:
                ref = 0.0
                continue
            m = -f
            if m - ref >= BAND:
                bet[i] = True
                ref = m
            else:
                ref = min(ref, m)
        for start in range(0, n, H):
            idx = np.where(bet[start:start + H])[0]
            if len(idx) == 0:
                continue
            t = start + int(idx[0])
            if t + H >= n or not np.isfinite(close[t]) or not np.isfinite(mu):
                continue
            K = H
            for k in range(1, H + 1):
                j = t + k
                v = r30_cl[j]
                if not np.isfinite(v):
                    v = r30_rec[j]
                if np.isfinite(v) and v >= 0:
                    K = k
                    break
            if not np.isfinite(close[t + K]):
                continue
            ret = close[t + K] / close[t] - 1.0
            ex = -(ret - mu * K)
            excess.append(ex)
            depth.append(r30_rec[t])

    excess = np.array(excess, dtype=float)
    depth = np.array(depth, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            tstat = float(mean_ex / (sd / np.sqrt(n_cases)))

    diff = None
    n_deep = n_shallow = 0
    okd = np.isfinite(depth)
    if okd.sum() >= 2:
        med = float(np.median(depth[okd]))
        deep = excess[okd][depth[okd] < med]
        shal = excess[okd][depth[okd] >= med]
        n_deep, n_shallow = int(len(deep)), int(len(shal))
        if n_deep > 0 and n_shallow > 0:
            diff = float(np.mean(deep) - np.mean(shal))
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"cases": n_cases, "deeper_half": n_deep, "shallower_half": n_shallow}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, below the plan's minimum of 30."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean excess fall could not be computed (zero spread), so neither rule is met."
    elif mean_ex > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean excess fall is positive with t >= 2 and the deeper-minus-shallower difference is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the deeper-minus-shallower depth check failed, which the plan calls inconclusive."
    elif mean_ex < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean excess fall is negative with t <= -2: the coin rises after these breaks more than its drift."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess fall lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "deeper-half minus shallower-half mean excess fall (split at median 30-day return)",
            "value": diff,
            "passed": (bool(sup_pass) if sup_pass is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
