import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    PERIOD = 30
    MIN_CASES = 30

    # ---------- prepare windows ----------
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
                d = d.sort_values("timestamp")
            d = d.reset_index(drop=True)
            for c in ["open", "high", "low", "close", "forecast"]:
                if c in d.columns:
                    d[c] = pd.to_numeric(d[c], errors="coerce")
            d["forecast"] = d["forecast"].fillna(0.0)
            prepared[(coin, w)] = d

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for (coin, w), d in prepared.items():
        low = d["low"]
        close = d["close"]
        prior_low = low.shift(1).rolling(PERIOD, min_periods=PERIOD).min()
        computable = prior_low.notna() & low.notna() & close.notna()
        situation = computable & (low < prior_low) & (close >= prior_low)
        active = (d["forecast"] != 0) & computable
        n_active += int(active.sum())
        n_agree += int((active & situation & (d["forecast"] < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_base = (
        "The situation is low below the lowest low of the 30 prior bars of the same window with close at or above it "
        "(bars without 30 prior bars in the window left out of the agreement), the expected side is short; "
        "a case is the first short bet (forecast rise of at least 2 points on the short side from its lowest level "
        "since the last bet, from 0 after a flat) in each 10-bar grid cell of a window, its return taken from that "
        "bet's close over 10 bars inside the window; the coin's drift is the mean of its non-overlapping 10-bar returns "
        "on the grid of all windows; the t clusters deviations by UTC day with a D/(D-1) correction; "
        "the supporting halves are |forecast| above the median versus at or below it."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": (
                "Fewer than 90 % of the bars with a non-zero forecast are short reclaim days "
                "(low under the prior 30-day lowest low, close back at or above it)."
            ),
            "reading": reading_base,
        }

    # ---------- drift per coin ----------
    coin_rets = {}
    for (coin, w), d in prepared.items():
        c = d["close"].values
        n = len(c)
        rs = []
        for p in range(0, n - H, H):
            if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                rs.append(c[p + H] / c[p] - 1.0)
        coin_rets.setdefault(coin, []).extend(rs)
    drift = {k: (float(np.mean(v)) if len(v) else np.nan) for k, v in coin_rets.items()}

    # ---------- cases ----------
    cases = []  # (unusual_short, abs_forecast, day)
    for (coin, w), d in prepared.items():
        f = d["forecast"].values
        c = d["close"].values
        n = len(d)
        m = np.where(f < 0, -f, 0.0)
        bet = np.zeros(n, dtype=bool)
        ref = 0.0
        for i in range(n):
            if m[i] <= 0:
                ref = 0.0
                continue
            if m[i] - ref >= BAND - 1e-12:
                bet[i] = True
                ref = m[i]
            else:
                ref = min(ref, m[i])
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bet[i]]
            if not idx:
                continue
            i = idx[0]
            if i + H >= n:
                continue
            if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                continue
            dr = drift.get(coin, np.nan)
            if not np.isfinite(dr):
                continue
            r = c[i + H] / c[i] - 1.0
            u = -(r - dr)
            if "timestamp" in d.columns:
                day = str(pd.Timestamp(d["timestamp"].iloc[i]).floor("D"))
            else:
                day = f"{w}_{i}"
            cases.append((u, abs(f[i]), day))

    n_cases = len(cases)
    days = sorted(set(x[2] for x in cases))
    n_days = len(days)

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([x[0] for x in cases], dtype=float)
        mean_u = float(u.mean())
        if n_cases > 1 and n_days > 1:
            dev = pd.Series(u - mean_u).groupby([x[2] for x in cases]).sum().values
            var = (n_days / (n_days - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 1:
        a = np.array([x[1] for x in cases], dtype=float)
        u = np.array([x[0] for x in cases], dtype=float)
        med = np.median(a)
        big = u[a > med]
        small = u[a <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)

    main = {
        "name": "mean unusual 10-bar short move per case, before costs",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases clustered by day", "value": t_val} if t_val is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases",
    }
    supporting = {
        "name": "mean unusual short move, larger |forecast| half minus smaller half",
        "value": sup_val,
        "passed": sup_pass,
    }
    counts = {"cases": n_cases, "days": n_days}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual short move is above 0 with t >= 2 over at least 30 cases, and the supporting check is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t, but the supporting check is at 0 or below (or not computable)."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual short move is below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
