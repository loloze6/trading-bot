import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    FC = "forecast"
    RAW = "debug_info.components.range_pos.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the rising calm profile (not vetoed to chop)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            hh = high.rolling(20, min_periods=20).max()
            ll = low.rolling(20, min_periods=20).min()
            rng = hh - ll
            pos_re = (2.0 * (close - ll) / rng.replace(0, np.nan) - 1.0).values
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
                raw = np.where(np.isnan(raw), pos_re, raw)
            else:
                raw = pos_re
            regime = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            active = f != 0
            n_active += int(active.sum())
            in_profile = regime == PROFILE_REGIME
            side_ok = np.sign(np.nan_to_num(raw, nan=0.0)) == np.sign(f)
            n_agree += int((active & in_profile & side_ok & ~np.isnan(raw)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of 10-bar forward return minus coin mean 10-bar return on forecast (non-overlapping grid, non-zero forecast, pooled)"
    threshold = "confirm: slope > 0 with t >= 2 and supporting check passed; reject: slope < 0 with t <= -2"
    sup_name = "mean directional excess return, top third of |forecast| minus bottom third"
    reading = ("The situation is the regime column equal to the profile regime 'unknown' (rising calm, not vetoed) with the "
               "forecast's sign equal to the sign of the raw range position; the slope is an OLS fit with intercept and a "
               "day-clustered standard error (G/(G-1) correction); the coin's mean 10-bar return is taken on the "
               "non-overlapping grid of all its windows; thirds of |forecast| are equal-count splits of the cases sorted "
               "by |forecast|; the plan's minimum of 100 cases, if not reached, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping grid cases with a non-zero forecast": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are rising-calm-profile bars whose forecast "
                           "sign matches the sign of the close's 20-bar range position."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d[FC], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D").values
            for i in range(0, len(d), H):
                if i + H >= len(d):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                rows.append((coin, f[i], r, ts[i]))
        coin_mean[coin] = float(np.mean(all_r)) if all_r else np.nan

    if rows:
        g = pd.DataFrame(rows, columns=["coin", "f", "r", "day"])
        g["ex"] = g["r"] - g["coin"].map(coin_mean)
        g = g[np.isfinite(g["f"]) & (g["f"] != 0) & np.isfinite(g["ex"])].reset_index(drop=True)
    else:
        g = pd.DataFrame(columns=["coin", "f", "r", "day", "ex"])
    n = int(len(g))
    n_days = int(g["day"].nunique()) if n else 0
    counts = {"non-overlapping grid cases with a non-zero forecast": n, "days": n_days}

    slope = None
    tstat = None
    if n >= 3:
        x = g["f"].values.astype(float)
        y = g["ex"].values.astype(float)
        xc = x - x.mean()
        sxx = float((xc ** 2).sum())
        if sxx > 0:
            slope = float((xc * (y - y.mean())).sum() / sxx)
            a = y.mean() - slope * x.mean()
            e = y - a - slope * x
            sc = pd.Series(xc * e).groupby(g["day"].values).sum().values
            G = len(sc)
            var = float((sc ** 2).sum()) / sxx ** 2
            if G > 1:
                var *= G / (G - 1)
            se = np.sqrt(var)
            tstat = float(slope / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n >= 3:
        order = np.argsort(np.abs(g["f"].values), kind="mergesort")
        parts = np.array_split(order, 3)
        dirx = np.sign(g["f"].values) * g["ex"].values
        bot = dirx[parts[0]]
        top = dirx[parts[2]]
        if len(bot) and len(top):
            sup_val = float(top.mean() - bot.mean())
            sup_pass = bool(sup_val > 0)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} non-overlapping grid cases with a non-zero forecast, below the plan's minimum of 100."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top third of |forecast| earns more in its direction than the bottom third."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check fails (top third does not beat bottom third)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "t of slope (day-clustered)", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
