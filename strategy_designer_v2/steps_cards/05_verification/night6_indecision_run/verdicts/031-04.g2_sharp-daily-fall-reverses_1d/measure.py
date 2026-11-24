import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    coin_mu = {}
    rows = []      # regression rows: day, forecast, y
    book_rows = [] # book rows: day, coin, gain, market

    for coin, wins in bars.items():
        # coin's mean daily return over all windows together
        all_r = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = c.shift(-1) / c - 1.0
            all_r.append(r.dropna())
        allr = pd.concat(all_r) if all_r else pd.Series(dtype=float)
        mu = float(allr.mean()) if len(allr) else np.nan
        coin_mu[coin] = mu

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce")
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D")

            # raw component value; recompute its sign from prices where missing
            ret_now = c / c.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            vol = ret_now.rolling(20, min_periods=20).std(ddof=1)
            raw_re = ret_now / vol
            raw = raw.where(raw.notna(), raw_re)
            situation = raw < 0  # a fall: the idea's situation, long side

            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())

            # next-day return inside the window
            r_next = c.shift(-1) / c - 1.0
            sel = (f > 0) & r_next.notna()
            for i in np.where(sel.values)[0]:
                rows.append((day.iloc[i], float(f.iloc[i]), float(r_next.iloc[i] - mu)))

            # book before costs: position held after the trade x next bar's return
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            ok = alloc.notna() & r_next.notna()
            for i in np.where(ok.values)[0]:
                book_rows.append((day.iloc[i + 1], coin,
                                  float(alloc.iloc[i] * r_next.iloc[i]),
                                  float(alloc.iloc[i] * mu)))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "OLS slope of next-day return minus coin mean on forecast (forecast > 0)"
    thr = "confirm if slope t >= 2 and timing gain > 0; reject if t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a down day traded long (raw scaled return < 0, forecast > 0), "
                           "but fewer than 90% of the bars with a non-zero forecast are such bars."),
            "reading": "The situation is a bar whose raw volatility-scaled return is below 0 (recomputed from closes where the raw value is missing), with the expected side long.",
        }

    # ---------- 2. main measure: clustered OLS slope ----------
    reg = pd.DataFrame(rows, columns=["day", "f", "y"])
    n_bars = int(len(reg))
    n_days = int(reg["day"].nunique()) if n_bars else 0

    slope = None
    t_val = None
    if n_bars >= 3 and reg["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_bars), reg["f"].values])
        y = reg["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        codes = pd.factorize(reg["day"])[0]
        G = codes.max() + 1
        for g in range(G):
            m = codes == g
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
        k = 2
        corr = (G / (G - 1)) * ((n_bars - 1) / (n_bars - k)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_val = float(beta[1] / se) if np.isfinite(se) and se > 0 else None

    # ---------- supporting check: timing gain ----------
    timing = None
    if book_rows:
        b = pd.DataFrame(book_rows, columns=["day", "coin", "gain", "mkt"])
        daily = b.groupby("day")[["gain", "mkt"]].mean()
        timing = float(daily["gain"].mean() - daily["mkt"].mean())
    sup_passed = None if timing is None else bool(timing > 0)

    counts = {"bars with forecast > 0": n_bars, "distinct days among them": n_days}

    if n_bars < 200 or n_days < 100:
        status = "not observable"
        decided = ("Fewer than 200 bars with forecast > 0 or fewer than 100 distinct days among them: "
                   "too few cases to judge.")
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it meets neither the confirm nor the reject rule."
    elif t_val >= 2 and timing is not None and timing > 0:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_val is None else {"name": "slope t, clustered by day", "value": t_val},
            "threshold": thr,
        },
        "supporting_check": {"name": "book timing gain before costs (mean daily)", "value": timing,
                             "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The slope is an OLS with intercept and day-clustered (CR1) standard errors over bars with forecast > 0 "
                    "that have a next bar in the same window, and the timing gain is the before-cost daily book "
                    "(position after trade x next-bar return, averaged over coins per day) minus position x coin mean return."),
    }
