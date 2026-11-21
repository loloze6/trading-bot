import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    BAND = 2.0
    TEN, KIJ, SEN, DISP = 9, 26, 52, 26
    MAX_AGE = 26
    MIN_CASES = 30

    def prep(df):
        df = df.copy()
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp")
        return df.reset_index(drop=True)

    # ---------- 1. situation check (recomputed from prices) ----------
    def situation(df):
        """Return arrays: determinable (bool), in_situation (bool) per bar."""
        hi = df["high"].astype(float)
        lo = df["low"].astype(float)
        cl = df["close"].astype(float).values
        tenkan = (hi.rolling(TEN, min_periods=TEN).max() + lo.rolling(TEN, min_periods=TEN).min()) / 2
        kijun = (hi.rolling(KIJ, min_periods=KIJ).max() + lo.rolling(KIJ, min_periods=KIJ).min()) / 2
        spanA = ((tenkan + kijun) / 2).shift(DISP).values
        spanB = ((hi.rolling(SEN, min_periods=SEN).max() + lo.rolling(SEN, min_periods=SEN).min()) / 2).shift(DISP).values
        n = len(df)
        top = np.fmax(spanA, spanB)
        bot = np.fmin(spanA, spanB)
        ok = ~(np.isnan(spanA) | np.isnan(spanB))
        state = np.zeros(n, dtype=int)  # 1 above, -1 below, 0 inside
        state[ok & (cl > top)] = 1
        state[ok & (cl < bot)] = -1
        det = np.zeros(n, dtype=bool)
        sit = np.zeros(n, dtype=bool)
        valid_idx = np.where(ok)[0]
        start = valid_idx[0] if len(valid_idx) else n
        for t in range(n):
            if not ok[t]:
                continue
            if state[t] != -1:
                det[t] = True
                sit[t] = False
                continue
            seg = state[start:t + 1]
            above = np.where(seg == 1)[0]
            if len(above):
                s = start + above[-1]
                after = np.where(state[s + 1:t + 1] == -1)[0]
                c = s + 1 + after[0]
                det[t] = True
                sit[t] = (t - c) <= MAX_AGE
            else:
                below = np.where(seg == -1)[0] + start
                if len(below) and below[0] < t - MAX_AGE:
                    det[t] = True
                    sit[t] = False
    # no above bar since a below bar older than 26 bars: the cross is older
        return det, sit

    n_det = 0
    n_agree = 0
    n_active_total = 0
    n_fallback_agree = 0
    for coin, wins in bars.items():
        for w, df0 in wins.items():
            df = prep(df0)
            if len(df) == 0:
                continue
            f = df["forecast"].astype(float).values
            active = (~np.isnan(f)) & (f != 0)
            det, sit = situation(df)
            n_active_total += int(active.sum())
            m = active & det
            n_det += int(m.sum())
            n_agree += int((m & sit & (f < 0)).sum())
            if "regime" in df.columns:
                reg = df["regime"].astype(str).values
                n_fallback_agree += int((active & (reg == "trending") & (f < 0)).sum())

    if n_det > 0:
        agreement = n_agree / n_det
        sit_reading = ("situation recomputed from in-window prices (cloud = 9/26/52 spans displaced 26; below the cloud "
                       "with the first close below after the last close above at most 26 bars back), checked on the "
                       f"{n_det} of {n_active_total} active bars where the in-window history makes it determinable")
    elif n_active_total > 0:
        agreement = n_fallback_agree / n_active_total
        sit_reading = ("no active bar had enough in-window history to recompute the cloud cross, so the check fell back "
                       "on the recorded regime and the forecast's short sign")
    else:
        agreement = None
        sit_reading = "no active bar in the record"

    passed = agreement is not None and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active_total), "determinable active bars": int(n_det)},
            "decided_by": ("fewer than 90 % of the active bars are short bars below the cloud within 26 bars of a "
                           "cross down from above, as the plan's Fidelity requires"),
            "reading": sit_reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 26-bar returns over all windows of the coin
        grid_rets = []
        prepped = {}
        for w, df0 in wins.items():
            df = prep(df0)
            prepped[w] = df
            cl = df["close"].astype(float).values
            for p in range(0, len(cl) - H, H):
                if np.isfinite(cl[p]) and np.isfinite(cl[p + H]) and cl[p] != 0:
                    grid_rets.append(cl[p + H] / cl[p] - 1)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in prepped.items():
            cl = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(df)
            side = 0
            ref = 0.0
            bets = []
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft == 0:
                    side, ref = 0, 0.0
                    continue
                s = 1 if ft > 0 else -1
                mag = abs(ft)
                if s != side:
                    side, ref = s, 0.0
                if mag - ref >= BAND - 1e-12:
                    if s < 0:
                        bets.append(t)
                    ref = mag
                else:
                    ref = min(ref, mag)
            seen = set()
            for t in bets:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(cl[t]) and np.isfinite(cl[t + H])) or cl[t] == 0:
                    continue
                r = cl[t + H] / cl[t] - 1
                unusual.append(-(r - drift))
                absf.append(abs(f[t]))

    u = np.array(unusual, dtype=float)
    a = np.array(absf, dtype=float)
    ncase = int(len(u))

    mean_u = float(np.mean(u)) if ncase > 0 else None
    t_u = None
    if ncase > 1:
        sd = np.std(u, ddof=1)
        t_u = float(mean_u / (sd / np.sqrt(ncase))) if sd > 0 else None

    diff = None
    t_d = None
    n_thin = n_thick = 0
    if ncase > 0:
        med = float(np.median(a))
        thin = u[a > med]
        thick = u[a <= med]
        n_thin, n_thick = int(len(thin)), int(len(thick))
        if n_thin > 0 and n_thick > 0:
            diff = float(np.mean(thin) - np.mean(thick))
        if n_thin > 1 and n_thick > 1:
            res = stats.ttest_ind(thin, thick, equal_var=False)
            if np.isfinite(res.statistic):
                t_d = float(res.statistic)

    check_passed = None
    if t_d is not None and diff is not None:
        check_passed = bool(diff > 0 and t_d >= 1)

    if ncase < MIN_CASES:
        status = "not observable"
        decided = f"fewer than 30 cases over all coins and windows ({ncase})"
    elif (t_u is not None and t_u <= -2) or (t_d is not None and t_d <= -2):
        status = "rejected"
        decided = ("reject rule: the mean unusual move has t <= -2" if (t_u is not None and t_u <= -2)
                   else "reject rule: the thin-minus-thick difference has Welch t <= -2")
    elif t_u is not None and mean_u > 0 and t_u >= 2 and check_passed is True:
        status = "confirmed"
        decided = ("confirm rule: the mean unusual move is positive with t >= 2 and the thin-minus-thick "
                   "difference is positive with t >= 1")
    else:
        status = "inconclusive"
        if t_u is not None and mean_u > 0 and t_u >= 2:
            decided = "inconclusive rule: the main measure meets the confirm rule but the thin-minus-thick check does not (t between -2 and 1)"
        else:
            decided = "inconclusive rule: the mean unusual move's t is between -2 and 2 (neither confirm nor reject)"

    reading = (sit_reading + "; a case is the first short bet (|forecast| rising >= 2 from its lowest since the last "
               "bet) in each 26-bar cell counted from each window's first row, and cases are split into thin (|forecast| "
               "above the median) and thick (at or below the median).")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 26-bar unusual move in the short direction",
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "ordinary t of the mean", "value": t_u},
            "threshold": "confirm: positive with t >= 2; reject: t <= -2",
        },
        "supporting_check": {
            "name": "thin-minus-thick unusual move, Welch t",
            "value": t_d,
            "passed": check_passed,
        },
        "counts": {"cases": ncase, "thin-cloud half": n_thin, "thick-cloud half": n_thick},
        "decided_by": decided,
        "reading": reading,
    }
