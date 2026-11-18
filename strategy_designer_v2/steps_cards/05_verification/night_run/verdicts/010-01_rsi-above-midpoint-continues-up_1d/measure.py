import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.rsi_share.last_history_value"
    H = 7
    MIN_CASES = 300

    # ---------- 1. Situation check ----------
    # Situation: share of the past 14 days the 14-day RSI spent above 50, graded.
    # Expected side: long when the share > 1/2, short when < 1/2.
    raw_all = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if RAW in df.columns:
                raw_all.append(pd.to_numeric(df[RAW], errors="coerce").values)
    raw_concat = np.concatenate(raw_all) if raw_all else np.array([])
    raw_concat = raw_concat[np.isfinite(raw_concat)]
    # The raw value is either the share already centred (has negatives) or the share in [0, 1].
    centred = bool(raw_concat.size > 0 and np.nanmin(raw_concat) < 0)
    offset = 0.0 if centred else 0.5

    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            centred_share = raw - offset
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            exp_sign = np.sign(np.round(centred_share, 9))
            ok = active & np.isfinite(centred_share) & (exp_sign != 0) & (exp_sign == np.sign(fc))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.90

    main_name = "pooled OLS slope of 7-bar forward return minus coin mean on forecast, non-overlapping samples"
    threshold = "t >= 2 confirms (with timing check), t <= -2 rejects, at least 300 independent cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the active bars have a forecast sign equal to the sign of the "
                          "14-day RSI-above-50 share minus one half, as the plan's situation and outcome require.",
            "reading": "The expected side is the sign of the component's raw share minus one half "
                       "(raw taken as already centred if it has negative values).",
        }

    # ---------- 2. Main measure ----------
    samples = []  # (coin, fwd, forecast)
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0 and np.isfinite(f):
                    samples.append((coin, c1 / c0 - 1.0, f))
    s = pd.DataFrame(samples, columns=["coin", "fwd", "fc"])
    n_cases = int(len(s))

    slope = None
    t_stat = None
    if n_cases >= 3:
        s["ex"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
        x = s["fc"].values.astype(float)
        y = s["ex"].values.astype(float)
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            resid = y - a - b * x
            se = float(np.sqrt(np.sum(resid ** 2) / (n_cases - 2) / sxx))
            slope = b
            t_stat = float(b / se) if se > 0 else None

    # ---------- 3. Supporting check: timing gain before costs ----------
    coin_mu = {}
    daily = []  # (window, timestamp, coin, gain, market_gain)
    for coin in bars:
        rets = []
        for w in bars[coin]:
            df = bars[coin][w]
            close = pd.to_numeric(df["close"], errors="coerce").values
            r = close[1:] / close[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan
    for coin in bars:
        mu = coin_mu[coin]
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            ts = df["timestamp"].values
            for t in range(1, len(df)):
                r = close[t] / close[t - 1] - 1.0 if close[t - 1] else np.nan
                p = alloc[t - 1]
                if np.isfinite(r) and np.isfinite(p) and np.isfinite(mu):
                    daily.append((w, ts[t], coin, p * r, p * mu))
    timing = None
    check_pass = None
    if daily:
        d = pd.DataFrame(daily, columns=["w", "ts", "coin", "gain", "mkt"])
        per_day = d.groupby(["w", "ts"])[["gain", "mkt"]].mean()
        timing = float(per_day["gain"].mean() - per_day["mkt"].mean())
        check_pass = bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, below the plan's minimum of 300."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_stat >= 2:
        if check_pass:
            status = "confirmed"
            decided = "The slope's t is 2 or more with at least 300 cases and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "The slope's t is 2 or more but the timing check fails: a confirming slope whose timing check fails is inconclusive."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 300 cases: later moves run against the side RSI held."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book mean daily timing gain before costs",
            "value": timing,
            "passed": check_pass,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": "The coin's mean 7-bar return is the mean of its non-overlapping 7-bar samples over all windows, "
                   "the regression has an intercept, and the per-coin book before costs earns the held allocation x the "
                   "coin's daily return, averaged over coins each day, with the market part being the allocation x the "
                   "coin's mean daily return over all windows.",
    }
