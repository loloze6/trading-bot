import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    LOW_N = 30
    MIN_EVENTS = 30
    RSI_COL = "debug_info.components.rsi_gap.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            if RSI_COL in d.columns:
                rsig = pd.to_numeric(d[RSI_COL], errors="coerce").to_numpy(dtype=float)
            else:
                rsig = np.full(len(d), np.nan)
            n = len(d)
            for t in range(n):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                # the prior 30 closes are needed inside the window
                if t < LOW_N or not np.isfinite(close[t]):
                    n_active_unverifiable += 1
                    continue
                prior = close[t - LOW_N:t]
                if not np.all(np.isfinite(prior)):
                    n_active_unverifiable += 1
                    continue
                n_active += 1
                newlow = close[t] < prior.min()
                gap_ok = np.isfinite(rsig[t]) and rsig[t] > 0
                side_ok = fc[t] > 0
                if newlow and gap_ok and side_ok:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = (
        "Situation checked on active bars that have 30 prior closes inside their window "
        "(earlier active bars cannot be recomputed and are left out of the agreement share), "
        "using the recorded rsi_gap raw value for the RSI gap; the coin's mean 20-bar return "
        "is taken on the non-overlapping grid (positions 0, 20, 40, ... of each window) pooled "
        "over all its windows; an event at t skips positive bars t+1..t+20 within the same window; "
        "the Spearman correlation is between the event's recorded forecast and its excess return."
    )

    main_name = "mean excess 20-bar forward return of non-overlapping positive-forecast events"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 events and Spearman > 0; reject: t <= -2 over >= 30 events"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars without 30 prior closes": int(n_active_unverifiable)},
            "decided_by": (
                "Fewer than 90% of the checkable active bars are long bars where the close is below its "
                "prior 30-close low and the RSI gap is above 0, so the config does not trade the plan's situation."
                if agreement is not None else
                "No active bar could be checked against the plan's situation."
            ),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    ev_fc = []
    ev_ex = []
    per_coin_events = {}
    for coin, wins in bars.items():
        # coin mean 20-bar return over all its windows (non-overlapping grid)
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            prepared.append((close, fc))
            n = len(close)
            for t in range(0, n - H, H):
                if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                    grid_rets.append(close[t + H] / close[t] - 1.0)
        if len(grid_rets) == 0:
            continue
        coin_mean = float(np.mean(grid_rets))

        cnt = 0
        for close, fc in prepared:
            n = len(close)
            t = 0
            last_start = -10 ** 9
            while t < n:
                if (t > last_start + H and np.isfinite(fc[t]) and fc[t] > 0 and t + H < n
                        and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    r = close[t + H] / close[t] - 1.0
                    ev_fc.append(float(fc[t]))
                    ev_ex.append(r - coin_mean)
                    last_start = t
                    cnt += 1
                t += 1
        per_coin_events[str(coin)] = cnt

    ev_ex = np.array(ev_ex, dtype=float)
    ev_fc = np.array(ev_fc, dtype=float)
    n_ev = int(len(ev_ex))

    mean_ex = float(np.mean(ev_ex)) if n_ev > 0 else None
    t_stat = None
    if n_ev >= 2:
        sd = float(np.std(ev_ex, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_ev)))
    rho = None
    if n_ev >= 3 and np.std(ev_fc) > 0 and np.std(ev_ex) > 0:
        rho = float(stats.spearmanr(ev_fc, ev_ex).correlation)
        if not np.isfinite(rho):
            rho = None
    sup_passed = (rho is not None and rho > 0) if rho is not None else (False if n_ev >= 3 else None)

    counts = {"non-overlapping events": n_ev}
    for c, k in per_coin_events.items():
        counts["events " + c] = int(k)

    if n_ev < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n_ev} non-overlapping events across all coins and windows, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean excess return cannot be computed (zero dispersion), so neither confirm nor reject is met."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Reject rule: the mean excess 20-bar return has t <= -2 over at least 30 events."
    elif t_stat >= 2 and mean_ex > 0 and sup_passed:
        status = "confirmed"
        decided = "Confirm rule: the mean excess 20-bar return is above 0 with t >= 2 over at least 30 events and the Spearman correlation is above 0."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: t >= 2 but the Spearman correlation between forecast and excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Spearman correlation of event forecast vs 20-bar excess return > 0",
            "value": rho,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
