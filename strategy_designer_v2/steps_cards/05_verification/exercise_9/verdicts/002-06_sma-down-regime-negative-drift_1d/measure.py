import numpy as np
import pandas as pd


def measure(bars):
    reading = ("The plan's component id 'sma_spread' is read from whichever "
               "'debug_info.components.*.last_history_value' column the record holds (here 'sma_cross_down'), "
               "and the situation is a raw spread below 0 with a negative forecast; "
               "the coin's mean bar return is pooled over all bars of all windows; "
               "the t of the weighted mean uses the weighted standard deviation over the Kish effective sample size; "
               "a down bar is a negative next-bar return; "
               "the supporting check passes when z >= 2, since the plan gives no threshold of its own; "
               "a separate down-cross stretch is a run, within one window, of consecutive bars with raw spread < 0 "
               "that holds at least one active bar; "
               "missing a minimum count gives 'not observable', as the instructions require.")

    def find_col(df):
        cols = [c for c in df.columns
                if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        pref = [c for c in cols if ".sma_spread." in c]
        if pref:
            return pref[0]
        return cols[0] if cols else None

    # ---------- Gather per-window data ----------
    n_active_total = 0
    n_agree = 0
    all_rets = []
    act_rets, act_w = [], []
    n_stretches = 0

    for coin, wins in bars.items():
        for wname, df in wins.items():
            df = df.reset_index(drop=True)
            col = find_col(df)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
            if col is not None:
                spread = pd.to_numeric(df[col], errors="coerce").astype(float)
            else:
                spread = pd.Series(np.nan, index=df.index)

            # Situation check
            m_act = fc.notna() & (fc != 0) & spread.notna()
            n_active_total += int(m_act.sum())
            n_agree += int((m_act & (spread < 0) & (fc < 0)).sum())

            # Next-bar return within this window
            nxt = close.shift(-1) / close - 1.0
            valid = nxt.notna() & np.isfinite(nxt)
            all_rets.extend(nxt[valid].tolist())

            m_short = valid & fc.notna() & (fc < 0)
            act_rets.extend(nxt[m_short].tolist())
            act_w.extend(fc[m_short].abs().tolist())

            # Down-cross stretches: runs of spread < 0 that hold an active bar
            below = (spread < 0).fillna(False).values
            act_arr = m_short.values
            i, n = 0, len(below)
            while i < n:
                if below[i]:
                    j = i
                    has_act = False
                    while j < n and below[j]:
                        if act_arr[j]:
                            has_act = True
                        j += 1
                    if has_act:
                        n_stretches += 1
                    i = j
                else:
                    i += 1

    agreement = (n_agree / n_active_total) if n_active_total > 0 else 0.0
    passed_sit = bool(n_active_total > 0 and agreement >= 0.9)

    threshold_txt = ("confirm if weighted excess return < 0 with t <= -2; "
                     "reject if > 0 with t >= +2; otherwise inconclusive")
    main_name = "|forecast|-weighted next-bar return minus coin mean, on short bars"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_total),
                       "down-cross stretches": int(n_stretches)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with the 50-day SMA "
                           "under the 200-day SMA: the forecast is active outside the plan's down-cross "
                           "situation or on the wrong side."),
            "reading": reading,
        }

    # ---------- Main measure ----------
    all_rets = np.asarray(all_rets, dtype=float)
    r = np.asarray(act_rets, dtype=float)
    w = np.asarray(act_w, dtype=float)
    mu_all = float(all_rets.mean()) if len(all_rets) else np.nan
    n_act = int(len(r))

    value, tstat = None, None
    if n_act >= 2 and w.sum() > 0 and np.isfinite(mu_all):
        x = r - mu_all
        sw = w.sum()
        wm = float(np.sum(w * x) / sw)
        n_eff = sw ** 2 / np.sum(w ** 2)
        var_w = np.sum(w * (x - wm) ** 2) / sw
        if n_eff > 1:
            var_w = var_w * n_eff / (n_eff - 1)
        se = np.sqrt(var_w / n_eff)
        value = wm
        tstat = float(wm / se) if se > 0 else None

    # ---------- Supporting check ----------
    z = None
    sup_passed = None
    if n_act > 0 and len(all_rets) > 0:
        p_all = float(np.mean(all_rets < 0))
        p_act = float(np.mean(r < 0))
        if 0 < p_all < 1:
            z = float((p_act - p_all) / np.sqrt(p_all * (1 - p_all) / n_act))
            sup_passed = bool(z >= 2)

    counts = {"active bars": n_act, "down-cross stretches": int(n_stretches)}

    # ---------- Decision ----------
    if n_act < 100:
        status = "not observable"
        decided = f"Fewer than 100 active bars ({n_act}) across the windows."
    elif n_stretches < 2:
        status = "not observable"
        decided = f"Fewer than 2 separate down-cross stretches ({n_stretches}) across the windows."
    elif value is None or tstat is None:
        status = "inconclusive"
        decided = "The weighted t-statistic could not be computed, so neither confirm nor reject is met."
    elif value < 0 and tstat <= -2:
        status = "confirmed"
        decided = "The weighted excess return is negative with t <= -2 (confirm rule)."
    elif value > 0 and tstat >= 2:
        status = "rejected"
        decided = "The weighted excess return is positive with t >= +2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if value is None else float(value),
            "statistic": None if tstat is None else {"name": "t of weighted mean", "value": float(tstat)},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "down-bar share on active vs all bars (binomial z)",
            "value": z,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
