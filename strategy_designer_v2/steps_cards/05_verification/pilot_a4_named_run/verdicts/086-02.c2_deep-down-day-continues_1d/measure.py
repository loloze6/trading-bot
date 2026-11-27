import numpy as np
import pandas as pd


def _component_raw(df, cid):
    col = f"debug_info.components.{cid}.last_history_value"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(x):
            try:
                if isinstance(x, dict):
                    v = x.get(cid, {})
                    if isinstance(v, dict):
                        return v.get("last_history_value", np.nan)
            except Exception:
                pass
            return np.nan
        return pd.to_numeric(df["debug_info.components"].map(get), errors="coerce")
    return pd.Series(np.nan, index=df.index)


def _short_bets(fc):
    # bet on the short side: a rise of |forecast| on the short side of >= 2 points,
    # measured from its lowest level on that side since the last bet (0 after flat/side change)
    m = np.where(fc < 0, -fc, 0.0)
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    for i, v in enumerate(m):
        if not np.isfinite(v) or v <= 0:
            ref = 0.0
            continue
        if v - ref >= 2.0 - 1e-12:
            bets[i] = True
            ref = v
        else:
            ref = min(ref, v)
    return bets


def measure(bars):
    H = 10
    total_active = 0
    agree = 0
    cases = []  # (day, unusual, absfc)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        prepared = []
        grid_rets = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w].reset_index(drop=True).copy()
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            regime = df["regime"].astype(str).to_numpy()
            raw = _component_raw(df, "scaled_fall").to_numpy(dtype=float)
            ret1 = pd.Series(close).pct_change().to_numpy()
            down = np.where(np.isfinite(raw), raw < 0, np.where(np.isfinite(ret1), ret1 < 0, False))
            profile = regime == "unknown"
            active = fc != 0
            situation = profile & down & (fc < 0)
            total_active += int(active.sum())
            agree += int((active & situation).sum())

            n = len(close)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1)
            prepared.append((close, fc, ts))

        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        for close, fc, ts in prepared:
            bets = _short_bets(fc)
            n = len(close)
            for start in range(0, n, H):
                idx = np.where(bets[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + idx[0]
                if t + H >= n or not np.isfinite(drift):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1
                u = -(r - drift)
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), u, abs(fc[t])))

    agreement = agree / total_active if total_active > 0 else 0.0
    passed = total_active > 0 and agreement >= 0.9
    threshold = "t >= +2 confirms (with deeper-minus-shallower > 0); t <= -2 rejects; fewer than 30 distinct case days is not observable"
    reading = ("Profile taken as the recorded regime 'unknown' (not vetoed to chop), down day as the scaled_fall raw value < 0; "
               "a case is the first short bet in each 10-bar grid cell of its window, the t clusters cases by UTC day with a D/(D-1) correction, "
               "and the median split puts cases strictly above the median of |forecast| in the deeper half, at or below in the shallower.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(total_active)},
            "decided_by": "Fewer than 90% of active bars are down days inside the rising agitated profile with a short forecast.",
            "reading": reading,
        }

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct case days": int(n_days)}

    mean_u = None
    tval = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases], dtype=float)
        mean_u = float(u.mean())
        if n_days >= 2:
            dev = pd.Series(u - mean_u, index=[c[0] for c in cases]).groupby(level=0).sum().to_numpy()
            se = np.sqrt(np.sum(dev ** 2) * n_days / (n_days - 1)) / n_cases
            tval = float(mean_u / se) if se > 0 else None

    diff = None
    if n_cases > 0:
        a = np.array([c[2] for c in cases], dtype=float)
        u = np.array([c[1] for c in cases], dtype=float)
        med = np.median(a)
        deep = u[a > med]
        shal = u[a <= med]
        if len(deep) > 0 and len(shal) > 0:
            diff = float(deep.mean() - shal.mean())
    sup_pass = (diff > 0) if diff is not None else False

    main = {
        "name": "mean unusual 10-bar move in the short direction over the cases",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases summed per day", "value": tval} if tval is not None else None,
        "threshold": threshold,
    }
    support = {"name": "deeper half minus shallower half mean unusual move", "value": diff, "passed": bool(sup_pass)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main t is at least +2 and the deeper-minus-shallower difference is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The main t is at most -2: the coin rises more than its normal drift after the signals."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The main t is at least +2 but the deeper-minus-shallower difference is not above 0."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
