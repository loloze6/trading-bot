import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            # recompute the 5-bar return from prices inside the window where the raw value is not recorded
            ret5 = close / close.shift(H) - 1.0
            raw_eff = raw.where(raw.notna(), ret5)
            regime = df["regime"].astype(str).str.lower()
            calm = regime != "chop"
            active = fc.notna() & (fc != 0)
            situ = calm & (raw_eff < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 5-bar forward excess return on forecast (grid bars with forecast < 0)"
    thr = "slope > 0 with t >= 2 confirms (with supporting check > 0); slope < 0 with t <= -2 rejects"
    sup_name = "mean short-side excess return on grid bars with forecast <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": "Fewer than 90% of the active bars (forecast != 0) are short bars after a 5-bar fall "
                          "(raw scaled return < 0) in the calm profile (regime not chop), so the config does not do what the Fidelity says.",
            "reading": "Situation = regime not 'chop' and raw scaled 5-bar return < 0 (recomputed from prices when not recorded), side short.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        coin_all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_all_rets.append(r)
                if np.isfinite(fc[i]):
                    coin_rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        if len(coin_all_rets) == 0:
            continue
        mu = float(np.mean(coin_all_rets))
        for (c, d, f, r) in coin_rows:
            rows.append({"coin": c, "day": d, "forecast": f, "excess": r - mu})

    data = pd.DataFrame(rows, columns=["coin", "day", "forecast", "excess"])
    neg = data[data["forecast"] < 0].copy()
    deep = data[data["forecast"] <= -2].copy()
    n_neg = int(len(neg))
    n_deep = int(len(deep))
    n_days = int(neg["day"].nunique()) if n_neg > 0 else 0

    # slope with day-clustered (same-day cases summed) standard error
    slope = None
    t_slope = None
    if n_neg >= 3 and neg["forecast"].var() > 0:
        x = neg["forecast"].values
        y = neg["excess"].values
        xm = x.mean()
        sxx = float(np.sum((x - xm) ** 2))
        b = float(np.sum((x - xm) * (y - y.mean())) / sxx)
        a = y.mean() - b * xm
        e = y - a - b * x
        u = pd.Series((x - xm) * e).groupby(neg["day"].values).sum().values
        G = len(u)
        if G > 1:
            corr = (G / (G - 1.0)) * ((n_neg - 1.0) / (n_neg - 2.0))
            var_b = corr * float(np.sum(u ** 2)) / sxx ** 2
            slope = b
            t_slope = float(b / np.sqrt(var_b)) if var_b > 0 else None

    sup_val = float((-deep["excess"]).mean()) if n_deep > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {"grid cases with forecast < 0": n_neg,
              "grid cases with forecast <= -2": n_deep,
              "days of the forecast < 0 cases": n_days}

    if n_neg < 100:
        status, decided = "not observable", f"Fewer than 100 grid cases with forecast < 0 ({n_neg})."
    elif n_deep < 30:
        status, decided = "not observable", f"Fewer than 30 grid cases with forecast <= -2 ({n_deep})."
    elif t_slope is None:
        status, decided = "inconclusive", "The slope's t could not be computed."
    elif slope > 0 and t_slope >= 2 and sup_pass:
        status, decided = "confirmed", "The slope is positive with t >= 2 and the supporting check is positive."
    elif slope < 0 and t_slope <= -2:
        status, decided = "rejected", "The slope is negative with t <= -2: deeper scaled falls are followed by higher excess returns."
    elif slope > 0 and t_slope >= 2:
        status, decided = "inconclusive", "A confirming slope with a non-positive supporting check."
    else:
        status, decided = "inconclusive", "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "slope t, same-day cases summed (day-clustered)", "value": t_slope}
                                       if t_slope is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val,
                             "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid cases are bars at positions 0,5,10,... of each window with a 5-bar forward return inside the window; "
                   "the coin's mean 5-bar return is the mean over all its grid returns in all windows; the slope's t sums the "
                   "regression scores per calendar day (day-clustered SE); the situation is regime not 'chop' with raw value < 0, short.",
    }
