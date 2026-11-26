import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    BAND = 2.0
    ER_P, R7_P, R30_P = 30, 7, 30
    ER_MAX = 0.3
    LHV = "debug_info.components.scaled_week.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            lhv = pd.to_numeric(df[LHV], errors="coerce").to_numpy() if LHV in df.columns \
                else np.full(len(df), np.nan)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns \
                else np.array([""] * len(df))
            absd = np.abs(np.diff(c, prepend=np.nan))
            for t in range(len(df)):
                if f[t] == 0 or not np.isfinite(f[t]):
                    continue
                n_active += 1
                # side expected: the sign of the 7-day move
                if t >= R7_P:
                    side = np.sign(c[t] / c[t - R7_P] - 1.0)
                elif np.isfinite(lhv[t]):
                    side = np.sign(lhv[t])
                else:
                    side = 0.0
                if t >= R30_P:
                    net = abs(c[t] - c[t - ER_P])
                    path = np.nansum(absd[t - ER_P + 1:t + 1])
                    er = net / path if path > 0 else np.nan
                    r7 = c[t] / c[t - R7_P] - 1.0
                    r30 = c[t] / c[t - R30_P] - 1.0
                    situ = (np.isfinite(er) and er <= ER_MAX and
                            ((r7 > 0 and r30 > 0) or (r7 < 0 and r30 < 0)))
                else:
                    situ = reg[t] == "trending"
                if situ and side != 0 and np.sign(f[t]) == side:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 7-day move over cases, in the forecast's direction"
    threshold = "confirm: mean > 0 with t >= 2 and top-minus-bottom third > 0; reject: mean < 0 with t <= -2"
    reading = ("A case is the first bet (a rise of |forecast| on its side of at least 2 points from its lowest level "
               "since the last bet, from 0 after a flat or side change) in each 7-bar cell counted from each window's "
               "first row, with the 7-bar return inside the window; the normal drift is the coin's mean 7-bar return "
               "on that grid over all windows; t is clustered by UTC day with a G/(G-1) correction; thirds are by "
               "sorted abs(forecast) split as evenly as possible; the plan's 'fewer than 30 cases or days' rule is "
               "reported as not observable; in the situation check, bars with under 30 bars of window history use the "
               "recorded regime for the situation and the 7-day move (or the raw scaled_week sign) for the side.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are bars with ER(30) <= 0.3 and same-sign 7- and 30-day "
                           "returns with the forecast on the side of the 7-day move."),
            "reading": reading,
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    cases = []  # (unusual move, abs forecast, day)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").astype(str).to_numpy()
            side, ref = 0.0, 0.0
            bet = np.zeros(len(df), dtype=bool)
            for t in range(len(df)):
                s = np.sign(f[t])
                a = abs(f[t])
                if s == 0:
                    side, ref = 0.0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                if a - ref >= BAND:
                    bet[t] = True
                    ref = a
                else:
                    ref = min(ref, a)
            for start in range(0, len(df), H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= len(df) or not np.isfinite(drift[coin]):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = np.sign(f[t]) * (r - drift[coin])
                cases.append((float(u), float(abs(f[t])), days[t]))

    n = len(cases)
    n_days = len(set(x[2] for x in cases))
    counts = {"cases": int(n), "distinct days": int(n_days)}

    mean_u, t_stat, diff = None, None, None
    if n > 0:
        u = np.array([x[0] for x in cases])
        a = np.array([x[1] for x in cases])
        d = np.array([x[2] for x in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby(d).sum().to_numpy()
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / n ** 2
            se = np.sqrt(var)
            t_stat = float(mean_u / se) if se > 0 else None
        if n >= 3:
            order = np.argsort(a, kind="mergesort")
            parts = np.array_split(order, 3)
            diff = float(u[parts[2]].mean() - u[parts[0]].mean())

    stat = {"name": "t of the mean, cases clustered by day", "value": t_stat} if t_stat is not None else None
    sup_pass = None if diff is None else bool(diff > 0)
    supporting = {"name": "top-third minus bottom-third mean unusual move by abs(forecast)",
                  "value": diff, "passed": sup_pass}
    main = {"name": main_name, "value": mean_u, "statistic": stat, "threshold": threshold}

    if n < 30 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n} cases (need 30) on {n_days} distinct days (need 30).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the top-minus-bottom-third difference is above 0."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif mean_u > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom-third difference is not above 0."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
