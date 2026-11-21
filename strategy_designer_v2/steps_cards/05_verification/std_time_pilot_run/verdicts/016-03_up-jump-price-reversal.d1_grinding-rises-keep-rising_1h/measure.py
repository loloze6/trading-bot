import numpy as np
import pandas as pd


def measure(bars):
    H = 72
    RAW = "debug_info.components.grind.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
            else:
                raw = pd.Series(np.nan, index=close.index)
            past = close / close.shift(H) - 1.0  # inside the window only
            active = fc.notna() & (fc != 0)
            # situation: the coin rose over the past 72 bars (from prices where computable)
            # and the rise is at least partly a grind (raw residual share > 0)
            rose = past.isna() | (past > 0)
            situation = rose & raw.notna() & (raw > 0)
            agree = active & situation & (fc > 0)  # expected side: long
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of forecast coefficient in pooled regression of next-72-bar excess return on forecast and past 72-bar return (rising grid bars)"
    threshold = "confirm if coefficient > 0 with t >= 2; reject if coefficient < 0 with t <= -2; else inconclusive; fewer than 300 rising grid cases is not enough"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are long bars after a 72-bar rise with a positive grind value, so the config does not do what the plan's Fidelity describes.",
            "reading": "Situation taken as a positive past 72-bar close-to-close rise (when computable inside the window) with a positive raw grind value, on the long side.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_fwd_all = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(close)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                fwd = close[t + H] / close[t] - 1.0
                if not np.isfinite(fwd):
                    continue
                coin_fwd_all.append(fwd)
                if t - H < 0:
                    continue
                pst = close[t] / close[t - H] - 1.0
                if np.isfinite(pst) and pst > 0 and np.isfinite(fc[t]):
                    coin_rows.append((fwd, fc[t], pst))
        if len(coin_fwd_all) == 0:
            continue
        mu = float(np.mean(coin_fwd_all))
        for fwd, f, p in coin_rows:
            rows.append((fwd - mu, f, p))

    n_cases = len(rows)
    counts = {"rising grid cases pooled over the coins": int(n_cases)}
    reading = ("Grid at positions 0,72,144,... of each window; rising cases need a past 72-bar close and a next-72-bar close inside the window; "
               "the coin's mean 72-bar return is the mean of the forward returns of all its grid bars over all windows; "
               "OLS with an intercept and the ordinary coefficient t.")

    if n_cases < 300:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 300 rising grid cases pooled over the coins, the plan's minimum.",
            "reading": reading,
        }

    arr = np.array(rows, dtype=float)
    y = arr[:, 0]
    X = np.column_stack([np.ones(n_cases), arr[:, 1], arr[:, 2]])
    beta, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    coef = float(beta[1])
    tval = None
    if rank == 3 and n_cases > 3:
        resid = y - X @ beta
        s2 = float(resid @ resid) / (n_cases - 3)
        cov = s2 * np.linalg.inv(X.T @ X)
        se = float(np.sqrt(cov[1, 1]))
        if se > 0 and np.isfinite(se):
            tval = float(coef / se)

    if tval is None:
        status = "inconclusive"
        decided = "The forecast coefficient's t could not be computed (degenerate regressors), so neither the confirm nor the reject rule is met."
    elif coef > 0 and tval >= 2:
        status = "confirmed"
        decided = "The forecast coefficient is positive with t >= 2 on at least 300 rising grid cases (confirm rule)."
    elif coef < 0 and tval <= -2:
        status = "rejected"
        decided = "The forecast coefficient is negative with t <= -2 (reject rule): grinding rises continue less than jump-made rises of the same size."
    else:
        status = "inconclusive"
        decided = "The forecast coefficient's t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": tval,
            "statistic": {"name": "OLS t of forecast coefficient", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
