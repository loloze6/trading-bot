import numpy as np
import pandas as pd


def measure(bars):
    def find_raw_col(df):
        cols = [c for c in df.columns
                if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        for c in cols:
            if ".sma_spread." in c:
                return c
        return cols[0] if cols else None

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            raw_col = find_raw_col(df)
            if raw_col is None or "forecast" not in df.columns:
                continue
            sub = df[["forecast", raw_col]].dropna()
            act = sub["forecast"] != 0
            n_active += int(act.sum())
            n_agree += int(((sub[raw_col] < 0) & (sub["forecast"] < 0) & act).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "|forecast|-weighted mean next-bar return minus coin mean, on bars with forecast < 0"
    threshold = "confirm if negative with t <= -2; reject if positive with t >= +2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a short only while the 50-day SMA is below the 200-day SMA, "
                           "but fewer than 90% of the non-zero forecasts are negative on bars with a negative SMA spread."),
            "reading": "Situation taken as raw SMA spread (last_history_value) < 0 with forecast < 0.",
        }

    # ---------- 2. Criterion ----------
    all_rets = []
    act_rets = []
    act_wts = []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            raw_col = find_raw_col(df)
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0
            fc = d["forecast"].astype(float)
            valid = nxt.notna()
            all_rets.extend(nxt[valid].tolist())
            m = valid & fc.notna() & (fc < 0)
            act_rets.extend(nxt[m].tolist())
            act_wts.extend(fc[m].abs().tolist())
            # down-cross stretches: runs of raw spread < 0 inside the window holding an active bar
            raw = d[raw_col].astype(float)
            below = (raw < 0).fillna(False).values
            active = (fc < 0).fillna(False).values
            i = 0
            L = len(below)
            while i < L:
                if below[i]:
                    j = i
                    has_act = False
                    while j < L and below[j]:
                        has_act = has_act or bool(active[j])
                        j += 1
                    if has_act:
                        n_stretches += 1
                    i = j
                else:
                    i += 1

    all_rets = np.asarray(all_rets, dtype=float)
    x = np.asarray(act_rets, dtype=float)
    wts = np.asarray(act_wts, dtype=float)
    n_act = int(len(x))
    coin_mean = float(all_rets.mean()) if len(all_rets) else np.nan

    value = None
    t_val = None
    if n_act >= 2 and wts.sum() > 0:
        ex = x - coin_mean
        sw = wts.sum()
        mw = float((wts * ex).sum() / sw)
        se = np.sqrt((wts ** 2 * (ex - mw) ** 2).sum()) / sw * np.sqrt(n_act / (n_act - 1))
        value = mw
        t_val = float(mw / se) if se > 0 else None

    # supporting check: share of down bars, active vs all, binomial z
    z = None
    sup_pass = None
    if n_act > 0 and len(all_rets) > 0:
        p_all = float((all_rets < 0).mean())
        p_act = float((x < 0).mean())
        if 0 < p_all < 1:
            z = float((p_act - p_all) / np.sqrt(p_all * (1 - p_all) / n_act))
            sup_pass = bool(z >= 2)

    if n_act < 100 or n_stretches < 2:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 100 active bars or fewer than 2 separate down-cross stretches across the windows."
    elif t_val is None:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic could not be computed."
    elif value < 0 and t_val <= -2:
        status = "confirmed"
        decided = "Confirm: the weighted excess return is negative with t <= -2."
    elif value > 0 and t_val >= 2:
        status = "rejected"
        decided = "Reject: the weighted excess return is positive with t >= +2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t lies strictly between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": value,
                         "statistic": ({"name": "t of weighted mean (sandwich SE)", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "binomial z, share of down next bars, active minus all",
                             "value": z, "passed": sup_pass},
        "counts": {"active bars": n_act, "down-cross stretches": int(n_stretches)},
        "decided_by": decided,
        "reading": ("Coin mean is the mean next-bar return pooled over all bars of all windows; the weighted t uses "
                    "SE = sqrt(sum w^2 (x-m)^2)/sum w * sqrt(n/(n-1)); a stretch is a run of raw SMA spread < 0 inside "
                    "a window containing at least one forecast < 0 bar; a down bar is a negative next-bar return, and "
                    "the supporting check passes at z >= 2."),
    }
