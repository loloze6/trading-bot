import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    PERIOD = 30
    BAND = 2.0
    MIN_CASES = 30
    COMP = "pierce"

    def _parse(v):
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return None
        return None

    def get_comp(df, cid, field):
        flat = "debug_info.components.%s.%s" % (cid, field)
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, v in enumerate(df["debug_info.components"].to_numpy()):
                d = _parse(v)
                if isinstance(d, dict) and isinstance(d.get(cid), dict):
                    x = d[cid].get(field)
                    try:
                        out[i] = float(x) if x is not None else np.nan
                    except Exception:
                        pass
        return out

    def to_day(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            unit = "ms" if s.abs().max() > 1e11 else "s"
            t = pd.to_datetime(s, unit=unit, utc=True)
        else:
            t = pd.to_datetime(s, utc=True)
        return t.dt.normalize().astype(str).to_numpy()

    n_active = 0
    n_agree = 0
    cases = []  # (coin, day, return, weight)
    coin_mean = {}

    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)

            # non-overlapping grid returns for the coin's normal drift
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)

            # situation: recorded raw value where present, else from prices
            raw = get_comp(df, COMP, "last_history_value")
            L = pd.Series(low).shift(1).rolling(PERIOD, min_periods=PERIOD).min().to_numpy()
            with np.errstate(invalid="ignore"):
                price_sit = (low < L) & (close >= L) & np.isfinite(L)
            sit = np.where(np.isfinite(raw), raw > 0, price_sit)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc < 0)).sum())

            # bets: rise of the short forecast of at least BAND from its lowest level since last bet
            post = get_comp(df, COMP, "post_pipeline_value")
            days = to_day(df["timestamp"])
            ref = 0.0
            side = 0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                s = int(np.sign(fc[i]))
                if s == 0:
                    ref, side = 0.0, 0
                    continue
                if s != side:
                    ref, side = 0.0, s
                mag = abs(fc[i])
                if mag - ref >= BAND:
                    if s < 0:
                        bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)

            # one case per 5-bar grid cell: the first bet in the cell
            for c0 in range(0, n, H):
                idx = [i for i in range(c0, min(c0 + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (close[i] > 0) or not np.isfinite(close[i + H]):
                    continue
                r = close[i + H] / close[i] - 1.0
                wgt = abs(post[i]) if np.isfinite(post[i]) else abs(fc[i])
                cases.append((coin, days[i], r, wgt))
        coin_mean[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean unusual 5-day move per case, short direction (fall positive)"
    thr = "t >= 2 on a fall to confirm (with supporting check); t <= -2 on a rise to reject"
    sup_name = "abs(post_pipeline_value)-weighted mean unusual move >= equal-weighted mean"
    reading = ("Situation checked on the pierce-and-reclaim rule only (recorded pierce raw value > 0, else recomputed "
               "from prices; the profile is added by code), side short; a case is a short bet (forecast rising by at "
               "least 2 points on the short side from its lowest level since the last bet), the first per 5-bar grid "
               "cell of each window, with the 5-bar return inside the window; normal drift is the coin's mean 5-bar "
               "return on the non-overlapping grid of all its windows; t uses deviations summed per day "
               "(clustered by day, G/(G-1) correction); the weight falls back to abs(forecast) if post_pipeline_value is missing.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars on a day that trades "
                           "below the prior 30-day low and closes at or above it."
                           if n_active > 0 else "No bar has a nonzero forecast, so the situation cannot be matched."),
            "reading": reading,
        }

    x = []
    wts = []
    dys = []
    for coin, day, r, wgt in cases:
        m = coin_mean.get(coin, np.nan)
        if not np.isfinite(m) or not np.isfinite(r):
            continue
        x.append(-(r - m))
        wts.append(wgt)
        dys.append(day)
    x = np.array(x, dtype=float)
    wts = np.array(wts, dtype=float)
    n_cases = int(len(x))
    n_days = int(len(set(dys)))

    mean = float(x.mean()) if n_cases else None
    t = None
    if n_cases >= 2:
        dev = pd.Series(x - mean).groupby(np.array(dys)).sum().to_numpy()
        G = len(dev)
        if G >= 2:
            se = np.sqrt(G / (G - 1) * np.sum(dev ** 2)) / n_cases
            t = float(mean / se) if se > 0 else None

    ok_w = np.isfinite(wts) & np.isfinite(x)
    wmean = None
    check = None
    if ok_w.sum() > 0 and wts[ok_w].sum() > 0:
        wmean = float(np.sum(x[ok_w] * wts[ok_w]) / np.sum(wts[ok_w]))
        check = bool(wmean >= mean)

    counts = {"cases": n_cases, "days": n_days}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = "Fewer than 30 cases (%d), so the result is inconclusive by the plan's minimum count." % n_cases
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif mean > 0 and t >= 2:
        if check:
            status = "confirmed"
            decided = "The mean unusual move is a fall with t >= 2 and the weighted mean is at least the equal-weighted mean."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is a fall with t >= 2 but the supporting check fails."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is a rise (a rebound) with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases summed per day", "value": t}
                                       if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name,
                             "value": (float(wmean - mean) if wmean is not None and mean is not None else None),
                             "passed": check},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
