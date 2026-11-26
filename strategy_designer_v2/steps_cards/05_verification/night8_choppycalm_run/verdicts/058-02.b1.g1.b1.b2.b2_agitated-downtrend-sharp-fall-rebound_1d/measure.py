import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    MIN_BARS = 100
    MIN_DAYS = 50

    # ---------- Situation check ----------
    n_active = 0
    n_agree = 0
    coin_mean = {}
    rows = []

    for coin, wins in bars.items():
        all_rets = []
        per_window = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0  # inside the window only
            all_rets.append(fwd.dropna().values)
            per_window.append((d, close, fwd))
        if all_rets:
            allr = np.concatenate(all_rets)
            coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan
        else:
            coin_mean[coin] = np.nan

        for d, close, fwd in per_window:
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            # raw value of the scaled return; recomputed from prices where not recorded
            ret1 = close / close.shift(1) - 1.0
            vol20 = ret1.rolling(20, min_periods=20).std()
            recomputed = ret1 / vol20
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            active = fc.notna() & (fc != 0)
            in_situation = (regime == "unknown") & (raw < 0)
            agree = active & in_situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            ts = pd.to_datetime(d["timestamp"], utc=True)
            day = ts.dt.floor("D")
            sel = fc.notna() & (fc > 0) & fwd.notna()
            for i in np.where(sel.values)[0]:
                rows.append((coin, float(fc.iloc[i]), float(fwd.iloc[i]), day.iloc[i]))

    reading = ("The falling agitated profile is read from the recorded regime ('unknown' = both chop vetoes passed, "
               "since the detector's components are not recorded) and the fall from the raw scaled return being negative "
               "(recomputed from closes where missing); the slope is an OLS of excess next-day return on the forecast with "
               "a day-clustered standard error; the plan's minimum counts are applied as 'not observable'.")

    main_name = "OLS slope of next-day excess return on forecast, positive-forecast bars"
    threshold = "confirm if slope t >= 2 (with supporting check), reject if slope t <= -2"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": None},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with a positive forecast": 0, "distinct days": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 100 bars with a positive forecast.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the long side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the active bars are long positions on a down day in the falling agitated "
                           "regime, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- Criterion ----------
    if rows:
        df = pd.DataFrame(rows, columns=["coin", "f", "r", "day"])
        df["mu"] = df["coin"].map(coin_mean)
        df["y"] = df["r"] - df["mu"]
        df = df[np.isfinite(df["y"]) & np.isfinite(df["f"])].reset_index(drop=True)
    else:
        df = pd.DataFrame(columns=["coin", "f", "r", "day", "mu", "y"])

    n = int(len(df))
    n_days = int(df["day"].nunique()) if n else 0
    counts = {"bars with a positive forecast": n, "distinct days": n_days}

    slope = None
    t_val = None
    if n >= 3 and df["f"].nunique() > 1:
        X = np.column_stack([np.ones(n), df["f"].values])
        y = df["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        codes = pd.factorize(df["day"])[0]
        G = codes.max() + 1
        scores = np.zeros((G, 2))
        np.add.at(scores, codes, X * u[:, None])
        meat = scores.T @ scores
        V = XtX_inv @ meat @ XtX_inv
        if G > 1 and n > 2:
            V = V * (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_val = float(slope / se) if np.isfinite(se) and se > 0 else None

    if n and df["f"].sum() > 0:
        wmean = float((df["f"] * df["y"]).sum() / df["f"].sum())
        check_pass = bool(wmean > 0)
    else:
        wmean = None
        check_pass = None

    main = {
        "name": main_name,
        "value": slope,
        "statistic": {"name": "t of the slope, day-clustered", "value": t_val} if t_val is not None else None,
        "threshold": threshold,
    }
    support = {"name": "forecast-weighted mean next-day excess return > 0", "value": wmean, "passed": check_pass}

    if n < MIN_BARS or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum count not reached: {n} bars with a positive forecast (need 100) on {n_days} distinct days "
                   f"(need 50).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
