import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    BAND = 2.0
    T_THR = 2.0
    MIN_CASES = 30
    COL_RAW = "debug_info.components.fall26.last_history_value"

    def ichimoku_state(df):
        hi = df["high"].astype(float)
        lo = df["low"].astype(float)
        cl = df["close"].astype(float)
        tenkan = (hi.rolling(9).max() + lo.rolling(9).min()) / 2.0
        kijun = (hi.rolling(26).max() + lo.rolling(26).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(26)
        span_b = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2.0).shift(26)
        top = pd.concat([span_a, span_b], axis=1).max(axis=1, skipna=False)
        bot = pd.concat([span_a, span_b], axis=1).min(axis=1, skipna=False)
        state = pd.Series(np.nan, index=df.index)
        known = top.notna() & bot.notna()
        state[known] = 0.0
        state[known & (cl > top)] = 1.0
        state[known & (cl < bot)] = -1.0
        outside = state.where(state != 0)
        prev_out = outside.ffill().shift(1)
        # a run of inside bars after the unknown start stays unknown
        return state, prev_out

    # ---------- 1. situation check ----------
    n_active = 0
    n_eval = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            cl = df["close"].astype(float)
            state, prev_out = ichimoku_state(df)
            ret_re = cl / cl.shift(H) - 1.0
            if COL_RAW in df.columns:
                raw = pd.to_numeric(df[COL_RAW], errors="coerce")
                ret = raw.where(raw.notna(), ret_re)
            else:
                ret = ret_re
            for i in range(len(df)):
                if fc.iloc[i] == 0:
                    continue
                n_active += 1
                s = state.iloc[i]
                r = ret.iloc[i]
                if pd.isna(s) or pd.isna(r):
                    continue
                if s == -1 and pd.isna(prev_out.iloc[i]):
                    continue
                n_eval += 1
                cross = (s == -1) and (prev_out.iloc[i] == 1)
                if cross and r < 0 and fc.iloc[i] < 0:
                    n_agree += 1

    agreement = (n_agree / n_eval) if n_eval > 0 else None
    passed = (agreement is not None and agreement >= 0.9) if n_eval > 0 else None
    reading_check = ("the situation is checked on the active bars where the cloud (52+26 bars of history) "
                     "and the prior outside state can be computed inside their window, with the 26-bar return "
                     "taken from the recorded fall26 raw value or recomputed from closes")
    if passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "checked active bars": int(n_eval)},
            "decided_by": ("fewer than 90% of the checkable active bars are short forecasts on a close that "
                           "crosses down from above the cloud to below it with a negative 26-day return"),
            "reading": reading_check + ".",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 26-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            cl = df["close"].astype(float).reset_index(drop=True).values
            for p in range(0, len(cl), H):
                if p + H < len(cl) and np.isfinite(cl[p]) and np.isfinite(cl[p + H]) and cl[p] > 0:
                    rets.append(cl[p + H] / cl[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    unusual = []
    absfc = []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            cl = df["close"].astype(float).values
            side = 0
            base = 0.0
            used_cells = set()
            for i in range(len(df)):
                f = fc[i]
                sg = int(np.sign(f))
                if sg != side:
                    side = sg
                    base = 0.0
                if side == 0:
                    continue
                mag = abs(f)
                is_bet = False
                if mag - base >= BAND:
                    is_bet = True
                    base = mag
                else:
                    base = min(base, mag)
                if not is_bet or side >= 0:
                    continue
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if i + H >= len(df):
                    continue
                if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H]) and cl[i] > 0):
                    continue
                r = cl[i + H] / cl[i] - 1.0
                unusual.append(-(r - d))
                absfc.append(mag)

    n = len(unusual)
    u = np.array(unusual, dtype=float)
    a = np.array(absfc, dtype=float)
    mean_u = float(np.mean(u)) if n > 0 else None
    t_u = None
    if n >= 2:
        sd = np.std(u, ddof=1)
        t_u = float(mean_u / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n >= 3 and np.std(a) > 0:
        slope = float(stats.linregress(a, u).slope)
    slope_pass = (slope > 0) if slope is not None else None

    main = {
        "name": "mean 26-bar unusual move (short direction) after cross bars",
        "value": mean_u,
        "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
    }
    support = {"name": "slope of unusual move on |forecast| at the cross", "value": slope,
               "passed": slope_pass}
    counts = {"cases across all coins and windows": int(n)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"fewer than {MIN_CASES} cases across all coins and windows ({n})."
    elif t_u is not None and mean_u > 0 and t_u >= T_THR and slope_pass is True:
        status = "confirmed"
        decided = "the mean unusual move is positive with t >= 2 and the supporting slope is above 0."
    elif t_u is not None and mean_u < 0 and t_u <= -T_THR:
        status = "rejected"
        decided = "the mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        if t_u is not None and mean_u > 0 and t_u >= T_THR:
            decided = "a positive main result with t >= 2 but a supporting slope at or below 0 (or not computable) is inconclusive."
        else:
            decided = "the t of the mean unusual move lies between -2 and 2 (or is not computable), which is inconclusive."

    reading = (reading_check + "; cases are the short bets (forecast rising by at least 2 points on the short side "
               "from its low since the last bet), one per 26-bar grid cell of each window, with the coin's drift "
               "the mean of its non-overlapping 26-bar returns over all windows, and the plan's 'fewer than 30 "
               "cases' rule reported as not observable.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement) if agreement is not None else None,
                            "passed": bool(passed) if passed is not None else True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
