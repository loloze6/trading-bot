import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    BAND = 2.0
    EPS = 1e-9
    VR_COL = "debug_info.components.dry.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_undetermined = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            vol = pd.to_numeric(df["volume"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            n = len(df)
            # ret14 from prices, inside the window only
            ret14 = np.full(n, np.nan)
            if n > H:
                ret14[H:] = close[H:] / close[:-H] - 1.0
            # vr: recorded raw value where present, else recomputed from volume
            vr_rec = (pd.to_numeric(df[VR_COL], errors="coerce").to_numpy(float)
                      if VR_COL in df.columns else np.full(n, np.nan))
            vs = pd.Series(vol)
            vr_calc = (vs.rolling(14, min_periods=14).mean()
                       / vs.rolling(30, min_periods=30).mean() - 1.0).to_numpy(float)
            vr = np.where(np.isfinite(vr_rec), vr_rec, vr_calc)
            active = fc != 0
            for i in np.where(active)[0]:
                if not (np.isfinite(ret14[i]) and np.isfinite(vr[i])):
                    n_undetermined += 1
                    continue
                n_active += 1
                if ret14[i] > 0 and vr[i] < 0 and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("Situation recomputed as close[t]/close[t-14]-1 > 0 and the recorded 'dry' raw volume ratio "
               "(recomputed 14/30 mean volume - 1 where not recorded) < 0, expected side short, with active bars "
               "whose 14-bar return cannot be computed inside the window left out of the agreement; a case is the "
               "first short bet (short forecast deepening by >= 2 points from its lowest short level since the last "
               "bet, reset at flat or side change) in each 14-bar grid cell of a window, counted only if its 14-bar "
               "forward return lies inside the window, drift is the coin's mean non-overlapping 14-bar return over "
               "all its windows, the day-clustered t uses a G/(G-1) correction, and fewer than 30 distinct days "
               "is reported as not observable.")

    main_name = "mean short-direction 14-bar unusual move (return minus drift, sign flipped)"
    main_thr = "mean > 0 with day-clustered t >= 2 confirms; mean < 0 with t <= -2 rejects"
    sup_name = "correlation of signal-bar forecast with 14-bar excess return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active_bars_checked": int(n_active), "active_bars_undetermined": int(n_undetermined)},
            "decided_by": ("Fewer than 90% of active bars are short bars with a positive 14-day return and the "
                           "14-day mean volume below the 30-day mean volume, so the forecast does not follow the "
                           "plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            for p in range(0, len(close) - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    cases = []  # (day, short_move, forecast, excess)
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            ts = _ts(df)
            n = len(df)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f < 0:
                    s = -f
                    if s - ref >= BAND - EPS:
                        bet[i] = True
                        ref = s
                    else:
                        ref = min(ref, s)
                else:
                    ref = 0.0
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or pd.isna(ts.iloc[i]):
                    continue
                ex = r - d
                cases.append((ts.iloc[i].normalize(), -ex, fc[i], ex))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)

    mean_v = None
    t_v = None
    corr = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases], float)
        mean_v = float(x.mean())
        dev = pd.Series(x - x.mean()).groupby([c[0] for c in cases]).sum().to_numpy(float)
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_v = float(mean_v / se) if se > 0 else None
        if n_cases > 2:
            fv = np.array([c[2] for c in cases], float)
            ev = np.array([c[3] for c in cases], float)
            if np.std(fv) > 0 and np.std(ev) > 0:
                corr = float(np.corrcoef(fv, ev)[0, 1])
    sup_pass = None if corr is None else bool(corr > 0)

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_days < 30:
        status = "not observable"
        decided = f"The cases fall on {n_days} distinct days, fewer than the plan's minimum of 30."
    elif mean_v is not None and t_v is not None and mean_v > 0 and t_v >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean short-direction unusual move is above 0 with t >= 2 and the supporting correlation is above 0."
    elif mean_v is not None and t_v is not None and mean_v < 0 and t_v <= -2:
        status = "rejected"
        decided = "The mean short-direction unusual move is below 0 with t <= -2: price rises versus drift after drying-volume rises."
    else:
        status = "inconclusive"
        if t_v is not None and t_v >= 2:
            decided = "t >= 2 but the supporting correlation is 0 or below (or undefined), so the idea is inconclusive."
        else:
            decided = "t lies between -2 and 2, so the idea is neither confirmed nor rejected."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_v,
                         "statistic": ({"name": "t of the mean, clustered by day", "value": t_v}
                                       if t_v is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": corr, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
