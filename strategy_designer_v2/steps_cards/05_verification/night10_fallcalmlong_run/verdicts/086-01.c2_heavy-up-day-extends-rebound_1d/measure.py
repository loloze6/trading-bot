import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    HV = "debug_info.components.heavy_volume.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            up = close / close.shift(1) - 1.0
            vr_prices = vol / vol.shift(1).rolling(20, min_periods=20).mean()
            if HV in df.columns:
                vr = df[HV].astype(float).where(df[HV].notna(), vr_prices)
            else:
                vr = vr_prices
            r5 = close.shift(1) / close.shift(6) - 1.0
            for i in range(len(df)):
                f = fc.iloc[i]
                if f == 0:
                    continue
                u, v, r = up.iloc[i], vr.iloc[i], r5.iloc[i]
                if pd.isna(u) or pd.isna(v) or pd.isna(r):
                    continue
                n_active += 1
                if (u > 0) and (v >= 1.5) and (r > 0) and (f > 0):
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None) and (agreement >= 0.9)

    reading = ("The situation is checked on its three day conditions (1-day return > 0, volume ratio >= 1.5 from the "
               "recorded heavy_volume raw value or the prices, close[t-1]/close[t-6]-1 > 0) with a long side, the profile "
               "being added by code and not recomputable within a window, and active bars whose conditions cannot be "
               "computed inside their window are left out; a case is the first bet (forecast rise >= 2 from its lowest "
               "positive level since its last bet, from 0 after a flat) in each 10-bar grid cell of a window with a full "
               "10-bar return ahead; the day-clustered t is mean / (sqrt(sum of per-day summed deviations^2) / n) with a "
               "D/(D-1) correction.")

    main_name = "mean unusual 10-day move of bets (return minus coin's normal 10-day drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars on an up close with volume >= 1.5x its prior "
                           "20-day mean and a positive prior 5-day return, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, vr)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            hv = df[HV].astype(float).to_numpy() if HV in df.columns else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            low = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            for start in range(0, len(df), H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= len(df) or np.isnan(drift[coin]):
                    continue
                ret = c[i + H] / c[i] - 1.0
                cases.append((ts.iloc[i].floor("D"), ret - drift[coin], hv[i]))

    n = len(cases)
    days = len(set(d for d, _, _ in cases))
    counts = {"cases": int(n), "days": int(days)}

    mean_u = None
    t = None
    rho = None
    if n > 0:
        x = np.array([u for _, u, _ in cases], dtype=float)
        mean_u = float(x.mean())
        if days > 1:
            s = pd.Series(x - mean_u, index=[d for d, _, _ in cases]).groupby(level=0).sum().to_numpy()
            se = np.sqrt(np.sum(s ** 2) * days / (days - 1)) / n
            t = float(mean_u / se) if se > 0 else None
        v = np.array([h for _, _, h in cases], dtype=float)
        ok = ~np.isnan(v)
        if ok.sum() >= 3:
            r = stats.spearmanr(v[ok], x[ok]).correlation
            rho = None if (r is None or np.isnan(r)) else float(r)
    sup_pass = None if rho is None else bool(rho > 0)

    if n < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n}): the plan's minimum count is not reached."
    elif t is not None and mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 over at least 30 cases and the Spearman correlation is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 with a Spearman correlation at or below 0 (or not computable): neither confirmed nor rejected."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or is not computable): neither confirmed nor rejected."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": None if t is None else {"name": "t of the mean, cases of one day as one", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman(heavy_volume raw ratio, unusual move) > 0", "value": rho, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
