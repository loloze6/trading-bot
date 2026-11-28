import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.lightness.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            up = close.diff()  # NaN on the window's first bar
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce")
            else:
                lhv = pd.Series(np.nan, index=df.index)
            prior_mean = vol.shift(1).rolling(20, min_periods=20).mean()
            vr_rec = vol / prior_mean - 1.0
            vr_c = lhv.where(lhv.notna(), vr_rec)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            active = fc != 0
            verifiable = up.notna() & vr_c.notna()
            # active bars whose situation can be told are counted
            act_idx = active & verifiable
            sit = (up > 0) & (vr_c < 0) & (regime == "mean_reversion")
            n_active += int(act_idx.sum())
            n_agree += int((act_idx & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The falling-calm profile is read from the detector's regime ('mean_reversion', since the profile "
               "components are not recorded), the up day from close above the prior close, light volume from the "
               "lightness raw value below 0 (recomputed from volume when missing), active bars whose up day or "
               "ratio cannot be computed are left out; a case is the first bet (forecast rise of >= 2 from its low "
               "since the last bet) in each 5-bar grid cell with its 5-bar return from that bar's close, the day t "
               "is cluster-robust by signal date with G/(G-1) correction, the halves are strictly above/below the "
               "median case forecast, and the plan's 'fewer than 30 distinct days' minimum is reported as "
               "'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of active bars are long bars on an up day with volume below its prior "
                           "20-day mean in the falling-calm regime (or there are no active bars)."),
            "reading": reading,
        }

    # ---------- 2. cases ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1.0
                coin_cases.append((ts.iloc[t].strftime("%Y-%m-%d"), r, float(fc[t])))
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        for d, r, f in coin_cases:
            if np.isfinite(drift):
                cases.append((d, r - drift, f))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)

    mean_u = None
    t_main = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([c[0] for c in cases]).sum().values
        G = len(dev)
        if G > 1:
            var = (dev ** 2).sum() / n_cases ** 2 * G / (G - 1)
            se = np.sqrt(var)
            t_main = float(mean_u / se) if se > 0 else None

    diff = None
    t_welch = None
    if n_cases > 0:
        f = np.array([c[2] for c in cases])
        u = np.array([c[1] for c in cases])
        med = np.median(f)
        hi, lo = u[f > med], u[f < med]
        if len(hi) > 0 and len(lo) > 0:
            diff = float(hi.mean() - lo.mean())
        if len(hi) > 1 and len(lo) > 1:
            tw = stats.ttest_ind(hi, lo, equal_var=False).statistic
            t_welch = float(tw) if np.isfinite(tw) else None
    check_pass = None if diff is None else bool(diff > 0)

    counts = {"cases": n_cases, "distinct days with cases": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct days with cases ({n_days})."
    elif t_welch is not None and t_welch <= -2:
        status = "rejected"
        decided = "The upper-minus-lower difference has Welch t <= -2: lighter up days are followed by smaller rises."
    elif mean_u is not None and t_main is not None and mean_u < 0 and t_main <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif mean_u is not None and t_main is not None and mean_u > 0 and t_main >= 2 and check_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the upper-minus-lower difference is above 0."
    else:
        status = "inconclusive"
        if t_main is not None and t_main >= 2 and mean_u > 0:
            decided = "Main t >= 2 but the check difference is at or below 0 (or not computable)."
        else:
            decided = "The main t lies between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 5-bar move of the cases",
            "value": mean_u,
            "statistic": None if t_main is None else {"name": "t of the mean, cases of one day pooled", "value": t_main},
            "threshold": "confirm: mean > 0 with t >= 2 (and check > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "upper-half minus lower-half (by forecast) mean unusual move",
            "value": diff,
            "passed": check_pass,
            "welch_t": t_welch,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
