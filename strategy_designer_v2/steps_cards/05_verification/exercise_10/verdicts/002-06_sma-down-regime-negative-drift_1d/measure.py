import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    def find_raw_col(df):
        cols = [c for c in df.columns
                if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        pref = [c for c in cols if ".sma_spread." in c]
        if pref:
            return pref[0]
        return cols[0] if cols else None

    act_total = 0
    act_agree = 0
    rows = []      # (excess placeholder later) next return, |forecast|, is_active
    all_rets = []
    n_stretches = 0

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: int(str(w).lstrip("w")) if str(w).lstrip("w").isdigit() else str(w)):
            df = bars[coin][win].reset_index(drop=True)
            raw_col = find_raw_col(df)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            raw = (pd.to_numeric(df[raw_col], errors="coerce").values.astype(float)
                   if raw_col is not None else np.full(len(df), np.nan))

            # situation check: active bars (forecast != 0) should be bars with SMA50 < SMA200, short side
            active = np.isfinite(fc) & (fc != 0)
            situ = np.isfinite(raw) & (raw < 0)
            act_total += int(active.sum())
            act_agree += int((active & situ & (fc < 0)).sum())

            # down-cross stretches: runs of consecutive bars with SMA50 below SMA200 in this window
            prev = False
            for s in situ:
                if s and not prev:
                    n_stretches += 1
                prev = bool(s)

            # next-bar returns inside the window only
            n = len(df)
            for t in range(n - 1):
                if not (np.isfinite(close[t]) and np.isfinite(close[t + 1]) and close[t] != 0):
                    continue
                r = close[t + 1] / close[t] - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    rows.append((r, abs(fc[t])))

    agreement = act_agree / act_total if act_total > 0 else 0.0
    passed_check = act_total > 0 and agreement >= 0.9

    main_name = "|forecast|-weighted mean of next-bar return minus coin mean bar return, on forecast<0 bars"
    threshold = "confirm if negative with t <= -2; reject if positive with t >= +2; otherwise inconclusive"
    reading = ("The coin's mean bar return is the mean next-bar return over all tested bars pooled across the 6 windows; "
               "the t of the weighted mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w); "
               "active bars are forecast<0 bars with a valid next return; down-cross stretches are runs of consecutive bars "
               "with the raw 50/200 SMA spread below 0 within a window; the raw spread is read from the record's only "
               "component column (sma_cross_down) since the config's id sma_spread is absent; the supporting check passes "
               "when the binomial z of the down-bar share (active minus all) is above 0.")

    if not passed_check:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(act_total), "down-cross stretches": int(n_stretches)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars where the 50-day SMA is "
                           "below the 200-day SMA, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    all_rets = np.asarray(all_rets, dtype=float)
    mu_all = float(all_rets.mean()) if len(all_rets) else np.nan
    r_act = np.array([x[0] for x in rows], dtype=float)
    w = np.array([x[1] for x in rows], dtype=float)
    n_act = len(r_act)

    value = None
    tstat = None
    if n_act >= 2 and w.sum() > 0:
        x = r_act - mu_all
        m = float(np.sum(w * x) / np.sum(w))
        se = np.sqrt(n_act / (n_act - 1.0) * np.sum(w ** 2 * (x - m) ** 2)) / np.sum(w)
        value = m
        tstat = float(m / se) if se > 0 else None

    # supporting check: share of down bars, active vs all, binomial z
    z = None
    sup_passed = None
    if n_act > 0 and len(all_rets) > 0:
        p_all = float(np.mean(all_rets < 0))
        p_act = float(np.mean(r_act < 0))
        if 0 < p_all < 1:
            z = float((p_act - p_all) / np.sqrt(p_all * (1 - p_all) / n_act))
            sup_passed = bool(z > 0)

    counts = {"active bars": int(n_act), "down-cross stretches": int(n_stretches)}

    if n_act < 100 or n_stretches < 2:
        status = "not observable"
        if n_act < 100:
            decided = f"Only {n_act} active bars, fewer than the plan's minimum of 100."
        else:
            decided = f"Only {n_stretches} separate down-cross stretches, fewer than the plan's minimum of 2."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif value < 0 and tstat <= -2:
        status = "confirmed"
        decided = "The weighted excess return is negative with t <= -2, meeting the confirm rule."
    elif value > 0 and tstat >= 2:
        status = "rejected"
        decided = "The weighted excess return is positive with t >= +2, meeting the reject rule."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and +2, meeting the inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if value is None else float(value),
            "statistic": None if tstat is None else {"name": "t of weighted mean", "value": float(tstat)},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "down-bar share on active bars vs all bars (binomial z)",
            "value": z,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
