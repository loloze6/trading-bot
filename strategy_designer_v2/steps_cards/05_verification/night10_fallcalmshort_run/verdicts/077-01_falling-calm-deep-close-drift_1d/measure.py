import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.peak_depth.last_history_value"
    PPV = "debug_info.components.peak_depth.post_pipeline_value"
    H = 3
    MIN_CASES = 100
    MIN_DAYS = 60

    def prep(df):
        d = df.copy().reset_index(drop=True)
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        for c in ["open", "high", "low", "close", "postRebalance_current_allocation"]:
            if c in d.columns:
                d[c] = pd.to_numeric(d[c], errors="coerce")
        for c in [LHV, PPV]:
            if c in d.columns:
                d[c] = pd.to_numeric(d[c], errors="coerce")
            else:
                d[c] = np.nan
        # Rebuild the depth from prices where the component was not recorded
        # (only possible once 20 bars of the window exist).
        H20 = d["high"].rolling(20, min_periods=20).max()
        r1 = d["close"].pct_change()
        sd20 = r1.rolling(20, min_periods=20).std()
        rebuilt = ((d["close"] - H20) / H20) / sd20
        d["_depth"] = d[LHV].where(d[LHV].notna(), rebuilt)
        return d

    data = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[(coin, w)] = prep(df)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for d in data.values():
        act = d["forecast"] != 0
        regime = d["regime"].astype(str).str.strip().str.lower()
        in_profile = regime == "unknown"  # the falling calm regime (no veto fired)
        below_high = d["_depth"] < 0
        short = d["forecast"] < 0
        n_active += int(act.sum())
        n_agree += int((act & in_profile & below_high & short).sum())

    reading = ("The falling calm profile is read from the recorded regime ('unknown' = no veto fired, since the "
               "detector's 365-bar components cannot be rebuilt inside 120-bar windows) and the situation as a close "
               "below its 20-day high (raw depth < 0) with a short forecast; the slope's t pools cases of one day by "
               "a day-clustered OLS standard error (with G/(G-1) correction); the supporting check uses the position's "
               "gain before costs per bar (each 1d bar is one day), averaged over the coins present each day; minimum "
               "counts not reached give 'not observable'.")

    main_name = "OLS slope of excess 3-day return on post_pipeline_value"
    main_thr = "confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"independent cases": 0, "distinct days": 0},
            "decided_by": "No bar has a nonzero forecast: fewer than 100 independent cases.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars inside the falling calm profile with "
                           "the close below its 20-day high, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. coin means (holding the coin) ----------
    coin_r3 = {}
    coin_r1 = {}
    for (coin, w), d in data.items():
        c = d["close"].values
        n = len(c)
        idx = np.arange(0, n - H, H)
        r3 = c[idx + H] / c[idx] - 1 if len(idx) else np.array([])
        coin_r3.setdefault(coin, []).extend(list(r3[np.isfinite(r3)]))
        r1 = c[1:] / c[:-1] - 1 if n > 1 else np.array([])
        coin_r1.setdefault(coin, []).extend(list(r1[np.isfinite(r1)]))
    mean3 = {k: (float(np.mean(v)) if len(v) else np.nan) for k, v in coin_r3.items()}
    mean1 = {k: (float(np.mean(v)) if len(v) else np.nan) for k, v in coin_r1.items()}

    # ---------- 3. cases ----------
    xs, ys, days = [], [], []
    for (coin, w), d in data.items():
        c = d["close"].values
        f = d["forecast"].values
        x = d[PPV].values
        ts = d["timestamp"]
        n = len(d)
        for i in range(0, n - H, H):
            if f[i] == 0:
                continue
            if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and np.isfinite(x[i])):
                continue
            if not np.isfinite(mean3.get(coin, np.nan)):
                continue
            ys.append(c[i + H] / c[i] - 1 - mean3[coin])
            xs.append(float(x[i]))
            days.append(ts.iloc[i].floor("D"))
    n_cases = len(xs)
    n_days = len(set(days))

    slope = None
    tval = None
    if n_cases >= 3:
        X = np.asarray(xs, float)
        Y = np.asarray(ys, float)
        xm = X.mean()
        sxx = float(((X - xm) ** 2).sum())
        if sxx > 0:
            b = float(((X - xm) * (Y - Y.mean())).sum() / sxx)
            a = Y.mean() - b * xm
            e = Y - a - b * X
            s = pd.Series((X - xm) * e).groupby(pd.Index(days)).sum().values
            G = len(s)
            if G > 1:
                var_b = (G / (G - 1)) * float((s ** 2).sum()) / sxx ** 2
                if var_b > 0:
                    tval = b / np.sqrt(var_b)
            slope = b

    # ---------- 4. supporting check ----------
    rows = []
    for (coin, w), d in data.items():
        c = d["close"].values
        pos = d["postRebalance_current_allocation"].values
        ts = d["timestamp"]
        m1 = mean1.get(coin, np.nan)
        for i in range(len(d) - 1):
            r = c[i + 1] / c[i] - 1
            if not (np.isfinite(r) and np.isfinite(pos[i])):
                continue
            rows.append((ts.iloc[i].floor("D"), pos[i] * r, pos[i] * m1))
    sup_value = None
    sup_pass = None
    if rows:
        bk = pd.DataFrame(rows, columns=["day", "gain", "mkt"]).dropna()
        daily = bk.groupby("day")[["gain", "mkt"]].mean()
        if len(daily):
            sup_value = float(daily["gain"].mean() - daily["mkt"].mean())
            sup_pass = bool(sup_value > 0)

    counts = {"independent cases": int(n_cases), "distinct days": int(n_days)}
    stat = None if tval is None else {"name": "OLS slope t, day-clustered", "value": float(tval)}
    main = {"name": main_name, "value": None if slope is None else float(slope),
            "statistic": stat, "threshold": main_thr}
    support = {"name": "book mean daily return minus position x coin mean daily return, before costs",
               "value": sup_value, "passed": sup_pass}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} independent cases (need 100) on {n_days} distinct days "
                   f"(need 60).")
    elif tval is None or slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting check passes (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper closes are followed by relative rebounds (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
