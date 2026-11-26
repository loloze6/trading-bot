import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    VG = "debug_info.components.vol_growth.last_history_value"
    F10 = "debug_info.components.fall10.last_history_value"

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            # recompute from prices where a raw value is not recorded
            recent = vol.rolling(30).mean()
            prior = vol.shift(30).rolling(30).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                vg_re = np.log(recent / prior)
            r10_re = (close / close.shift(10) - 1.0) * 100.0
            vg = df[VG].astype(float) if VG in df.columns else pd.Series(np.nan, index=df.index)
            r10 = df[F10].astype(float) if F10 in df.columns else pd.Series(np.nan, index=df.index)
            vg = vg.where(vg.notna(), vg_re)
            r10 = r10.where(r10.notna(), r10_re)
            active = fc != 0
            situ = (vg > 0) & (r10 < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation is checked as recorded log volume ratio > 0 and 10-day return < 0 (recomputed from "
               "prices where not recorded), long side, with the falling profile left to the profile code as the "
               "Fidelity line states; a case is the first bet (forecast rise >= 2 points from its lowest level on its "
               "side since the last bet, from 0 after a flat or side change) in each 5-bar grid cell, its 5-bar return "
               "taken from that bet's close; the coin's mean 5-day return uses the 5-bar grid of all its windows; "
               "in-position cells are grid bars with a non-zero held allocation; the t is cluster-by-day; the plan's "
               "minimum counts (30 cases, 20 days) give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 5-day move of the bets", "value": None, "statistic": None,
                             "threshold": "t >= 2 positive to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the active bars are long bars of the plan's situation (volume grown "
                           "against the prior 30 days and a negative 10-day return)" if n_active > 0 else
                           "The record has no active bar, so the config never takes the plan's situation"),
            "reading": reading,
        }

    # ---------- main measure ----------
    case_moves, case_days = [], []
    corr_f, corr_x = [], []
    for coin in sorted(bars):
        wins = bars[coin]
        # coin's mean 5-day return over all windows, on the grid
        grid_rets = []
        for w in sorted(wins):
            df = wins[w].reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))

        for w in sorted(wins):
            df = wins[w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            ts = to_time(df["timestamp"])
            alloc = (df["postRebalance_current_allocation"].astype(float).fillna(0.0).values
                     if "postRebalance_current_allocation" in df.columns else np.zeros(n))

            # bets
            bet = np.zeros(n, dtype=bool)
            bet_side = np.zeros(n)
            side = 0
            level = 0.0
            for i in range(n):
                s = 1 if f[i] > 0 else (-1 if f[i] < 0 else 0)
                if s == 0:
                    side = 0
                    level = 0.0
                    continue
                if s != side:
                    side = s
                    level = 0.0
                v = s * f[i]
                if v - level >= BAND:
                    bet[i] = True
                    bet_side[i] = s
                    level = v
                else:
                    level = min(level, v)

            for start in range(0, n, H):
                end = min(start + H, n)
                idx = np.where(bet[start:end])[0]
                if len(idx) > 0:
                    t = start + int(idx[0])
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                        r = c[t + H] / c[t] - 1.0
                        case_moves.append(bet_side[t] * (r - drift))
                        case_days.append(ts.iloc[t].floor("D"))
                # supporting check on the in-position grid bar
                if start + H < n and alloc[start] != 0 and np.isfinite(c[start]) and \
                        np.isfinite(c[start + H]) and c[start] != 0 and np.isfinite(f[start]):
                    corr_f.append(f[start])
                    corr_x.append(c[start + H] / c[start] - 1.0 - drift)

    n_cases = len(case_moves)
    n_days = len(set(case_days))
    mean_move = float(np.mean(case_moves)) if n_cases else None

    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        x = np.array(case_moves)
        dev = pd.Series(x - x.mean()).groupby(pd.Series(case_days)).sum().values
        D = len(dev)
        se = np.sqrt(np.sum(dev ** 2) * D / (D - 1)) / n_cases
        if se > 0:
            t_stat = float(x.mean() / se)

    corr = None
    if len(corr_f) >= 3 and np.std(corr_f) > 0 and np.std(corr_x) > 0:
        corr = float(np.corrcoef(corr_f, corr_x)[0, 1])
    check_pass = (corr is not None and corr > 0)

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum counts are not reached ({n_cases} cases against 30, "
                   f"{n_days} distinct days against 20).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_move > 0 and t_stat >= 2 and check_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the forecast/unusual-move correlation is above 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move has t <= -2."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The mean unusual move has t >= 2 but the supporting correlation check fails."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 5-day move of the bets",
            "value": mean_move,
            "statistic": ({"name": "t of the mean, cases summed per day", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": "positive with t >= 2 (and check passing) confirms; t <= -2 rejects",
        },
        "supporting_check": {
            "name": "correlation of forecast and unusual 5-day move over in-position grid cells",
            "value": corr,
            "passed": check_pass if corr is not None else None,
        },
        "counts": {"cases": int(n_cases), "distinct days": int(n_days),
                   "in-position cells": int(len(corr_f))},
        "decided_by": decided,
        "reading": reading,
    }
