import numpy as np
import pandas as pd


def measure(bars):
    RET_COL = "debug_info.components.ret14.last_history_value"
    H = 2
    MIN_THURSDAYS = 100

    # ---------- per-coin mean 2-bar return over all windows (non-overlapping grid) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx) == 0:
                continue
            r = c[idx + H] / c[idx] - 1.0
            rets.extend(list(r[np.isfinite(r)]))
        coin_mean[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    xs, ys, keys = [], [], []

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # Situation: the bar's close is Thursday's close, i.e. the coming daily bar starts on Friday.
            next_start = ts + pd.Timedelta(days=1)
            is_sit = (next_start.dt.weekday == 4).to_numpy()

            # 14-bar return: recorded raw value, else recomputed from closes inside the window.
            rec = (pd.to_numeric(df[RET_COL], errors="coerce").to_numpy(dtype=float)
                   if RET_COL in df.columns else np.full(n, np.nan))
            recomp = np.full(n, np.nan)
            if n > 14:
                recomp[14:] = close[14:] / close[:-14] - 1.0
            ret14 = np.where(np.isfinite(rec), rec, recomp)

            active = np.isfinite(fc) & (fc != 0)
            exp_side = np.sign(ret14)
            agree = active & is_sit & np.isfinite(ret14) & (exp_side != 0) & (np.sign(fc) == exp_side)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # Cases: Thursday-close bars with a recorded forecast and a 2-bar return inside the window.
            cm = coin_mean.get(coin, np.nan)
            for i in np.where(is_sit)[0]:
                if i + H >= n or not np.isfinite(fc[i]):
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or not np.isfinite(cm):
                    continue
                xs.append(fc[i])
                ys.append(r - cm)
                keys.append(ts.iloc[i].strftime("%Y-%m-%d"))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "slope of the 2-bar forward return minus the coin's mean 2-bar return, regressed on the forecast, on Thursday-close bars"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 100 distinct Thursdays"
    reading = ("A Thursday-close bar is a bar whose next daily bar starts on a Friday (UTC); the expected side is the sign of the "
               "recorded 14-bar return (recomputed from closes where not recorded); the coin's mean 2-bar return is taken on the "
               "non-overlapping grid of all its windows; every Thursday-close bar with a recorded forecast (zero included) and an "
               "in-window 2-bar return is a case; the t is an OLS slope t with standard errors clustered by Thursday date "
               "(small-sample correction G/(G-1)*(N-1)/(N-2)); fewer than 100 distinct Thursdays gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on its side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Thursday-close bars whose forecast sign "
                           "matches the sign of the 14-bar return, as the plan's Fidelity requires."),
            "reading": reading,
        }

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    k = np.asarray(keys)
    n_cases = int(len(x))
    n_thu = int(len(np.unique(k))) if n_cases else 0
    counts = {"distinct Thursdays": n_thu, "cases (coin-Thursdays)": n_cases}

    slope, t = None, None
    if n_cases >= 3:
        xm, ym = x.mean(), y.mean()
        dx = x - xm
        sxx = float(np.sum(dx ** 2))
        if sxx > 0:
            b = float(np.sum(dx * (y - ym)) / sxx)
            a = ym - b * xm
            e = y - a - b * x
            score = pd.Series(dx * e).groupby(k).sum().to_numpy()
            G = len(score)
            if G > 1:
                var = float(np.sum(score ** 2)) / sxx ** 2
                var *= (G / (G - 1.0)) * ((n_cases - 1.0) / max(n_cases - 2.0, 1.0))
                se = np.sqrt(var)
                t = float(b / se) if se > 0 else None
            slope = b

    stat = {"name": "t of the OLS slope, clustered by Thursday date", "value": t} if t is not None else None

    if n_thu < MIN_THURSDAYS:
        status = "not observable"
        decided = f"Only {n_thu} distinct Thursdays with a recorded forecast and an in-window 2-bar return, under the plan's minimum of 100."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation in the forecast), so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 over at least 100 distinct Thursdays (the plan's confirm rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 over at least 100 distinct Thursdays (the plan's reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which neither confirms nor rejects (the plan's inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": float(slope) if slope is not None else None,
                         "statistic": stat,
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
