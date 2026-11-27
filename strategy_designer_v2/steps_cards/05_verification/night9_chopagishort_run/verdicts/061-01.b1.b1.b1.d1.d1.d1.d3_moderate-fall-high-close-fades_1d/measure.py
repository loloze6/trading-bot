import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0

    def _ret_pct(close, p):
        c = close.to_numpy(dtype=float)
        out = np.full(len(c), np.nan)
        if len(c) > p:
            out[p:] = (c[p:] / c[:-p] - 1.0) * 100.0
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    frames = {}
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            frames[(coin, w)] = df
            close = df["close"].astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            ret5 = _ret_pct(close, 5)
            ret20 = _ret_pct(close, 20)
            ret60 = _ret_pct(close, 60)
            hi = df["high"].astype(float).to_numpy()
            lo = df["low"].astype(float).to_numpy()
            cl = close.to_numpy()
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            reg_mr = reg == "mean_reversion"
            for i in range(len(df)):
                if f[i] == 0:
                    continue
                n_active += 1
                # profile: volatility percentile cannot be rebuilt (365-bar lookback, warm-up not recorded),
                # so the detector's recorded regime stands for it; price conditions recomputed where computable
                ok = bool(reg_mr[i])
                if not np.isnan(ret60[i]):
                    ok = ok and (-10.0 <= ret60[i] <= 10.0)
                if not np.isnan(ret5[i]):
                    ok = ok and (ret5[i] < 0.0)
                if not np.isnan(ret20[i]):
                    ok = ok and (-20.0 <= ret20[i] <= -10.0)
                if not np.isnan(loc[i]):
                    ok = ok and (loc[i] >= 0.5)
                ok = ok and (f[i] < 0)
                if ok:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean short-direction unusual 5-bar move per case"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"
    reading_base = ("Profile taken from the recorded regime (its volatility percentile cannot be rebuilt from the "
                    "recorded bars) with ret5, ret20, ret60 and close location recomputed from prices where the "
                    "window has the history; a case is the first short bet (rise of |forecast| >= 2) in each 5-bar "
                    "grid cell of a window with a full 5-bar return in that window; 'fewer than 30 cases on fewer "
                    "than 20 distinct days' read as not observable if either count is short; the median split puts "
                    "|forecast| above the median in the larger half and the rest in the smaller half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars inside the choppy "
                           "agitated profile with ret5 < 0, ret20 between -20 and -10 and close location >= 0.5."),
            "reading": reading_base,
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin in sorted(bars.keys()):
        rs = []
        for (c, w), df in frames.items():
            if c != coin:
                continue
            cl = df["close"].astype(float).to_numpy()
            for p in range(0, len(cl) - H, H):
                if np.isfinite(cl[p]) and np.isfinite(cl[p + H]) and cl[p] > 0:
                    rs.append(cl[p + H] / cl[p] - 1.0)
        drift[coin] = float(np.mean(rs)) if rs else np.nan

    # ---------- 3. cases ----------
    cases = []  # (unusual move, |forecast|, day)
    for (coin, w), df in sorted(frames.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
        cl = df["close"].astype(float).to_numpy()
        n = len(df)
        bet = np.zeros(n, dtype=bool)
        base = 0.0
        prev_short = False
        for i in range(n):
            if f[i] < 0:
                mag = -f[i]
                if not prev_short:
                    base = 0.0
                if mag - base >= BAND:
                    bet[i] = True
                    base = mag
                else:
                    base = min(base, mag)
                prev_short = True
            else:
                prev_short = False
                base = 0.0
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bet[i]]
            if not idx:
                continue
            i = idx[0]
            if i + H >= n or not np.isfinite(drift.get(coin, np.nan)):
                continue
            if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H]) and cl[i] > 0):
                continue
            r = cl[i + H] / cl[i] - 1.0
            um = -(r - drift[coin])
            ts = df["timestamp"].iloc[i]
            day = str(ts.date()) if pd.notna(ts) else f"{coin}-{w}-{i}"
            cases.append((um, abs(f[i]), day))

    n_cases = len(cases)
    days = sorted(set(c[2] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_um = float(np.mean([c[0] for c in cases])) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        x = np.array([c[0] for c in cases])
        m = x.mean()
        dser = pd.Series(x - m).groupby([c[2] for c in cases]).sum().to_numpy()
        var = (n_days / (n_days - 1.0)) * np.sum(dser ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(m / se) if se > 0 else None

    sup_val = None
    if n_cases >= 2:
        absf = np.array([c[1] for c in cases])
        x = np.array([c[0] for c in cases])
        med = np.median(absf)
        big = x[absf > med]
        small = x[absf <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    main = {"name": main_name, "value": mean_um,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together", "value": t_val},
            "threshold": threshold}
    supporting = {"name": "larger-|forecast| half minus smaller half, mean unusual move",
                  "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} cases on {n_days} distinct days (plan needs 30 cases on 20 days)."
    elif mean_um is None or t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither confirm nor reject rule is met."
    elif mean_um > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-direction unusual move above 0 with t >= 2 and the supporting check above 0."
        else:
            status = "inconclusive"
            decided = "Mean short-direction unusual move above 0 with t >= 2 but the supporting check fails."
    elif mean_um < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2: prices rose after these closes."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-direction unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
