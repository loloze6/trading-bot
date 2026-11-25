import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.vs_fall.last_history_value"
    H = 1
    FC_CUT = 5.0
    VOL_WIN = 60

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            price_ret = close / close.shift(1) - 1.0  # inside the window only
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: a one-day fall (vol-scaled 1-day return < 0); fall back to price return where not recorded
            fall_val = raw.where(raw.notna(), price_ret)
            situation = fall_val < 0
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean next-bar excess return (vs coin's all-window mean daily return) on bars with forecast >= 5"
    thr = "confirm: mean > 0 with ordinary t >= 2 and high-vol minus low-vol > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation bars are those where the recorded vol-scaled 1-day return (price return where unrecorded) is "
               "below 0, long side; the 60-day std is recomputed within each window (60 returns, min 60, missing earlier), "
               "the high-volatility half is std > pooled median of cases with a std and the low half is std <= median, "
               "and the plan's minimum counts not reached give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are one-day falls with a long forecast, "
                           "so the config does not do what the plan's Fidelity says (long-only after falls)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        all_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            daily = close / close.shift(1) - 1.0
            vol = daily.rolling(VOL_WIN, min_periods=VOL_WIN).std()
            all_rets.append(fwd.dropna().values)
            # grid of h=1: every bar of the window
            grid = np.arange(0, len(df), H)
            sel = pd.Series(False, index=df.index)
            sel.iloc[grid] = True
            m = sel & (fc >= FC_CUT) & fwd.notna()
            for i in df.index[m]:
                coin_cases.append((float(fwd.iloc[i]), float(vol.iloc[i]) if pd.notna(vol.iloc[i]) else np.nan))
        if len(all_rets):
            allr = np.concatenate(all_rets) if len(all_rets) else np.array([])
            allr = allr[np.isfinite(allr)]
            coin_mean = float(allr.mean()) if allr.size else np.nan
        else:
            coin_mean = np.nan
        for r, v in coin_cases:
            if np.isfinite(coin_mean):
                case_rows.append((r - coin_mean, v))

    ex = np.array([c[0] for c in case_rows], dtype=float)
    vols = np.array([c[1] for c in case_rows], dtype=float)
    n = int(ex.size)

    mean_ex = float(ex.mean()) if n > 0 else None
    if n > 1:
        sd = float(ex.std(ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        t = None

    okv = np.isfinite(vols)
    ex_v = ex[okv]
    vv = vols[okv]
    if vv.size > 0:
        med = float(np.median(vv))
        hi = ex_v[vv > med]
        lo = ex_v[vv <= med]
    else:
        hi = np.array([])
        lo = np.array([])
    n_hi, n_lo = int(hi.size), int(lo.size)
    diff = float(hi.mean() - lo.mean()) if (n_hi > 0 and n_lo > 0) else None
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {
        "cases with forecast >= 5": n,
        "high-volatility half cases": n_hi,
        "low-volatility half cases": n_lo,
    }

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases with forecast >= 5, below the plan's minimum of 100."
    elif n_hi < 30 or n_lo < 30:
        status = "not observable"
        decided = f"A volatility half has fewer than 30 cases (high {n_hi}, low {n_lo}), below the plan's minimum."
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_ex > 0 and t >= 2:
        if diff is not None and diff > 0:
            status = "confirmed"
            decided = "Mean excess > 0 with t >= 2 and high-vol minus low-vol difference > 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the high-volatility minus low-volatility difference is <= 0 (inconclusive rule)."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess < 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t is None else {"name": f"ordinary t of the mean (n={n})", "value": t},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean excess high-vol half minus low-vol half (split at pooled median 60-day std)",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
