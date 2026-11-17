import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    ALLOC = "postRebalance_current_allocation"
    RAW = "debug_info.components.fade.last_history_value"
    REG = "mean_reversion"

    # ---------- coin mean daily return over all windows (within-window returns only) ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check + collection ----------
    n_active = 0
    n_agree = 0
    main_vals = []
    down_vals = []
    up_vals = []

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            if n == 0:
                continue
            prev_ret = np.full(n, np.nan)
            if n > 1:
                prev_ret[1:] = close[1:] / close[:-1] - 1.0
            fwd = np.full(n, np.nan)
            if n > 1:
                fwd[:-1] = close[1:] / close[:-1] - 1.0
            regime = df["regime"].astype(str).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            alloc = (pd.to_numeric(df[ALLOC], errors="coerce").to_numpy(dtype=float)
                     if ALLOC in df.columns else np.full(n, np.nan))
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in df.columns else np.full(n, np.nan))

            # day's move sign: from prices, fallback to the component's raw value on a window's first bar
            move_sign = np.sign(prev_ret)
            fb = ~np.isfinite(prev_ret) & np.isfinite(raw)
            move_sign[fb] = np.sign(raw[fb])

            # situation check on active bars
            active = np.isfinite(fc) & (fc != 0)
            for i in np.where(active)[0]:
                n_active += 1
                in_sit = regime[i] == REG
                ms = move_sign[i]
                if in_sit and np.isfinite(ms) and ms != 0 and np.sign(fc[i]) == -ms:
                    n_agree += 1

            # criterion bars: regime == mean_reversion, 1-bar horizon (grid step 1 = every bar)
            sit = regime == REG
            ex = fwd - mu
            m_ok = sit & np.isfinite(alloc) & np.isfinite(ex)
            main_vals.extend((alloc[m_ok] * ex[m_ok]).tolist())

            s_ok = sit & np.isfinite(prev_ret) & np.isfinite(ex)
            rev = -np.sign(prev_ret) * ex
            down_vals.extend(rev[s_ok & (prev_ret < 0)].tolist())
            up_vals.extend(rev[s_ok & (prev_ret > 0)].tolist())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of allocation x (next-bar return - coin mean daily return) on mean_reversion bars"
    main_thr = "confirm: t >= 2 with positive mean; reject: t <= -2"
    sup_name = "down-day minus up-day mean reversal return (Welch t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(len(main_vals)),
                       "down-day bars": int(len(down_vals)),
                       "up-day bars": int(len(up_vals))},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are mean_reversion-regime bars with the "
                           "forecast opposite to the day's move, so the config does not trade the plan's situation and side."),
            "reading": "The regime part of the situation is read from the recorded `regime` column (the detector's decision) and the day's move sign from close[t]/close[t-1]-1 within the window.",
        }

    mv = np.asarray(main_vals, dtype=float)
    dv = np.asarray(down_vals, dtype=float)
    uv = np.asarray(up_vals, dtype=float)
    n_main, n_down, n_up = len(mv), len(dv), len(uv)

    main_mean = float(np.mean(mv)) if n_main else None
    main_t = None
    if n_main > 1:
        sd = float(np.std(mv, ddof=1))
        main_t = float(main_mean / (sd / np.sqrt(n_main))) if sd > 0 else 0.0

    diff = None
    welch = None
    if n_down > 1 and n_up > 1:
        diff = float(np.mean(dv) - np.mean(uv))
        tt = stats.ttest_ind(dv, uv, equal_var=False)
        welch = float(tt.statistic) if np.isfinite(tt.statistic) else 0.0

    sup_passed = None
    if diff is not None and welch is not None:
        sup_passed = bool(diff > 0 and welch >= 2)

    counts = {"active bars": int(n_main), "down-day bars": int(n_down), "up-day bars": int(n_up)}

    if n_main < 200 or n_down < 50 or n_up < 50:
        status = "not observable"
        missing = []
        if n_main < 200:
            missing.append(f"active bars {n_main} < 200")
        if n_down < 50:
            missing.append(f"down-day bars {n_down} < 50")
        if n_up < 50:
            missing.append(f"up-day bars {n_up} < 50")
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif main_t is None:
        status = "inconclusive"
        decided = "The main-measure t could not be computed."
    elif main_t <= -2:
        status = "rejected"
        decided = "Reject rule: main-measure t <= -2."
    elif main_t >= 2 and main_mean > 0:
        if sup_passed:
            status = "confirmed"
            decided = "Confirm rule: main t >= 2 with positive mean and down-minus-up difference > 0 with Welch t >= 2."
        elif welch is not None and welch <= -2:
            status = "rejected"
            decided = "Reject rule: main measure confirms but the down-minus-up Welch t <= -2 (up days reverse more)."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: main measure confirms but the down-minus-up check does not reach Welch t >= 2 with a positive difference nor t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: main-measure t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": main_mean,
            "statistic": ({"name": "ordinary t of the mean", "value": main_t} if main_t is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Active bars are the mean_reversion-regime bars with a next close in the same window and a recorded allocation, "
                    "down/up days are those with close[t]/close[t-1]-1 below/above zero inside the window (zero-return and window-first bars excluded), "
                    "the coin mean is over all within-window daily returns, and the plan's 'below minimum, inconclusive' is reported as 'not observable' per the workflow."),
    }
