import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.sma_cross.last_history_value"
    LAGS = 10

    # ---------- gather per-window data ----------
    segments = []  # one entry per (coin, window)
    act_total = 0
    act_agree = 0
    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp") if "timestamp" in df.columns else df
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in df.columns else np.full(len(df), np.nan))

            # situation check: active bars (forecast != 0) should be bars with
            # 50-SMA above 200-SMA (raw spread > 0) and forecast > 0 (long)
            act = np.isfinite(fc) & (fc != 0)
            act_total += int(act.sum())
            act_agree += int((act & np.isfinite(raw) & (raw > 0) & (fc > 0)).sum())

            # next-bar return inside the window
            nxt = np.full(len(close), np.nan)
            if len(close) > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            valid = np.isfinite(nxt) & np.isfinite(fc)
            r = nxt[valid]
            ind = (fc[valid] > 0)

            # distinct spans: maximal runs of forecast > 0 within the window
            pos = np.isfinite(fc) & (fc > 0)
            n_spans = int(np.sum(pos & ~np.concatenate([[False], pos[:-1]])))

            segments.append({"coin": coin, "r": r, "ind": ind, "spans": n_spans})

    agreement = (act_agree / act_total) if act_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    if act_total > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(act_total)},
            "decided_by": ("The plan's situation is 'long while the 50-day SMA is above the 200-day SMA', "
                           "but fewer than 90% of the bars with a non-zero forecast have a positive raw SMA "
                           "spread and a positive forecast."),
            "reading": "Situation taken as raw sma_cross last_history_value > 0 with forecast > 0 on every bar where forecast != 0.",
        }

    # ---------- main measure ----------
    r_all = np.concatenate([s["r"] for s in segments]) if segments else np.array([])
    i_all = np.concatenate([s["ind"] for s in segments]) if segments else np.array([], dtype=bool)
    N = int(len(r_all))
    n1 = int(i_all.sum())
    n_spans = int(sum(s["spans"] for s in segments))

    excess = None
    t_nw = None
    if N > 1 and n1 > 1:
        m_all = float(r_all.mean())
        m_in = float(r_all[i_all].mean())
        excess = m_in - m_all
        p = n1 / N
        # influence function of (mean_in - mean_all)
        gamma = np.zeros(LAGS + 1)
        for s in segments:
            r, ind = s["r"], s["ind"]
            if len(r) == 0:
                continue
            psi = ind * (r - m_in) / p - (r - m_all)
            for j in range(LAGS + 1):
                if j < len(psi):
                    gamma[j] += float(np.sum(psi[j:] * psi[:len(psi) - j]))
        gamma /= N
        lrv = gamma[0] + 2.0 * sum((1.0 - j / (LAGS + 1.0)) * gamma[j] for j in range(1, LAGS + 1))
        if lrv > 0:
            se = np.sqrt(lrv / N)
            t_nw = float(excess / se)

    # ---------- supporting check ----------
    k_up = 0
    exp_up = 0.0
    var_up = 0.0
    coins = sorted(set(s["coin"] for s in segments))
    for c in coins:
        rc = np.concatenate([s["r"] for s in segments if s["coin"] == c])
        ic = np.concatenate([s["ind"] for s in segments if s["coin"] == c])
        if len(rc) == 0:
            continue
        p0 = float(np.mean(rc > 0))
        n1c = int(ic.sum())
        k_up += int(np.sum(rc[ic] > 0))
        exp_up += n1c * p0
        var_up += n1c * p0 * (1.0 - p0)
    z = None
    share_diff = None
    if n1 > 0:
        share_diff = (k_up - exp_up) / n1
        if var_up > 0:
            z = float((k_up - exp_up) / np.sqrt(var_up))
    sup_passed = None if z is None else bool(z >= 2.0 and share_diff > 0)

    # ---------- decision ----------
    enough = (n_spans >= 30) and (n1 >= 1000)
    if not enough:
        status = "inconclusive"
        decided = "Fewer than 30 distinct up-cross spans or fewer than 1000 bars with a positive forecast, so the plan calls it inconclusive."
    elif excess is None or t_nw is None:
        status = "inconclusive"
        decided = "The excess return or its Newey-West t could not be computed, so no verdict is possible."
    elif excess > 0 and t_nw >= 2 and sup_passed:
        status = "confirmed"
        decided = "Excess mean next-bar return is above 0 with Newey-West t >= 2 and the up-bar share is higher with z >= 2."
    elif excess < 0 and t_nw <= -2:
        status = "rejected"
        decided = "Excess mean next-bar return is below 0 with Newey-West t <= -2: returns in the cross spans are lower than holding."
    elif excess > 0 and t_nw >= 2:
        status = "inconclusive"
        decided = "Excess return is positive with t >= 2 but the up-bar share check does not reach z >= 2, so the confirm rule is not fully met."
    else:
        status = "inconclusive"
        decided = "The Newey-West t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed or act_total == 0)},
        "main_measure": {
            "name": "mean next-bar return when forecast > 0 minus mean next-bar return over all bars, pooled",
            "value": None if excess is None else float(excess),
            "statistic": None if t_nw is None else {"name": "Newey-West t (10 lags)", "value": float(t_nw)},
            "threshold": "excess > 0 with t >= 2 to confirm; excess < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "up-bar share when forecast > 0 minus coin-baseline up share (binomial z)",
            "value": None if z is None else float(z),
            "passed": sup_passed,
        },
        "counts": {
            "distinct up-cross spans": int(n_spans),
            "bars with a positive forecast": int(n1),
            "all bars": int(N),
        },
        "decided_by": decided,
        "reading": ("Spans are maximal runs of forecast > 0 inside each window; the t-statistic uses a Bartlett "
                    "Newey-West variance of the influence function of (mean_in - mean_all), with autocovariances "
                    "taken only within windows; an up bar is a positive next-bar return; the up-share z-test is "
                    "required for confirmation."),
    }
