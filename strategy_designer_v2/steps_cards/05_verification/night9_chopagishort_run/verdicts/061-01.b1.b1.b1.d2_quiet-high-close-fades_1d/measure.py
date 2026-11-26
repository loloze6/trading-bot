import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_DAYS = 30
    COMP = "small_gain"

    def _comp_series(df, comp, field):
        flat = "debug_info.components.%s.%s" % (comp, field)
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce").reset_index(drop=True)
        vals = []
        if "debug_info.components" in df.columns:
            for x in df["debug_info.components"].tolist():
                v = np.nan
                d = x
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(comp)
                    if isinstance(c, dict):
                        try:
                            v = float(c.get(field))
                        except Exception:
                            v = np.nan
                vals.append(v)
        else:
            vals = [np.nan] * len(df)
        return pd.Series(vals, dtype=float)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df0 in wins.items():
            if df0 is None or len(df0) == 0:
                continue
            df = df0.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rng = high - low
            cl = (close - low) / rng.where(rng > 0)
            # gain: recorded centred value (gain - 1) where recorded, else rebuilt from prices
            rec = _comp_series(df, COMP, "last_history_value")
            r1 = close / close.shift(1) - 1.0
            mabs = r1.abs().rolling(20, min_periods=20).mean()
            gain_px = r1 / mabs.where(mabs > 0)
            gain = (rec + 1.0).where(rec.notna(), gain_px)
            profile = df["regime"].astype(str).str.lower() != "chop"
            situation = profile & (cl >= 0.8) & (gain > 0.0) & (gain < 1.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
            prepared[(coin, w)] = (df, close, fc)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("The profile is read from the recorded regime (not 'chop', since its 365-bar volatility percentile "
               "cannot be rebuilt from the recorded bars), the gain from the recorded small_gain raw value + 1 "
               "(else rebuilt from prices with the 20-bar window including the bar), a case is the first short bet "
               "(rise of the short forecast of at least 2 points) in each 5-bar grid cell, forecast size is |forecast|, "
               "the correlation is Pearson, and the day-clustered t uses summed daily deviations with a D/(D-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 5-day move in the short's direction", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2 (confirm); mean < 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the active bars (%.1f %%) are high-close (>= 80 %% of range), small-gain "
                           "(0 < gain < 1 usual move) up days in the choppy-agitated profile with a short forecast."
                           % (100 * agreement)),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    coin_rets = {}
    for (coin, w), (df, close, fc) in prepared.items():
        c = close.values
        for p in range(0, len(c) - H, H):
            if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                coin_rets.setdefault(coin, []).append(c[p + H] / c[p] - 1.0)
    for coin, lst in coin_rets.items():
        drift[coin] = float(np.mean(lst)) if lst else np.nan

    # ---------- cases ----------
    cases = []  # (day, unusual, size)
    for (coin, w), (df, close, fc) in prepared.items():
        c = close.values
        f = fc.values
        ts = pd.to_datetime(df["timestamp"], utc=True)
        ref = 0.0
        bet = np.zeros(len(f), dtype=bool)
        for i in range(len(f)):
            if f[i] < 0:
                s = -f[i]
                ref = min(ref, s)
                if s - ref >= BAND:
                    bet[i] = True
                    ref = s
            else:
                ref = 0.0
        for start in range(0, len(f), H):
            idx = [i for i in range(start, min(start + H, len(f))) if bet[i]]
            if not idx:
                continue
            i = idx[0]
            if i + H >= len(c):
                continue
            if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                continue
            d = drift.get(coin, np.nan)
            if not np.isfinite(d):
                continue
            ret = c[i + H] / c[i] - 1.0
            unusual = -(ret - d)
            cases.append((ts.iloc[i].normalize(), float(unusual), float(abs(f[i]))))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)

    mean_u = None
    t = None
    corr = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        sz = np.array([x[2] for x in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([x[0] for x in cases]).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
            t = float(mean_u / np.sqrt(var)) if var > 0 else None
        if n_cases > 2 and np.std(u) > 0 and np.std(sz) > 0:
            corr = float(np.corrcoef(sz, u)[0, 1])

    corr_pass = None if corr is None else bool(corr > 0)
    counts = {"distinct days with cases": int(n_days), "cases": int(n_cases)}
    main = {"name": "mean unusual 5-day move in the short's direction",
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None,
            "threshold": "mean > 0 with t >= 2 and correlation > 0 (confirm); mean < 0 with t <= -2 (reject)"}
    supp = {"name": "correlation of forecast size with unusual move", "value": corr, "passed": corr_pass}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 30 distinct days with cases (%d), the plan's minimum count." % n_days
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2:
        if corr_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and the size-move correlation is above 0."
        else:
            status = "inconclusive"
            decided = "A confirm-level t whose correlation check fails is inconclusive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2: the price rises more than its usual drift after high closes on small gains."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
