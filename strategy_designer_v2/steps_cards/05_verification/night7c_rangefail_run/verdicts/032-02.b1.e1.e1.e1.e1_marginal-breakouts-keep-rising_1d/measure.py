import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    BAND = 2.0
    MCOL = "debug_info.components.margin.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if MCOL in df.columns:
                m = pd.to_numeric(df[MCOL], errors="coerce")
            else:
                m = pd.Series(np.nan, index=df.index)
            prior_max = close.shift(1).rolling(60, min_periods=60).max()
            m_px = (close / prior_max - 1.0) * 100.0
            m_use = m.where(m.notna(), m_px)
            active = fc != 0
            situ = (m_use > 0) & m_use.notna()
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "Welch t of excess 20-bar return, small-margin half minus large-margin half"
    threshold = "confirm t >= 2 with small half rising more and supporting check passing; reject t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars where the close is above the prior 60-day closing high, as the plan's situation requires.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    # coin normal 20-bar drift over all windows (non-overlapping grid)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (excess, margin, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            if MCOL in df.columns:
                mg = pd.to_numeric(df[MCOL], errors="coerce").to_numpy()
            else:
                mg = np.full(len(df), np.nan)
            n = len(df)
            # bets: rise of the long forecast of at least BAND from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            prev_long = False
            for i in range(n):
                fi = f[i]
                if fi > 0:
                    if not prev_long:
                        low = 0.0
                    low = min(low, fi)
                    if fi - low >= BAND:
                        bet[i] = True
                        low = fi
                    prev_long = True
                else:
                    prev_long = False
                    low = 0.0
            # first bet in each 20-bar grid cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                if not np.isfinite(mg[t]) or not np.isfinite(drift[coin]):
                    continue
                r = c[t + H] / c[t] - 1.0
                cases.append((r - drift[coin], float(mg[t]), float(f[t])))

    arr = np.array(cases, dtype=float).reshape(-1, 3)
    n_cases = int(arr.shape[0])
    if n_cases > 0:
        med = float(np.median(arr[:, 1]))
        small = arr[arr[:, 1] <= med, 0]
        large = arr[arr[:, 1] > med, 0]
    else:
        small = np.array([])
        large = np.array([])
    n_s, n_l = int(len(small)), int(len(large))

    fw = None
    if n_cases > 0 and np.sum(arr[:, 2]) != 0:
        fw = float(np.sum(arr[:, 0] * arr[:, 2]) / np.sum(arr[:, 2]))
    sup_pass = None if fw is None else bool(fw > 0)

    diff = float(np.mean(small) - np.mean(large)) if (n_s > 0 and n_l > 0) else None
    tval = None
    if n_s >= 2 and n_l >= 2:
        tt = stats.ttest_ind(small, large, equal_var=False)
        tval = float(tt.statistic) if np.isfinite(tt.statistic) else None

    counts = {"cases": n_cases, "small-margin half": n_s, "large-margin half": n_l}
    reading = ("Cases are the first long bet (forecast rise of at least 2 points, holding-period rule) in each 20-bar grid cell "
               "of each window with a full 20-bar return inside the window; the pooled median split puts margins <= median "
               "in the small half; the coin's drift is its mean non-overlapping 20-bar return over all its windows.")

    if n_s < 20 or n_l < 20 or tval is None:
        status = "not observable"
        decided = "Each half needs at least 20 cases, and this minimum is not reached."
    elif tval >= 2 and diff > 0 and sup_pass:
        status = "confirmed"
        decided = "Welch t >= 2 with the small-margin half rising more and the forecast-weighted mean excess return above 0."
    elif tval <= -2 and diff < 0:
        status = "rejected"
        decided = "Welch t <= -2 with the large-margin half rising more than the small-margin half."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Welch t >= 2 but the forecast-weighted mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "Welch t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": None if tval is None else {"name": "Welch t", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 20-bar return > 0",
            "value": fw,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
