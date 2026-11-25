import numpy as np
import pandas as pd

RAW_COL = "debug_info.components.scaled_rise.last_history_value"
H = 5


def _recompute_raw(close):
    # 5-day return over (20-day std of daily returns * sqrt(5)), from the window's own prices
    r1 = close.pct_change()
    ret5 = close / close.shift(5) - 1.0
    sd = r1.rolling(20, min_periods=20).std()
    return ret5 / (sd * np.sqrt(5.0))


def _clustered_slope_t(x, y, groups):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    g = pd.Series(groups)
    meat = np.zeros((2, 2))
    G = 0
    for _, idx in g.groupby(g).groups.items():
        ii = np.asarray(list(idx))
        s = X[ii].T @ resid[ii]
        meat += np.outer(s, s)
        G += 1
    k = 2
    if G < 2 or n <= k:
        return float(beta[1]), None, G
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    if not np.isfinite(se) or se == 0:
        return float(beta[1]), None, G
    return float(beta[1]), float(beta[1] / se), G


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            recomputed = _recompute_raw(pd.to_numeric(df["close"], errors="coerce"))
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: a rise over the last 5 days (raw scaled return > 0), expected side: long
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "slope of 5-bar excess return on forecast",
                "value": None,
                "statistic": None,
                "threshold": "slope t >= 2 confirms (with positive mean excess return), <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the active bars are long bars after a 5-day rise "
                           "(5-day return over the 20-day swing above 0), as the plan's Fidelity requires"
                           if n_active > 0 else "The record has no active bars to compare with the plan's situation."),
            "reading": "The situation is a positive raw scaled_rise value (recomputed from the window's prices where missing) with a long forecast; the calm profile is not part of the check.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_grid.append({
                    "coin": coin,
                    "date": ts.iloc[i].normalize(),
                    "fwd": c1 / c0 - 1.0,
                    "forecast": fc[i],
                })
        if not coin_grid:
            continue
        cg = pd.DataFrame(coin_grid)
        mean_ret = cg["fwd"].mean()  # coin's mean 5-bar return over all its windows (grid)
        cg["excess"] = cg["fwd"] - mean_ret
        rows.append(cg)

    if rows:
        allg = pd.concat(rows, ignore_index=True)
        sample = allg[allg["forecast"].notna() & (allg["forecast"] > 0) & allg["excess"].notna()]
    else:
        sample = pd.DataFrame(columns=["coin", "date", "fwd", "forecast", "excess"])

    n_cases = int(len(sample))
    n_dates = int(sample["date"].nunique()) if n_cases else 0
    threshold = "slope t >= 2 with positive mean excess return confirms; slope t <= -2 rejects; else inconclusive; at least 100 grid cases"
    reading = ("Grid at positions 0,5,10,... of each window with a full 5-bar forward return; excess = return minus the coin's mean "
               "5-bar return over all grid bars of all its windows; slope t uses OLS with standard errors clustered by date "
               "(CR1 correction) to pool same-date cases; the plan's 'fewer than 100 grid cases' minimum is reported as not observable.")

    counts = {"grid cases with forecast > 0": n_cases, "dates": n_dates}

    if n_cases < 100:
        mean_ex = float(sample["excess"].mean()) if n_cases else None
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": "slope of 5-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean 5-bar excess return > 0", "value": mean_ex,
                                 "passed": (bool(mean_ex > 0) if mean_ex is not None else None)},
            "counts": counts,
            "decided_by": f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 100.",
            "reading": reading,
        }

    slope, t, G = _clustered_slope_t(sample["forecast"].to_numpy(), sample["excess"].to_numpy(),
                                     sample["date"].astype(str).to_numpy())
    mean_ex = float(sample["excess"].mean())
    sup_pass = bool(mean_ex > 0)

    if t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation), so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return is positive (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess return is not positive (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of 5-bar excess return on forecast",
            "value": float(slope),
            "statistic": ({"name": "slope t, clustered by date", "value": float(t)} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": "mean 5-bar excess return > 0", "value": mean_ex, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
