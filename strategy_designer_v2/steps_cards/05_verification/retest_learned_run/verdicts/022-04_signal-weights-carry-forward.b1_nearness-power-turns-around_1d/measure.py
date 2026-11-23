import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.excess_power_counter.last_history_value"

    # ---------- 1. situation check ----------
    # Situation: graded excess past power (w - wbar) times the nearness z-score.
    # Expected side: a counter-bet, so the forecast sign should be minus the sign of that product.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(f) == -np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (5-bar return minus coin's mean 5-bar return), non-overlapping, pooled"
    threshold = "confirm: mean > 0 with t >= 2 over >= 300 cases and timing gain > 0; reject: mean < 0 with t <= -2 over >= 300 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": None},
            "decided_by": "Fewer than 90% of active bars carry the sign opposite to the product of excess past power and nearness z-score, which the plan's counter-bet requires.",
            "reading": "Situation bars are those with a non-zero raw component value; the expected side is minus its sign.",
        }

    # ---------- 2. main measure ----------
    products = []
    for coin, wins in bars.items():
        rets, fcs = [], []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for i in range(0, n - H, H):
                if i + H >= n:
                    break
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r) and np.isfinite(f[i]):
                    rets.append(r)
                    fcs.append(f[i])
        if len(rets) == 0:
            continue
        rets = np.asarray(rets)
        fcs = np.asarray(fcs)
        mu = rets.mean()
        products.extend(list(fcs / 10.0 * (rets - mu)))
    products = np.asarray(products, dtype=float)
    n_cases = int(len(products))
    if n_cases >= 2:
        mean_p = float(products.mean())
        sd = float(products.std(ddof=1))
        t = float(mean_p / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    else:
        mean_p = float(products.mean()) if n_cases == 1 else None
        t = None

    # ---------- 3. supporting check: timing gain ----------
    recs = []
    for coin, wins in bars.items():
        coin_daily = []
        per_win = []
        for wname, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp")
            d["day"] = d["timestamp"].dt.floor("D")
            last = d.groupby("day").tail(1).set_index("day")
            c = pd.to_numeric(last["close"], errors="coerce")
            pos = pd.to_numeric(last["postRebalance_current_allocation"], errors="coerce")
            r_next = c.shift(-1) / c - 1.0
            coin_ret = (c / c.shift(1) - 1.0).dropna()
            coin_daily.extend(list(coin_ret.values))
            per_win.append(pd.DataFrame({"day": last.index, "pos": pos.values, "rnext": r_next.values}))
        if not per_win:
            continue
        mu_d = float(np.nanmean(coin_daily)) if coin_daily else np.nan
        x = pd.concat(per_win, ignore_index=True).dropna(subset=["pos", "rnext"])
        x["gain"] = x["pos"] * x["rnext"]
        x["mkt"] = x["pos"] * mu_d
        x["coin"] = coin
        recs.append(x)
    if recs:
        allx = pd.concat(recs, ignore_index=True).dropna(subset=["gain", "mkt"])
        byday = allx.groupby("day")[["gain", "mkt"]].mean()
        timing = float(byday["gain"].mean() - byday["mkt"].mean()) if len(byday) else None
    else:
        timing = None
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_cases < 300 or t is None:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 300."
    elif mean_p > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Main mean positive with t >= 2 over at least 300 cases, and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "Main mean positive with t >= 2, but the timing gain is not above 0."
    elif mean_p < 0 and t <= -2:
        status = "rejected"
        decided = "Main mean negative with t <= -2 over at least 300 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_p,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book mean daily return before costs minus gain from market's rise",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": "Every grid row (0, 5, 10, ...) with a 5-bar return inside its window is a case, flat forecasts included as zero products, and the coin's mean 5-bar return is taken over the same grid of all its windows.",
    }
