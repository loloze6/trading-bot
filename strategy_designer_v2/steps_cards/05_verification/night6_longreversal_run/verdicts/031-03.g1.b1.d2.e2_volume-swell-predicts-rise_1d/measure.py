import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.vol_swell.last_history_value"

    def _raw_ratio(df):
        # The component's raw value, or rebuilt from volume inside the window when missing.
        if RAW in df.columns:
            raw = pd.to_numeric(df[RAW], errors="coerce")
        else:
            raw = pd.Series(np.nan, index=df.index)
        vol = pd.to_numeric(df["volume"], errors="coerce")
        rebuilt = vol.rolling(14, min_periods=14).mean() / vol.rolling(30, min_periods=30).mean() - 1.0
        return raw.where(raw.notna(), rebuilt)

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = _raw_ratio(df)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # Expected side: long when the ratio is above 1 (raw > 0), short when below 1 (raw < 0).
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    sit_passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of forward 14-bar return minus normal 14-bar drift on the forecast, grid bars"
    main_threshold = "confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2"

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"grid cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the active bars have a forecast whose sign matches the sign of the "
                           "14-day/30-day mean volume ratio minus 1 (long above 1, short below 1), as the Fidelity states."),
            "reading": "Situation side taken as the sign of the raw component value (ratio - 1); bars with a raw value of 0 or missing count as disagreeing.",
        }

    # ---------- 2. Main measure ----------
    cases = []          # (coin, day, forecast, fwd return)
    coin_grid_rets = {}  # coin -> list of non-overlapping 14-bar returns (normal drift)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.setdefault(coin, []).append(r)
                if np.isfinite(fc[i]):
                    cases.append((coin, ts.iloc[i].normalize(), float(fc[i]), r))

    drift = {c: float(np.mean(v)) for c, v in coin_grid_rets.items() if len(v) > 0}
    if cases:
        cdf = pd.DataFrame(cases, columns=["coin", "day", "f", "r"])
        cdf["y"] = cdf["r"] - cdf["coin"].map(drift)
        cdf = cdf.dropna(subset=["y", "f"])
    else:
        cdf = pd.DataFrame(columns=["coin", "day", "f", "r", "y"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    slope = None
    tval = None
    if n_cases >= 3 and n_days >= 2 and cdf["f"].var() > 0:
        X = np.column_stack([np.ones(n_cases), cdf["f"].values.astype(float)])
        y = cdf["y"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        codes = pd.factorize(cdf["day"])[0]
        G = codes.max() + 1
        for g in range(G):
            m = codes == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp")
            c = pd.to_numeric(df["close"], errors="coerce")
            rets.append(c.pct_change().dropna())
        if rets:
            allr = pd.concat(rets)
            if len(allr):
                coin_mu[coin] = float(allr.mean())

    book_rows = []
    for coin, wins in bars.items():
        if coin not in coin_mu:
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts")
            d["day"] = d["ts"].dt.normalize()
            daily = d.groupby("day").last()
            v = pd.to_numeric(daily["postRebalance_total_value"], errors="coerce")
            pos = pd.to_numeric(daily["postRebalance_current_allocation"], errors="coerce")
            br = v.pct_change()
            mr = pos.shift(1) * coin_mu[coin]
            tmp = pd.DataFrame({"book": br, "mkt": mr}).iloc[1:].dropna()
            tmp["day"] = tmp.index
            book_rows.append(tmp)
    timing = None
    if book_rows:
        bdf = pd.concat(book_rows, ignore_index=True)
        per_day = bdf.groupby("day")[["book", "mkt"]].mean()
        if len(per_day):
            timing = float(per_day["book"].mean() - per_day["mkt"].mean())
    timing_passed = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    counts = {"grid cases": n_cases, "distinct days": n_days}
    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided_by = (f"The plan's minimum of 200 grid cases over 100 distinct days is not reached "
                      f"({n_cases} cases, {n_days} days).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if timing_passed:
            status = "confirmed"
            decided_by = "Confirm: the slope is positive with t >= 2 and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided_by = "Inconclusive: a positive slope with t >= 2 but a timing gain of 0 or less."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "Reject: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": sit_passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS t, standard errors clustered by day", "value": tval},
            "threshold": main_threshold,
        },
        "supporting_check": {"name": "timing gain (book mean daily return minus market-rise gain)",
                             "value": timing, "passed": timing_passed},
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Slope is an OLS with intercept of (forward 14-bar return minus the coin's mean non-overlapping "
                    "14-bar return over all its windows) on the grid-bar forecast, all grid bars with a full 14-bar "
                    "forward return included, t from day-clustered standard errors; the market-rise gain uses the "
                    "position held from the previous day's close times the coin's mean daily close return; and the "
                    "plan's 'fewer cases' rule is reported as 'not observable' per the workflow."),
    }
