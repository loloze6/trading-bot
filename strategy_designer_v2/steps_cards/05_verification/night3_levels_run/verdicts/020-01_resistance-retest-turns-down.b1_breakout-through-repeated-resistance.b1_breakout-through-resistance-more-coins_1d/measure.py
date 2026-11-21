import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    PERIOD = 90
    SIDE = 2
    LEVEL_BAND = 0.02
    RAW = "debug_info.components.res_break.last_history_value"

    def prep(df):
        df = df.sort_values("timestamp").reset_index(drop=True)
        close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
        fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
        if RAW in df.columns:
            raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
        else:
            raw = np.full(len(df), np.nan)
        return close, fc, raw

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            close, fc, raw = prep(df)
            prev = np.r_[np.nan, close[:-1]]
            with np.errstate(invalid="ignore"):
                situ = (raw > 0) & (close > prev)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long bars where the component "
                          "records a positive breakout value on a close rising through a past level, as the Fidelity's "
                          "long-only crossing situation requires.",
            "reading": "The situation is a bar with a positive raw component value and a close above the previous "
                       "close (a cross from at-or-below a level to above it), on the long side.",
        }

    # ---------- helpers ----------
    def swing_highs(close, t):
        lo = max(0, t - PERIOD)
        idx = []
        for i in range(lo, t - SIDE):  # i + SIDE <= t - 1
            if i - SIDE < 0:
                continue
            c = close[i]
            if not np.isfinite(c):
                continue
            nb = np.r_[close[i - SIDE:i], close[i + 1:i + SIDE + 1]]
            if np.all(np.isfinite(nb)) and np.all(c > nb):
                idx.append(i)
        return idx

    def recompute_N(close, raw, t):
        if t < 1 or not np.isfinite(close[t]) or not np.isfinite(close[t - 1]):
            return None
        sh = swing_highs(close, t)
        if not sh:
            return None
        levels = close[sh]
        c, p = close[t], close[t - 1]
        cands = [L for L in levels if p <= L < c and L > 0]
        if not cands:
            return None
        best_int = None
        best_cnt = None
        for L in cands:
            cnt = int(np.sum(np.abs(levels - L) <= LEVEL_BAND * L))
            margin = (c - L) / L * 100.0
            if np.isfinite(raw[t]) and margin > 0:
                imp = raw[t] / margin
                r = round(imp)
                if r >= 1 and abs(imp - r) < 0.01:
                    if best_int is None or r > best_int:
                        best_int = int(r)
            if best_cnt is None or cnt > best_cnt:
                best_cnt = cnt
        return best_int if best_int is not None else best_cnt

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close, _, _ = prep(df)
            for s in range(0, len(close) - H, H):
                a, b = close[s], close[s + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    unusual = []
    Ns = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close, fc, raw = prep(df)
            n = len(close)
            floor = 0.0
            bets = []
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    floor = 0.0
                    continue
                if f - floor >= BAND:
                    bets.append(t)
                    floor = f
                else:
                    floor = min(floor, f)
            used_cells = set()
            for t in bets:
                cell = t // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0) or not np.isfinite(drift[coin]):
                    continue
                u = (b / a - 1.0) - drift[coin]
                unusual.append(u)
                Ns.append(recompute_N(close, raw, t))

    unusual = np.array(unusual, dtype=float)
    n_cases = int(len(unusual))
    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    if n_cases >= 2 and np.std(unusual, ddof=1) > 0:
        t_stat = float(mean_u / (np.std(unusual, ddof=1) / np.sqrt(n_cases)))
    else:
        t_stat = None

    hi = np.array([u for u, N in zip(unusual, Ns) if N is not None and N >= 3], dtype=float)
    lo = np.array([u for u, N in zip(unusual, Ns) if N is not None and N <= 2], dtype=float)
    if len(hi) > 0 and len(lo) > 0:
        diff = float(np.mean(hi) - np.mean(lo))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False

    counts = {"cases": n_cases, "cases with N >= 3": int(len(hi)), "cases with N <= 2": int(len(lo))}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (no spread), so it is not beyond +/-2."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 on at least 30 cases, and the N>=3 minus N<=2 difference is positive."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2, >= 30 cases) but the supporting difference is not positive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 on at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move is between -2 and 2 on at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 10-bar move of long cases",
            "value": mean_u,
            "statistic": {"name": "one-sample t", "value": t_stat} if t_stat is not None else None,
            "threshold": "mean above 0 with t >= 2 on at least 30 cases to confirm; below 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "mean unusual move N>=3 minus N<=2",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "A case is the first forecast rise of at least 2 points above its floor (reset to 0 when the "
                   "forecast is flat) in each 10-bar grid cell of a window, and N is recomputed from the window's own "
                   "closes (swing-high closes above their 2 neighbours on each side within the past 90 bars, using the "
                   "crossed level whose N x margin matches the recorded raw value, else the one with most touches), "
                   "with cases where no crossed level is found left out of the supporting check.",
    }
