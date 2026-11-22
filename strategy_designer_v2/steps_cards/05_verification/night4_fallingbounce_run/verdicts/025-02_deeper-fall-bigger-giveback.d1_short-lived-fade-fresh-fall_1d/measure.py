import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    BAND = 2.0
    MIN_CASES = 30
    LHV = "debug_info.components.bounce.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret90 = close / close.shift(90) - 1.0
            ret30 = close / close.shift(30) - 1.0
            reg_rec = (df["regime"].astype(str) == "mean_reversion")
            # double-fall regime: recomputed from prices where history allows, else the recorded regime decision
            both_ok = ret90.notna() & ret30.notna()
            regime_ok = np.where(both_ok, (ret90 < 0) & (ret30 < 0), reg_rec)
            # one-day rise: the raw vol-scaled 1-day return where recorded, else the price return
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            r1 = close / close.shift(1) - 1.0
            rise = np.where(raw.notna(), raw > 0, r1 > 0)
            active = (fc != 0).values
            sit_short = regime_ok.astype(bool) & rise.astype(bool) & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int((active & sit_short).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "abs(forecast)-weighted mean short-direction 2-bar unusual move"
    threshold = "t >= 2 over at least 30 cases confirms (with supporting check); t <= -2 over at least 30 cases rejects"
    reading = ("Regime recomputed from prices where 90 bars of window history exist, else the recorded regime; "
               "a rise is a positive raw vol-scaled 1-day return; a case is the first short bet (forecast falling by >= 2 "
               "points from its lowest short level since the last bet, from 0 after flat) in each 2-bar grid cell from the "
               "window's first row; drift is the coin's mean 2-bar return on that grid over all windows; the t of the "
               "weighted mean uses the weighted standard error sqrt(sum w^2 (v-m)^2)/sum w x sqrt(n/(n-1)); the median "
               "split puts abs(forecast) >= median in the larger half and < median in the smaller, halves compared by "
               "unweighted means.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the 90-day and "
                           "30-day double-fall regime on a one-day rise, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # drift per coin: mean 2-bar return on the non-overlapping grid, all windows
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rs.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rs)) if rs else np.nan

    vals, wts = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(f)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                s = -f[i] if f[i] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, s)
                if s - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = s
            for k in range(0, n, H):
                idx = [j for j in range(k, min(k + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                r = c[t + H] / c[t] - 1.0
                vals.append(-(r - d))
                wts.append(abs(f[t]))

    v = np.array(vals, dtype=float)
    wv = np.array(wts, dtype=float)
    n_cases = int(len(v))

    value, tstat = None, None
    if n_cases >= 2 and wv.sum() > 0:
        m = float(np.sum(v * wv) / np.sum(wv))
        se = np.sqrt(np.sum(wv ** 2 * (v - m) ** 2)) / np.sum(wv) * np.sqrt(n_cases / (n_cases - 1))
        value = m
        tstat = float(m / se) if se > 0 else None
    elif n_cases == 1 and wv.sum() > 0:
        value = float(v[0])

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        med = float(np.median(wv))
        big = v[wv >= med]
        small = v[wv < med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(np.mean(big) - np.mean(small))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure has t >= 2 over at least 30 cases and the larger-forecast half moved further down than the smaller half."
        else:
            status = "inconclusive"
            decided = "The main measure has t >= 2 over at least 30 cases but the supporting check fails, which the plan calls inconclusive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2 over at least 30 cases: the bounces kept rising beyond the coin's drift."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": value,
                         "statistic": ({"name": "t of the weighted mean", "value": tstat} if tstat is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move, larger abs(forecast) half minus smaller half",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
