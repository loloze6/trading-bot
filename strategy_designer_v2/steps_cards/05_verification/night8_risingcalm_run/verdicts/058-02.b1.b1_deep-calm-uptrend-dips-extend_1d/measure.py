import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    LHV = "debug_info.components.scaled_pullback.last_history_value"

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            # depth below the 5-day closing high: from the recorded raw value,
            # recomputed from the window's closes where the raw value is missing
            hi5 = close.rolling(5, min_periods=5).max()
            price_depth = (close - hi5) / hi5
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            below_high = np.where(raw.notna(), raw < 0,
                                  np.where(price_depth.notna(), price_depth < 0, False))
            # rising calm profile = the bars where neither veto fired (regime "unknown")
            profile = d["regime"].astype(str).str.lower().eq("unknown").values
            situation = profile & below_high
            active = fc.notna().values & (fc.fillna(0).values != 0)
            short = fc.fillna(0).values < 0
            n_active += int(active.sum())
            n_agree += int((active & situation & short).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of (forecast/10) x (5-bar forward return minus coin's mean 5-bar return), forecast<0, non-overlapping grid"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None, "distinct days": None},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short bars in the rising calm "
                           "profile (regime 'unknown') with the close below its 5-day closing high"),
            "reading": "the rising calm profile is read from the recorded regime ('unknown' = no veto fired), since the detector's components are not recorded",
        }

    # ---------------- 2. criterion ----------------
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        all_rets = []
        per_coin = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[p]) and fc[p] < 0 and not pd.isna(ts.iloc[p]):
                    per_coin.append((fc[p], r, ts.iloc[p].floor("D")))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        coin_mean[coin] = mu
        for f, r, day in per_coin:
            rows.append({"coin": coin, "f": f, "ex": r - mu, "prod": (f / 10.0) * (r - mu), "day": day})

    cases = pd.DataFrame(rows, columns=["coin", "f", "ex", "prod", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_prod = float(cases["prod"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2:
        dev = cases["prod"] - mean_prod
        D = dev.groupby(cases["day"]).sum().values
        G = len(D)
        if G >= 2:
            var = (G / (G - 1.0)) * float(np.sum(D ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_prod / se) if se > 0 else None

    # supporting check: thirds by forecast
    sup_val, sup_pass = None, None
    if n_cases >= 3:
        s = cases.sort_values("f", kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        deep = float(s["ex"].iloc[:k].mean())
        shallow = float(s["ex"].iloc[n_cases - k:].mean())
        sup_val = deep - shallow
        sup_pass = bool(deep < shallow)

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"minimum counts not reached: {n_cases} cases (need 100) on {n_days} distinct days (need 60)")
    elif t_val is None:
        status = "inconclusive"
        decided = "the t of the mean product could not be computed, so it meets neither confirm nor reject"
    elif mean_prod > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean product positive with t >= 2 and the deepest third's mean excess return below the shallowest third's"
        else:
            status = "inconclusive"
            decided = "confirm-strength t but the supporting check (deepest third below shallowest third) failed"
    elif mean_prod < 0 and t_val <= -2:
        status = "rejected"
        decided = "mean product negative with t <= -2: deeper pullbacks are followed by recoveries"
    else:
        status = "inconclusive"
        decided = "t of the mean product lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_prod,
            "statistic": ({"name": "t of the mean, cases of one day summed as one piece of evidence", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 5-bar return, deepest third minus shallowest third (must be < 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("the rising calm profile is the recorded regime 'unknown'; grid cells need a full 5-bar forward return "
                    "inside the window; the coin's mean is over all its grid returns in all windows; thirds are n//3 cases "
                    "at each end sorted by forecast; the t uses a day-clustered standard error."),
    }
