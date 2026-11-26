import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.low_close.last_history_value"
    PPV = "debug_info.components.low_close.post_pipeline_value"
    BAND = 2.0
    H = 1
    MIN_CASES = 30
    EPS = 1e-9

    # ---------- per-coin normal drift (mean 1-bar return over all windows, non-overlapping grid) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    n_active = 0
    n_agree = 0
    cases = []  # (day, unusual, ppv)

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            o_h = df["high"].astype(float)
            o_l = df["low"].astype(float)
            o_c = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values

            # ---------- situation from raw values / prices ----------
            rng = o_h - o_l
            cl_px = (o_h - o_c) / rng.replace(0, np.nan)
            if LHV in df.columns:
                cl_rec = pd.to_numeric(df[LHV], errors="coerce")
                cl = cl_rec.where(cl_rec.notna(), cl_px)
            else:
                cl = cl_px
            r1 = o_c.pct_change()
            sd = r1.rolling(30, min_periods=30).std()
            rw = (rng / o_c) / sd.replace(0, np.nan)
            cl_ok = (cl >= 0.75 - EPS).fillna(False).values
            rw_ok = (rw >= 2.0 - EPS).values
            rw_known = rw.notna().values
            situ = cl_ok & np.where(rw_known, rw_ok, True)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

            # ---------- cases: rises of the forecast of at least the band ----------
            ppv = pd.to_numeric(df[PPV], errors="coerce").values if PPV in df.columns else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = o_c.values
            ref = 0.0
            prev_side = 0
            for t in range(len(df)):
                f = fc[t]
                side = int(np.sign(f))
                if side == 0 or side != prev_side:
                    ref = 0.0
                a = abs(f)
                bet = False
                if side != 0 and a - ref >= BAND - EPS:
                    bet = True
                    ref = a
                elif side != 0:
                    ref = min(ref, a)
                prev_side = side
                if bet and side > 0 and t + H < len(df):  # grid of h=1: every bar is its own cell
                    r = c[t + H] / c[t] - 1.0
                    d = drift.get(coin, np.nan)
                    if np.isfinite(r) and np.isfinite(d):
                        u = (r - d) * 1.0  # long direction
                        cases.append((ts.iloc[t].floor("D"), u, ppv[t]))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else agreement >= 0.9

    main_name = "mean next-day unusual move (long, drift removed), day-pooled t"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation checked as range/close over the std (ddof 1) of the last 30 in-window daily returns >= 2 and "
               "close location from the high >= 0.75 (recorded raw value, else from prices), using the location alone on "
               "the first bars of a window where 30 returns are not yet available, profile vetoes not re-checked; cases are "
               "long-side forecast rises of >= 2 points from the lowest level since the last bet, and the supporting split "
               "puts cases strictly above the median post_pipeline_value in the upper half, the rest in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(range/close over 30-day return std >= 2 and close in the bottom quarter of the range)."),
            "reading": reading,
        }

    n = len(cases)
    if n > 0:
        cdf = pd.DataFrame(cases, columns=["day", "u", "ppv"])
        u = cdf["u"].values.astype(float)
        m = float(np.mean(u))
        dev = cdf.assign(d=u - m).groupby("day")["d"].sum().values
        n_days = int(len(dev))
        se = float(np.sqrt(np.sum(dev ** 2)) / n)
        tstat = float(m / se) if se > 0 else None
        sub = cdf.dropna(subset=["ppv"])
        diff = None
        if len(sub) >= 2:
            med = sub["ppv"].median()
            up = sub[sub["ppv"] > med]["u"]
            lo = sub[sub["ppv"] <= med]["u"]
            if len(up) > 0 and len(lo) > 0:
                diff = float(up.mean() - lo.mean())
    else:
        m, tstat, n_days, diff = None, None, 0, None

    sup_pass = None if diff is None else bool(diff > 0)
    counts = {"cases": int(n), "days": int(n_days)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 30 cases."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero standard error)."
    elif m > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 over at least 30 cases, and the upper-half minus lower-half difference is positive."
        else:
            status = "inconclusive"
            decided = "Positive mean with t >= 2 but the nearness difference is at or below 0 (or cannot be computed): inconclusive."
    elif m < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": None if tstat is None else {"name": "t of the mean, cases of one day pooled", "value": tstat},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean unusual move, split at median low_close post_pipeline_value",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
