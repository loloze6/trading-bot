import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    MIN_CASES = 100
    RAW = "debug_info.components.day_move_swing.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # Where the component is not recorded, rebuild the day's move sign
            # from prices inside the window.
            day_ret = close / close.shift(1) - 1.0
            move = raw.where(raw.notna(), day_ret)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            agitated = regime.str.lower() != "chop"
            active = fc != 0
            n_active += int(active.sum())
            ok = active & agitated & move.notna() & (np.sign(move) == np.sign(fc)) & (move != 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of demeaned 5-bar forward return on forecast"
    threshold = "slope > 0 with t >= 2 (confirm), slope < 0 with t <= -2 (reject), on at least 100 cases"

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are agitated-profile (non-chop) bars "
                          "whose forecast sign matches the sign of the day's move in swing units.",
            "reading": "The agitated profile is read as the regime not being 'chop' (the veto fires at swing "
                       "percentile <= 0.5); the expected side is the sign of the day's raw move.",
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0 and not pd.isna(ts.iloc[i]):
                    coin_cases.append((f, r, ts.iloc[i].floor("D")))
        if len(coin_grid_rets) == 0:
            continue
        mu = float(np.mean(coin_grid_rets))
        for f, r, day in coin_cases:
            xs.append(float(f))
            ys.append(r - mu)
            days.append(day)

    n_cases = len(xs)
    n_days = len(set(days))
    reading = ("Agitated profile read as regime != 'chop'; the forecast is regressed with an intercept, and "
               "'cases of one day summed together' is read as a day-clustered standard error (each day's "
               "score contributions summed, G/(G-1) correction); the coin mean is over its non-overlapping "
               "5-bar grid returns of all windows.")

    slope = None
    tval = None
    if n_cases >= 3:
        x = np.array(xs)
        y = np.array(ys)
        X = np.column_stack([np.ones(n_cases), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            bread = np.linalg.inv(XtX)
            beta = bread @ X.T @ y
            e = y - X @ beta
            dser = pd.Series(days)
            codes = pd.factorize(dser)[0]
            G = codes.max() + 1
            scores = X * e[:, None]
            S = np.zeros((G, 2))
            np.add.at(S, codes, scores)
            meat = S.T @ S
            V = bread @ meat @ bread
            if G > 1:
                V = V * (G / (G - 1.0))
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    counts = {"non-overlapping cases with a non-zero forecast": int(n_cases), "days": int(n_days)}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases with a non-zero forecast, below the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed on the cases, so neither rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 on at least 100 cases (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 100 cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": bool(passed) if agreement is not None else None},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "slope t (day-clustered)", "value": tval} if tval is not None else None),
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
