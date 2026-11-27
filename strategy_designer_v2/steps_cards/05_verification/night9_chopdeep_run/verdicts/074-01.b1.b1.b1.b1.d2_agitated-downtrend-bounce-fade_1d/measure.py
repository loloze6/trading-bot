import numpy as np
import pandas as pd


def measure(bars):
    EPS = 1e-9
    BAND = 2.0
    W_COL = "debug_info.components.width.last_history_value"
    L_COL = "debug_info.components.near_high.last_history_value"

    def num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    cases = []  # (coin, day, forecast, next_ret)
    coin_mean = {}

    for coin, wins in bars.items():
        # coin's mean daily (1-bar) return over all its windows, never across windows
        all_r = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            c = pd.to_numeric(df["close"], errors="coerce").values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                all_r.append(r[np.isfinite(r)])
        rr = np.concatenate(all_r) if all_r else np.array([])
        coin_mean[coin] = float(np.mean(rr)) if rr.size else np.nan

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            if df.empty:
                continue
            o = pd.to_numeric(df["open"], errors="coerce")
            h = pd.to_numeric(df["high"], errors="coerce")
            l = pd.to_numeric(df["low"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # up day: 1-bar return > 0 (inside the window)
            up_ret = c / c.shift(1) - 1.0

            # range over its 20-bar mean bar range (current bar included), recomputed as fallback
            rng = h - l
            width_rc = rng / rng.rolling(20, min_periods=20).mean()
            width = num(df, W_COL)
            width = width.where(width.notna(), width_rc)

            # close location in range (1 at the high), recomputed as fallback
            loc_rc = (c - l) / rng.replace(0, np.nan)
            loc = num(df, L_COL)
            loc = loc.where(loc.notna(), loc_rc)

            situ = (up_ret > 0) & (width >= 1.0 - EPS) & (loc >= 0.75 - EPS)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

            # ---------- cases: short bets of at least the band ----------
            nxt = c.shift(-1) / c - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ref = 0.0
            prev_short = False
            for i in range(len(df)):
                fi = float(f.iloc[i])
                if fi < 0:
                    m = -fi
                    if not prev_short:
                        ref = 0.0
                    if m - ref >= BAND - EPS:
                        if np.isfinite(nxt.iloc[i]):
                            cases.append((coin, ts.iloc[i].floor("D"), fi, float(nxt.iloc[i])))
                        ref = m
                    else:
                        ref = min(ref, m)
                    prev_short = True
                else:
                    ref = 0.0
                    prev_short = False

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90
    main_name = "mean short-side unusual next-day move (next-day return minus coin's mean daily return, sign flipped)"
    threshold = "confirm: mean > 0 with t >= 2 (cases of one day grouped); reject: t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct days with cases": 0},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short bars of the plan's "
                           "situation (up day, range >= its 20-day mean bar range, close in the top quarter)"
                           if n_active > 0 else "the record has no bar with a non-zero forecast"),
            "reading": "situation checked on the adapted regime's three conditions, the market-profile veto only narrowing it.",
        }

    cdf = pd.DataFrame(cases, columns=["coin", "day", "forecast", "nxt"])
    if not cdf.empty:
        cdf["mu"] = cdf["coin"].map(coin_mean)
        cdf["x"] = -(cdf["nxt"] - cdf["mu"])
        cdf = cdf[np.isfinite(cdf["x"])]
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    def clustered_t(sub):
        if len(sub) < 2:
            return np.nan, np.nan
        x = sub["x"].values
        mean = float(np.mean(x))
        dev = pd.Series(x - mean).groupby(sub["day"].values).sum().values
        D = len(dev)
        if D < 2:
            return mean, np.nan
        var = np.sum(dev ** 2) * D / (D - 1) / (len(x) ** 2)
        se = np.sqrt(var)
        return mean, (float(mean / se) if se > 0 else np.nan)

    mean, t = clustered_t(cdf) if n_cases else (np.nan, np.nan)

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        a = cdf["forecast"].abs()
        med = float(a.median())
        big = cdf[a > med]["x"]
        small = cdf[a <= med]["x"]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": n_cases, "distinct days with cases": n_days}

    def clean(v):
        return None if v is None or not np.isfinite(v) else float(v)

    if n_days < 30:
        status = "not observable"
        decided = f"only {n_days} distinct days with cases, fewer than the plan's minimum of 30."
    elif np.isfinite(t) and mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "the mean short-side unusual move is above 0 with t >= 2 and the larger-|forecast| half beats the smaller half."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = "the mean short-side unusual move has t <= -2: the next day rises more than usual after such days."
    elif np.isfinite(t) and mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "a confirming main measure whose larger half does not beat the smaller half."
    else:
        status = "inconclusive"
        decided = "the t of the mean short-side unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": clean(mean),
            "statistic": {"name": "t of the mean, cases of one day grouped", "value": clean(t)},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual move of larger-|forecast| half minus smaller half",
            "value": clean(sup_val) if sup_val is not None else None,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are short bets (forecast moving at least 2 points further short from its lowest short level "
                    "since the last bet, from 0 after flat or a side change) with the coin's mean taken over all next-day "
                    "returns of all its windows, the t uses per-day summed deviations with a D/(D-1) correction, the median "
                    "split puts ties in the smaller half, and the situation check uses the adapted regime's three conditions "
                    "(the profile veto only narrows it)."),
    }
