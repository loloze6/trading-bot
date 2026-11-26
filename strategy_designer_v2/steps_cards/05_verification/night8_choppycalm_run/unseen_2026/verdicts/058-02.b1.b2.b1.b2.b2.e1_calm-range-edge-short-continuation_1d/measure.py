import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.range_pos.last_history_value"
    PP = "debug_info.components.range_pos.post_pipeline_value"
    ALLOC = "postRebalance_current_allocation"
    H = 2
    PERIOD = 20

    # ---------- prepare frames ----------
    frames = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            for c in ["open", "high", "low", "close", FC, ALLOC]:
                if c in d.columns:
                    d[c] = pd.to_numeric(d[c], errors="coerce")
            for c in [RAW, PP]:
                if c not in d.columns:
                    d[c] = np.nan
                d[c] = pd.to_numeric(d[c], errors="coerce")
            d["day"] = d["timestamp"].dt.floor("D")
            # range position from prices: 20 bars, current bar included, inside the window
            hh = d["high"].rolling(PERIOD, min_periods=PERIOD).max()
            ll = d["low"].rolling(PERIOD, min_periods=PERIOD).min()
            rng = hh - ll
            d["pos_px"] = np.where(rng > 0, (d["close"] - ll) / rng, np.nan)
            frames[(coin, w)] = d

    # ---------- situation check ----------
    # map the recorded raw value to the 0..1 range position (scale read from bars where both exist)
    xs, ys = [], []
    for d in frames.values():
        m = d["pos_px"].notna() & d[RAW].notna()
        xs.append(d.loc[m, "pos_px"].values)
        ys.append(d.loc[m, RAW].values)
    xs = np.concatenate(xs) if xs else np.array([])
    ys = np.concatenate(ys) if ys else np.array([])
    a, b, good = 0.0, 1.0, False
    if len(xs) > 10 and np.std(xs) > 0 and np.std(ys) > 0:
        b, a = np.polyfit(xs, ys, 1)
        corr = np.corrcoef(xs, ys)[0, 1]
        good = bool(corr > 0.9 and b != 0)

    n_active, n_agree = 0, 0
    for d in frames.values():
        pos = d["pos_px"].copy()
        if good:
            fill = (d[RAW] - a) / b
            pos = pos.fillna(fill)
        fc = d[FC]
        active = fc.notna() & (fc != 0)
        calm = d["regime"].astype(str) == "unknown"
        side = np.sign(pos - 0.5)
        agree = active & calm & pos.notna() & (np.sign(fc) == side) & (side != 0)
        n_active += int(active.sum())
        n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of slope of 2-bar forward return minus normal drift on range_pos post_pipeline_value (day-clustered)"
    thr = "confirm t >= 2 with timing gain > 0; reject t <= -2; inconclusive otherwise or < 300 grid cases or < 100 distinct days"

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"grid cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the active bars are calm bars whose forecast sign matches the side of the close "
                           "in its 20-day range (long above the middle, short below), as the Fidelity requires."),
            "reading": ("Calm is the regime 'unknown' (not the 'chop' veto); the range position is (close - 20-bar low) / "
                        "(20-bar high - 20-bar low) from prices, the recorded raw value mapped to it where prices lack 20 bars."),
        }

    # ---------- main measure ----------
    drift = {}
    grid = {}
    for (coin, w), d in frames.items():
        c = d["close"].values
        idx = np.arange(0, len(d) - H, H)
        fwd = c[idx + H] / c[idx] - 1.0
        g = d.iloc[idx].copy()
        g["fwd"] = fwd
        grid[(coin, w)] = g
        drift.setdefault(coin, []).append(fwd[np.isfinite(fwd)])
    drift = {k: (float(np.mean(np.concatenate(v))) if len(np.concatenate(v)) else np.nan) for k, v in drift.items()}

    rows = []
    for (coin, w), g in grid.items():
        m = g[FC].notna() & (g[FC] != 0) & g[PP].notna() & np.isfinite(g["fwd"])
        s = g.loc[m]
        for _, r in s.iterrows():
            rows.append((r["fwd"] - drift[coin], r[PP], r["day"]))
    n_cases = len(rows)
    n_days = len(set(r[2] for r in rows)) if rows else 0

    slope, tstat = None, None
    if n_cases >= 3:
        y = np.array([r[0] for r in rows], float)
        x = np.array([r[1] for r in rows], float)
        days = np.array([r[2] for r in rows])
        X = np.column_stack([np.ones(n_cases), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            bread = np.linalg.inv(XtX)
            beta = bread @ X.T @ y
            e = y - X @ beta
            meat = np.zeros((2, 2))
            uniq = pd.Series(np.arange(n_cases)).groupby(pd.Series(days)).indices
            G = len(uniq)
            for _, ix in uniq.items():
                sg = X[ix].T @ e[ix]
                meat += np.outer(sg, sg)
            K = 2
            corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - K)) if G > 1 else np.nan
            V = corr * bread @ meat @ bread
            slope = float(beta[1])
            se = float(np.sqrt(V[1, 1])) if np.isfinite(V[1, 1]) and V[1, 1] > 0 else np.nan
            tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    # ---------- supporting check: timing gain before costs ----------
    mu = {}
    for (coin, w), d in frames.items():
        r = (d["close"] / d["close"].shift(1) - 1.0).values[1:]
        mu.setdefault(coin, []).append(r[np.isfinite(r)])
    mu = {k: (float(np.mean(np.concatenate(v))) if len(np.concatenate(v)) else np.nan) for k, v in mu.items()}
    recs = []
    for (coin, w), d in frames.items():
        r = d["close"] / d["close"].shift(1) - 1.0
        held = d[ALLOC].shift(1)
        gain = held * r
        mkt = held * mu[coin]
        m = gain.notna() & mkt.notna()
        recs.append(pd.DataFrame({"day": d.loc[m, "day"], "gain": gain[m], "mkt": mkt[m]}))
    timing = None
    if recs:
        allr = pd.concat(recs)
        if len(allr):
            daily = allr.groupby("day")[["gain", "mkt"]].mean()
            timing = float(daily["gain"].mean() - daily["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_cases < 300 or n_days < 100:
        status = "not observable"
        decided = f"Minimum counts not reached: {n_cases} grid cases (need 300) on {n_days} distinct days (need 100)."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above 0."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is 0 or less."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (None if agreement is None else float(agreement)), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": tstat,
            "statistic": (None if tstat is None else {"name": "day-clustered OLS slope t", "value": tstat}),
            "threshold": thr,
        },
        "supporting_check": {"name": "timing gain: book mean daily return minus market-rise gain, before costs",
                             "value": timing, "passed": sup_pass},
        "counts": {"grid cases": int(n_cases), "distinct days": int(n_days)},
        "decided_by": decided,
        "reading": ("Calm is the regime 'unknown', the expected side is the close above/below the middle of its 20-bar "
                    "high-low range; the normal drift is the coin's mean 2-bar return on all grid bars of all its windows; "
                    "the regression has an intercept with CR1 day-clustered errors; the book before costs is the held "
                    "allocation times the next bar's close-to-close return, averaged over coins per day."),
    }
