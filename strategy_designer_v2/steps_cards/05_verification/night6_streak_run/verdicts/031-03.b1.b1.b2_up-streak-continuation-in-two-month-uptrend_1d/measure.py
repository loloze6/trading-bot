import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    LH = "debug_info.components.streak.last_history_value"

    def prep(df):
        d = df.copy().reset_index(drop=True)
        d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
        d["day"] = d["ts"].dt.floor("D")
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        return d

    data = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[(coin, w)] = prep(df)

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for (coin, w), d in data.items():
        c = d["close"]
        r30 = c / c.shift(30) - 1.0
        r60 = c / c.shift(60) - 1.0
        regime_rec = d["regime"].astype(str) == "trending"
        trend = pd.Series(np.where(r60.notna() & r30.notna(),
                                   (r30 > 0) & (r60 > 0),
                                   regime_rec), index=d.index).astype(bool)
        if LH in d.columns:
            raw = pd.to_numeric(d[LH], errors="coerce")
        else:
            raw = pd.Series(np.nan, index=d.index)
        up_close = c > c.shift(1)
        streak_on = pd.Series(np.where(raw.notna(), raw > 0, up_close), index=d.index).astype(bool)
        situation = trend & streak_on
        active = d["forecast"] != 0
        n_active += int(active.sum())
        n_agree += int((active & situation & (d["forecast"] > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    main_name = "slope of forward 20-bar return minus the coin's mean 20-bar return on the forecast, trending-regime grid bars"
    threshold = "slope t >= 2 confirms (with mean unusual move > 0); slope t <= -2 rejects"
    reading = ("Regime recomputed from prices as 30- and 60-bar close returns > 0 (recorded regime used on a window's first 60 bars), "
               "streak situation = raw streak value > 0, side long; the slope is an OLS with intercept on all trending grid bars "
               "(forecast 0 included) with day-clustered (CR1) standard errors; the coin's mean 20-bar return is over all its windows' grid; "
               "a case is a forecast rise of >= 2 from its lowest long level since the last bet (0 after flat), the first in each grid cell with a 20-bar forward return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the 30d>0 and 60d>0 regime "
                           "with an up-close streak, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Coin drift: mean 20-bar return on the grid over all windows ----------
    grid_rows = []
    for (coin, w), d in data.items():
        c = d["close"].values
        n = len(d)
        for p in range(0, n, H):
            if p + H < n and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                ret = c[p + H] / c[p] - 1.0
            else:
                ret = np.nan
            grid_rows.append({"coin": coin, "w": w, "pos": p, "ret": ret,
                              "fc": float(d["forecast"].iloc[p]),
                              "regime": str(d["regime"].iloc[p]),
                              "day": d["day"].iloc[p]})
    g = pd.DataFrame(grid_rows)
    drift = g.dropna(subset=["ret"]).groupby("coin")["ret"].mean().to_dict()

    # ---------- 3. Main measure ----------
    reg = g[(g["regime"] == "trending") & g["ret"].notna()].copy()
    reg["y"] = reg["ret"] - reg["coin"].map(drift)
    reg = reg.dropna(subset=["y"])
    pos_cases = reg[reg["fc"] > 0]
    n_cases = int(len(pos_cases))
    n_days = int(pos_cases["day"].nunique())

    slope = None
    t_slope = None
    if len(reg) >= 3 and reg["fc"].var() > 0 and reg["day"].nunique() >= 2:
        X = np.column_stack([np.ones(len(reg)), reg["fc"].values])
        y = reg["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        days = reg["day"].values
        for dd in pd.unique(days):
            m = days == dd
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
        N, K = X.shape
        G = len(pd.unique(days))
        V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((N - 1) / (N - K))
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    # ---------- 4. Supporting check: mean unusual move of the cases ----------
    unusual = []
    for (coin, w), d in data.items():
        f = d["forecast"].values
        c = d["close"].values
        n = len(d)
        low = 0.0
        bet = np.zeros(n, dtype=bool)
        for i in range(n):
            fi = f[i]
            if fi <= 0:
                low = 0.0
                continue
            if fi - low >= 2.0 - 1e-12:
                bet[i] = True
                low = fi
            elif fi < low:
                low = fi
        dr = drift.get(coin, np.nan)
        for p in range(0, n, H):
            for i in range(p, min(p + H, n)):
                if bet[i] and i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    if np.isfinite(dr):
                        unusual.append(c[i + H] / c[i] - 1.0 - dr)
                    break
    mean_unusual = float(np.mean(unusual)) if len(unusual) > 0 else None
    supp_passed = (mean_unusual is not None) and (mean_unusual > 0)

    counts = {"grid cases in the regime with a forecast above 0": n_cases,
              "distinct days": n_days,
              "trending grid bars in the slope": int(len(reg)),
              "supporting cases": int(len(unusual))}

    # ---------- 5. Decision ----------
    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided_by = (f"Minimum not reached: {n_cases} grid cases in the regime with a forecast above 0 (need 100) "
                      f"on {n_days} distinct days (need 50).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and supp_passed:
        status = "confirmed"
        decided_by = "The slope t is 2 or more and the cases' mean unusual move is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope t is 2 or more but the cases' mean unusual move is at or below 0."
    else:
        status = "inconclusive"
        decided_by = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "slope t, cases of one day clustered", "value": t_slope}
                                       if t_slope is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual 20-bar move of the cases (forecast rises >= 2, one per grid cell)",
                             "value": mean_unusual,
                             "passed": bool(supp_passed) if mean_unusual is not None else None},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
