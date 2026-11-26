import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 28
    RAW = "debug_info.components.week_multiple.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy; vetoes send everything else to "chop"

    def _f(x):
        try:
            x = float(x)
            return x if np.isfinite(x) else None
        except Exception:
            return None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            in_profile = df["regime"].astype(str) == PROFILE_REGIME
            # expected side: long when the raw centred multiple (multiple - 1) is above 0, short when below
            side_ok = raw.notna() & (raw != 0) & (np.sign(raw) == np.sign(fc))
            agree = active & in_profile & side_ok
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None and agreement >= 0.9) or n_active == 0

    main_name = "t of the slope of the coin-demeaned 28-bar forward return on the forecast, pooled over coins, non-overlapping grid, non-zero forecast bars"
    main_threshold = "t >= 2 with at least 50 grid cases (and timing gain > 0) confirms; t <= -2 with at least 50 grid cases rejects"
    supp_name = "timing gain: book mean daily return minus position held x coin's mean daily return"
    reading = ("Profile bars are those whose recorded regime is 'unknown' (the only regime with a strategy) and the expected side "
               "is the sign of the raw centred multiple; the coin's mean 28-bar return is taken on all its windows' non-overlapping "
               "grid bars, the regression has an intercept, and the timing gain uses daily returns of postRebalance_total_value "
               "with the previous day's postRebalance_current_allocation for the market part.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _f(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on its side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy-calm profile bars whose forecast sign "
                           "matches the sign of the raw centred multiple (multiple - 1)."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    xs, ys_raw, coins_of = [], [], []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    xs.append(fc[i])
                    ys_raw.append(r)
                    coins_of.append(coin)
        coin_grid_rets[coin] = np.mean(allr) if len(allr) else np.nan

    ys = np.array([ys_raw[k] - coin_grid_rets[coins_of[k]] for k in range(len(ys_raw))], dtype=float)
    xs = np.array(xs, dtype=float)
    ok = np.isfinite(ys) & np.isfinite(xs)
    xs, ys = xs[ok], ys[ok]
    n_cases = int(len(xs))

    slope, tval = None, None
    if n_cases >= 3 and np.var(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            tval = float(lr.slope / lr.stderr)

    # ---------- 3. supporting check: timing gain ----------
    # coin's mean daily return over all its windows
    pieces = []
    coin_mu = {}
    for coin, wins in bars.items():
        rets_all = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["_day"] = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            g = d.groupby("_day", sort=True).last()
            close = pd.to_numeric(g["close"], errors="coerce")
            val = pd.to_numeric(g["postRebalance_total_value"], errors="coerce")
            pos = pd.to_numeric(g["postRebalance_current_allocation"], errors="coerce")
            cr = close / close.shift(1) - 1.0
            br = val / val.shift(1) - 1.0
            held = pos.shift(1)
            rets_all.append(cr.iloc[1:].dropna())
            per_win.append(pd.DataFrame({"day": g.index[1:], "book": br.iloc[1:].to_numpy(),
                                         "held": held.iloc[1:].to_numpy(), "coin": coin}))
        mu = pd.concat(rets_all).mean() if len(rets_all) and sum(len(r) for r in rets_all) else np.nan
        coin_mu[coin] = mu
        pieces.extend(per_win)

    timing = None
    if pieces:
        P = pd.concat(pieces, ignore_index=True)
        P["mu"] = P["coin"].map(coin_mu)
        P = P.dropna(subset=["book", "held", "mu"])
        if len(P):
            P["mkt"] = P["held"] * P["mu"]
            daily = P.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    supp_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_cases < 50:
        status = "not observable"
        decided = f"Fewer than 50 grid cases with a non-zero forecast ({n_cases}): the minimum count is not reached."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif tval >= 2 and supp_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more with at least 50 grid cases, and the timing gain is above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is at or below 0: a confirming slope with a failed check."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 50 grid cases."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 with at least 50 grid cases."

    return {
        "status": status,
        "situation_check": {"agreement": _f(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": _f(tval),
                         "statistic": ({"name": "OLS slope t", "value": float(tval)} if tval is not None else None),
                         "threshold": main_threshold},
        "supporting_check": {"name": supp_name, "value": _f(timing), "passed": supp_pass},
        "counts": {"grid cases with a non-zero forecast": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
