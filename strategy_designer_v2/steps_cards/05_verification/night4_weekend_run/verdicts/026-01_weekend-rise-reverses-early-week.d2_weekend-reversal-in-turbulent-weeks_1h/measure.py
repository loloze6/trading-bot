import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    LHV = "debug_info.components.weekend_gain.last_history_value"

    def _ts(df):
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if ts.isna().all():
            ts = pd.to_datetime(df["timestamp"], unit="ms", utc=True, errors="coerce")
        return ts

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = _ts(df)
            start_mon0 = ((ts.dt.weekday == 0) & (ts.dt.hour == 0)).values
            cts = ts + pd.Timedelta(hours=1)
            close_mon0 = ((cts.dt.weekday == 0) & (cts.dt.hour == 0)).values
            is_monday_bar = start_mon0 | close_mon0
            regime_ok = (df["regime"].astype(str) == "mean_reversion").values
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").values
            else:
                lhv = np.full(len(df), np.nan)
            past = np.full(len(df), np.nan)
            if len(df) > H:
                past[H:] = close[H:] / close[:-H] - 1.0
            wk_ret = np.where(np.isfinite(lhv), lhv, past)
            rise = np.isfinite(wk_ret) & (wk_ret > 0)
            active = f != 0
            sit = is_monday_bar & regime_ok & rise & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "abs(forecast)-weighted mean unusual 48-bar fall (short side)"
    thr = "t >= 2 over at least 100 cases to confirm; t <= -2 over at least 100 cases to reject"
    reading = ("The Monday bar is taken as the bar whose start or close time is Monday 00:00 UTC (the engine's clock may read either), "
               "the volatility-rank condition is read from the recorded regime 'mean_reversion' since the detector's components are not "
               "recorded and cannot be rebuilt inside a window, the weekend rise from last_history_value (or the 48-bar price return); "
               "the t of the weighted mean uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); the normal drift is "
               "the coin's mean 48-bar return on the non-overlapping grid of all its windows; the median split puts abs(forecast) above "
               "the median in the larger half and the rest in the smaller half, with unweighted half means.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a nonzero forecast are Monday-00:00 bars after a weekend rise in the "
                           "high-volatility regime with a short forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        grid = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    grid.append(r)
        drift = float(np.mean(grid)) if grid else np.nan
        if not np.isfinite(drift):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in np.nonzero(f != 0)[0]:
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                side = np.sign(f[i])
                xs.append(float(side * (r - drift)) * -1.0 * -1.0 if False else float(side * (r - drift)))
                ws.append(float(abs(f[i])))

    x = np.array(xs, dtype=float)
    wts = np.array(ws, dtype=float)
    n = int(len(x))
    counts = {"cases": n}

    if n < 2 or wts.sum() <= 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 100 cases: the plan's minimum count of 100 cases is not reached.",
            "reading": reading,
        }

    sw = wts.sum()
    m = float((wts * x).sum() / sw)
    se = float(np.sqrt(n / (n - 1.0) * np.sum(wts ** 2 * (x - m) ** 2)) / sw)
    t = float(m / se) if se > 0 else 0.0

    med = float(np.median(wts))
    big = x[wts > med]
    small = x[wts <= med]
    if len(big) > 0 and len(small) > 0:
        diff = float(big.mean() - small.mean())
        chk = bool(diff > 0)
    else:
        diff, chk = None, None

    main = {"name": main_name, "value": m, "statistic": {"name": "t of the weighted mean", "value": t},
            "threshold": thr}
    sup = {"name": "mean unusual fall, larger half minus smaller half of abs(forecast)", "value": diff, "passed": chk}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases: the plan's minimum of 100 cases is not reached."
    elif t >= 2 and chk is True:
        status = "confirmed"
        decided = "Confirm: the weighted mean unusual fall has t >= 2 over at least 100 cases and the size check is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "Reject: the weighted mean unusual fall has t <= -2 over at least 100 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the size check (larger half minus smaller half) is at 0 or below."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the t of the weighted mean unusual fall lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
