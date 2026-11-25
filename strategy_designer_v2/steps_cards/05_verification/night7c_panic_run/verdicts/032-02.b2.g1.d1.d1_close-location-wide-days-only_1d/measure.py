import numpy as np
import pandas as pd


def measure(bars):
    LH = "debug_info.components.loc_width.last_history_value"
    PP = "debug_info.components.loc_width.post_pipeline_value"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- build rows ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            h = _num(d, "high").to_numpy(dtype=float)
            l = _num(d, "low").to_numpy(dtype=float)
            c = _num(d, "close").to_numpy(dtype=float)
            fc = _num(d, "forecast").to_numpy(dtype=float)
            lh = _num(d, LH).to_numpy(dtype=float)
            pp = _num(d, PP).to_numpy(dtype=float)
            regime = d["regime"].astype(str).to_numpy() if "regime" in d.columns else np.array([""] * len(d))
            rng = h - l
            loc = 2.0 * c - h - l
            # mean range of bars t-20..t-1, inside the window
            M_px = pd.Series(rng).shift(1).rolling(20, min_periods=20).mean().to_numpy()
            # mean range recovered from the component's raw value: lh = loc / M
            with np.errstate(divide="ignore", invalid="ignore"):
                M_lh = np.where(np.isfinite(lh) & (lh != 0), loc / lh, np.nan)
            M = np.where(np.isfinite(M_px), M_px, M_lh)
            with np.errstate(invalid="ignore"):
                wide = np.isfinite(M) & (rng > M * (1.0 + 1e-12))
            exp_side = -np.sign(loc)  # long after a low close, short after a high close

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            ok = active & wide & (np.sign(fc) == exp_side) & (exp_side != 0)
            n_agree += int(ok.sum())

            nxt = np.full(len(c), np.nan)
            if len(c) > 1:
                nxt[:-1] = c[1:] / c[:-1] - 1.0
            exc = nxt - coin_mean[coin]
            days = ts.dt.floor("D").astype("int64").to_numpy()
            for i in range(len(d)):
                if regime[i] == "mean_reversion":
                    rows.append((coin, w, days[i], pp[i], fc[i], exc[i]))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    sit = {"agreement": agreement, "passed": passed}

    main_name = "pooled slope of next-day excess return on post_pipeline_value, mean_reversion bars"
    thr = "confirm: slope > 0 with day-clustered t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2 or supporting mean < 0 with t <= -2; at least 300 distinct days with regime bars"
    reading = ("Width is recomputed per window as range > mean range of the previous 20 bars (from prices, or from "
               "last_history_value where the window has under 20 prior bars); the slope is OLS with intercept and "
               "day-clustered standard error (scores summed per UTC day, G/(G-1) correction); the supporting check "
               "uses the floor(n/3) regime bars with the largest |forecast| and a day-clustered t of the mean; the "
               "day count is the distinct UTC days of regime bars with a valid forecast value and next-day return.")

    if n_active == 0:
        return {"status": "not observable", "situation_check": sit,
                "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
                "supporting_check": None, "counts": {"distinct days with regime bars": 0},
                "decided_by": "The record has no active bars, so neither the situation nor the criterion can be observed.",
                "reading": reading}
    if not passed:
        return {"status": "mismatch", "situation_check": sit,
                "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
                "supporting_check": None, "counts": {},
                "decided_by": ("Fewer than 90% of the non-zero forecasts fall on days wider than the previous 20-day "
                               "mean range with a long after a low close / short after a high close, as the Fidelity states."),
                "reading": reading}

    R = pd.DataFrame(rows, columns=["coin", "win", "day", "pp", "fc", "exc"])

    # ---------- main measure: pooled slope, day-clustered t ----------
    A = R[np.isfinite(R["pp"]) & np.isfinite(R["exc"])].copy()
    n_days = int(A["day"].nunique())
    slope = None
    t_slope = None
    if len(A) >= 3 and A["pp"].var() > 0:
        x = A["pp"].to_numpy(float)
        y = A["exc"].to_numpy(float)
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        b = float(np.sum(xd * (y - y.mean())) / sxx)
        a = y.mean() - b * x.mean()
        e = y - a - b * x
        sc = pd.Series(xd * e).groupby(A["day"].to_numpy()).sum().to_numpy()
        G = len(sc)
        if G > 1:
            var = (G / (G - 1)) * float(np.sum(sc ** 2)) / sxx ** 2
            slope = b
            t_slope = float(b / np.sqrt(var)) if var > 0 else None
        else:
            slope = b

    # ---------- supporting check ----------
    S = R[np.isfinite(R["fc"]) & np.isfinite(R["exc"])].copy()
    S["absf"] = S["fc"].abs()
    k = len(S) // 3
    sup_mean = None
    sup_t = None
    if k >= 2:
        top = S.sort_values("absf", ascending=False, kind="mergesort").head(k)
        v = (np.sign(top["fc"].to_numpy(float)) * top["exc"].to_numpy(float))
        m = float(v.mean())
        dev = pd.Series(v - m).groupby(top["day"].to_numpy()).sum().to_numpy()
        G = len(dev)
        sup_mean = m
        if G > 1:
            se = np.sqrt((G / (G - 1)) * float(np.sum(dev ** 2))) / len(v)
            sup_t = float(m / se) if se > 0 else None
    sup_pass = (sup_mean is not None and sup_mean > 0)
    supporting = {"name": "mean of sign(forecast) x next-day excess return, top third by |forecast|",
                  "value": sup_mean, "passed": bool(sup_pass) if sup_mean is not None else None}

    counts = {"distinct days with regime bars": n_days,
              "regime bars in the slope": int(len(A)),
              "bars in the top third": int(k)}
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "day-clustered t of the slope", "value": t_slope} if t_slope is not None else None),
            "threshold": thr}

    if n_days < 300:
        return {"status": "not observable", "situation_check": sit, "main_measure": main,
                "supporting_check": supporting, "counts": counts,
                "decided_by": f"Only {n_days} distinct days with regime bars, below the plan's minimum of 300.",
                "reading": reading}
    if slope is None or t_slope is None:
        return {"status": "inconclusive", "situation_check": sit, "main_measure": main,
                "supporting_check": supporting, "counts": counts,
                "decided_by": "The slope or its t could not be computed, so neither the confirm nor the reject rule is met.",
                "reading": reading}

    if (slope < 0 and t_slope <= -2) or (sup_mean is not None and sup_t is not None and sup_mean < 0 and sup_t <= -2):
        status = "rejected"
        if slope < 0 and t_slope <= -2:
            dec = f"Reject: the slope is negative with t = {t_slope:.2f} <= -2."
        else:
            dec = f"Reject: the supporting check's mean is below 0 with t = {sup_t:.2f} <= -2."
    elif slope > 0 and t_slope >= 2 and sup_pass:
        status = "confirmed"
        dec = f"Confirm: the slope is positive with t = {t_slope:.2f} >= 2 and the supporting check's mean is above 0."
    else:
        status = "inconclusive"
        if slope > 0 and t_slope >= 2 and not sup_pass:
            dec = "Inconclusive: a positive slope with t >= 2 but a failed supporting check."
        else:
            dec = f"Inconclusive: the slope's t = {t_slope:.2f} lies between -2 and 2 and no reject rule is met."

    return {"status": status, "situation_check": sit, "main_measure": main,
            "supporting_check": supporting, "counts": counts,
            "decided_by": dec, "reading": reading}
