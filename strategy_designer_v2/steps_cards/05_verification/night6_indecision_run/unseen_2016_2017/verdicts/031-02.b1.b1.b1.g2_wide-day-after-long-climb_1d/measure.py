import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    FC = "forecast"
    RAW = "debug_info.components.rise20.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            rng = (d["high"].astype(float) - d["low"].astype(float))
            mean20 = rng.rolling(20, min_periods=20).mean()
            ratio = rng / mean20.replace(0, np.nan)
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            active = f != 0
            computable = ratio.notna()
            sel = active & computable
            if not sel.any():
                continue
            wide = ratio >= 1.5
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                rise_ok = raw.isna() | (raw > 0)
            else:
                rise_ok = pd.Series(True, index=d.index)
            agree = sel & wide & (f > 0) & rise_ok
            n_active += int(sel.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation recomputed as (high-low) of bar t over the mean high-low of the 20 bars ending at t inside each "
               "window, on the active bars where it can be computed, with the expected side long and the raw 20-day rise "
               "positive where recorded; the slope's t is an OLS slope (with intercept) of excess 3-bar return on "
               "forecast with standard errors clustered by calendar day (scores summed per day, small-sample corrected), "
               "and the coin's mean 3-bar return is the mean over its non-overlapping 3-bar grid returns of all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are wide days (range / 20-day mean range >= 1.5) held long "
                           "after a 20-day rise, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            f = pd.to_numeric(d[FC], errors="coerce").values
            reg = d["regime"].astype(str).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if reg[i] == "trending" and np.isfinite(f[i]) and f[i] > 0:
                    coin_cases.append((ts.iloc[i].normalize(), float(f[i]), r))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for day, fv, r in coin_cases:
            rows.append((coin, day, fv, r - mu))

    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mm_name = "t of the slope of excess 3-bar return on forecast (day-clustered)"
    mm_thr = "confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2"
    sc_name = "forecast-weighted mean excess 3-bar return > 0"

    slope = None
    tval = None
    wmean = None
    if n_cases >= 3:
        fx = np.array([r[2] for r in rows], dtype=float)
        y = np.array([r[3] for r in rows], dtype=float)
        dk = np.array([r[1].value for r in rows])
        if fx.sum() > 0:
            wmean = float(np.sum(y * fx) / np.sum(fx))
        X = np.column_stack([np.ones(n_cases), fx])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ (X.T @ y)
            e = y - X @ beta
            scores = X * e[:, None]
            sdf = pd.DataFrame(scores, columns=["a", "b"])
            sdf["g"] = dk
            S = sdf.groupby("g")[["a", "b"]].sum().values
            G = S.shape[0]
            meat = S.T @ S
            if G > 1 and n_cases > 2:
                corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
                V = corr * XtX_inv @ meat @ XtX_inv
                se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
                slope = float(beta[1])
                tval = float(slope / se) if np.isfinite(se) and se > 0 else None
            else:
                slope = float(beta[1])

    sc_passed = None if wmean is None else bool(wmean > 0)

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_cases} cases (need 100) and {n_days} distinct days (need 60).")
    elif tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sc_passed:
        status = "confirmed"
        decided_by = "The slope's t is >= 2 and the forecast-weighted mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided_by = "The slope's t is <= -2: larger prior rises are followed by smaller excess 3-day returns on wide days."
    elif tval >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is >= 2 but the forecast-weighted mean excess return is <= 0."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": tval,
            "statistic": ({"name": "day-clustered OLS slope t", "value": tval} if tval is not None else None),
            "threshold": mm_thr,
        },
        "supporting_check": {"name": sc_name, "value": wmean, "passed": sc_passed},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
