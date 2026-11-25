import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"

    def _ts(s):
        t = pd.to_datetime(s, utc=True, errors="coerce")
        if t.isna().all():
            t = pd.to_datetime(s, unit="ms", utc=True, errors="coerce")
        return t

    # ---------- collect per-coin frames, drift over all windows ----------
    rows = []
    agree_n = 0
    active_n = 0
    for coin, wins in bars.items():
        coin_rets = []
        coin_frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d = d.sort_values("timestamp") if "timestamp" in d.columns else d
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float)
            ret_today = close / close.shift(1) - 1.0          # inside the window only
            nxt = close.shift(-1) / close - 1.0                # inside the window only
            raw = pd.to_numeric(d[RAW], errors="coerce").astype(float) if RAW in d.columns \
                else pd.Series(np.nan, index=d.index)
            # situation: today's (vol-scaled) return is a fall; raw where recorded, else from prices
            raw_sign = raw.where(raw.notna(), ret_today)
            situation = raw_sign < 0
            active = fc.notna() & (fc != 0)
            active_n += int(active.sum())
            agree_n += int((active & situation & (fc > 0)).sum())
            coin_rets.append(nxt.dropna().values)
            day = _ts(d["timestamp"]).dt.floor("D")
            coin_frames.append(pd.DataFrame({"coin": coin, "window": w, "day": day.values,
                                             "fc": fc.values, "nxt": nxt.values}))
        if not coin_frames:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        drift = float(np.mean(allr)) if len(allr) else np.nan
        cf = pd.concat(coin_frames, ignore_index=True)
        cf["excess"] = cf["nxt"] - drift
        rows.append(cf)

    agreement = float(agree_n / active_n) if active_n > 0 else 0.0
    sit_passed = bool(active_n > 0 and agreement >= 0.90)

    main_name = "slope of next-day return minus drift against forecast, on forecast > 0"
    main_thr = "slope t (by day) >= 2 confirms (with supporting check); <= -2 rejects"
    sup_name = "forecast-weighted mean next-day excess return, t by day"

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_n)},
            "decided_by": f"Only {agreement:.1%} of active bars are long on a down day (raw vol-scaled return < 0), below the 90 % required by the plan's situation and side.",
            "reading": "The situation is taken as a bar whose raw vol-scaled return is negative (recomputed from closes where the raw value is missing), on the long side.",
        }

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(
        columns=["coin", "window", "day", "fc", "nxt", "excess"])
    cases = data[(data["fc"] > 0) & data["excess"].notna() & data["day"].notna()].copy()
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique())

    # ---------- main: OLS slope, day-clustered t ----------
    slope = None
    slope_t = None
    if n_cases >= 3 and n_days >= 2:
        x = cases["fc"].values.astype(float)
        y = cases["excess"].values.astype(float)
        xm, ym = x.mean(), y.mean()
        sxx = float(np.sum((x - xm) ** 2))
        if sxx > 0:
            b = float(np.sum((x - xm) * (y - ym)) / sxx)
            a = ym - b * xm
            e = y - a - b * x
            sc = pd.Series((x - xm) * e).groupby(cases["day"].values).sum().values
            G = len(sc)
            var = float(np.sum(sc ** 2)) / sxx ** 2 * (G / (G - 1))
            slope = b
            slope_t = float(b / np.sqrt(var)) if var > 0 else None

    # ---------- supporting: forecast-weighted mean, day-clustered t ----------
    wmean = None
    wmean_t = None
    if n_cases >= 2 and n_days >= 2:
        wts = cases["fc"].values.astype(float)
        y = cases["excess"].values.astype(float)
        W = float(wts.sum())
        if W > 0:
            m = float(np.sum(wts * y) / W)
            dev = pd.Series(wts * (y - m) / W).groupby(cases["day"].values).sum().values
            G = len(dev)
            se = float(np.sqrt(np.sum(dev ** 2) * G / (G - 1)))
            wmean = m
            wmean_t = float(m / se) if se > 0 else None

    sup_passed = None
    if wmean is not None and wmean_t is not None:
        sup_passed = bool(wmean > 0 and wmean_t >= 2)

    counts = {"distinct days with forecast > 0": n_days, "cases (coin-days with forecast > 0)": n_cases}

    if n_days < 300:
        status = "not observable"
        decided = f"Only {n_days} distinct days with forecast > 0 across the coins, under the plan's minimum of 300."
    elif (slope_t is not None and slope_t <= -2) or (wmean_t is not None and wmean_t <= -2):
        status = "rejected"
        decided = "Reject rule met: the slope's t is <= -2 or the weighted mean excess return has t <= -2."
    elif slope_t is not None and slope_t >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm rule met: the slope's t is >= 2 and the weighted mean excess return is > 0 with t >= 2."
    else:
        status = "inconclusive"
        decided = "Neither rule met: the slope's t and the weighted mean's t do not reach the confirm (both) or reject thresholds."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "slope t, day-clustered", "value": slope_t} if slope_t is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": "Every bar with forecast > 0 and a next close in its window is a case (1-bar horizon, so the grid is every bar), drift is the coin's mean next-day return over all its windows, both t's sum each day's contributions across coins into one cluster (with the G/(G-1) correction), and the plan's 'fewer than 300 days' is reported as not observable.",
    }
