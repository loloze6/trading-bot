import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.fade_move.last_history_value"
    PPV = "debug_info.components.fade_move.post_pipeline_value"

    # ---------- coin mean daily return over all windows (inside windows only) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- collect rows ----------
    n_active = 0
    n_agree = 0
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            # raw component value: recorded, else recomputed from prices (inside the window)
            r1 = close / close.shift(1) - 1.0
            recomputed = r1 / r1.rolling(20, min_periods=20).std()
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            # post-pipeline value for the regression (forecast as fallback)
            if PPV in d.columns:
                xval = pd.to_numeric(d[PPV], errors="coerce")
                xval = xval.where(xval.notna(), fc)
            else:
                xval = fc

            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True)
            dayk = ts.dt.floor("D")

            active = fc.notna() & (fc != 0)
            # situation check: situation = a graded (non-zero) scaled move; side = against it
            exp_side = -np.sign(raw)
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == exp_side)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            m = active & xval.notna() & (xval != 0) & nxt.notna()
            cm = coin_mean.get(coin, np.nan)
            for i in np.where(m.values)[0]:
                xs.append(float(xval.iloc[i]))
                ys.append(float(nxt.iloc[i]) - cm)
                days.append(dayk.iloc[i])

    threshold_txt = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    main_name = "slope of next-day excess return on post_pipeline forecast (day-clustered t)"
    reading = ("Situation bars are active bars whose raw scaled move (last_history_value, recomputed from prices if missing) "
               "is non-zero with the forecast of the opposite sign; the excess return subtracts the coin's mean 1-bar return "
               "over all its windows; the t uses day-clustered standard errors with a G/(G-1) correction; the top fifth is "
               "|forecast| at or above the 80th percentile of the regression cases; the plan's minimum counts are applied "
               "to the regression cases and, per instructions, give 'not observable' when not met.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"non-zero-forecast bars": 0, "distinct days": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 200 non-zero-forecast bars over 60 days is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"non-zero-forecast bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars take the side against the day's scaled move that the "
                           "plan's Fidelity states (short after an up move, long after a down move)."),
            "reading": reading,
        }

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    days_arr = np.array(days)
    n = len(x)
    n_days = int(len(pd.unique(days_arr))) if n else 0
    counts = {"non-zero-forecast bars": int(n), "distinct days": int(n_days)}

    # supporting check
    sup_val = None
    sup_pass = None
    if n > 0:
        ax = np.abs(x)
        q = np.quantile(ax, 0.8)
        top = ax >= q
        if top.sum() > 0:
            sup_val = float(np.mean(np.sign(x[top]) * y[top]))
            sup_pass = bool(sup_val > 0)

    slope = None
    tstat = None
    if n >= 3 and np.var(x) > 0:
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        slope = float(np.sum(xd * (y - y.mean())) / sxx)
        intercept = y.mean() - slope * x.mean()
        e = y - intercept - slope * x
        sc = pd.Series(xd * e).groupby(pd.Series(days_arr).values).sum().values
        G = len(sc)
        if G > 1:
            var = (G / (G - 1)) * float(np.sum(sc ** 2)) / sxx ** 2
            if var > 0:
                tstat = float(slope / np.sqrt(var))

    sup = {"name": "mean next-day excess return in forecast direction, top fifth of |forecast|",
           "value": sup_val, "passed": sup_pass}
    mm = {"name": main_name, "value": slope,
          "statistic": ({"name": "day-clustered OLS t", "value": tstat} if tstat is not None else None),
          "threshold": threshold_txt}
    sc_out = {"agreement": float(agreement), "passed": True}

    if n < 200 or n_days < 60:
        miss = []
        if n < 200:
            miss.append(f"{n} non-zero-forecast bars (< 200)")
        if n_days < 60:
            miss.append(f"{n_days} distinct days (< 60)")
        return {"status": "not observable", "situation_check": sc_out, "main_measure": mm,
                "supporting_check": sup, "counts": counts,
                "decided_by": "Minimum count not reached: " + " and ".join(miss) + ".",
                "reading": reading}

    if slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the supporting check passes."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {"status": status, "situation_check": sc_out, "main_measure": mm,
            "supporting_check": sup, "counts": counts, "decided_by": decided, "reading": reading}
