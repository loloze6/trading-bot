import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_pos.last_history_value"
    CALM = "unknown"  # the config's default regime (vol percentile <= 0.5) carries the strategy: the calm profile

    def prep(df):
        d = df.copy().reset_index(drop=True)
        d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
        d["day"] = d["ts"].dt.floor("D")
        d["calm"] = d["regime"].astype(str) == CALM
        return d

    data = {c: {w: prep(df) for w, df in wins.items() if df is not None and len(df) > 0}
            for c, wins in bars.items()}

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for c, wins in data.items():
        for w, d in wins.items():
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            # fallback: recompute the close's position in its 20-bar high-low range (today's bar included)
            hh = d["high"].rolling(20, min_periods=20).max()
            ll = d["low"].rolling(20, min_periods=20).min()
            rng = (hh - ll).replace(0, np.nan)
            pos = (2.0 * (d["close"] - ll) / rng - 1.0).values
            raw = np.where(np.isnan(raw), pos, raw)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & d["calm"].values & ~np.isnan(raw) & (np.sign(fc) == np.sign(np.nan_to_num(raw)))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    situation = {"agreement": agreement, "passed": passed}
    main_name = "clustered-by-day t of the slope of 5-bar excess return on forecast, in-profile grid bars"
    main_thr = "t >= +2 confirms (with timing part > 0); t <= -2 rejects; between is inconclusive"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are calm-profile bars whose forecast sign "
                           "matches the close's side of its 20-day range midpoint (above: long, below: short)."),
            "reading": "The calm profile is read as regime 'unknown' (the config's only regime with a strategy); the side is the sign of the raw range position.",
        }

    # ---------- 2. main measure ----------
    rows = []
    for c, wins in data.items():
        # normal drift: mean 5-bar return on the non-overlapping grid of all the coin's windows
        all_r = []
        for w, d in wins.items():
            cl = d["close"].values.astype(float)
            idx = np.arange(0, len(d) - H, H)
            all_r.extend(list(cl[idx + H] / cl[idx] - 1.0))
        if len(all_r) == 0:
            continue
        drift = float(np.nanmean(all_r))
        for w, d in wins.items():
            cl = d["close"].values.astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            idx = np.arange(0, len(d) - H, H)
            for i in idx:
                if not d["calm"].iat[i]:
                    continue
                r = cl[i + H] / cl[i] - 1.0
                if np.isnan(r) or np.isnan(fc[i]):
                    continue
                rows.append((d["day"].iat[i], fc[i], r - drift))
    cases = pd.DataFrame(rows, columns=["day", "x", "y"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t_slope = None
    if n_cases >= 3 and cases["x"].var() > 0 and n_days >= 2:
        X = np.column_stack([np.ones(n_cases), cases["x"].values])
        y = cases["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, g in cases.assign(u=u).groupby("day"):
            gi = g.index.values
            s = (X[gi] * u[gi][:, None]).sum(axis=0)
            meat += np.outer(s, s)
        G = n_days
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1]))
        t_slope = float(slope / se) if se > 0 else None

    # ---------- supporting check: timing part ----------
    per_day = {}
    for c, wins in data.items():
        rets = []
        for w, d in wins.items():
            cl = d["close"].values.astype(float)
            if len(cl) > 1:
                rets.extend(list(cl[1:] / cl[:-1] - 1.0))
        if len(rets) == 0:
            continue
        mu = float(np.nanmean(rets))
        for w, d in wins.items():
            cl = d["close"].values.astype(float)
            pos = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").values
            for i in range(len(d) - 1):
                r = cl[i + 1] / cl[i] - 1.0
                if np.isnan(r) or np.isnan(pos[i]):
                    continue
                per_day.setdefault(d["day"].iat[i], []).append((pos[i] * r, pos[i] * mu))
    if per_day:
        book = np.array([np.mean([a for a, _ in v]) for v in per_day.values()])
        mkt = np.array([np.mean([b for _, b in v]) for v in per_day.values()])
        timing = float(book.mean() - mkt.mean())
    else:
        timing = None
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"non-overlapping in-profile cases": n_cases, "distinct days": n_days}
    supporting = {"name": "book mean daily return before costs minus market-rise gain (timing part)",
                  "value": timing, "passed": timing_pass}
    stat = {"name": "slope t, clustered by day", "value": t_slope} if t_slope is not None else None

    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided = (f"The minimum of 200 non-overlapping in-profile cases on at least 100 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so it meets neither the confirm nor the reject rule."
    elif t_slope >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope's t is +2 or more and the timing part is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is +2 or more but the timing part is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": {"name": main_name, "value": slope, "statistic": stat, "threshold": main_thr},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": ("In-profile means regime 'unknown' on the grid bar (positions 0,5,10,... of each window, forward return inside the window), "
                    "all such bars are regressed with an intercept on the recorded forecast including forecast 0, the slope's t uses "
                    "day-clustered standard errors with the usual G/(G-1)*(N-1)/(N-K) correction, the drift is the coin's mean "
                    "non-overlapping 5-bar return over all its windows, and the timing part uses each bar as a day with the coins "
                    "present that day averaged."),
    }
