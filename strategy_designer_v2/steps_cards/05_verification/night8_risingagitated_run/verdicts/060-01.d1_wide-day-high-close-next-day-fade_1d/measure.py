import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    CL = "debug_info.components.close_loc.last_history_value"

    # ---------- 1. situation check: falling agitated profile + wide day, short side ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            ret = c.pct_change()
            rng = (h - l) / c
            # wide: range/close over std of the last 20 daily returns (accept either the
            # inclusive or exclusive-of-today window, ddof 1 or 0)
            s_inc1 = ret.rolling(20, min_periods=20).std(ddof=1)
            s_inc0 = ret.rolling(20, min_periods=20).std(ddof=0)
            s_exc1 = ret.shift(1).rolling(20, min_periods=20).std(ddof=1)
            s_exc0 = ret.shift(1).rolling(20, min_periods=20).std(ddof=0)
            ratios = pd.concat([rng / s_inc1, rng / s_inc0, rng / s_exc1, rng / s_exc0], axis=1)
            ratios = ratios.replace([np.inf, -np.inf], np.nan)
            wide_known = ratios.notna().any(axis=1)
            wide = (ratios >= 2.0 * (1 - 1e-6)).any(axis=1)
            # falling: 60-bar price evolution in percent below -10
            evo = (c / c.shift(60) - 1.0) * 100.0
            fall_known = evo.notna()
            falling = evo < -10.0
            # agitated (365-day vol percentile) cannot be rebuilt inside ~120-bar windows:
            # the detector's decision (regime not vetoed to chop) stands for it
            regime_ok = d["regime"].astype(str) != "chop"
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            active = fc != 0
            for i in np.where(active.values)[0]:
                n_active += 1
                w_ok = bool(wide.iloc[i]) if wide_known.iloc[i] else bool(regime_ok.iloc[i])
                f_ok = bool(falling.iloc[i]) if fall_known.iloc[i] else bool(regime_ok.iloc[i])
                if not (wide_known.iloc[i] and fall_known.iloc[i]):
                    n_active_uncomputable += 1
                sit = w_ok and f_ok and bool(regime_ok.iloc[i])
                if sit and fc.iloc[i] < 0:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Wide is recomputed as (high-low)/close over the std of 20 daily returns (accepting inclusive or "
               "exclusive-of-today windows), falling as the 60-bar % change below -10, the agitated percentile "
               "(365-day lookback, not rebuildable in the windows) and any part not computable on a window's first "
               "bars are taken from the recorded regime not being 'chop'; the per-day t uses deviations summed per "
               "day (clustered standard error); thirds are equal splits of the cases sorted by close_loc raw value "
               "and the excess return there is unsigned (next-day return minus the coin's mean).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual next-day move in the short's direction", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "days with cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling, "
                           "agitated profile on a wide day (range >= 2 x 20-day return std)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin's mean daily return over all its windows
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            all_r.append((c.shift(-1) / c - 1.0).dropna())
        if not all_r:
            continue
        mu = float(pd.concat(all_r).mean())
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            nxt = c.shift(-1) / c - 1.0
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            cl = pd.to_numeric(d[CL], errors="coerce") if CL in d.columns else pd.Series(np.nan, index=d.index)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(len(d)):
                if fc.iloc[i] < 0 and np.isfinite(nxt.iloc[i]):
                    ex = float(nxt.iloc[i]) - mu
                    rows.append({"day": ts.iloc[i].floor("D"), "excess": ex, "unusual": -ex,
                                 "cl": float(cl.iloc[i]) if pd.notna(cl.iloc[i]) else np.nan})

    cases = pd.DataFrame(rows, columns=["day", "excess", "unusual", "cl"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["unusual"].mean()) if n_cases else None
    t_val = None
    if n_cases > 0 and n_days > 1:
        dev = cases["unusual"] - mean_u
        S = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1)) * float(np.sum(S ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    cc = cases.dropna(subset=["cl"])
    if len(cc) >= 3:
        order = np.argsort(cc["cl"].values, kind="mergesort")
        parts = np.array_split(order, 3)
        ex = cc["excess"].values
        sup_val = float(ex[parts[2]].mean() - ex[parts[0]].mean())
        sup_pass = bool(sup_val < 0)

    counts = {"days with cases": n_days, "cases": n_cases}
    main = {"name": "mean unusual next-day move in the short's direction",
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day summed", "value": t_val} if t_val is not None else None,
            "threshold": "above 0 with t >= 2 (and supporting check) to confirm; below 0 with t <= -2 to reject"}
    sup = {"name": "top third minus bottom third of close_loc, mean next-day excess return",
           "value": sup_val, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} days with cases, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move in the short's direction above 0 with t >= 2, and the top-minus-bottom third difference is below 0."
        else:
            status = "inconclusive"
            decided = "A confirming t with a failed supporting check (top-minus-bottom third difference not below 0)."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move in the short's direction below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
