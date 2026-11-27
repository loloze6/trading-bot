import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_week_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            regime = df["regime"].astype(str).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # 7-day return from prices, inside the window, as fallback where raw is missing
            r7 = np.full(len(df), np.nan)
            if len(df) > 7:
                r7[7:] = close[7:] / close[:-7] - 1.0
            rise_sign = np.where(np.isfinite(raw), np.sign(raw), np.sign(r7))
            rise_sign = np.nan_to_num(rise_sign, nan=0.0)
            in_profile = regime == "unknown"
            active = fc != 0
            ok = active & in_profile & (rise_sign > 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 3-day move after a forecast rise of >= 2 points"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2; reject: t <= -2"
    sup_name = "upper minus lower half (forecast median split) mean unusual move"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars inside the falling calm "
                          "profile (regime 'unknown') with a positive 7-day rise, as the Fidelity's situation requires.",
            "reading": "The profile is read from the recorded regime ('unknown' = no veto, i.e. falling and calm) and the "
                       "7-day rise from the sign of the raw scaled return (prices where it is not recorded).",
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        # coin's normal drift: mean non-overlapping 3-bar return over all its windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").values
            # bets: rise of the forecast on its (long) side of >= BAND from its lowest level since last bet
            ref = 0.0
            prev_side = 0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                f = fc[i]
                side = 1 if f > 0 else (-1 if f < 0 else 0)
                if side == 0:
                    ref = 0.0
                    prev_side = 0
                    continue
                if side != prev_side:
                    ref = 0.0
                prev_side = side
                a = abs(f)
                ref = min(ref, a) if ref > 0 else ref
                if a - ref >= BAND:
                    if side > 0:
                        bet[i] = True
                    ref = a
            seen_cells = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= len(df):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                ret = c[i + H] / c[i] - 1.0
                cases.append((days[i], ret - drift, float(fc[i])))

    n = len(cases)
    if n > 0:
        u = np.array([x[1] for x in cases])
        f = np.array([x[2] for x in cases])
        d = np.array([x[0] for x in cases])
        mean_u = float(np.mean(u))
        dev = pd.Series(u - mean_u).groupby(pd.Series(d)).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1)) * np.sum(dev ** 2) / (n ** 2)
            t_main = float(mean_u / np.sqrt(var)) if var > 0 else float("nan")
        else:
            t_main = float("nan")
        med = float(np.median(f))
        up = u[f > med]
        lo = u[f <= med]
    else:
        mean_u, t_main, D = None, float("nan"), 0
        up, lo = np.array([]), np.array([])

    n_up, n_lo = int(len(up)), int(len(lo))
    if n_up >= 2 and n_lo >= 2:
        diff = float(np.mean(up) - np.mean(lo))
        t_sup = float(stats.ttest_ind(up, lo, equal_var=False).statistic)
    else:
        diff, t_sup = None, float("nan")

    counts = {"cases": int(n), "upper half cases": n_up, "lower half cases": n_lo, "days with cases": int(D)}

    def fin(x):
        return x is not None and np.isfinite(x)

    sup_pass = None
    if diff is not None and fin(t_sup):
        sup_pass = bool(diff > 0 and t_sup >= 2)

    if n < 40 or n_up < 20 or n_lo < 20:
        status = "not observable"
        decided = "The plan's minimum counts are not reached (fewer than 40 cases in total or fewer than 20 in a half)."
    elif (fin(t_main) and t_main <= -2) or (fin(t_sup) and t_sup <= -2):
        status = "rejected"
        decided = "Reject rule: the main measure's t <= -2 (reversal) or the supporting difference's t <= -2."
    elif fin(t_main) and mean_u > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule: mean unusual move positive with t >= 2 and upper-minus-lower difference positive with t >= 2."
    else:
        status = "inconclusive"
        decided = "Neither the confirm nor the reject rule holds (a t between -2 and 2 on the main measure or the supporting check)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases of the same day summed",
                          "value": t_main if fin(t_main) else None},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "A case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, from 0 "
                   "after flat) in each 3-bar grid cell counted from each window's first row, drift is the coin's mean "
                   "grid 3-bar return over all its windows, the upper half is forecast > median and the lower half "
                   "forecast <= median, the day-clustered t uses a D/(D-1) correction, and the plan's 'too few cases is "
                   "inconclusive' is reported as 'not observable' per the workflow.",
    }
