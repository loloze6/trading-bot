import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    P = 14
    LHV = "debug_info.components.ret14.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = the coin's 14-day return; outcome = a higher return follows,
    # so the expected side is long after a 14-day rise and short after a 14-day fall.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            lhv = df[LHV].astype(float).values if LHV in df.columns else np.full(len(df), np.nan)
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                if i >= P and close[i - P] > 0:
                    r = close[i] / close[i - P] - 1.0
                else:
                    r = lhv[i]
                n_active += 1
                if np.isfinite(r) and r != 0 and np.sign(r) == np.sign(f):
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of coin-demeaned non-overlapping 7-bar forward return on forecast"
    threshold = "confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2"
    sup_name = "book mean daily gain before costs minus gain from market's own rise (timing)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping cases": None},
            "decided_by": (f"Only {agreement:.1%} of active bars have a forecast whose sign matches the sign of the "
                           "coin's 14-day return, below 90%: the config does not go long after 14-day rises and "
                           "short after 14-day falls as the plan's Fidelity says."),
            "reading": "The 14-day return was computed from closes inside the window, and from last_history_value "
                       "on the first 14 bars of a window.",
        }

    # ---------- 2. Main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                if not np.isfinite(fc[i]):
                    continue
                rows.append((coin, fc[i], close[i + H] / close[i] - 1.0))
    s = pd.DataFrame(rows, columns=["coin", "f", "r"])
    n = int(len(s))

    slope = None
    tval = None
    if n >= 3:
        s["rd"] = s["r"] - s.groupby("coin")["r"].transform("mean")
        x = s["f"].values
        y = s["rd"].values
        if np.std(x) > 0:
            res = stats.linregress(x, y)
            slope = float(res.slope)
            tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------- 3. Supporting check: timing part of book gain ----------
    coin_daily = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_daily[coin] = float(np.mean(allr)) if len(allr) else np.nan

    recs = []
    for coin, wins in bars.items():
        mu = coin_daily[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            a = df[ALLOC].astype(float).values
            ts = pd.to_datetime(df["timestamp"]).values
            for i in range(len(df) - 1):
                g = c[i + 1] / c[i] - 1.0
                if not (np.isfinite(a[i]) and np.isfinite(g) and np.isfinite(mu)):
                    continue
                recs.append((ts[i + 1], a[i] * g, a[i] * mu))
    timing = None
    sup_passed = None
    if recs:
        b = pd.DataFrame(recs, columns=["ts", "gain", "mkt"])
        d = b.groupby("ts")[["gain", "mkt"]].mean()
        timing = float(d["gain"].mean() - d["mkt"].mean())
        sup_passed = bool(timing > 0)

    # ---------- 4. Decision ----------
    if n < 100 or tval is None:
        status = "not observable"
        decided = f"Only {n} non-overlapping 7-bar cases (or no usable slope), below the plan's minimum of 100."
    elif slope > 0 and tval >= 2 and sup_passed:
        status = "confirmed"
        decided = "Slope positive with t >= 2 and the timing part of the book's gain is above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Slope negative with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the timing gain is 0 or below (or not measurable)."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": timing, "passed": sup_passed},
        "counts": {"non-overlapping cases": n},
        "decided_by": decided,
        "reading": ("Each coin's mean 7-bar return is the mean of its non-overlapping grid returns over all windows; "
                    "the book's gain before costs is the held allocation times the next close-to-close return, "
                    "averaged over coins per day, and its market part uses each coin's mean daily return over all windows."),
    }
