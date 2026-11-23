import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    POS = "postRebalance_current_allocation"

    # ---------- 1. Situation check: down day (close < prior close, same window) and long forecast ----------
    n_active = 0
    n_agree = 0
    n_active_unknown_prev = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            prev = close.shift(1)
            active = fc.notna() & (fc != 0)
            known = prev.notna() & close.notna()
            down = (close < prev) & known
            n_active_unknown_prev += int((active & ~known).sum())
            act_known = active & known
            n_active += int(act_known.sum())
            n_agree += int((act_known & down & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "mean timing gain on bars in a position",
                "value": None,
                "statistic": None,
                "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 300 bars in a position",
            },
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": (
                "Fewer than 90% of the bars with a non-zero forecast are down days (close below the prior close) "
                "with a long forecast, so the config does not trade the plan's situation on its side."
                if agreement is not None else
                "No active bar with a known prior close: the situation cannot be checked against the forecast."
            ),
            "reading": "The situation is checked as close below the prior close within the same window with forecast > 0; "
                       "the first bar of each window has no prior close in the record and is left out of the check.",
        }

    # ---------- 2. Coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            r = (close.shift(-1) / close - 1).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- 3. Timing gain on bars in a position ----------
    gains, fcs, excess = [], [], []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            pos = pd.to_numeric(df[POS], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            rnext = close.shift(-1) / close - 1
            m = pos.notna() & (pos != 0) & rnext.notna()
            if not m.any():
                continue
            p = pos[m].values
            rn = rnext[m].values
            gains.append(p * rn - p * mu)
            mf = m & fc.notna()
            fcs.append(fc[mf].values)
            excess.append((rnext[mf] - mu).values)

    g = np.concatenate(gains) if gains else np.array([])
    n_pos = int(g.size)
    mean_g = float(np.mean(g)) if n_pos > 0 else None
    t_g = None
    if n_pos > 1:
        sd = float(np.std(g, ddof=1))
        t_g = float(mean_g / (sd / np.sqrt(n_pos))) if sd > 0 else None

    # ---------- 4. Supporting check: top vs bottom third by forecast ----------
    f_all = np.concatenate(fcs) if fcs else np.array([])
    e_all = np.concatenate(excess) if excess else np.array([])
    sup_val, sup_t, sup_pass = None, None, None
    if f_all.size >= 6:
        order = np.argsort(f_all, kind="mergesort")
        thirds = np.array_split(order, 3)
        bot = e_all[thirds[0]]
        top = e_all[thirds[2]]
        sup_val = float(np.mean(top) - np.mean(bot))
        if top.size > 1 and bot.size > 1:
            tt = stats.ttest_ind(top, bot, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
        sup_pass = bool(sup_t is not None and sup_val > 0 and sup_t > 0)

    # ---------- 5. Decision ----------
    if n_pos < 300:
        status = "not observable"
        decided_by = f"Only {n_pos} bars in a position, fewer than the plan's minimum of 300."
    elif t_g is None:
        status = "inconclusive"
        decided_by = "The timing gain's t could not be computed (zero spread)."
    elif t_g >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The mean timing gain has t >= 2 over at least 300 bars in a position and the top third beats the bottom third with Welch t > 0."
    elif t_g >= 2:
        status = "inconclusive"
        decided_by = "t >= 2 but the supporting check fails."
    elif t_g <= -2:
        status = "rejected"
        decided_by = "The mean timing gain has t <= -2 over at least 300 bars in a position."
    else:
        status = "inconclusive"
        decided_by = "The timing gain's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean timing gain on bars in a position (position x (next-day return - coin mean daily return))",
            "value": mean_g,
            "statistic": {"name": "ordinary t of the mean", "value": t_g} if t_g is not None else None,
            "threshold": "t >= 2 to confirm (with supporting check), t <= -2 to reject, over at least 300 bars in a position",
        },
        "supporting_check": {
            "name": "top third minus bottom third by forecast of next-day return minus coin mean, Welch t > 0",
            "value": sup_val,
            "passed": sup_pass,
            "welch_t": sup_t,
        },
        "counts": {"bars in a position": n_pos},
        "decided_by": decided_by,
        "reading": "Bars in a position are bars with a non-zero postRebalance_current_allocation and a next close in the same window; "
                   "the thirds are cut by forecast pooled over all coins and windows (stable sort, equal-size split); "
                   "the situation check uses close below the prior close within the window with forecast > 0, leaving out each window's first bar.",
    }
